---
name: pitch-deck
description: Crafting investor pitch decks, sales proposals, and persuasive business narratives — story arc, slide-by-slide structure, the ask, and objection handling. Use when the user asks for a pitch deck, investor presentation, fundraising materials, sales proposal, sponsorship/partnership pitch, or wants to make a business argument persuasive to a specific audience.
---

# Pitch Deck & Persuasive Business Documents

A pitch is a decision-forcing narrative: it exists to get a specific yes from a specific audience. Every slide either advances the argument toward the ask or gets cut. Beautiful decks with no argument lose to ugly decks with an inevitable one.

## Step 0 — Define the yes

Before any content: **who** is the audience (pre-seed angel ≠ Series A fund ≠ bank ≠ enterprise buyer), **what exact yes** do we need (meeting? term sheet? signed pilot?), and **what do they need to believe** for yes to be rational? List those 3–5 beliefs — the deck's job is to install them, in order. Confirm the ask amount/terms with the user; a pitch without a concrete ask is a status update.

## The investor deck — 10–12 slides, one idea each

The narrative arc: *the world changed → big problem → we solve it uniquely → it's working → huge if it keeps working → this team wins → join now.*

1. **Title** — company, one-line description a stranger repeats correctly ("Stripe for X" only if precise), contact.
2. **Problem** — who suffers, how much it costs them, why current solutions fail. Make it *felt*: one concrete story or damning number beats five bullets.
3. **Why now** — the shift (tech/regulatory/behavioral) that makes this newly possible. Answers "why hasn't this been done?"
4. **Solution** — what the customer experiences (demo shots > architecture); the one mechanism that makes it work.
5. **Traction** — the strongest evidence, honestly framed: revenue curve, retention cohort, usage growth, signed LOIs, waitlist w/ conversion. Real numbers with axes; growth *rates* with absolute bases. This slide moves rounds — front-load it (slide 3) if it's strong.
6. **Market** — bottom-up TAM/SAM/SOM (from `market-analysis`); the beachhead and expansion logic.
7. **Business model** — who pays what; unit economics (CAC, LTV, margin, payback) once real; pricing evidence.
8. **Competition** — honest 2×2 or table on dimensions *customers* choose by; your durable advantage. Never "no competitors"; never a feature-checklist where you win every row (reads as rigged).
9. **Go-to-market** — the repeatable channel, its math, proof it works at small scale.
10. **Team** — why *these people* are unfairly suited: relevant wins, domain scars, key gaps + hiring plan.
11. **Financials** — 3-year driver-based summary (from `financial-model`): revenue, burn, the milestone path.
12. **Ask** — amount, what it buys (18–24 months to which milestones), and the milestone → next-round logic. Specific: "€1.5M for 20 months: ship X, reach €80k MRR, raise A."

Rules of the form: one idea per slide, headline states the *takeaway* ("Retention is 94% at month 6", not "Retention"), ≤ 30 words of body, every chart labeled and honest (no truncated axes, absolute + relative shown). Appendix slides for the deep questions (detailed financials, security, cap table) — anticipate the top 10 diligence questions and park answers there.

## Sales proposal / enterprise pitch variant

Different yes, different arc: *their* stated problem in *their* words → cost of inaction (quantified) → proposed solution mapped to their evaluation criteria → proof (case studies, pilot results, references) → implementation plan with their effort minimized → pricing with options (anchor high, 2–3 tiers) → risk reversal (pilot, SLA, exit terms) → next step with a date. Personalization is the whole game: a proposal that could be sent to their competitor unchanged will lose.

## Narrative quality bar

- [ ] The "beliefs to install" from Step 0 each map to specific slides; nothing else survives.
- [ ] A stranger reading only the headlines gets the full argument (headline test — read them aloud in sequence).
- [ ] Every claim has evidence on-slide or in appendix; adjectives ("huge", "revolutionary") replaced by numbers or deleted.
- [ ] The three hardest objections (why won't the incumbent do this? why is this defensible? why this price?) are answered *before* the audience asks — pre-empting reads as confidence.
- [ ] Honesty check: nothing on any slide that dies in diligence. One caught exaggeration poisons every other claim.
- [ ] The ask is specific and the last thing they see.

## Working method

1. Write the narrative as 10–12 headline sentences first; get user sign-off on the argument before designing anything.
2. Then build slides (Markdown outline, or HTML/pptx if asked), traction and financial exhibits computed from real inputs the user provides — never invent traction numbers; mark placeholders `[TK]` loudly.
3. Deliver with: the deck, speaker notes per slide (what to *say*, which is more than what's shown), and the anticipated-objections list with answers.
