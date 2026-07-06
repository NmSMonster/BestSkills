---
name: test-driven-development
description: Red–green–refactor discipline for implementing features and fixing bugs with tests written first. Use when the user asks to build a feature with TDD, asks for "tests first", wants high-confidence changes in critical code, or when adding behavior to code that already has a test suite. Also covers designing good test cases, table-driven tests, and what NOT to test.
---

# Test-Driven Development

TDD is a design tool that happens to produce tests. The test written first forces you to define the interface and the observable behavior before the implementation biases you.

## The loop (never skip a step)

1. **RED** — Write one small test for the next slice of behavior. Run it. **Watch it fail for the right reason** (assertion failure on the behavior, not an import error or typo). A test you never saw fail proves nothing.
2. **GREEN** — Write the *minimum* code to pass. Resist generalizing. Hard-coding is legal here; the next test will force the generalization.
3. **REFACTOR** — With the suite green, clean up: remove duplication, improve names, extract structure. Run the suite after each refactor step. Never refactor on red.
4. Commit at green (when the user's workflow uses commits). Small green commits make review and bisection trivial.

Slice size check: if a test takes more than ~10 lines of implementation to pass, the slice was too big — back up and split it.

## Ordering test cases

Build behavior in this order — it keeps every step small:
1. Degenerate case (empty input, zero, null) — establishes the interface.
2. Simplest real case (one item, happy path).
3. Generalization (many items, boundaries: max, min, off-by-one).
4. Error cases (invalid input, failure of a dependency) — assert the *specific* error, not just "raises".
5. Nasty edge cases discovered while implementing — add each as a test immediately, even mid-slice.

## What makes a test good

- **Tests behavior through the public interface**, not implementation details. If renaming a private method breaks tests, they're too coupled.
- **One reason to fail.** Multiple asserts are fine if they verify one behavior; two behaviors means two tests.
- **Name states the rule**: `test_expired_token_is_rejected`, not `test_token_2`.
- **Arrange–Act–Assert** visually separated. No branching or loops in the test body — if you need them, use table-driven/parametrized tests:
  - Python: `@pytest.mark.parametrize`; JS/TS: `test.each`; Go: table tests with subtests.
- **Deterministic**: fixed seeds, frozen clocks (`freezegun`, fake timers), no real network. Fakes over mocks where possible; when mocking, mock *your own* boundary interfaces, not third-party internals.
- **Fast**: the red–green loop dies if the suite takes minutes. Keep the unit loop under seconds; push slow integration checks to a separate tier that runs before finishing the task.

## What NOT to test

- Framework/library behavior (don't test that the ORM saves).
- Trivial pass-throughs, getters, generated code.
- Exact copies of the implementation (asserting a mock was called with the same formula the code contains) — that's a change-detector, not a test.

## Bug fixing with TDD

Every bug fix starts with a failing test that reproduces the bug at the lowest level that can express it. Then fix. The test is the regression guard and the proof. No exceptions — if the bug "can't be tested", that's a design smell worth reporting to the user.

## Working in a legacy codebase

- If the target code has no tests and is hard to test, first write a **characterization test**: capture current behavior (even if ugly) with golden/snapshot assertions, then proceed with the loop for the new behavior.
- Follow the repo's existing test conventions (runner, fixtures, naming, directory layout) — read 2–3 existing test files before writing yours.

## Definition of done

- All new behavior is covered by tests that were seen failing first.
- Full relevant suite passes; no skipped/`xfail` tests added without user sign-off.
- Coverage of the changed lines is high *because behavior is specified*, not because lines were chased.
- Report to the user: behaviors now specified (test list), anything intentionally untested and why.
