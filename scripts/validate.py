#!/usr/bin/env python3
"""
BestSkills validator — the enforceable quality gate for the collection.

Checks, for every skill and manifest:
  - all *.json parse
  - each marketplace plugin has a real plugin.json at its source
  - marketplace plugin list == plugins/ directory list (no orphans, no phantoms)
  - SKILL.md frontmatter: valid YAML, name==folder, name is [a-z0-9-]{1,64}
  - description present, <=1024 chars, colon-safe (no unquoted ': '), has a trigger clause
  - referenced `references/<file>.md` exist
  - cross-references of the form `pack:skill` resolve to real packs/skills

Exit 0 if clean, 1 otherwise. No external deps beyond PyYAML.
Run from the repo root:  python3 scripts/validate.py
"""
import json
import re
import sys
import pathlib

try:
    import yaml
except ImportError:
    sys.exit("PyYAML required: pip install pyyaml")

ROOT = pathlib.Path(__file__).resolve().parent.parent
TRIGGER = re.compile(r"\bUse when\b|\bUse this\b|\bUse before\b")
NAME_RE = re.compile(r"[a-z0-9-]{1,64}")
# skill-like tokens allowed to appear in `pack:skill` refs but not be repo skills
EXTERNAL_SKILLS = {"dataviz", "claude-api"}


def main() -> int:
    errors: list[str] = []

    # 1. all JSON parses
    for j in ROOT.rglob("*.json"):
        if ".git" in j.parts:
            continue
        try:
            json.loads(j.read_text())
        except Exception as e:  # noqa: BLE001
            errors.append(f"{j.relative_to(ROOT)}: invalid JSON: {e}")

    plugins_dir = ROOT / "plugins"
    pack_dirs = {p.name for p in plugins_dir.iterdir() if p.is_dir()}

    # 2 & 3. marketplace ↔ directories
    mp_path = ROOT / ".claude-plugin" / "marketplace.json"
    mp = json.loads(mp_path.read_text())
    mp_names = set()
    for p in mp["plugins"]:
        mp_names.add(p["name"])
        src = ROOT / p["source"]
        if not (src / ".claude-plugin" / "plugin.json").exists():
            errors.append(f"marketplace: plugin '{p['name']}' missing plugin.json at {p['source']}")
    if mp_names != pack_dirs:
        errors.append(f"marketplace/plugins-dir mismatch: {mp_names ^ pack_dirs}")

    # 4-7. skills
    skills = sorted(plugins_dir.rglob("SKILL.md"))
    skill_names = {s.parent.name for s in skills}
    for s in skills:
        rel = s.relative_to(ROOT)
        text = s.read_text()
        m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
        if not m:
            errors.append(f"{rel}: missing YAML frontmatter")
            continue
        raw = m.group(1)
        try:
            fm = yaml.safe_load(raw)
        except Exception as e:  # noqa: BLE001
            errors.append(f"{rel}: frontmatter not valid YAML: {e}")
            continue

        name = fm.get("name", "")
        if name != s.parent.name:
            errors.append(f"{rel}: name '{name}' != folder '{s.parent.name}'")
        if not NAME_RE.fullmatch(name or ""):
            errors.append(f"{rel}: name '{name}' not [a-z0-9-]{{1,64}}")

        desc = fm.get("description", "")
        if not desc:
            errors.append(f"{rel}: missing description")
        else:
            if len(desc) > 1024:
                errors.append(f"{rel}: description {len(desc)} > 1024 chars")
            if not TRIGGER.search(desc):
                errors.append(f"{rel}: description has no trigger clause (Use when/this/before)")
        # colon-safety: the raw description line must be quoted if it contains ': '
        dm = re.search(r"^description:\s*(.+)$", raw, re.M)
        if dm and dm.group(1)[0] not in "\"'" and ": " in dm.group(1):
            errors.append(f"{rel}: unquoted ': ' in description (YAML colon trap)")

        # referenced files exist
        for ref in re.finditer(r"`references/([a-z0-9-]+\.md)`", text):
            if not (s.parent / "references" / ref.group(1)).exists():
                errors.append(f"{rel}: references/{ref.group(1)} not found")

        # cross-references pack:skill
        for cr in re.finditer(r"([a-z]+-pro):([a-z0-9-]+)", text):
            pack, sk = cr.group(1), cr.group(2)
            if pack not in pack_dirs:
                errors.append(f"{rel}: cross-ref unknown pack '{pack}' ({cr.group(0)})")
            elif sk not in skill_names:
                errors.append(f"{rel}: cross-ref unknown skill '{sk}' ({cr.group(0)})")

        # `x` skill mentions
        for sm in re.finditer(r"`([a-z0-9-]+)`\s+skill", text):
            tok = sm.group(1)
            if tok not in skill_names and tok not in EXTERNAL_SKILLS:
                errors.append(f"{rel}: '`{tok}` skill' does not resolve")

    print(f"Scanned {len(skills)} skills across {len(pack_dirs)} packs, "
          f"{len(list(plugins_dir.rglob('references/*.md')))} reference files.")
    if errors:
        print(f"\n✗ {len(errors)} problem(s):")
        for e in errors:
            print(f"  - {e}")
        return 1
    print("✓ All checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
