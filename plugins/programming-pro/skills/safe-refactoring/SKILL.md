---
name: safe-refactoring
description: Behavior-preserving refactoring of existing or legacy code — restructuring, renaming, extracting modules, untangling dependencies, or paying down tech debt without breaking anything. Use when the user asks to refactor, clean up, modernize, split a large file/function, remove duplication, or make code testable. Enforces safety nets, small reversible steps, and proof that behavior did not change.
---

# Safe Refactoring

A refactor changes structure, never behavior. The moment behavior changes intentionally, it's a feature/fix and must be separated out. The core discipline: **you must be able to prove, at every step, that behavior is unchanged.**

## Before touching anything

1. **Scope the contract.** List the observable behaviors of the code being refactored: public functions/endpoints, side effects (files, DB, network, logs that other systems parse), error types, ordering guarantees, performance characteristics that callers rely on.
2. **Find all callers.** `grep`/LSP-search every entry point, including reflective/string-based uses (routes, DI containers, serialized names, templates, config files). Dynamic call sites are where refactors die.
3. **Build the safety net.**
   - Existing tests: run them, record the baseline (which pass, how long).
   - Gaps: write **characterization tests** for the behaviors you'll touch — assert what the code *does now*, bugs included. Golden-file/snapshot tests are fine here.
   - No test infrastructure at all? Create a minimal harness or a script that exercises the code end-to-end and diffs the output before/after.
4. **Verify the net catches.** Deliberately break the code (flip a condition), see a test fail, revert. A net you haven't seen catch is decoration.

## The step loop

Work in steps so small that each one is obviously correct and independently revertible:

1. Apply ONE mechanical transformation (see catalog below).
2. Run the fast test suite.
3. Green → commit (or checkpoint). Red → **revert the step**, don't debug forward. A failed refactor step means the step was too big or an assumption was wrong.
4. Repeat.

If the user's workflow has commits: one transformation per commit, message states the transformation ("Extract PriceCalculator from OrderService, no behavior change"). Never mix a refactor commit with a behavior-change commit.

## Transformation catalog (prefer mechanical moves)

- **Rename** (symbol, file) — use LSP/IDE-grade rename or exhaustive grep including strings and docs.
- **Extract function/class/module** — copy body, delegate old site to new one, migrate callers one by one, then remove the old site.
- **Inline** the trivial indirection nobody needs.
- **Introduce parameter / replace global** — thread the dependency explicitly; default the parameter to the old global first so callers migrate gradually.
- **Strangler pattern** for big replacements: build the new path alongside the old, route callers over incrementally (flag or one call site at a time), delete the old path only when unreferenced — verify with grep, not memory.
- **Branch by abstraction** when a dependency swap can't be atomic: insert an interface, implement both sides, flip, remove.
- **Duplication removal**: only merge code that is duplicated *by meaning*, not just by shape. Two similar-looking blocks that change for different reasons must stay separate.

## Hard rules

- Never refactor and change behavior in the same step. If you spot a bug mid-refactor: note it, finish or checkpoint the refactor, then fix the bug as its own change with its own test.
- Never "improve" error messages, log formats, JSON field names, or public API shapes silently — those are behavior. Flag them to the user as proposed behavior changes.
- Keep the code working after **every** step — no long broken intermediate states.
- Don't expand scope. "While I'm here" is how a 20-line refactor becomes a 2,000-line PR. Keep a `notes` list of tempting follow-ups and report them at the end instead.
- Respect the codebase's conventions even when you disagree — consistency beats local perfection.

## Finishing

1. Full suite green, plus the characterization tests.
2. Diff review pass of your own: read the complete diff top to bottom as a reviewer would; check for leftover debug code, dead code, orphaned files, stale comments/docstrings referencing old names.
3. Verify no accidental behavior deltas: if output can be captured (CLI output, API responses, generated files), diff before vs. after.
4. Report: what changed structurally, proof behavior is preserved (tests/diffs run), bugs or follow-ups discovered but *not* done, and any behavior changes that need a user decision.
