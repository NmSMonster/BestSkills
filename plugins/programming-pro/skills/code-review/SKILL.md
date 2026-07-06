---
name: code-review
description: Reviewing a diff, pull request, or code change for correctness, security, and maintainability — and writing review feedback that helps rather than nitpicks. Use when the user asks to review code, review a PR/diff, check a change before merge, give feedback on someone's code, or self-review before pushing. Covers what to read first, the defect classes to hunt, severity triage, and how to phrase comments so they land.
---

# Code Review

A review protects the codebase and teaches the author — in that order. Its output is a **triaged list of findings**, each anchored to a line, each with a severity and a concrete fix or question. The failure mode to avoid is a pile of style nits that misses the one race condition that will page someone at 3 a.m.

Per-language and per-change-type checklists: `references/review-checklists.md`.

## Before reading a single line

1. **Read the intent.** PR title/description, linked issue, the "why." A change can be flawless code and still be the wrong change — you can't judge correctness without knowing the goal.
2. **Size the blast radius.** What does this touch? Public API, auth, data model, money, concurrency, a hot path? Blast radius sets your rigor: a copy tweak gets a glance; an auth change gets line-by-line paranoia.
3. **Get it in front of you runnable.** For anything nontrivial, check out the branch. Reading a diff in isolation hides what the surrounding function does — the bug is usually in the interaction, not the added line.

## Reading order (findings hide in this order)

Review in decreasing order of consequence — if you run out of time, you spent it on what matters:

1. **Correctness of the core logic** — does it do what the description claims, including the edge cases the description forgot?
2. **Security & data safety** — untrusted input, authz, secrets, injection, PII. (see checklist)
3. **Failure & concurrency** — what happens when the network dies, the input is empty, two of these run at once, the transaction half-commits?
4. **API/contract** — is this a breaking change dressed as an addition? Do callers survive it?
5. **Tests** — do they exist, do they test *behavior* (not mocks echoing the implementation), do they cover the new edge cases, would they actually fail if the code broke?
6. **Maintainability** — naming, duplication, complexity, dead code. Real, but below all of the above.
7. **Style** — only what a linter can't catch; everything a linter *can* catch shouldn't be a human comment.

## The defect-hunting mindset

For each changed function, ask the questions that find real bugs:
- **Boundaries**: empty, null/None, zero, negative, one, max, off-by-one, unicode, huge input, duplicate. Which boundary did the author not test?
- **Error paths**: every call that can fail — is the failure handled, swallowed, or ignored? Does an exception leave state half-mutated? Are errors logged with enough context to debug?
- **Concurrency**: shared mutable state, check-then-act races, unguarded caches, non-idempotent retries, ordering assumptions.
- **Resource lifetime**: opened files/connections/locks — are they released on *every* path including the error path? Unbounded growth (caches, lists, retries)?
- **Trust**: is any input from outside (user, network, file, env) used without validation? Concatenated into SQL/HTML/shell/paths?
- **State & consistency**: can this leave the system in an invalid state if it fails midway? Is the DB transaction boundary correct?
- **Assumptions**: what must be true for this code to work (sorted input, non-null field, single-threaded, timezone)? Is that guaranteed or hoped?

Trace at least one realistic execution path *and* one failure path by hand. "Looks right" is not review; following the values is.

## Severity triage (label every finding)

| Level | Meaning | Merge impact |
|---|---|---|
| 🔴 **Blocking** | Bug, security hole, data loss, breaking change, missing critical test | Must fix before merge |
| 🟠 **Should-fix** | Real problem, non-catastrophic; edge case, poor error handling, risky pattern | Fix now or file a tracked follow-up |
| 🟡 **Consider** | Improvement: clarity, duplication, better approach — author's judgment | Optional |
| 🔵 **Nit / praise** | Trivial style, or explicitly calling out good work | Non-blocking; mark as nit |

Separating these is the whole craft: if everything sounds equally urgent, the author can't tell the security hole from the variable-name preference, and both get equal (i.e. random) attention. Lead the review with the blocking items.

## Writing comments that land

- **Anchor + specific + actionable.** `file:line` → what's wrong → why it matters → suggested fix or a question. "This could NPE if `user.address` is null on the guest-checkout path — guard it or make the field non-optional?" beats "null safety?".
- **Ask, don't assume, when you might be wrong.** "Is `items` guaranteed non-empty here? If a caller passes `[]` this indexes out of bounds." Phrasing as a question invites the context you lack and isn't wrong if you missed something.
- **Explain the why**, especially for should-fix and consider — the author learns a principle, not just a patch. A review is the cheapest teaching moment in engineering.
- **Praise real cleverness and good tests.** Reviews that are only negative train people to fear reviews. One genuine 🔵 praise per review is not padding.
- **Mark nits as nits** explicitly (`nit:`) so the author knows they're optional. Don't let taste masquerade as correctness.
- **Don't rewrite their code in your style.** If it's correct, clear, and consistent with the codebase, personal preference is not a finding.
- **Suggest, offer, respect autonomy.** For non-blocking items the author decides. For blocking ones, be clear it's blocking and why — kindly, but unambiguously.

## Scope discipline

- Review the diff, not the whole codebase. Pre-existing issues in untouched code → note briefly or file separately; don't hold this PR hostage to them.
- If the PR is too big to review well (hundreds of lines across many concerns), say so and ask to split it — a rubber-stamp on an unreviewable PR is worse than no review.
- Don't demand gold-plating a change doesn't need. Match the bar to the blast radius.

## Deliverable

```
## Review summary
Verdict: Approve / Approve-with-nits / Request-changes — one-line reason.
Blast radius: <what this touches> · Rigor applied: <light / standard / paranoid>

## 🔴 Blocking (N)
- file:line — problem → why it matters → fix/question

## 🟠 Should-fix (N)
## 🟡 Consider (N)
## 🔵 Nits & praise

## What I verified
How I checked (ran it / traced path X / ran the tests) — and what I did NOT check.
```

Always state what you *didn't* verify. A review that implies more coverage than it did is worse than an honest partial one. If you couldn't run it, say so. If auth was out of your depth, say that too.
