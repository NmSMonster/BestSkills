---
name: api-integration
description: Integrating with third-party APIs and webhooks robustly — auth, pagination, rate limits, retries, idempotency, error handling, and webhook receivers. Use when the user asks to integrate/consume an external API, call a REST/GraphQL service, handle API auth (OAuth/API keys), deal with rate limiting or flaky APIs, process webhooks, or build a client/connector. Focuses on integrations that survive production, not just the happy-path first call.
---

# API Integration

The first successful call is 10% of the work. The other 90% is what happens when the token expires, the API returns 429, the network blips mid-request, the webhook fires twice, or the response shape changes. This skill builds integrations that survive all of that — because in production, all of that happens.

## Step 1 — Read the API before writing code

- Get the **docs, auth model, rate limits, and error format** first. Skipping this guarantees a rewrite.
- Identify: base URL + versioning, auth mechanism, pagination style, rate-limit headers, error envelope, and whether there's a **sandbox/test environment** (use it — never develop against production data).
- Make one manual call with `curl` to see the *real* response shape (docs lie or lag). Save an example response; you'll model against it.

## Step 2 — Authentication, done safely

- **Secrets from env/secret store, never in code or committed.** (`.env` gitignored; `.env.example` documents the keys.)
- **API key**: simplest — send in header; rotate-able; scope to least privilege.
- **OAuth2**: implement the token lifecycle — obtain, **cache with expiry**, and refresh *before* expiry (or on a 401, refresh once and retry). Don't fetch a new token per request; don't let an expired token cause a storm of failures.
- **HMAC/signed requests**: sign per the spec exactly (canonicalization is where these break); verify against their example.
- Store tokens in memory or a secure store, not logs. Never log the `Authorization` header.

## Step 3 — The resilience layer (this is the skill)

Wrap every call with these — they're not optional for production:

**Timeouts** — connect *and* read timeout on every request. A hung request with no timeout hangs your whole job. Set them explicitly; defaults are often infinite.

**Retries with exponential backoff + jitter** — but only for the *right* failures:
- Retry: network errors, timeouts, 429, 502/503/504. These are transient.
- Never retry: 400, 401, 403, 404, 422 — the request is wrong; retrying just repeats the error. Fix or surface it.
- Backoff: `base * 2^attempt` + random jitter (jitter prevents synchronized retry storms). Cap attempts (3–5) and total wait. **Honor `Retry-After`** if the API sends it — that's the server telling you exactly when to come back.

**Rate-limit handling** — read the rate-limit headers (`X-RateLimit-Remaining`, `Retry-After`); throttle proactively before you hit the wall, not just reactively after 429. For bulk work, a token-bucket limiter keeps you under the ceiling.

**Idempotency** — for any write you might retry (create/charge/send), use the API's idempotency key if it offers one, so a retry after a timeout doesn't create a duplicate. If it doesn't, design your own dedupe (check-before-create, or a natural key). A timed-out POST *may have succeeded* — assume it did and verify, don't blindly recreate.

**Circuit breaking** for high-volume integrations — after N consecutive failures, stop hammering a down service and fail fast for a cooldown; it protects both sides.

## Step 4 — Handle responses like they'll surprise you

- **Check status before parsing.** Don't `.json()` a 500 error page. Branch on status class.
- **Validate the shape.** Parse into a typed structure / validate against a schema; don't assume a field exists because the docs say so. Missing/null/renamed fields are the top runtime break — handle them, don't `KeyError` in production.
- **Errors**: map the API's error envelope to your own errors with enough context to debug (status, error code, request id from their response header — log that id; it's what their support will ask for). Never swallow an error into a silent `None`.
- **Pagination**: implement the API's actual style (cursor / offset / link-header) and **follow it to completion** — don't stop at page 1 and think you have all the data. Guard against infinite loops (cursor not advancing). Stream/accumulate incrementally for large sets.

## Step 5 — Webhooks (receiving events)

If the integration receives webhooks:
- **Verify the signature** on every incoming webhook (HMAC of the raw body with the shared secret) — an unverified webhook endpoint is a spoofing hole.
- **Respond fast (2xx) and process async.** Do minimal work in the handler; enqueue the payload and process it out-of-band. Slow handlers cause the sender to time out and *retry*, multiplying load.
- **Expect duplicates and out-of-order delivery.** Webhooks are at-least-once: dedupe on the event id, and don't assume event A arrives before event B. Make processing idempotent.
- Return 2xx only after you've *safely stored* the event (so their retry stops); if you can't process, return 5xx so they retry later.

## Step 6 — Test and observe

- Test against the sandbox and with **simulated failures**: force a 429, a timeout, a malformed response, an expired token — verify your retry/refresh/error paths actually work. The happy path always works; the failure paths are what you're really building.
- **Log** each call's outcome (endpoint, status, latency, their request-id) — not the secrets/PII. When the integration misbehaves in prod, these logs are your only witness.
- Record the API version you built against; watch their changelog for breaking changes.

## Deliverable

A client/integration with: auth + token lifecycle, a shared request wrapper (timeout + retry/backoff + rate-limit handling), typed response parsing with validation, mapped errors, complete pagination, and (if applicable) a signature-verifying, idempotent, async webhook handler. Plus: config via env, a sandbox-tested failure-path check, and notes on the API's limits and quirks you discovered.

## Rules

- No production integration without timeouts and bounded retries on transient-only failures.
- Idempotency on any retryable write — never risk a double charge/send.
- Secrets never in code or logs; verify webhook signatures always.
- Follow pagination to the end; validate response shape; log the provider's request-id for debugging.
