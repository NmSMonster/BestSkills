---
name: workflow-automation
description: Turning manual processes into scheduled, monitored, unattended automations — cron jobs, file watchers, CI scheduled workflows, notification hooks, and multi-step scripts that run without a human. Use when the user asks to schedule something, run a task periodically, automate a recurring chore, watch for changes and react, chain tools into a pipeline, or make an existing script production-safe for unattended runs.
---

# Workflow Automation

An automation is a script that runs when nobody is watching. That changes every design decision: it must fail loudly, never fire twice by accident, and be diagnosable from its logs alone at 3 a.m. The gap between "script that works" and "automation" is exactly these properties.

## Step 1 — Specify the workflow

Before writing anything, pin down:
- **Trigger**: schedule (cron), event (file appears, webhook, email), or condition (page changed, threshold crossed)?
- **Steps** and their failure semantics: if step 3 of 5 fails, do we retry step 3, roll back, or alert and halt? Decide per step, don't discover in production.
- **Success/failure notification**: who learns what, on which channel? Default: notify on failure and on anomaly; on success stay silent or emit a one-line log (noisy successes train humans to ignore alerts).
- **Overlap policy**: what if a run is still going when the next trigger fires? (Almost always: skip with a lockfile.)

## Step 2 — Make the core script unattended-grade

Non-negotiables for any script that runs unattended:

```bash
#!/usr/bin/env bash
set -euo pipefail                       # fail loudly, not silently
exec 9>"/tmp/myjob.lock"; flock -n 9 || exit 0   # no overlapping runs
trap 'notify "myjob FAILED at line $LINENO"' ERR
```
Python equivalent: top-level try/except that logs + notifies + exits nonzero; `filelock` for the lock.

- **Idempotent**: running twice = running once (checkpoint files, upserts, "skip if output exists"). Assume every trigger will eventually double-fire.
- **Timestamped structured logs** to a file: start, each step, counts, duration, end status. `echo` to a terminal nobody watches is not logging.
- **Timeouts** on every network call and on the whole job (`timeout 30m ./job.sh` in the crontab).
- **Retries with exponential backoff for transient failures only** (network, 429/5xx) — never retry logic errors; max 3, then alert. Retrying a bug 100 times is 100 bugs.
- **Absolute paths everywhere**; cron's environment is nearly empty — no PATH assumptions, no `~`, source required env explicitly (e.g. `.env` file readable only by the job user, `chmod 600`). Secrets never in the crontab or the script body.

## Step 3 — Choose the trigger mechanism

| Need | Use |
|---|---|
| Time-based on a server | `cron` (simple) or systemd timers (better logging, `Persistent=true` catch-up, no overlap via unit) |
| Time-based, no server | scheduled CI: GitHub Actions `on: schedule` (note: UTC, min interval ~5 min, can be delayed) |
| React to file changes | `inotifywait -m -e close_write` loop, or watchdog (Python); debounce bursts |
| React to a webhook | smallest viable receiver (existing app route, or serverless/CI `repository_dispatch`) |
| Poll an external condition | cron + state file: fetch → compare to last state → act only on *change* (see below) |

Cron hygiene: comment each entry with what/why/owner; redirect output (`>> /var/log/myjob.log 2>&1`); test the exact command as the cron user first; remember cron won't run missed jobs after downtime (systemd `Persistent=true` will).

## The change-detection pattern (most common automation)

"Tell me when X changes" — price, page, stock, ranking, status:

```
fetch current state → normalize (strip timestamps/session noise!) →
hash/compare vs data/last_state → identical? exit 0 quietly
→ changed? save new state FIRST, then notify with a diff
```
Normalization is where these fail: pages embed rotating tokens/dates, so diff the *extracted fields*, not the raw HTML. Save-then-notify ordering prevents re-alerting forever when the notifier errors.

## Notifications

- Failure alerts must contain: job name, timestamp, step that failed, the actual error line, and where the full log lives. "Job failed" alone guarantees a bad morning.
- Channels, simplest first: email (`mail`/SMTP script), Slack/Discord/Telegram webhook (one `curl -X POST` with JSON), ntfy.sh for phone push with zero setup.
- **Dead-man's switch for critical jobs**: a job that stops running can't alert about it. Use healthchecks.io-style ping ("job pings on success; service alerts if no ping in 25h") for anything that matters.

## Step 4 — Deploy checklist

- [ ] Ran the full flow manually as the target user in the target environment.
- [ ] Forced a failure (bad URL, kill mid-run) → alert actually arrived, lock released, rerun recovered cleanly.
- [ ] Double-triggered on purpose → no duplicate side effects.
- [ ] Logs rotating or bounded (`logrotate` or dated files + cleanup step).
- [ ] Everything (script, crontab line/unit file, .env.example, README with "how to disable") committed to the repo.
- [ ] The off switch is documented and one command long.

## Report to the user

Deliver: what triggers it, what it does step-by-step, how it notifies and when, how to check it's alive, how to disable it, and what was tested (including the forced failure).
