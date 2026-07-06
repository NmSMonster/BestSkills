---
name: deep-research
description: Multi-phase web research with source triangulation, citations, and stated confidence — for any nontrivial question requiring investigation across multiple sources. Use when the user asks to research a topic, find out what the research or evidence says about something, compare options, investigate a market/technology/company/claim, produce a report or briefing, or asks a question whose answer isn't reliably in one place. Not for simple lookups a single search answers, and not for a formal synthesis of academic papers (use literature-review).
---

# Deep Research

Research quality is decided by process, not effort. Volume of searching is worthless without triangulation, source discrimination, and honest uncertainty. The deliverable is always: findings, each traceable to sources, each with a confidence level.

For source-quality judgment calls, load `references/source-evaluation.md`.

## Phase 0 — Frame (2 minutes, saves hours)

Before any search, write down:
- **The decision this research serves.** "Compare vector databases" really means "which one should we adopt, given our constraints." Ask the user for constraints only if the answer would change materially.
- **Sub-questions** (3–7) whose answers compose the final answer.
- **What would change the conclusion** — the facts to hunt hardest for.
- **Freshness requirement**: is a 2023 source fine, or does this need last-quarter data (pricing, versions, market share, laws)?

## Phase 1 — Search strategy

- Run **multiple differently-phrased queries per sub-question**, not one: the terminology insiders use, the terminology critics use, and the vendor's own terms all surface different results. Include the counter-query explicitly ("X problems", "X vs", "migrating away from X").
- Prioritize primary sources: official docs, filings, papers, changelogs, court records, direct data — over articles *about* them. When a secondary source cites a primary one, open the primary one.
- For anything time-sensitive, constrain recency and note publication dates. An undated page is a red flag for factual claims.
- Track a **source log** as you go: URL, date, what it supports, quality tier (see references). You will not remember later.

## Phase 2 — Triangulate

- **Key claims need 2+ independent sources.** Independent means different origin — twenty articles citing the same press release are one source. Trace the citation chain to the origin before counting it twice.
- Actively seek disconfirmation for every major finding. If you can't find any criticism of a product/claim/paper, you haven't looked — search for it explicitly.
- Distinguish claim types and hold them to different bars:
  - Verifiable fact (number, date, spec) → find the primary source.
  - Expert judgment → note who, and their incentive.
  - Vendor claim / marketing → report as claim, never as fact.
  - Community sentiment (forums, reviews) → useful signal, sample it broadly, never quote one thread as consensus.
- When sources conflict, don't average them — investigate *why* (different date? definition? incentive?) and report the conflict with your read.

## Phase 3 — Synthesize

Structure the output around the sub-questions, not around the sources ("Source A says…" is a book report, not research). For every finding attach:

- **Citation**: linked source(s) with dates.
- **Confidence**: 
  - **High** — multiple independent quality sources agree, incl. primary.
  - **Medium** — solid single source or converging indirect evidence.
  - **Low** — thin, dated, or conflicting evidence; stated as such.
- Numbers get context or they mislead: base, date, definition, source's incentive ("$4.2B market (Vendor-sponsored report, 2025; independent estimates run ~40% lower)").

## Deliverable format

```
# <Question being answered>
## TL;DR — the answer in 3–6 sentences, decision-ready
## Key findings — per sub-question: finding, evidence, confidence
## Conflicts & caveats — where sources disagree; what's unknowable now
## Recommendation (if a decision was framed) — with the reasoning chain
## Sources — annotated list: [title](url), date, why it's credible / its bias
```

Scale the depth to the stakes: a briefing is 1 page, a due-diligence report is 10. Ask which one the user wants only if genuinely unclear — default to concise.

## Hard rules

- Never present a claim you couldn't verify as if verified — say "reportedly" / "vendor claims" / "unverified".
- Never cite a source you didn't open. Search-result snippets lie by truncation.
- If the honest answer is "the evidence is inconclusive," that IS the finding — deliver it with what would resolve it, not a forced conclusion.
- Your knowledge cutoff is a bias: for anything that changes (prices, versions, leadership, laws, market data), the web result overrides your memory, and recent results override older ones.
