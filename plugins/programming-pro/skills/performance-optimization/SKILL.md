---
name: performance-optimization
description: Measurement-first performance work — profiling, finding bottlenecks, fixing slow code, slow queries, high memory use, slow builds, or latency/throughput problems. Use when the user says something is slow, wants it faster, asks about optimization, scaling, N+1 queries, caching, or resource usage. Enforces baseline → profile → fix the biggest cost → re-measure, and forbids blind micro-optimization.
---

# Performance Optimization

The cardinal rule: **never optimize what you haven't measured.** Intuition about bottlenecks is wrong more often than right, and an optimization without a baseline is indistinguishable from noise. Every claim of "faster" in your final report must carry two numbers.

## Workflow

### 1. Define the target
- What operation, under what load, and what does "fast enough" mean? Get a concrete budget (e.g., "p95 < 300 ms at 100 RPS", "batch completes < 10 min"). If the user has none, propose one — optimization without a stop condition never ends.
- Optimize the metric that matters: latency (and *which percentile* — p95/p99, not mean), throughput, memory, startup time, or cost. They trade against each other.

### 2. Baseline (before reading any code)
- Reproduce the slowness with a repeatable measurement: a benchmark script, a timed test, `hyperfine` for CLIs, load test for services, `EXPLAIN ANALYZE` for queries.
- Realistic data size and warm/cold state matter — 100 rows hides what 1M rows screams.
- Run ≥ 5 iterations; record median and spread. Save the exact command so the after-measurement is identical.

### 3. Profile — let the data point
- CPU: sampling profiler (`py-spy`/cProfile, Node `--cpu-prof`/clinic, `pprof`, `perf`), read as flame graph. Look for the widest frames, not the deepest.
- Memory: heap snapshots/`tracemalloc`/`pprof -alloc_space`; look for retention (leaks) vs. churn (allocation rate) — different fixes.
- I/O & waiting: wall time ≫ CPU time means the answer is in blocking calls — trace queries, HTTP calls, disk. For services, per-request tracing/log timing beats a profiler.
- Databases: log slow queries; `EXPLAIN ANALYZE` the top ones; count queries per request (N+1 detection: does query count scale with result size?).
- Identify the top 1–3 costs. **If the top item is < 20% of total time, no single fix will save you** — report that honestly rather than shaving 3%.

### 4. Fix in order of leverage
Work down this ladder — each level typically dominates the ones below:
1. **Don't do the work**: cache it, precompute it, do it lazily, skip it entirely when the result isn't used, dedupe repeated identical calls.
2. **Do less work**: better algorithm/data structure (O(n²)→O(n log n), list-scan→dict/set lookup), fetch only needed columns/fields, paginate, filter at the source (push predicates into the DB/API), right index for the query.
3. **Do the work in bulk**: batch queries (N+1 → 1 join or `IN`), bulk inserts, pipeline network calls, buffered I/O.
4. **Do it concurrently**: parallelize independent I/O (async/`gather`, thread pools), only *after* levels 1–3 — parallelizing waste is still waste.
5. **Do it cheaper**: micro-optimizations (allocation reuse, hot-loop tweaks, vectorization/numpy, compiled paths) — only in a profiler-confirmed hot loop.

One change at a time → re-measure with the identical baseline command → keep if it wins, revert if it doesn't. Log each experiment (change, before, after).

### 5. Verify you broke nothing
- Full test suite green. Perf fixes love to change semantics (caching adds staleness, concurrency adds races, batching changes error granularity — one item failing now fails the batch: decide and document).
- For caches: define invalidation, TTL, and size bound *at introduction time*. An unbounded cache is a memory leak with good PR.

### 6. Report
Table of before → after for the target metric, the root cause(s) in plain language, what was changed, the trade-offs accepted (memory-for-speed, staleness, complexity), and what the next bottleneck would be if more speed is needed.

## Anti-patterns

- Optimizing code because it *looks* slow. Looks lie; profiles don't.
- Benchmarking on trivial data, in debug builds, or with the profiler attached for the final numbers.
- Rewriting to a "faster language/framework" as step one — it's step ten, after the algorithm and I/O are fixed.
- Adding concurrency to code with shared mutable state without a synchronization plan.
- Deleting the benchmark after finishing. Check it in — it's the regression guard.
