---
name: roadmap-planning
description: Prioritizing and sequencing what to build — product roadmaps, feature prioritization, backlog ordering, and deciding what to do next and what to cut. Use when the user asks to build a roadmap, prioritize features/backlog, decide what to work on next, plan a quarter/release, choose between competing initiatives, or say no to scope. Grounded in outcomes and prioritization frameworks, not a wishlist with dates.
---

# Roadmap Planning

A roadmap is a set of prioritization decisions, not a list of features with dates. Its real job is deciding *what not to do* — because everything can't be built, and the cost of building the wrong things is the highest cost in product. A good roadmap is defensible ("here's why this before that"), outcome-oriented, and honest about uncertainty. A bad one is a dated wishlist that's obsolete in a month and treated as a promise.

## Step 1 — Anchor to outcomes, not output

Before prioritizing anything, establish **what outcomes the roadmap serves** — the product/business goals (grow activation, reduce churn, enter a segment, hit a revenue target). Features are means; outcomes are ends. Every candidate item gets judged by *how much it moves an outcome*, not by how much someone wants it or how cool it is. This reframing is what turns a wishlist into a strategy.

Prefer framing the roadmap around **themes/outcomes** ("improve onboarding conversion") over a locked feature list — it keeps the team focused on the goal and free to find the best solution, and it ages far better than "ship features A, B, C by date."

## Step 2 — Gather and understand the candidates

Collect the possible work (features, fixes, debt, bets) from all sources: user requests, data, strategy, sales, support, engineering. For each, understand enough to judge it:
- **Value**: which outcome does it move, for how many users, how much? What's the evidence (not just who asked loudest)?
- **Effort/cost**: rough size, dependencies, risk. Get engineering's read — PM guesses on effort are usually wrong.
- **Confidence**: how sure are we it'll work? A high-value/low-confidence bet is different from a sure thing.
- **Urgency/timing**: is there a deadline, a market window, a dependency, a decaying opportunity?

## Step 3 — Prioritize with a framework (not gut alone)

Use an explicit framework so decisions are consistent and defensible — the framework structures the judgment, it doesn't replace it:

- **RICE**: `(Reach × Impact × Confidence) / Effort`. Great for comparing many items objectively. Reach = how many affected per period; Impact = how much per user; Confidence = your certainty (%); Effort = person-time. Score, rank, sanity-check.
- **Value vs. Effort (2×2)**: quick and visual. **Quick wins** (high value, low effort) → do first. **Big bets** (high value, high effort) → plan deliberately. **Fill-ins** (low value, low effort) → maybe, between. **Money pits** (low value, high effort) → don't. Plot everything; the map makes the decision obvious.
- **Kano** (for feature *types*): distinguish must-haves (basic expectations — absence hurts, presence doesn't delight), performance features (more is better), and delighters (unexpected wins). Cover the must-haves before chasing delighters.
- **Weighted scoring** against your specific criteria when you have several outcomes to balance.

No framework is truth — they're aids to consistent thinking. Score, then step back: does the ranking make strategic sense? Adjust for strategy the numbers can't see (a foundational investment, a competitive necessity), but *state* when you override the score and why.

## Step 4 — Sequence

Ranking isn't sequencing. Order the work considering:
- **Dependencies**: what must come before what (foundations before features built on them).
- **Quick wins early**: deliver value and momentum soon; don't front-load only 6-month epics.
- **Balance**: mix new value, tech debt/reliability, and bets — an all-features roadmap accrues debt that eventually halts everything; an all-debt one delivers no visible value. Reserve capacity for each.
- **Risk**: tackle the riskiest assumptions early (a cheap experiment before a big build) so you fail cheap, not expensive.
- **Capacity realism**: plan to actual team capacity minus the reality tax (support, bugs, meetings, the unexpected). Overstuffed roadmaps are how everything ships late.

## Step 5 — Handle time and uncertainty honestly

- **Near-term specific, far-term fuzzy.** "Now / Next / Later" horizons are more honest than precise dates months out. Commit firmly to the current cycle; keep later intentionally loose — you'll learn things that change it.
- If dates are required (launches, commitments), give ranges and flag the assumptions and risks. A false-precision date is a broken promise waiting to happen.
- A roadmap is a **living document reviewed regularly**, not a contract. New information should change it — that's the roadmap working, not failing. Communicate changes and the *why*.

## Step 6 — Say no, clearly

The hardest and most valuable output: **explicitly deciding what you won't do**, and being able to explain why (lower priority against the outcomes, not aligned with strategy, poor value/effort). A roadmap that tries to do everything commits to nothing. Saying no to good-but-lower ideas is what makes room to do the important ones well. Keep a visible "not now / not doing" list so stakeholders see their request was considered, not ignored.

## Deliverable

A prioritized roadmap: the outcomes it serves, the prioritized initiatives (with the framework scores/reasoning that ranked them), sequenced into Now/Next/Later (or the cycle), the capacity assumption, the key risks, and an explicit "not doing / deprioritized" list with reasons. Right-size it — a startup gets a lean themed roadmap; a larger org gets more structure. Present it so a stakeholder understands not just *what's* planned but *why this order*.

## Rules

- Prioritize by outcome impact, not by who asked loudest or what's exciting.
- Use a framework for consistency, then apply strategic judgment on top — and state overrides.
- Sequence for dependencies, early value, risk-reduction, and a debt/features/bets balance.
- Plan to realistic capacity; near-term firm, far-term fuzzy; no false-precision dates.
- Decide and communicate what you *won't* do — that's the roadmap's core value.
- Treat it as living; update on new information and explain the change.
