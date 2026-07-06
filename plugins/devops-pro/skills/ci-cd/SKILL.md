---
name: ci-cd
description: Designing and fixing continuous integration and delivery pipelines — build, test, lint, and deploy automation in GitHub Actions, GitLab CI, and similar. Use when the user asks to set up CI/CD, write or debug a pipeline/workflow, automate tests or deployment on push, speed up a slow pipeline, add deployment gates, or fix a failing/flaky build. Focuses on fast, reliable, safe-to-deploy pipelines with rollback — not just "green checkmark".
---

# CI/CD

A pipeline is the safety rail between a developer's commit and production. Its job: catch problems early, prove the build is deployable, and ship it safely — fast enough that people actually wait for it. A slow, flaky, or falsely-green pipeline is worse than none, because it trains the team to ignore it.

## The pipeline stages (fail fast, cheap checks first)

Order stages so the fastest, most-likely-to-fail checks run first — a developer shouldn't wait 10 minutes to learn a linter failed in 10 seconds:

1. **Lint & format** (seconds) — style, obvious errors. Fastest feedback.
2. **Build / compile** — fails fast if it doesn't build.
3. **Unit tests** — fast, isolated, the bulk of coverage.
4. **Integration tests** — slower, real dependencies (DB, services via containers).
5. **Security & quality gates** — dependency scan (known CVEs), secret scanning, SAST, coverage threshold.
6. **Package** — build the artifact/image *once*, then promote that same artifact through environments (never rebuild per stage — you'd deploy something you didn't test).
7. **Deploy** — to staging, then production (gated — see below).

Run independent stages in **parallel** (lint ∥ unit tests ∥ build) to cut wall-clock time; use a matrix for multi-version/multi-OS.

## CI (Continuous Integration) — the correctness gate

- **Trigger on every push and PR.** The whole point is catching breakage before merge. Branch protection: no merge unless CI is green.
- **Reproducible builds**: pin dependency versions (lockfiles), pin tool/action versions (not `@latest` — it makes builds non-deterministic and is a supply-chain risk), pin the runner image. A build that passes today and fails tomorrow with no code change is a pinning failure.
- **Cache aggressively** but correctly: dependency caches keyed on the lockfile hash, build caches, Docker layer caching. Caching is the biggest lever on pipeline speed — but a stale cache causes phantom passes, so key it precisely and bust it when inputs change.
- **Keep it fast.** Target CI under ~10 minutes for the inner loop. Slow pipelines get bypassed. Parallelize, cache, split slow test suites into their own tier, run the heaviest checks only where needed.

## Handling flaky tests (a pipeline killer)

Flaky tests destroy trust in CI — people start re-running until green and ignore real failures. Do **not** paper over them with blanket auto-retries. When a test is flaky: quarantine it (mark, run separately, don't block), file it, and fix the root cause (usually a race, shared state, time/ordering, or a real intermittent bug — see `programming-pro:systematic-debugging`). A retry-until-green pipeline is a pipeline that no longer tests anything.

## CD (Continuous Delivery/Deployment) — the safety gate

- **Deploy the exact artifact you tested.** Build once, promote the same immutable artifact/image through staging → prod. Rebuilding per environment means prod runs untested bits.
- **Progressive rollout, not big-bang.** Use a strategy that limits blast radius and enables instant rollback:
  - **Blue-green**: deploy the new version alongside the old, switch traffic, keep the old ready for instant rollback.
  - **Canary**: route a small % of traffic to the new version, watch metrics, ramp up if healthy, roll back if not.
  - **Rolling**: replace instances gradually with health checks.
- **Health checks and automated rollback**: the deploy isn't done when the process starts — it's done when health checks pass. Wire automatic rollback on failed health checks or a metric regression (error rate, latency). Never a deploy that can't be undone in one step.
- **Gates before production**: automated (all tests, security, staging smoke tests pass) and, where warranted, a manual approval. Higher-risk envs get more gates.
- **Decouple deploy from release** with feature flags: ship code dark, turn features on independently. This makes deploys boring and rollback a flag flip.

## Secrets & security in pipelines

- **Never hardcode secrets** in pipeline files or logs. Use the platform's secrets store / OIDC to cloud providers (short-lived credentials over long-lived keys). Mask secrets in logs.
- **Least privilege** for the pipeline's credentials — a CI token that can do anything is a breach waiting to happen. Scope it to what the job needs.
- **Supply-chain hygiene**: pin third-party actions to a commit SHA (not a moving tag), review what they access, scan dependencies for CVEs, generate an SBOM for critical systems.
- Protect deployment to prod behind branch/environment protections and required reviews.

## Observability of the pipeline itself

- **Notify on failure** with actionable info (what failed, link to logs) — to the right channel, not a black hole. Don't notify on every success (alert fatigue).
- Make failures **diagnosable**: surface the failing test/step and its output; upload artifacts (logs, screenshots, coverage) on failure.
- Track pipeline health: duration trends (catch the slow creep), failure rate, flaky-test rate. A pipeline is a product; maintain it.

## Debugging a broken pipeline

1. **Read the actual error** in the failing step's log — not the summary. The real cause is usually specific and near the bottom.
2. **Reproduce locally** where possible (run the same command, or use `act`/local runners) — faster than push-and-pray loops.
3. **Isolate**: is it the code, the environment (works locally, fails in CI → env difference: versions, env vars, missing service, permissions), the cache (bust it and retry), or a flaky test (re-run — if it passes with no change, it's flaky, not fixed)?
4. Fix the root cause; don't add a sleep or a blanket retry to make red go green.

## Deliverable

For a setup: the pipeline config (stages, triggers, caching, parallelism), the deploy strategy with rollback, secrets handling, and failure notifications — plus how it's gated before prod. For a fix: the diagnosed root cause (env / cache / flaky / real bug), the fix, and verification that the pipeline is genuinely green (not retry-green). For a speedup: the measured before/after and what changed (caching, parallelism, test tiering).

## Rules

- Fail fast: cheapest checks first, parallelize the rest, keep the inner loop under ~10 min.
- Pin everything (deps, tools, actions, runners) for reproducible, supply-chain-safe builds.
- Build the artifact once; promote the same one through environments.
- Every prod deploy has health checks and one-step rollback; roll out progressively.
- Never hardcode secrets; least-privilege pipeline credentials; mask logs.
- Fix flaky tests, don't retry-hide them — a falsely-green pipeline tests nothing.
