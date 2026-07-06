---
name: product-requirements
description: Writing product requirements that align a team on what to build and why — PRDs, specs, user stories, and acceptance criteria. Use when the user asks for a PRD, product spec, requirements doc, user stories, feature spec, or needs to define what to build before engineering starts. Focuses on the problem and success criteria over prescribing implementation, and on being clear enough to build from without ambiguity.
---

# Product Requirements

A requirements doc exists to get everyone building the *same right thing* — it aligns product, design, and engineering on the problem, the solution's shape, and what "done" means, before expensive work starts. The two failure modes: too vague (everyone interprets differently, wrong thing gets built) and too prescriptive (dictates implementation, wastes the team's expertise, goes stale instantly). Aim between: crisp on the *what and why*, open on the *how*.

## Start with the problem, not the feature

The most important discipline: **define the problem before the solution.** A PRD that opens with "build a dashboard" has skipped the only question that matters — *why*. Start with:
- **The problem / opportunity**: what user or business problem are we solving? What's the evidence it's real and worth solving (data, research, support tickets, revenue)? Who has this problem?
- **The goal & success metrics**: what outcome defines success, measurably? "Reduce checkout abandonment from 40% to 25%" — not "improve checkout." If you can't state how you'll know it worked, you're not ready to spec it. This metric is what the whole doc is accountable to.
- **Why now**: priority rationale — why this over the other things the team could build.

Solving the wrong problem excellently is the most expensive mistake in product; this section prevents it.

## The PRD structure

```
# <Feature> PRD
## Problem & context — what problem, for whom, evidence it matters
## Goals & success metrics — the measurable outcome(s); how we'll know it worked
## Non-goals — what this explicitly does NOT do (scope guardrails)
## Users & use cases — who uses it, the scenarios/jobs-to-be-done
## Requirements — what it must do (see below)
## UX — flows/wireframes or a link (pairs with ui-ux-design)
## Acceptance criteria — testable conditions for "done"
## Open questions & risks — what's unresolved, what could go wrong
## Out of scope / future — the deliberate later
```

**Non-goals deserve special emphasis** — explicitly stating what you're *not* building is one of the highest-value parts of a spec. It prevents scope creep, cuts debate, and focuses the team. Most under-specified docs are missing their non-goals.

## Writing the requirements

- **User stories** frame requirements around user value: "As a [user], I want to [action] so that [benefit]." The "so that" is essential — it carries the *why*, which lets engineers make good local decisions. A story without it is a demand without context.
- **Prioritize explicitly** (MoSCoW: Must / Should / Could / Won't, or P0/P1/P2). Not everything is required for v1 — mark what's essential vs. nice-to-have, so when time gets tight (it will), the cuts are pre-decided, not panic-decided.
- **Specify behavior, including edge cases**: the happy path *and* what happens on error, empty, limits, permissions, concurrent use. Vague requirements get the edge cases wrong because nobody decided them.
- **Describe the what, not the how.** "Users can filter results by date" (what) not "add a MongoDB aggregation with a date index" (how — that's engineering's call). Constrain implementation only where there's a real requirement (a compliance rule, a performance budget, an existing-system constraint) — then state it as a constraint with its reason.

## Acceptance criteria (what makes it testable)

Each requirement needs **acceptance criteria**: specific, testable conditions that define done. Given/When/Then works well:
> Given a logged-in user with items in cart, When they apply an expired promo code, Then they see "This code has expired" and the total is unchanged.

Good acceptance criteria are unambiguous (two people would agree whether it's met), cover the edge/error cases, and are testable. They're the contract between "built" and "accepted" — and they double as the QA checklist.

## Quality bar

- [ ] The problem and *why* are clear before any solution; success is measurable.
- [ ] Non-goals and out-of-scope are stated — scope is fenced.
- [ ] Requirements are prioritized (must vs. nice-to-have).
- [ ] Behavior is specified including errors/edges, not just the happy path.
- [ ] Acceptance criteria are testable and unambiguous.
- [ ] It says *what and why*, leaving *how* to the builders except where a real constraint exists.
- [ ] Open questions and risks are surfaced, not hidden.
- [ ] A new engineer/designer could build the right thing from this without a meeting to decode it (then have the meeting anyway — but to refine, not to translate).

## Working method

- Right-size it: a small feature gets a one-pager; a major initiative gets the full doc. A 20-page PRD for a button is waste; a one-liner for a payments overhaul is negligence.
- Draft with **open questions marked inline** (`⚠ TBD: which currencies at launch?`) — surfacing unknowns is more valuable than papering over them. Resolve them with the right people before build.
- A PRD is a living alignment tool, not a contract carved in stone — update it as understanding evolves, but track changes so the team isn't building to a stale version.
- Collaborate: the best requirements come *from* engineering and design input, not thrown *over the wall*. Write it to invite their expertise (that's why you leave the "how" open).
