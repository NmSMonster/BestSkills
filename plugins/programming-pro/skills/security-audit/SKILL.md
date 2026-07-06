---
name: security-audit
description: Defensive security review of a codebase or change — finding vulnerabilities before attackers do, across injection, auth, secrets, crypto, dependencies, and data exposure. Use when the user asks for a security review/audit, wants to check code for vulnerabilities, is hardening an app before launch, reviewing a security-sensitive change, or asks "is this secure". Defensive only — finds and fixes weaknesses; does not build attacks or exploit third-party systems.
---

# Security Audit

Find the weaknesses before an attacker does, and hand back fixes — not just a list of fears. The output is a triaged set of findings, each with: the vulnerability, a concrete exploit scenario that proves it's real, the severity, and the remediation. A finding you can't turn into "here's how it gets abused" is usually noise.

**Scope: defensive.** This skill reviews the user's own (or authorized) code to harden it. It does not write exploits against third parties, build malware, or attack live systems you don't own. Proof-of-concept reasoning stays at the level needed to demonstrate a flaw to its owner.

## Method

Work threat-first: for each **trust boundary** (where data crosses from less-trusted to more-trusted — user→server, service→service, internet→internal), ask what an attacker controls and what they could reach. Most vulnerabilities live at these boundaries.

Prioritize by the OWASP-style high-impact classes; don't audit alphabetically, audit by what actually gets exploited.

## The hunt (in priority order)

### 1. Injection — untrusted data reaching an interpreter
- **SQL**: any query built by string concatenation/format with input → SQL injection. Require parameterized queries/prepared statements everywhere. Check ORMs for raw-query escape hatches.
- **Command**: input reaching `system`/`exec`/`subprocess` with a shell → command injection. Require arg arrays, no shell, allowlists.
- **Path**: input in file paths → traversal (`../`). Require canonicalization + a base-dir check.
- **XSS**: input rendered into HTML without encoding → stored/reflected XSS. Require context-aware output encoding; check `dangerouslySetInnerHTML`/`v-html`/template `| safe`.
- **Others**: LDAP, XML (XXE — disable external entities), template injection (SSTI), NoSQL, header/CRLF injection, deserialization of untrusted data.

### 2. Broken authentication & session
- Passwords hashed with bcrypt/scrypt/argon2 (never MD5/SHA-1/plain/reversible). Salted, correct work factor.
- Session tokens: CSPRNG-generated, httpOnly + Secure + SameSite cookies, expiry, rotation on login/privilege change, server-side revocation.
- MFA available for sensitive accounts; no auth bypass via unverified email/predictable reset tokens; rate-limited login (brute-force / credential-stuffing defense).

### 3. Broken authorization (the most common real breach)
- **Object-level (IDOR/BOLA)**: every request that references a resource id re-checks that *this* user may access *that* object — not just "is authenticated." This is the #1 API vulnerability; check every endpoint.
- **Function-level**: admin actions gated server-side, not just hidden in the UI.
- Fails closed; no privilege decision based on client-supplied role/id; no mass-assignment letting a request set fields it shouldn't (`isAdmin=true`).

### 4. Secrets & sensitive data
- No secrets in source, config, logs, or history (scan the diff and repo for keys, tokens, passwords, `.env`, high-entropy strings). If found in history, treat as compromised → rotate, don't just delete.
- Secrets from a vault/env, not hardcoded. Least-privilege scoped.
- PII/credentials/tokens/full-PAN never logged. Sensitive data encrypted at rest and in transit (TLS enforced, no downgrade).

### 5. Cryptography
- Standard libraries, never hand-rolled. TLS for transport. AEAD (e.g. AES-GCM) for data; no ECB, no static IVs.
- Randomness from a CSPRNG (`secrets`, `crypto.randomBytes`), never `Math.random`/`rand()` for tokens.
- No MD5/SHA-1 for security; no hardcoded keys/IVs.

### 6. Dependencies & supply chain
- Run the ecosystem auditor (`npm audit`, `pip-audit`, `osv-scanner`, Dependabot data) — flag known CVEs, especially in transitive deps.
- Pinned/locked versions; no typosquat-looking packages; no unmaintained deps in critical paths.

### 7. Misconfiguration & exposure
- Debug mode off in prod; verbose errors/stack traces not leaked to users; default credentials changed.
- Security headers (CSP, HSTS, X-Content-Type-Options, etc.); CORS not `*` on authenticated endpoints.
- Directory listing off; admin/actuator/metrics endpoints not public; cloud storage buckets not public.
- Rate limiting and resource limits (payload size, query depth) — DoS resistance.

### 8. SSRF, redirects, and business logic
- User-supplied URLs fetched server-side → SSRF (block internal ranges/metadata endpoints, allowlist). Open redirects validated.
- Business-logic flaws: negative quantities, price manipulation, race conditions on balance/inventory (TOCTOU), replay of one-time actions, workflow steps skippable.

## Severity (CVSS-style, but plain)

| Level | Meaning |
|---|---|
| 🔴 **Critical** | Remote unauth code exec, auth bypass, mass data exposure, injection reaching prod data |
| 🟠 **High** | Authenticated privilege escalation, IDOR to sensitive data, stored XSS, secret leak |
| 🟡 **Medium** | Reflected XSS, missing hardening that needs a chain to exploit, weak crypto not yet broken |
| 🔵 **Low / info** | Defense-in-depth gaps, verbose errors, missing header with low impact |

Rate by **impact × exploitability**. A theoretical issue behind three other controls is Low; an unauthenticated IDOR on user data is Critical regardless of how "simple" it looks.

## Deliverable

```
# Security audit — <scope>
Date · What was reviewed · What was NOT reviewed (be explicit about coverage limits)

## Summary — overall posture, count by severity, the 3 things to fix first

## Findings (severity-ordered)
### [🔴 Critical] SQL injection in /api/search
Location: file:line
Vulnerability: user `q` concatenated into SQL.
Exploit scenario: `q = "'; DROP TABLE..."` → arbitrary SQL as the app DB user.
Remediation: parameterize (example). Verify: re-test with the payload.

## Positive notes — controls done right (don't only report gaps)
## Recommendations — hardening beyond the specific findings
```

## Rules

- Every finding needs a concrete exploit scenario — no hand-waving "this might be insecure."
- Prove it where safe (a payload that demonstrates, run against the *user's own* code/test env), never against systems the user doesn't own.
- Report false-positive risk honestly; mark uncertain findings "needs verification."
- Pair every finding with a fix. A security audit that only frightens, without a path to safety, has failed.
- State coverage limits plainly — an audit that implies more thoroughness than it delivered is a security risk of its own.
