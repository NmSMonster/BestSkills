---
name: data-analysis
description: Analyzing a dataset to answer a question honestly — cleaning, exploring, choosing the right statistics, and presenting findings without misleading. Use when the user gives you data (CSV/Excel/JSON/database) and wants insights, trends, summaries, correlations, comparisons, or "what does this data say". Also for reviewing someone else's analysis for statistical errors. Enforces question-first analysis, data validation before conclusions, and honest uncertainty.
---

# Data Analysis

The job is a *defensible answer to a question*, not a gallery of charts. Most bad analysis fails in one of two places: trusting dirty data, or torturing clean data into a conclusion it doesn't support. This workflow guards both.

Statistical pitfalls and how to avoid them: `references/statistical-pitfalls.md`. For any visualization, also load the `dataviz` skill before drawing.

## Phase 1 — Question before data

Write the question down first, precisely: "Did feature X change 30-day retention for cohort Y?" not "look at the data." An analysis without a pre-stated question finds whatever the analyst wants to find (that's how p-hacking happens). Note:
- What decision hangs on the answer.
- What result would be surprising / would change the decision.
- What you'd expect if nothing interesting is going on (the null).

If the user hasn't given a question, propose 2–3 sharp ones from the data's shape and confirm which matters — don't silently pick.

## Phase 2 — Meet the data before analyzing it

**Never compute a statistic on data you haven't validated.** First pass, mechanically:
- **Shape**: rows, columns, types, memory. Load it, look at `head`, `dtypes`, and a random sample (not just the top — the top is often unrepresentative or a header artifact).
- **Missingness**: nulls per column, and *why* — missing-at-random vs. systematically missing (a sensor that fails at high load isn't random). How missingness is handled changes the answer; decide deliberately (drop / impute / keep as category) and record it.
- **Validity**: ranges (negative ages, prices of 0, dates in the future), categoricals (typos, `"N/A"`/`"null"`/`""` as distinct nulls, inconsistent casing/encoding), duplicates (exact and by natural key).
- **Distribution**: for each key numeric — min/max/median/quantiles, skew, and **outliers**. Look at them individually; an outlier is either the most interesting row or a data-entry bug, and you must know which before it wrecks a mean.
- **Units & definitions**: what one row *means* (an event? a user? a user-day?), what each column actually measures, timezone of timestamps, currency of money. The #1 silent error is analyzing a column that means something other than its name.

Output of this phase is a short **data-quality note**: what's dirty, what you did about it, what caveats survive. This note is part of the final deliverable, not scaffolding to throw away.

## Phase 3 — Explore, then confirm

1. **Explore (generate hypotheses)**: aggregate, group, cross-tab, plot distributions and relationships. Let the data suggest patterns.
2. **Confirm (test hypotheses)**: for each pattern that matters, ask *is it real or is it noise?* — check the sample size behind it, the spread, whether it survives an obvious confounder (see pitfalls reference).
- Keep exploration and confirmation honest: a pattern found while exploring needs confirming on the question you *started* with, not a new question invented to fit the pattern.

## Phase 4 — Right statistic, honestly computed

- **Prefer the median and quantiles** to the mean for anything skewed (income, latency, counts) — report p50/p90/p95, not just the average, which a few outliers dominate.
- **Always report dispersion and n** with any central number: "avg 4.2 (sd 3.1, n=18)" tells the truth; "avg 4.2" hides that it's noise.
- **Rates need denominators and base rates**: "conversions up 50%" is meaningless without the base (0.2%→0.3%?) and the absolute counts.
- **Comparisons need a fair baseline**: same period, same population, same definition. Watch for survivorship (only surviving accounts in the "after" set) and selection.
- **Correlation is not causation** — say "associated with," and name the plausible confounders. Only claim causation with a design that supports it (experiment, or a clearly-stated identification argument).
- **Uncertainty is a finding**: give ranges/confidence intervals where you can, and state when n is too small to conclude anything. "The data can't answer this yet" is a legitimate, valuable result.

## Phase 5 — Present without misleading

- Lead with the answer to the Phase-1 question in one or two sentences, then the evidence.
- Every number carries its context: n, time window, definition, and source.
- Charts follow the `dataviz` skill: honest axes (no truncated y-axis to exaggerate), right chart for the relationship, labeled, absolute + relative shown.
- Separate **what the data shows** from **what you infer** from **what you recommend** — three different confidence levels, visibly distinct.
- State the caveats that would change the conclusion, and what data would resolve them.

## Tooling

- Use pandas/polars (Python) or the user's stack; write the analysis as a **script or notebook that reproduces every number**, not one-off computations. The reader must be able to rerun it. Print intermediate sanity checks (row counts after each filter — a join that silently drops half the rows is the classic disaster).
- Save cleaned data and the analysis script; the deliverable is reproducible, not a screenshot of a result.

## Hard rules

- No conclusion from unvalidated data. The Phase-2 note is mandatory.
- No cherry-picking the window/segment that shows the desired result — if you tried several, say how many.
- No false precision: "42.7%" from n=14 is a lie of significance; round to what the data supports.
- If asked to prove a predetermined conclusion, report what the data actually says instead — an analysis that only confirms is worthless.
