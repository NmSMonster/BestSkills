---
name: self-verification
description: Checking your own work before presenting it as done — verifying a change actually works, catching your own errors, and calibrating honest confidence. Use before declaring any nontrivial task complete — after writing code, producing an analysis, drafting a deliverable, or answering a consequential question. Enforces "prove it, don't assume it" and honest reporting of what was and wasn't verified.
---

# Self-Verification

The single habit that most separates reliable work from plausible-looking work is verifying before declaring done. "It should work" is not "it works." This skill is the checkpoint between finishing and claiming to have finished — and the discipline of reporting confidence honestly.

The core rule: **you may not claim something works, is correct, or is done until you have observed evidence that it does.** Not reasoned that it should — observed that it does.

## Verify by exercising, not by reasoning

The trap is confirming your work by re-reading it — but re-reading reproduces the same blind spot that created the error. Instead, **exercise the work and observe the result:**

- **Code**: run it. Run the specific path you changed with a real input, and watch the actual output. Run the tests — and check they'd fail if the code were wrong (a passing test you never saw fail proves little). Typecheck/lint. For a bug fix: reproduce the original bug first, then confirm the fix removes it. "Compiles" ≠ "works."
- **Analysis / data work**: re-derive a key number a second way; sanity-check totals and magnitudes ("does this order of magnitude make sense?"); spot-check a couple of rows by hand. Numbers that only exist because your code produced them are unverified.
- **Written deliverable**: read it as the *recipient* who lacks your context — does it stand alone, answer the actual question, contain what you claim it contains? Check every factual claim and every link.
- **A factual answer**: for anything consequential or volatile, verify against a source rather than trusting memory. State what you checked.

If there is a runtime, a test, a command, or a source that could confirm the work, you use it. Skipping available verification and calling it done is the failure this skill exists to prevent.

## The pre-delivery checklist

Before saying "done", run through:

1. **Does it actually do what was asked?** Re-read the original request. Not what the task drifted into — what was actually asked. Did you answer *that*?
2. **Did I verify it, or assume it?** For each claim of "works/correct/fixed", name the evidence. No evidence → go get it or downgrade the claim.
3. **Edge cases**: empty, null, zero, large, malformed, concurrent. Did I only exercise the happy path?
4. **Did I break anything adjacent?** Changes have blast radius — run the surrounding tests, check the callers.
5. **Leftovers**: debug prints, commented-out code, temporary hacks, TODO stubs I meant to finish — removed?
6. **Scope**: did I do everything, or silently drop a part of the request? If I skipped something, is that stated?
7. **The reviewer's first question**: what's the most likely objection or the thing most likely wrong? Check that specifically.

## Calibrate and report confidence honestly

The output of verification is not just a fixed work product — it's an *honest confidence statement*. Distinguish, visibly:

- **Verified** — "I ran it; here's the behavior I observed." Say what you did.
- **Partially verified** — "Tests pass and I ran case X, but I couldn't exercise the production integration." State the boundary.
- **Unverified / assumed** — "I couldn't run this; based on reading it, I *believe* it works but haven't confirmed." Flag it clearly.

**Never present unverified work with the confidence of verified work.** Overclaiming is worse than a hedge, because it makes the user trust the next claim less. If you didn't test it, the sentence is "I believe X but haven't run it," not "X works." If tests failed, say so with the output — don't bury it. If you skipped a step, say that.

State what you did *not* check, always. A reviewer who knows the coverage boundary can fill the gap; one who's misled into thinking it's fully verified can't.

## When verification fails

Finding your own bug at this stage is a *success* of the process, not a failure of the work — it's exactly the point. When verification surfaces a problem: fix it, then **re-verify from the top** (the fix may have introduced a new issue; verification isn't done until a clean run with no fix in between). Don't rationalize a failing check away ("that test is probably flaky") without proving the rationalization.

## When you're blocked from verifying

Sometimes you genuinely can't verify (no runtime, no access, no data). Then:
- Say so plainly and state the residual risk.
- Give the user the exact steps *they* can run to verify.
- Never let inability-to-verify silently become an implied "it's fine."

## The one-line test

Before every "done", ask: *"If the user runs this right now, will it work — and do I actually know that, or am I hoping?"* If hoping, either go verify, or say you're hoping. That honesty is what makes you trustworthy on the next task.
