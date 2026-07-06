# BestSkills

Professional-grade **Agent Skills** for Claude (Opus 4.8, Sonnet 5, and newer) — four plugin packs covering programming, research, web automation, and business. Each skill encodes a complete working discipline: workflow, quality bars, anti-patterns, and deliverable formats — not just tips.

## Installation

### As Claude Code plugins (recommended)

```
/plugin marketplace add nmsmonster/bestskills
/plugin install programming-pro@bestskills
/plugin install research-pro@bestskills
/plugin install automation-pro@bestskills
/plugin install business-pro@bestskills
```

Install only the packs you need — each is independent.

### As standalone skills

Copy any skill folder into your skills directory — works with Claude Code, the Claude API (`/v1/skills`), and any Agent-Skills-compatible harness:

```bash
# personal (all projects)
cp -r plugins/research-pro/skills/deep-research ~/.claude/skills/

# project-scoped
cp -r plugins/programming-pro/skills/systematic-debugging .claude/skills/
```

## Skill catalog

### 🛠 programming-pro

| Skill | What it enforces |
|---|---|
| `systematic-debugging` | Hypothesis-driven debugging: reproduce first, bisect, prove the root cause, prove the fix |
| `test-driven-development` | Red–green–refactor discipline, test-case ordering, what makes tests good, what not to test |
| `safe-refactoring` | Behavior-preserving changes: characterization tests, one mechanical step at a time, revert-don't-debug |
| `api-design` | REST/GraphQL/library contracts: consistency, errors, pagination, versioning, compatibility |
| `performance-optimization` | Measure → profile → fix the biggest cost → re-measure; the leverage ladder; no blind micro-optimization |

### 🔎 research-pro

| Skill | What it enforces |
|---|---|
| `deep-research` | Multi-phase research: framing, counter-queries, source triangulation, cited findings with confidence levels |
| `fact-check` | Claim decomposition, tracing to primary sources, explicit verdicts incl. "misleading" with the trick named |
| `literature-review` | Thematic synthesis across papers, evidence tables, consensus vs. contested, gap analysis |
| `competitive-analysis` | Decision-framed competitor teardowns: facts-only matrices, positioning reads, strategic implications |
| `digital-footprint-audit` | **Defensive, consent-gated** OSINT self-audit: map your own public exposure, score it (sensitivity × discoverability × removability + aggregation risk), and get a prioritized removal + monitoring plan. Includes source-map, risk-scoring, and remediation-playbook references |

### 🤖 automation-pro

| Skill | What it enforces |
|---|---|
| `web-automation` | Playwright-driven browsing of any site: durable selectors, condition waits, sessions/logins, incremental building; includes a patterns reference |
| `data-pipeline` | Resilient fetch→parse→normalize→validate→export pipelines: raw persistence, resumability, quarantine, run summaries |
| `workflow-automation` | Unattended-grade scheduled jobs: locks, idempotency, failure alerts, change-detection pattern, dead-man's switches |

### 💼 business-pro

| Skill | What it enforces |
|---|---|
| `market-analysis` | Bottom-up TAM/SAM/SOM with shown work, five-forces structure, beachhead segmentation |
| `business-plan` | Lean canvas → full plan; testable claims, unit economics, the honest risks section |
| `financial-model` | Driver-based models: assumptions/model/outputs separation, cash trough & runway, scenarios, sanity battery |
| `pitch-deck` | Decision-forcing narratives: belief mapping, slide-by-slide arc, headline test, objection pre-emption |

## Design principles

These skills follow the [Agent Skills](https://code.claude.com/docs/en/skills) format and are written **for the model, not about the topic**:

- **Trigger-rich descriptions** — frontmatter states *what* and *when*, so skills activate reliably.
- **Process over trivia** — each skill is an enforceable workflow with hard rules and stop conditions, not a listicle.
- **Progressive disclosure** — heavy reference material (source-evaluation rubric, Playwright patterns) lives in `references/` and loads only when needed.
- **Honest-output bias** — every skill requires shown work, cited sources, stated confidence, or before/after numbers. No skill lets the model assert what it didn't verify.
- **Composability** — skills reference each other where workflows connect (e.g. `business-plan` → `financial-model` → `pitch-deck`).
- **Safety by design** — capability-sensitive skills are consent-gated and defensive. `digital-footprint-audit` audits *your own* (or an explicitly authorized) footprint to shrink it; it refuses to profile non-consenting third parties. The line is whose footprint, with whose consent, toward defense vs. targeting.

## Repository layout

```
.claude-plugin/marketplace.json      # marketplace manifest
plugins/
  programming-pro/
    .claude-plugin/plugin.json
    skills/<skill-name>/SKILL.md     # + references/ where applicable
  research-pro/ …
  automation-pro/ …
  business-pro/ …
```

## Po polsku (skrót)

Kolekcja profesjonalnych skilli dla Claude w czterech pakietach: **programowanie**, **research**, **automatyzacja** (w tym poruszanie się po dowolnych stronach www przez Playwright) i **biznes**. Instalacja: `/plugin marketplace add nmsmonster/bestskills`, a potem `/plugin install <pakiet>@bestskills` — albo skopiuj wybrany folder skilla do `~/.claude/skills/`. Każdy skill to kompletna metodyka pracy z twardymi zasadami jakości, nie zbiór porad.

## License

MIT — see [LICENSE](LICENSE).
