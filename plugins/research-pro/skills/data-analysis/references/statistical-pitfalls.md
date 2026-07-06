# Statistical Pitfalls

The errors that turn a confident analysis into a wrong one. Each entry: the trap, how to spot it, what to do. Run this list against your own analysis before delivering, and against anyone else's when reviewing.

## Aggregation & grouping traps

**Simpson's paradox** — a trend in every subgroup reverses when you pool them. Spot: whenever you aggregate across groups of unequal size or mix. Do: analyze within meaningful subgroups; be suspicious of any single pooled number comparing two populations with different composition. (Classic: a treatment worse overall but better in every severity group, because it was given to sicker patients.)

**Base-rate neglect** — judging a rate without its base. "90% accurate test" on a 1-in-1000 disease is mostly false positives. Do: always compute the absolute numbers behind a percentage; for classifiers, look at precision at the real base rate, not accuracy.

**Ecological fallacy** — inferring about individuals from group averages (or vice versa). Group-level correlation ≠ individual-level. Do: keep the unit of analysis matched to the unit of the claim.

## Sampling & selection traps

**Selection bias** — the sample isn't the population you're claiming about. Spot: how were these rows collected? Survey respondents, users who didn't churn, successful trades. Do: name who's *missing* and whether their absence skews the answer.

**Survivorship bias** — analyzing only the things that made it. Returns of *current* funds, health of *retained* users, planes that came back. Do: ask "what got filtered out before this dataset existed?"

**Nonresponse / missing-not-at-random** — the missing data differs systematically from the present data. Do: treat missingness as a variable; test whether missing rows differ on observables.

## Significance & multiplicity traps

**p-hacking / multiple comparisons** — test enough slices and something looks "significant" by chance. Spot: subgroup fishing, trying many metrics/windows, "we found that Tuesday users in region 3…". Do: state hypotheses before looking; if you tested k things, say so and adjust (Bonferroni/FDR) or treat findings as exploratory needing confirmation.

**Confusing significance with importance** — a tiny, useless effect can be "statistically significant" at huge n; a large, important effect can be "non-significant" at tiny n. Do: report effect *size* and practical meaning, not just a p-value. p < 0.05 is not a truth stamp.

**Garden of forking paths** — analysis choices (which outliers to drop, how to bin, which covariates) made after seeing the data, each defensible, together fitting noise. Do: pre-specify choices where possible; report how sensitive the result is to them.

## Causation traps

**Correlation ≠ causation** — the default error. Two variables move together because: A→B, B→A, C→both (confounder), coincidence, or selection. Do: state "associated"; list confounders; reserve causal language for experiments or a defended identification strategy.

**Confounding** — a lurking variable drives both. Ice-cream sales and drownings (summer). Do: for any causal-sounding claim, brainstorm the third variable; control for it or concede you can't.

**Regression to the mean** — extreme measurements are followed by less-extreme ones by chance alone, faking "improvement." The worst performers "improve" after intervention even if the intervention did nothing. Do: use a control group; don't attribute mean-reversion to your action.

**Reverse causation** — you have the arrow backwards ("hospitals cause death": sick people go to hospitals). Do: check the time order and the mechanism.

## Measurement & presentation traps

**Goodhart's law** — once a metric is a target, it stops measuring what it did. Spot: optimizing a proxy (clicks) for the real goal (value). Do: watch for gaming; triangulate with a second metric.

**Truncated / dual axes** — a y-axis not starting at 0, or two axes chosen to fake correlation. Do: honest axes; if truncation is justified (zoom on small variation), label it loudly.

**Mean of a skewed distribution** — average income, latency, response time. The mean sits above the median and describes almost no one. Do: median + p90/p95; show the distribution shape.

**False precision** — "37.42%" from n=20. Reporting more digits than the sample supports. Do: round to the data's resolution; show n next to every rate.

**Ratio & percentage-change ambiguity** — "increased 200%", "1 in 5 fewer" — absolute vs relative, and of what base. Do: give both the relative change and the absolute numbers.

## Time-series specific

- **Seasonality** mistaken for trend — compare like periods (YoY, same weekday), or deseasonalize.
- **Autocorrelation** — successive points aren't independent; naive significance tests overstate confidence.
- **Cherry-picked window** — a start/end date chosen to show the desired slope. Do: show the full series; justify the window.

## The review pass

Before delivering any analysis, ask:
1. Is the unit of analysis consistent with the claim?
2. What's missing from this data, and does its absence bias the answer?
3. Did I compare fairly (same period, population, definition)?
4. Is this correlation dressed as causation?
5. How many things did I try before this result?
6. Does the effect *matter*, not just "significant"?
7. Would this survive an obvious confounder?
8. Am I reporting more precision/certainty than n supports?

If any answer is uncomfortable, that caveat goes in the deliverable.
