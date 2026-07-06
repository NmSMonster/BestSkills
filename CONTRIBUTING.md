# Contributing & Skill-Authoring Standard

This is the quality bar every skill in BestSkills is held to. It's not bureaucracy — it's the exact standard that makes these skills reliably *fire at the right time* and *change what the model does*. A skill that doesn't meet this bar dilutes the collection; hold the line.

The golden rule: **a skill encodes an enforceable working discipline the model wouldn't otherwise hold — not a topic summary the model already knows.** If a competent model already does the thing well without the skill, the skill is noise. Write skills for the judgment calls, the ordering, the anti-patterns, and the "do this before that" rules that are easy to skip under pressure.

## Directory layout (non-negotiable)

```
plugins/<pack>/
  .claude-plugin/plugin.json         # name, version, description, author
  skills/<skill-name>/
    SKILL.md                         # the skill (required)
    references/<topic>.md            # heavy detail, loaded on demand (optional)
```
- `<skill-name>` is lowercase-kebab, ≤64 chars, and **exactly matches** the `name:` in the frontmatter and the folder name.
- Every pack is registered in `.claude-plugin/marketplace.json` with a `source` path that has a real `plugin.json`.

## Frontmatter (the highest-leverage 3 lines in the whole skill)

```yaml
---
name: skill-name
description: <What it does>. Use when <explicit triggers: the phrasings, tasks, and situations that should activate it>.
---
```

Rules that the validator enforces — a violation breaks skill selection:
- **`name` matches the folder**, is `[a-z0-9-]{1,64}`.
- **`description` ≤ 1024 characters.** This is the ONLY thing the model sees when deciding whether to load the skill — it must carry its full weight.
- **It must contain an explicit trigger clause** ("Use when…", "Use this…", "Use before…"). Triggers are the difference between a skill that fires and one that sits dead. Enumerate the real situations, task phrasings, and synonyms a user would use.
- **Colon-safe**: if the description contains `: ` (colon-space) it must be quoted, or YAML parsing breaks. Prefer em-dashes over colons in descriptions.
- **Third person, describing the model's action** ("Reviewing a diff for…"), not "You should…" or "I will…".
- **No volatile facts** (prices, version numbers, model IDs) in a skill body — those rot. Point to a skill/reference that owns the volatile facts (e.g. `claude-api`) instead of hardcoding them.

### Description disambiguation

When two skills live near each other, their descriptions must draw the boundary so the *right* one fires:
- `copywriting` (persuade/convert) vs `technical-writing` (explain/document) vs `email-drafting` (a specific message).
- `deep-research` (open question, many sources) vs `due-diligence` (vet a specific entity) vs `competitive-analysis` (compare competitors for a decision) vs `fact-check` (verify specific claims).
- `systematic-debugging` (find a bug in calm) vs `incident-response`-style CI work vs `code-review` (evaluate a diff).

State what each is *for* and, where useful, what it's *not* for. Overlapping triggers cause the wrong skill to fire — which is worse than no skill.

## The body — what good looks like

Structure varies by skill, but the best ones share this shape:

1. **A one-paragraph frame**: what standard the output is held to, and the core principle. Name the failure mode the skill exists to prevent.
2. **A workflow with ordered phases/steps.** Each step should be concrete enough to act on. Order matters — put "do this first" first (fail-fast, reproduce-before-fixing, question-before-data).
3. **Hard rules and/or anti-patterns.** The explicit "never do X" and "stop if Y" lines. This is often the most valuable section — it's what the model skips without the skill.
4. **A deliverable/output format** where the skill produces an artifact — so results are consistent and complete. Use a fenced template.

Writing quality bar:
- **Imperative and specific.** "Reverse-search each profile photo (Yandex is strongest on faces)" beats "consider image search."
- **Every rule earns its place.** If a line is generic advice the model already follows, cut it. Density of *non-obvious* guidance is the metric.
- **Prefer tables and checklists** for enumerable things (severity levels, source tiers, decision matrices) — they're scannable and the model applies them faithfully.
- **Honest-output bias**: bake in cited sources, shown work, stated confidence, before/after numbers, or verification. No skill should let the model assert what it didn't verify.
- **Cross-link** where workflows connect (`` `pack:skill` ``), but don't over-link — only where the handoff is real.

## Length & progressive disclosure

- **Keep `SKILL.md` focused** — target ≈ 50–90 lines. Long enough to encode the discipline, short enough to stay loaded and read.
- **Push heavy detail to `references/`**: exhaustive checklists, code-pattern libraries, rubrics, per-language tables. The skill body says *when* to load the reference; the reference holds the depth. This keeps the always-loaded part lean and the detail available on demand.
- If a `SKILL.md` exceeds ~100 lines, ask whether a chunk belongs in a reference file.

## Before you submit — the validation gate

Run the repo validator (checks JSON, YAML frontmatter, name/folder match, description length, colon-safety, trigger presence, marketplace↔dirs, and cross-reference integrity):

```bash
python3 scripts/validate.py
```

A skill is not done until:
- [ ] It encodes a discipline the model wouldn't reliably hold on its own (not a topic recap).
- [ ] Frontmatter passes all validator checks; the trigger clause enumerates real activation situations.
- [ ] Its description disambiguates from neighboring skills.
- [ ] The body has an ordered workflow, explicit rules/anti-patterns, and (if it produces an artifact) a deliverable template.
- [ ] Heavy detail is in `references/`, not bloating the body.
- [ ] Cross-references resolve to real skills/files.
- [ ] No volatile facts hardcoded; nothing that will be wrong in six months.

Meet this bar and the collection stays what it claims to be: the best skills on the market.
