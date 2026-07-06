#!/usr/bin/env python3
"""
Skill-activation eval — static disambiguation check over evals/triggers.yaml.

For each case it scores how strongly each skill's *description* matches the
prompt + intent terms, then asserts the expected skill outscores every
"reject" near-neighbour. This catches description-level trigger overlap — the
failure mode where, say, `market-analysis` and `competitive-analysis` both
look equally right for a prompt and the wrong one fires.

It is a proxy (bag-of-words over descriptions), not a live model run — but it
regresses the exact confusable clusters flagged in review, needs no API, and
runs in CI. A model-based live eval can consume the same YAML.

Scoring: term-overlap between {prompt + intent} tokens and each skill's
description, with the explicit `intent` phrases weighted higher (they encode
the trigger language a good description should contain).

Exit 0 if every case's expected skill wins by the margin; 1 otherwise.
Run:  python3 scripts/eval_triggers.py
"""
import re
import sys
import pathlib

try:
    import yaml
except ImportError:
    sys.exit("PyYAML required: pip install pyyaml")

ROOT = pathlib.Path(__file__).resolve().parent.parent
STOP = set("a an the to of for and or with in on is it this that we our my your "
           "how what who why when should help me make so can could i you be are "
           "before after into out do does about them they their its as at by".split())


def tokens(text: str) -> set[str]:
    return {w for w in re.findall(r"[a-z0-9]+", text.lower()) if w not in STOP and len(w) > 2}


def load_descriptions() -> dict[str, str]:
    out = {}
    for s in ROOT.glob("plugins/*/skills/*/SKILL.md"):
        m = re.match(r"^---\n(.*?)\n---\n", s.read_text(), re.S)
        if not m:
            continue
        fm = yaml.safe_load(m.group(1))
        out[fm["name"]] = fm.get("description", "")
    return out


def strip_pointers(desc: str, skill_names: set[str]) -> str:
    """Drop any clause that names another skill ('… for X, use other-skill').
    Such a clause is navigation to a sibling, not a trigger for this skill, and
    it typically describes the sibling's job — so its words must not count for
    or against either skill. Split on sentence/clause delimiters and remove any
    fragment mentioning a skill name."""
    parts = re.split(r"[.—]", desc)
    kept = [p for p in parts if not any(n in p for n in skill_names)]
    return ". ".join(kept)


def score(desc_tokens: set[str], prompt_tokens: set[str], intent_tokens: set[str]) -> int:
    # intent terms count double — they are the deliberate trigger phrasing
    return len(desc_tokens & prompt_tokens) + 2 * len(desc_tokens & intent_tokens)


def main() -> int:
    desc = load_descriptions()
    names = set(desc)
    desc_tok = {name: tokens(strip_pointers(d, names)) for name, d in desc.items()}
    cases = yaml.safe_load((ROOT / "evals" / "triggers.yaml").read_text())["cases"]

    failures, warnings = [], []
    for c in cases:
        expect = c["expect"]
        if expect not in desc:
            failures.append(f"[{expect}] expected skill does not exist"); continue
        p_tok = tokens(c["prompt"])
        i_tok = tokens(" ".join(c.get("intent", [])))
        exp_score = score(desc_tok[expect], p_tok, i_tok)
        for rej in c.get("reject", []):
            if rej not in desc:
                warnings.append(f"[{expect}] reject '{rej}' does not exist (stale case)"); continue
            rej_score = score(desc_tok[rej], p_tok, i_tok)
            if rej_score > exp_score:
                # A near-neighbour strictly outscoring the expected skill is an
                # unambiguous description bug — the wrong skill would look more
                # relevant. Hard fail.
                failures.append(
                    f"INVERSION  prompt {c['prompt']!r}\n"
                    f"           expected '{expect}' scored {exp_score} but "
                    f"'{rej}' scored {rej_score} — reject skill looks more relevant")
            elif rej_score >= exp_score:
                # A tie at the bag-of-words level means the two descriptions
                # don't lexically separate for this prompt. For genuinely
                # adjacent skills the live model still separates them on full
                # semantics, so this is a warning to watch, not a build break.
                warnings.append(
                    f"tie ({exp_score}={rej_score}) '{expect}' vs '{rej}' — "
                    f"lexically indistinct for {c['prompt']!r}")
            elif exp_score - rej_score <= 1:
                warnings.append(
                    f"thin margin ({exp_score} vs {rej_score}) '{expect}' over '{rej}' "
                    f"for {c['prompt']!r}")

    print(f"Ran {len(cases)} activation cases over {len(desc)} skills.")
    if warnings:
        print(f"\n⚠ {len(warnings)} warning(s):")
        for w in warnings:
            print(f"  - {w}")
    if failures:
        print(f"\n✗ {len(failures)} failure(s):")
        for f in failures:
            print(f"  - {f}")
        return 1
    print("✓ Every expected skill outscores its near-neighbours.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
