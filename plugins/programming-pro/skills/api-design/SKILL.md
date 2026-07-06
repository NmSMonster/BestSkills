---
name: api-design
description: Designing and reviewing HTTP/REST, GraphQL, or internal library APIs — resources, endpoints, naming, versioning, pagination, error contracts, auth, and backward compatibility. Use when the user asks to design an API, add endpoints, review an API spec, define request/response schemas, or evolve an existing API without breaking clients.
---

# API Design

An API is a promise you can't easily take back. Optimize for the reader of the docs and the client developer at 2 a.m., not for the implementation. This skill covers designing new APIs and — more often — evolving existing ones safely.

## Process

1. **Inventory first.** In an existing codebase, read the current API surface before designing anything: routes/resolvers, naming style, error envelope, auth mechanism, pagination style. **Consistency with the existing API beats textbook correctness** — a second pagination style is worse than a mediocre-but-uniform one.
2. **Design the contract before the code.** Write the endpoint list + request/response examples (or OpenAPI/GraphQL SDL) and get user sign-off if choices are contentious.
3. **Walk the client's day**: for each consumer use case, write the literal sequence of calls needed. If a common workflow takes 4 round-trips, redesign.
4. Implement, then verify the contract with example-based tests (request in → status + body out), including every documented error case.

## REST design rules

**Resources & URLs**
- Nouns, plural, kebab/lower: `/orders/{orderId}/line-items`. Verbs only for true actions that aren't CRUD: `POST /orders/{id}/cancel`.
- Nest at most one level; beyond that, filter: `/line-items?orderId=…`.
- IDs opaque and stable; never expose auto-increment DB ids in new public APIs (use UUID/prefixed ids: `ord_8f3k…`).

**Methods & semantics**
- GET safe + cacheable, never mutates. PUT full replace (idempotent), PATCH partial, DELETE idempotent (second delete → 404 or 204, pick one and document).
- Any POST a client may retry (payments, orders, sends) accepts an **`Idempotency-Key`** header; store and replay the original response.

**Status codes** — small, consistent palette:
- 200 read/update, 201 + `Location` create, 202 async accepted, 204 no body.
- 400 malformed, 401 unauthenticated, 403 unauthorized, 404 absent-or-hidden, 409 state conflict, 422 valid syntax/invalid semantics, 429 rate limited (+ `Retry-After`).
- 5xx = *our* fault only. Never map validation errors to 500, never map downstream timeouts to 400.

**Errors** — one envelope everywhere, machine-readable first (RFC 9457 problem+json or equivalent):
```json
{ "type": "https://api.example.com/errors/insufficient-funds",
  "title": "Insufficient funds", "status": 409,
  "detail": "Balance 12.50 is below charge 20.00.",
  "errors": [{ "field": "amount", "code": "too_large" }] }
```
Field-level codes are for programs; `detail` is for humans. Never leak stack traces or internal names.

**Pagination, filtering, sorting**
- Default to **cursor pagination** (`?cursor=…&limit=…` → `{ items, next_cursor }`); offset pagination only for small, static datasets. Always enforce and document a max `limit`.
- Filters as explicit params (`?status=paid&created_after=…`), sort as `?sort=-created_at`.

**Versioning & compatibility**
- Version only on breaking change; prefer additive evolution. `/v1/` path prefix is the pragmatic default.
- Non-breaking: adding optional fields, new endpoints, new enum values **only if docs told clients to tolerate unknowns**. Breaking: removing/renaming fields, type changes, tightening validation, changing defaults or error codes.
- Deprecate with headers (`Deprecation`, `Sunset`) + docs + timeline; never silently.

## GraphQL specifics

- Schema-first; nullable by default only where absence is genuinely meaningful.
- Mutations return the mutated object + `userErrors: [{field, code, message}]` — reserve top-level GraphQL errors for system failures.
- Paginate every list field (Relay connections or documented equivalent); enforce depth/complexity limits.

## Library/internal APIs

- Make the common case one obvious call with good defaults; make misuse unrepresentable (types over docs, enums over strings, require what's mandatory in the constructor).
- Accept broad types, return precise ones. Don't expose internal mutable state.
- Same compatibility bar as HTTP: renaming a public function is a breaking change with a deprecation path.

## Security & operational checklist

- [ ] AuthN mechanism stated per endpoint; authZ enforced at the resource (object-level checks — the #1 real-world API hole is IDOR/BOLA).
- [ ] Input validated against a schema; unknown fields rejected or ignored *consistently*.
- [ ] Rate limits defined and surfaced (`429` + headers). Payload size limits set.
- [ ] No secrets/PII in URLs (they land in logs). Sensitive fields redacted from logs.
- [ ] Timeouts, and retry guidance documented (which calls are safe to retry).
- [ ] Every example in the docs actually runs — test them.

## Deliverable

Present the design as: endpoint table (method, path, purpose, auth) → representative request/response examples → error catalog → compatibility notes (what's breaking vs. additive if evolving an existing API) → open questions for the user.
