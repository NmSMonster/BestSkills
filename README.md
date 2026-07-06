# BestSkills

Professional-grade **Agent Skills** for Claude (Opus 4.8, Sonnet 5, and newer) — eight plugin packs covering programming, research, web automation, business, communication, orchestration, marketing, and product. Each skill encodes a complete working discipline: workflow, quality bars, anti-patterns, and deliverable formats — not just tips.

## Installation

### As Claude Code plugins (recommended)

```
/plugin marketplace add nmsmonster/bestskills
/plugin install programming-pro@bestskills
/plugin install research-pro@bestskills
/plugin install automation-pro@bestskills
/plugin install business-pro@bestskills
/plugin install communication-pro@bestskills
/plugin install orchestration-pro@bestskills
/plugin install marketing-pro@bestskills
/plugin install product-pro@bestskills
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
| `code-review` | Triaged diff review: read-order by consequence, defect-hunting mindset, severity levels, comments that land; per-language checklists |
| `api-design` | REST/GraphQL/library contracts: consistency, errors, pagination, versioning, compatibility |
| `performance-optimization` | Measure → profile → fix the biggest cost → re-measure; the leverage ladder; no blind micro-optimization |
| `security-audit` | Defensive vuln review by trust boundary: injection, authz/IDOR, secrets, crypto, deps — each finding with an exploit scenario and a fix |
| `database-design` | Schema modeling from access patterns, indexing verified with EXPLAIN, zero-downtime expand→contract migrations |
| `git-workflow` | Rebases, conflict resolution, history rewriting, and recovery — reflog-first, never lose committed work |
| `frontend-architecture` | Component boundaries and correct state placement (local/shared/server/URL), data-fetching lifecycle, feature-based structure |
| `accessibility` | WCAG-AA a11y: semantic HTML first, keyboard + screen-reader support, contrast, tested with keyboard and SR — not just an automated scan |

### 🔎 research-pro

| Skill | What it enforces |
|---|---|
| `deep-research` | Multi-phase research: framing, counter-queries, source triangulation, cited findings with confidence levels |
| `fact-check` | Claim decomposition, tracing to primary sources, explicit verdicts incl. "misleading" with the trick named |
| `literature-review` | Thematic synthesis across papers, evidence tables, consensus vs. contested, gap analysis |
| `competitive-analysis` | Decision-framed competitor teardowns: facts-only matrices, positioning reads, strategic implications |
| `data-analysis` | Question-first analysis: validate data before concluding, right statistic, honest uncertainty; includes a statistical-pitfalls reference |
| `due-diligence` | Vetting a company/vendor/investment: existence, ownership, financials, legal/sanctions, reputation → risk-weighted verdict |
| `digital-footprint-audit` | **Defensive, consent-gated** OSINT self-audit: map your own public exposure, score it (sensitivity × discoverability × removability + aggregation risk), and get a prioritized removal + monitoring plan. Includes source-map, risk-scoring, and remediation-playbook references |

### 🤖 automation-pro

| Skill | What it enforces |
|---|---|
| `web-automation` | Playwright-driven browsing of any site: durable selectors, condition waits, sessions/logins, incremental building; includes a patterns reference |
| `data-pipeline` | Resilient fetch→parse→normalize→validate→export pipelines: raw persistence, resumability, quarantine, run summaries |
| `workflow-automation` | Unattended-grade scheduled jobs: locks, idempotency, failure alerts, change-detection pattern, dead-man's switches |
| `api-integration` | Production-grade third-party API clients: auth/token lifecycle, timeouts, retry+backoff on transient-only failures, idempotency, pagination, signed idempotent webhooks |

### 💼 business-pro

| Skill | What it enforces |
|---|---|
| `market-analysis` | Bottom-up TAM/SAM/SOM with shown work, five-forces structure, beachhead segmentation |
| `business-plan` | Lean canvas → full plan; testable claims, unit economics, the honest risks section |
| `financial-model` | Driver-based models: assumptions/model/outputs separation, cash trough & runway, scenarios, sanity battery |
| `pitch-deck` | Decision-forcing narratives: belief mapping, slide-by-slide arc, headline test, objection pre-emption |
| `pricing-strategy` | Value-based pricing over cost-plus: willingness-to-pay, model choice, good-better-best tiering & anchoring |
| `negotiation` | BATNA/ZOPA/reservation-price prep, interests over positions, trade-don't-concede — practical, not manipulative |

### 🗣 communication-pro

| Skill | What it enforces |
|---|---|
| `technical-writing` | Docs for the reader's task: right mode (tutorial/how-to/reference/explanation), scannable structure, runnable examples, README/ADR/RFC/runbook templates |
| `email-drafting` | Outcome-first emails incl. the hard ones — saying no, pushing back, bad news, chasing, apologizing — clear and kind at once |
| `meeting-notes` | Transcript → decisions, owned action items, open questions; compression with flagged gaps, not a verbatim retelling |
| `presentation-builder` | Talks as spoken arguments: tension→resolution arc, one takeaway, show-don't-list slides, delivery notes |

### 🧭 orchestration-pro (the meta-layer — multiplies every other skill)

| Skill | What it enforces |
|---|---|
| `task-planning` | Scope → decompose into verifiable steps → sequence by risk/dependency → decide do-vs-delegate and when to ask; re-plan on contact with reality |
| `self-verification` | Prove-don't-assume before "done": exercise the work, run the pre-delivery checklist, report honest confidence and what wasn't checked |
| `building-with-claude` | LLM app engineering: prompt design, structured output, tool use, agents, RAG, and the eval loop that separates a demo from a product |

### 📣 marketing-pro

| Skill | What it enforces |
|---|---|
| `copywriting` | Conversion copy: benefits over features (the "so what?" test), PAS/AIDA structure, headlines, one CTA, proof — clear beats clever |
| `seo` | Rank by satisfying search intent: keyword+intent research, on-page structure, E-E-A-T, technical SEO — no keyword-stuffing tricks |
| `content-strategy` | Goal + audience → pillars, channel mix, sustainable cadence, and the distribution/repurposing half everyone skips |

### 🎯 product-pro

| Skill | What it enforces |
|---|---|
| `ui-ux-design` | Flow before screens, Nielsen heuristics, visual hierarchy, every state (empty/loading/error), forms — usability over decoration |
| `product-requirements` | PRDs that start from the problem and success metric, explicit non-goals, prioritized requirements, testable acceptance criteria |
| `roadmap-planning` | Prioritize by outcome (RICE / value-effort), sequence for risk and early value, Now/Next/Later honesty, and saying no clearly |

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
  communication-pro/ …
  orchestration-pro/ …
  marketing-pro/ …
  product-pro/ …
```

## Po polsku (skrót)

Kolekcja profesjonalnych skilli dla Claude w ośmiu pakietach: **programowanie**, **research**, **automatyzacja** (w tym poruszanie się po dowolnych stronach www przez Playwright), **biznes**, **komunikacja**, **orkiestracja** (meta-warstwa: planowanie, weryfikacja, budowanie z Claude), **marketing** i **produkt**. Instalacja: `/plugin marketplace add nmsmonster/bestskills`, a potem `/plugin install <pakiet>@bestskills` — albo skopiuj wybrany folder skilla do `~/.claude/skills/`. Każdy skill to kompletna metodyka pracy z twardymi zasadami jakości, nie zbiór porad. Claude sam wybiera odpowiedni skill na podstawie pola `description` z nagłówka — dlatego opisy są nasycone wyzwalaczami „użyj gdy…".

## License

MIT — see [LICENSE](LICENSE).
