---
name: data-pipeline
description: Building resilient data extraction and transformation pipelines — scraping at scale, API harvesting, fetch→parse→normalize→export flows, ETL scripts, and recurring data collection. Use when the user asks to scrape/collect/aggregate data from websites or APIs, convert or clean datasets, export to CSV/JSON/SQLite, or set up repeatable data ingestion. Complements web-automation (which covers driving the browser itself).
---

# Data Pipeline

A pipeline's value is measured on run #50, not run #1. Design for: partial failure, re-running without damage, and source drift. The throwaway script that "worked once" is the most expensive artifact in data work.

## Architecture: separate the stages

Always structure as **fetch → parse → normalize → validate → export**, with raw data persisted between fetch and parse:

```
fetch   → data/raw/…          (verbatim responses: HTML/JSON, one file per item/page, with timestamp)
parse   → extract fields from raw files (touches no network)
normalize → types, units, encodings, dedupe
validate  → schema + sanity checks; quarantine bad records, don't drop silently
export    → data/out/name-YYYY-MM-DD.csv / .jsonl / SQLite
```

Why raw persistence is non-negotiable: when parsing logic has a bug (it will), you re-parse from disk in seconds instead of re-hammering the source for an hour — and you can diff raw snapshots when the source changes.

## Fetching

- **Find the structured source first**: the JSON API behind the page, sitemap.xml, RSS, bulk export, or an official dataset. Parsing HTML is the fallback, not the default. (`curl -s URL` and inspect; check `/api/`, `__NEXT_DATA__`, sitemap.)
- **Politeness defaults**: 1 req/s (raise only with permission), honest User-Agent, obey `robots.txt`, back off exponentially on 429/5xx (2s→4s→8s, max 3 retries), hard-stop on repeated 403 and report. Check ToS for anything commercial-scale; escalate conflicts to the user.
- **Resumability**: keep a manifest (`done.txt` / SQLite table) of fetched keys; on restart, skip completed ones. Every long fetch loop must survive Ctrl-C + rerun.
- **Timeouts on everything** (connect + read); a pipeline that can hang is a pipeline that will.
- Log progress: `[143/2100] fetched product/8812 (200, 1.2s)` — silence for an hour is indistinguishable from a hang.

## Parsing

- HTML: `selectolax` or BeautifulSoup+lxml; select by semantic attributes, not positional paths. JSON: parse into typed structures early.
- **Extract-or-explain**: every field extraction either succeeds or records *why* (`{"field": "price", "error": "selector matched 0 nodes", "url": …}`). Never let a missing node silently become `None` in the output — count and report extraction failures per field.
- Keep a small **fixture set**: save 3–5 representative raw files and write assert-based tests of the parser against them. When the source changes layout, these tests localize the break instantly.

## Normalization — where correctness dies quietly

- Types at the boundary: parse dates to ISO-8601 with explicit timezone, money to `(amount_decimal, currency)` — never float for money — numbers stripped of locale formatting (`"1 234,56"` vs `"1,234.56"`).
- Encode everything UTF-8; normalize unicode (NFC), trim whitespace, collapse internal whitespace where meaning allows.
- Dedupe on a declared natural key; log how many duplicates were merged.
- Nulls: distinguish "source says empty" from "extraction failed" — different columns or sentinel handling.

## Validation gate (before export)

- Schema check per record (pydantic / jsonschema / hand-rolled asserts): required fields present, types right, values in sane ranges (price > 0, date not in future…).
- **Batch sanity**: row count vs. expectation (±20% of last run → warn), % nulls per column, min/max of numerics. A scraper that silently returns 12 rows instead of 1,200 is worse than one that crashes.
- Invalid records → `data/quarantine/` with reasons, counted in the run summary. Never silently dropped.

## Export

- CSV for spreadsheets (UTF-8 **with BOM** if Excel is the consumer, proper quoting), JSONL for downstream processing, **SQLite when there's any querying/joining/incremental updating** — it's the best default for >1 table or >1 run.
- Idempotent writes: output keyed by date/run-id, or upsert into SQLite on natural key. Rerunning a pipeline must never duplicate rows.
- Every run emits a **run summary**: fetched / parsed / valid / quarantined / exported counts, duration, and warnings. Print it and append to `runs.log`.

## Recurring pipelines

- Make the entry point one command (`python pipeline.py --since 2026-07-01`), config via args/env — no editing code to change dates.
- Incremental mode: fetch only new/changed items (by date cursor, id watermark, or ETag/Last-Modified) — full refetch is a fallback, not the schedule.
- Schedule with cron/systemd-timer/CI (see the `workflow-automation` skill); alert on failure *and* on anomaly (row-count sanity), not just on crash.

## Definition of done

- [ ] Rerun-safe (resumable fetch, idempotent export) — actually rerun it and check.
- [ ] Parser fixture tests pass; extraction failure counts are reported per field.
- [ ] Validation gate active; quarantine populated instead of silent drops.
- [ ] Run summary printed with counts a human can sanity-check.
- [ ] Politeness settings stated in the report (rate, UA, robots status).
