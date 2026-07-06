---
name: systematic-debugging
description: Hypothesis-driven debugging workflow for any bug, error, crash, flaky test, or unexpected behavior. Use when the user reports something broken, failing, wrong output, a regression, an exception, or "it worked yesterday" — before proposing any fix. Enforces reproduce-first, bisection, root-cause verification, and a fix that is proven rather than guessed.
---

# Systematic Debugging

Debugging is a search problem. Guessing fixes burns the user's time and trust; this workflow finds the actual cause and proves the fix. Never patch a symptom you cannot explain.

## Iron rules

1. **Reproduce before you touch anything.** A bug you cannot reproduce is a bug you cannot verify as fixed.
2. **One hypothesis at a time.** Every experiment must be able to *falsify* the current hypothesis.
3. **Change one variable per experiment.** If you changed two things and it works, you learned nothing.
4. **The fix is done when the reproduction passes AND you can state the root cause in one sentence.** "It works now" is not a root cause.
5. **Revert every diagnostic change** (prints, sleeps, disabled checks) before finishing.

## Workflow

### Phase 1 — Capture the crime scene
- Get the exact error: full stack trace, logs, failing command, expected vs. actual output. If the user paraphrased, run it yourself.
- Record environment facts that matter: versions, OS, branch, recent changes (`git log --oneline -15`, `git diff HEAD~5 --stat`).
- Write down the **minimal reproduction command** and confirm it fails deterministically. If it's flaky, run it 10–20 times and record the failure rate first — that rate is your baseline signal.

### Phase 2 — Localize
Pick the cheapest applicable localization strategy, in this order:

| Situation | Strategy |
|---|---|
| Worked before, broken now | `git bisect` (or manual bisect over commits) — this is almost always fastest, do it before reading code |
| Error has a stack trace | Read the trace bottom-up; open the deepest frame in *your* code first |
| Wrong output, no error | Binary-search the data flow: log/assert intermediate values at the midpoint, then halve |
| Fails only in one environment | Diff the environments (versions, env vars, config, data) before diffing code |
| Flaky | Look for time, ordering, shared state, network, and randomness; try forcing each (fixed seed, single thread, frozen clock) |

- Prefer **adding assertions** over adding prints: an assertion documents the expectation and fails loudly at the exact divergence point.
- When bisecting code paths, comment nothing out that changes behavior for other tests — use feature flags or copies in scratch files.

### Phase 3 — Hypothesize and test
For each hypothesis, write (in your working notes or the conversation):
```
Hypothesis: <specific, falsifiable cause>
Prediction: if true, then <observable X> when I <experiment>
Result: <observed> → confirmed / rejected
```
- Rejected hypotheses are progress. Keep a short list so you never re-test one.
- If three hypotheses in a row fail, zoom out: question an assumption from Phase 1 (Is it even running the code I think? Right binary? Right config? Cached artifact?). Verify with a deliberately-broken change ("if I add `raise` here, does it crash?") — if not, you're editing dead code.

### Phase 4 — Fix and prove
1. State the root cause in one sentence before writing the fix.
2. Write a **failing test that encodes the bug** (or keep the reproduction script) — run it, watch it fail.
3. Apply the minimal fix at the root cause, not at the symptom site.
4. Run: the new test (now passes), the original reproduction (passes), and the surrounding test suite (no regressions).
5. Search for **siblings of the bug**: the same mistaken pattern elsewhere (`grep` for the same API misuse, same copy-pasted block). Fix or report them.

### Phase 5 — Report
Deliver to the user, in this order: root cause (one sentence) → evidence → the fix and why it's minimal → how it was verified → any sibling risks found. Do not narrate the dead-ends unless asked.

## Anti-patterns (hard stops)

- **Shotgun debugging**: changing several plausible things and re-running. Undo, and go back to Phase 3.
- **Fixing the test** to match broken behavior without proving the behavior is actually correct.
- Adding `sleep`, retries, or `try/except pass` to make a symptom disappear. These are concealment, not fixes — allowed only as an explicitly-labeled temporary mitigation the user approves.
- Declaring victory on "can't reproduce anymore" without knowing what changed.
- Trusting memory of the codebase over reading the current code — always re-read the function you're blaming.

## Common rationalizations (recognize these — they're the failure mode, not you being efficient)

| Excuse | Reality |
|---|---|
| "This is obviously just a typo/off-by-one, I don't need to reproduce it" | Obvious guesses are wrong often enough that skipping reproduction just means shipping an unverified fix with high confidence — the dangerous kind |
| "I already know what's wrong from reading the code" | Reading is a hypothesis generator, not evidence. State it as Phase 3's hypothesis and test it like any other |
| "The user is in a hurry, let me just try a fix" | A guessed fix that misses costs more of their time than 5 minutes of reproduction — you'll be back here after it doesn't work |
| "It works now, that's good enough" | Without a stated root cause you don't know if it's fixed or just moved/hidden. One sentence of root cause is the actual finish line |
| "I'll add a broad try/except so it stops crashing" | That's concealment, not a fix — the bug still fires, you just stopped being told about it |
| "I tested it once and it passed" | One pass after a fix for an intermittent bug is noise, not signal — rerun at the same rate you measured the failure at |
| "Three hypotheses failed, let me try a fourth similar one" | Three failures in the same direction mean a wrong assumption upstream, not bad luck — zoom out per Phase 3, don't keep drilling the same hole |

## Red flags — stop and go back to the workflow if you notice yourself

- Proposing a fix before you've run the reproduction yourself
- Changing more than one thing between test runs
- Explaining *why* the fix should work instead of showing that it does
- About to remove a debug print/sleep and move on without confirming it was the actual cause
- Saying "should be fixed now" instead of "fixed: `<root cause>`, verified by `<test>`"

## Escalation

If after Phase 3 the cause is still unknown and you've spent significant effort: summarize confirmed facts, rejected hypotheses, and the single most-informative next experiment — then present that to the user instead of looping silently.
