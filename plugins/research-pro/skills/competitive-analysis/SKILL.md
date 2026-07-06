---
name: competitive-analysis
description: Structured teardown of competitors, products, or vendors — feature and pricing comparison, positioning, strengths/weaknesses, and strategic read. Use when the user asks to compare competitors/products/tools, analyze a competitor, build a comparison matrix, evaluate vendors for a decision, or asks "who are the players in X and how do they differ".
---

# Competitive Analysis

The output of competitive analysis is a **decision aid**, not an encyclopedia of companies. Everything gathered must ladder up to: what does this mean for the user's decision or strategy?

## Phase 0 — Frame the decision

Establish (ask only if it materially changes the work):
- **Whose perspective**: buying a tool? competing against these companies? investing? The same facts read differently.
- **Decision criteria**: the 4–8 dimensions that actually matter to the user (price, specific capabilities, integrations, compliance, support, lock-in risk, viability…). These become the comparison axes — not the union of every vendor's feature list.
- **The field**: direct competitors, indirect substitutes (spreadsheet, in-house build, "do nothing"), and emerging entrants. Include the substitutes — they're the most-forgotten competitor and often the real one.

Cap the deep-dive set at 3–6; list the long tail in one line each.

## Phase 1 — Gather (per competitor)

Work sources in this order of reliability:
1. **Product itself**: docs, changelog/release notes (velocity + direction signal), public demo/trial, API reference (reveals real capabilities behind marketing nouns), status page (reliability).
2. **Pricing page** — capture actual numbers *with date*; note what's gated behind "Contact sales" (that's a segment signal, not an absence of price). Model total cost at the user's realistic scale, including overage/seat math.
3. **Customers' voice**: G2/Capterra (read the 2–3-star reviews — 5s and 1s are noise), Reddit/HN threads, GitHub issues for OSS. Hunt for the repeated complaint — one theme across many reviewers is signal.
4. **Company trajectory**: funding/filings, hiring pages (what they're building next), leadership changes, layoffs; for public cos, the 10-K competition & risk sections — companies are legally motivated to be honest there.
5. **Vendor marketing** — last, and only as claims. The comparison pages vendors write about each other are useful precisely for what each chooses to attack.

Log every source with dates — pricing and features rot within months.

## Phase 2 — Analyze

- **Comparison matrix** on the decision criteria from Phase 0. Cells contain facts ("SOC 2 Type II, since 2024"), not adjectives ("strong security"). Unknown = "unverified", never a guess.
- **Positioning read** per competitor: who they win with and why (their best-fit customer), where they lose (the repeated complaint, the missing capability), pricing strategy (premium/penetration/usage-based) and what that says about their target.
- **Strategic dynamics**: where the market is consolidating, what the changelogs say everyone is racing toward, moats (network effects, data, switching costs, distribution) vs. imitable features, and any red flags (stalled changelog, exec exodus, acquisition rumors → roadmap risk).
- Force the "so what": every finding gets an implication for the user's decision. A finding with no implication gets cut.

## Deliverable

```
# Competitive analysis: <space>, for <decision>
## Bottom line — recommendation / read in 3–5 sentences
## The field — map of players incl. substitutes, one line each
## Comparison matrix — criteria × competitors, facts only, dated
## Per-competitor read — wins-with / loses-on / trajectory (3–6 deep dives)
## Strategic implications — what this means for the user's decision, risks, timing
## Sources — dated, annotated
```

## Rules

- Vendor claims are labeled as such everywhere ("claims 99.99% SLA").
- No adjective without evidence: replace "market leader" with the metric and its source, or drop it.
- Date-stamp the whole analysis prominently — it depreciates fast.
- If two options are genuinely close, say so and identify the tiebreaker question, rather than manufacturing a winner.
