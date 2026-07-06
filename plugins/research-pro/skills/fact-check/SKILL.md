---
name: fact-check
description: Verifying specific claims, statistics, quotes, or statements against primary sources with an explicit verdict. Use when the user asks "is it true that…", wants a claim/article/post verified or debunked, questions a statistic or quote, or needs pre-publication checking of a document's factual claims. Delivers per-claim verdicts with evidence, not vague impressions.
---

# Fact-Check

A fact-check delivers a **verdict per claim, with evidence** — not an essay of vibes. The unit of work is the individual claim; the standard of proof is the primary source.

## Step 1 — Decompose

Break the input into individual checkable claims. A single sentence often contains several:

> "Company X, the market leader, laid off 30% of staff in January after revenue fell for a third straight quarter."

→ (a) X is the market leader, (b) laid off 30%, (c) in January, (d) revenue fell, (e) for three consecutive quarters. Each gets its own verdict — (b) can be true while (a) and (e) are false.

Classify each claim:
- **Empirical** (number, date, event, attribution) → checkable, proceed.
- **Definitional** ("largest" by what measure?) → pin the definition first; many "false" claims are true under one definition and false under another. Report both.
- **Opinion/prediction** → not checkable; label it as such and move on. Don't grade opinions as facts.

## Step 2 — Trace to origin

For each empirical claim, hunt the **primary source**: the filing, dataset, paper, transcript, or original announcement — not coverage of it.

- Statistics: find the actual study/dataset. Check: sample size, year of data (not year of article), what was actually measured vs. what the claim says it measured. The #1 fact-check failure mode is a real number describing a different thing.
- Quotes: find the full transcript/video. Check for context stripping — the sentence before and after, whether it was hypothetical, sarcastic, or quoting someone else.
- Events: two independent contemporaneous reports, or one primary record.
- Superlatives ("first", "biggest", "only"): search for counterexamples directly — one counterexample settles it.
- Viral claims: check dedicated fact-checkers (Snopes, AFP, Reuters/AP fact check, Demagog for PL) *and* still trace the primary source yourself — fact-checkers err too.

Beware **citogenesis**: claim appears in Wikipedia/article → gets cited by others → the echoes are then offered as confirmation. Trace dates: who said it *first*, based on what?

## Step 3 — Verdict

Use this scale, one verdict per claim:

| Verdict | Meaning |
|---|---|
| ✅ **True** | Matches primary sources; numbers within rounding |
| 🟡 **Mostly true** | Core accurate; detail off (wrong year, rounded aggressively, outdated figure that was once right) |
| 🟠 **Misleading** | Technically-true statement engineered to imply something false (cherry-picked range, wrong base, definition games) — explain the mechanism |
| ❌ **False** | Contradicted by primary evidence |
| ❓ **Unverifiable** | No adequate source exists either way — say what *would* settle it |

"Misleading" is the most valuable verdict you can issue — it's where most real-world deception lives. Always name the trick: truncated axis, absolute-vs-relative ("doubled" from 0.1% to 0.2%), survivorship, denominator swap, correlation-as-causation.

## Step 4 — Report

```
## Verdict summary
| # | Claim | Verdict | One-line basis |

## Detail (per claim)
Claim: <exact wording checked>
Verdict: <emoji + label>
Evidence: <what the primary source actually says, quoted/linked, dated>
Note: <definition issues, context, how the error likely arose>
```

## Rules

- Check the claim **as stated**, then note the nearby true version if one exists ("False as stated; the correct figure is 12%, not 30%").
- Never issue ✅/❌ from your training memory alone for anything post-2023, volatile, or contested — search. Memory is a hypothesis, not evidence.
- Symmetric standards: apply the same rigor to claims you expect to be true as to ones you expect to be false. Write down your prior, then try to break it.
- Absence of evidence for an extraordinary claim, after a genuine search of where evidence *would* be, supports ❌/❓ — say which search you ran.
- Cite everything; date everything; link the primary source, not the aggregator.
