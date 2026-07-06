---
name: market-analysis
description: Sizing and analyzing a market — TAM/SAM/SOM built bottom-up, segmentation, growth drivers, industry structure (Porter's forces), trends, and entry assessment. Use when the user asks how big a market is, whether to enter one, for a market overview/landscape, market sizing for a pitch or plan, or "is there a market for X". Produces defensible numbers with shown work, not copied headline figures.
---

# Market Analysis

The output is a defensible view of how big, how fast-growing, and how winnable a market is — with every number's derivation shown. A market analysis whose numbers can't survive the question "where did that come from?" is decoration.

## Step 1 — Define the market precisely

Most bad market analysis dies here. Write one sentence: **who** (customer segment) buying **what** (product category) for **which job**, in **which geography**. "The AI market" is not a market; "mid-market EU e-commerce companies buying customer-service automation" is. Note adjacent definitions you're excluding — reviewers will ask.

## Step 2 — Size it: TAM / SAM / SOM

Build **bottom-up first**; use top-down only as a cross-check.

- **Bottom-up TAM** = (number of potential buyers in the defined market) × (realistic annual spend per buyer). Get buyer counts from statistical offices (Eurostat/GUS/census business registries), industry associations, LinkedIn counts, app-store data; get spend from actual price points × usage, or existing budget lines being displaced.
- **SAM** = the TAM slice your model can serve (geography, segment, channel, language, regulatory reach today).
- **SOM** = what you can plausibly capture in 3–5 years given the go-to-market — justified by an acquisition math ("N reps × M deals/yr × ACV", or "X% of channel traffic × conversion"), **never** "we assume 1% of the market".
- **Top-down cross-check**: analyst headline number (Gartner/IDC/Statista) — if it diverges from bottom-up by >2×, investigate whose definition differs. Report both with the reconciliation.
- Show every equation with its inputs and each input's source + date. Run a sensitivity: which single assumption moves the result most; give a low/base/high range rather than one false-precision number.

Red flags to avoid in your own work: citing a market-report headline that includes segments you don't serve; multiplying "everyone on earth" by a price; SOM stated as an unjustified % of TAM.

## Step 3 — Structure: is this market *good*?

Size without structure misleads — a huge market can be unwinnable. Assess Porter's five forces, each with evidence and a High/Med/Low rating:

1. **Rivalry** — competitor count and concentration, price-based vs. feature-based competition, growth rate (growing markets tolerate entrants; flat ones fight for share).
2. **New-entrant threat** — capital, regulation, tech moats, distribution lock-ups. If entry is easy for you, it's easy for the next ten.
3. **Buyer power** — concentration of customers, switching costs, price sensitivity.
4. **Supplier power** — dependence on platforms/APIs/channels that can re-price you (an app built on one API has a supplier problem).
5. **Substitutes** — including "do nothing" and "spreadsheet + intern", usually the largest competitor in B2B.

Add the modern sixth: **platform/regulatory dependence** — one algorithm change or ruling away from a different market?

## Step 4 — Dynamics

- **Growth rate** with driver decomposition: is growth from more buyers, higher prices, or more usage per buyer? They have different futures.
- **Trends & timing**: technology shifts, regulation in the pipeline, funding climate, demographic movement. For each: evidence, direction, and *so-what* for entry timing.
- **Segmentation**: split the market 2–3 ways (size, vertical, geography, willingness-to-pay); identify the beachhead segment — underserved + reachable + painful problem — and say why.

## Deliverable

```
# Market analysis: <precise market definition>
## Bottom line — size (range), growth, attractiveness verdict, best entry point (5 sentences)
## Sizing — TAM/SAM/SOM: equations, inputs w/ sources+dates, low/base/high, top-down reconciliation
## Structure — five forces table (rating + evidence), overall winnability read
## Dynamics — growth drivers, trends w/ implications, segmentation & beachhead
## Risks & unknowns — what would change the verdict; data you couldn't get
## Sources — dated, annotated
```

## Rules

- Every number: source, date, and whether it's reported fact or your derivation.
- Vendor-sponsored market reports are labeled as such and never the sole basis for the headline size.
- State the as-of date prominently; market data ages in quarters.
- If the honest verdict is "small market" or "structurally hostile", deliver it plainly — a true unfavorable analysis is worth more than a flattering one.
