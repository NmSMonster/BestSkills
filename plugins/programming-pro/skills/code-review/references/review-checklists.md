# Review Checklists

Targeted checklists by change type and language. Don't run all of them on every PR — pick the ones the blast radius calls for. These jog memory for defect classes that are easy to miss under time pressure; they don't replace tracing the logic by hand.

## By change type

### Auth / permissions change (paranoid rigor)
- [ ] Authorization checked at the **resource/object** level, not just "is logged in" (IDOR/BOLA is the #1 real-world API hole).
- [ ] Fails **closed** — an error or unknown state denies access, never grants it.
- [ ] No authz decision made on the client side / trusting a client-supplied role or id.
- [ ] Session/token: expiry enforced, rotation on privilege change, revocation works.
- [ ] The change doesn't widen an existing scope silently (diff the permission set before/after).

### Input handling / anything touching untrusted data
- [ ] Validated against a schema at the boundary; unknown/extra fields handled consistently.
- [ ] Parameterized queries — **no** string-built SQL. No shell command built from input. Paths sanitized (no `../`).
- [ ] Output encoded for its sink (HTML escape, JSON, etc.) — XSS/injection prevented at render.
- [ ] Size/length/range limits (prevent resource exhaustion); numeric inputs bounded.
- [ ] Encoding/unicode handled; no assumption of ASCII.

### Data model / migration
- [ ] Migration is **reversible** or has a tested rollback; safe to run on a live table (no long lock on a big table without a strategy).
- [ ] Backward compatible with the currently-deployed code (expand/contract: add nullable → backfill → enforce, in separate deploys).
- [ ] Indexes for the new query patterns; no unindexed foreign keys on hot paths.
- [ ] Nullability, defaults, and constraints match the code's assumptions.
- [ ] Data backfill handles nulls, huge row counts (batched), and partial failure.

### Concurrency / async
- [ ] Shared mutable state is guarded; no check-then-act race (TOCTOU).
- [ ] Retries are idempotent; no double-charge / double-send on retry.
- [ ] Locks acquired in a consistent order (deadlock); released on every path.
- [ ] `await`/promises: no unawaited async, no swallowed rejection, no blocking the event loop.
- [ ] Timeouts on all external calls; cancellation propagates.

### API / public contract
- [ ] Additive, not breaking (no removed/renamed fields, tightened validation, changed defaults or error codes) — or the version bump is deliberate.
- [ ] Pagination on any list that can grow; max limits enforced.
- [ ] Error responses follow the existing envelope; status codes correct (4xx client, 5xx us).
- [ ] Backward compat for existing clients verified.

### Tests (on every PR)
- [ ] New behavior has tests that would **fail if the code were reverted** (mentally revert and check).
- [ ] Edge cases from the logic (empty, boundary, error) are covered, not just the happy path.
- [ ] Tests assert behavior through the public interface, not mocks re-stating the implementation (change-detector smell).
- [ ] No flakiness introduced (real time/network/random without control).
- [ ] Test names state the rule being verified.

### Performance-sensitive path
- [ ] No N+1 query (query count independent of result size?).
- [ ] No O(n²) hidden in nested loops over request-scaled data.
- [ ] Caches are bounded and have invalidation.
- [ ] Large payloads streamed, not fully buffered.

## By language (common real bugs)

### Python
- Mutable default args (`def f(x=[])`) — shared across calls.
- Bare `except:` / `except Exception: pass` swallowing errors.
- Late-binding closures in loops; `is` vs `==` for values.
- Missing `with` for files/locks; resource leaks on exception.
- `datetime` without tz; float for money.

### JavaScript / TypeScript
- `==` vs `===`; truthiness bugs on `0` / `""` / `null`.
- Unawaited promises; unhandled rejection; `forEach` with async.
- `any` escapes defeating the type system; non-null `!` hiding a real null.
- Mutating props/state directly (React); missing deps in `useEffect`; stale closures.
- Floating-point money; `JSON.parse` without try/catch on untrusted input.

### Go
- Ignored `error` returns; `err` shadowing in `:=`.
- Loop variable captured by goroutine (pre-1.22 semantics) / closure.
- Nil map write; nil pointer deref; unclosed `defer` in a loop.
- Goroutine leaks (no ctx cancellation / unbounded spawn); data race on shared var (run `-race`).

### Java / Kotlin
- `NullPointerException` on unchecked returns; `Optional` misuse.
- Resource leaks — not using try-with-resources.
- `equals`/`hashCode` inconsistency; mutable objects as map keys.
- Swallowed `InterruptedException`; shared mutable state without synchronization.

### SQL
- Missing `WHERE` on `UPDATE`/`DELETE` (catastrophe).
- Implicit type coercion defeating an index; function on an indexed column in `WHERE`.
- `SELECT *` in production code; N+1 from ORM lazy loading.
- Transaction scope too wide (long locks) or too narrow (inconsistent reads).

## Security quick-scan (any language)
- [ ] No secrets/keys/tokens committed (scan the diff for high-entropy strings, `.env`, credentials).
- [ ] No logging of PII, passwords, tokens, full card numbers.
- [ ] Dependencies added: reputable, pinned, no known critical CVE, not typosquatting a popular name.
- [ ] Crypto: standard library, not hand-rolled; no MD5/SHA1 for passwords (use bcrypt/argon2); randomness from a CSPRNG.
- [ ] Error messages don't leak stack traces / internal paths to users.
