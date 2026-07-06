---
name: database-design
description: Designing and evolving database schemas — tables, relationships, keys, indexes, normalization, and safe migrations that don't break production. Use when the user asks to design a schema/data model, add or change tables/columns, fix slow queries via indexing, plan a migration, choose between SQL and NoSQL, or review a database design. Covers relational modeling, indexing strategy, and zero-downtime schema changes.
---

# Database Design

The schema is the most expensive thing to get wrong — application code is rewritten in an afternoon; a bad data model is lived with for years and migrated at 2 a.m. Design for the queries you'll actually run and the changes you'll actually make, and evolve it without ever taking the system down.

## Phase 1 — Model from the domain and the queries

1. **Entities & relationships first.** List the real-world things (users, orders, products) and how they relate (one-to-many, many-to-many, one-to-one). Draw it. Each entity → a table; each many-to-many → a join table.
2. **Then the access patterns.** Write the actual queries the app will run ("get a user's last 10 orders with line items", "top products by revenue this month"). **The schema exists to serve these** — a beautiful normalized model that makes the hot query a 6-table join is a bad model. Design and index for the reads/writes you'll really do.
3. **Choose the store deliberately.** Default to a relational DB (Postgres) — it's the right answer far more often than trends suggest: transactions, constraints, joins, and flexibility you'll need later. Reach for NoSQL only with a reason (document store for genuinely schemaless/hierarchical data; key-value for cache/session; wide-column for massive write-scale with known access patterns). "It's web-scale" is not a reason.

## Phase 2 — Relational modeling

**Keys**
- Every table has a primary key. Prefer a surrogate key (auto-increment `bigint`, or UUID/ULID if you need to generate ids client-side or hide counts). Add unique constraints on the real natural keys (email, sku) separately.
- Foreign keys **with constraints enabled** — let the DB enforce referential integrity; "we'll handle it in the app" is how orphan rows and corruption happen. Decide `ON DELETE` behavior explicitly (cascade / restrict / set null).

**Normalization — then denormalize on purpose**
- Normalize to 3NF as the default: each fact in one place, no update anomalies. A value that can be derived or that duplicates another row is a bug waiting to desynchronize.
- Denormalize **only** for a measured read-performance need, and when you do: document it, and make the write path keep the copies consistent (trigger, transaction, or a rebuild job). Un-owned denormalization rots.

**Types & constraints — the DB is your last line of defense**
- Tightest correct type: `int`/`bigint` deliberately (will it overflow?), `numeric`/`decimal` for money (**never float**), `timestamptz` for time (always store UTC, with timezone type), native `boolean`/`enum`, `text` over arbitrary `varchar(n)` limits unless a limit is meaningful.
- `NOT NULL` wherever null is invalid; `CHECK` constraints for ranges and rules (`price >= 0`, valid status); `UNIQUE` for real uniqueness. Constraints catch bugs the app forgot — they're free correctness.
- Nullable means "genuinely optional or unknown" — not "I didn't decide." Distinguish "no value" from "empty" from "zero."

## Phase 3 — Indexing strategy

Indexes are the difference between 3 ms and 3 s — and between fast reads and slow writes. Index intentionally:
- **Index what you filter, join, and sort on.** Every foreign key used in joins; columns in `WHERE`, `ORDER BY`, and unique constraints.
- **Composite index order matters**: match the query's filter/sort order; the leftmost columns must be the ones you filter on. `(user_id, created_at)` serves "this user's rows newest-first"; the reverse doesn't.
- **Don't over-index**: every index slows writes and costs storage. Drop unused ones. Don't index low-cardinality columns alone (a boolean) — usually useless.
- **Verify with the planner**: `EXPLAIN ANALYZE` the real query on realistic data volume. A sequential scan on a big table in a hot query is the signal. Watch for indexes defeated by functions on the column or type mismatches.
- Know the specialized ones when relevant: partial indexes (index only the rows you query), covering indexes (`INCLUDE` to serve a query from the index alone), GIN/GiST (full-text, JSON, geo).

## Phase 4 — Safe migrations (never break prod)

Schema changes run against a live system with the *old* code still deployed. The rule: **every migration is backward-compatible with the currently-running code**, and reversible.

**Expand → migrate → contract** (the zero-downtime pattern), each step a separate deploy:
1. **Expand**: add the new structure (nullable column, new table, new index) — old code ignores it, keeps working.
2. **Backfill & dual-write**: new code writes both old and new; backfill existing rows in **batches** (never one giant `UPDATE` that locks a huge table).
3. **Migrate reads**: switch reads to the new structure once backfill is verified complete.
4. **Contract**: after the old code is fully gone, drop the old column/constraint.

Danger list — these lock or break things; plan around them:
- Adding a `NOT NULL` column with no default on a big table → rewrite/lock. Add nullable, backfill, then add the constraint (validated separately, e.g. `NOT VALID` then `VALIDATE`).
- Renaming/dropping a column that deployed code still uses → instant errors. Expand/contract instead.
- Creating an index on a big table → use the non-locking form (`CREATE INDEX CONCURRENTLY` in Postgres).
- Every migration has a tested **down/rollback**; test the migration on a prod-sized copy before running it for real.

## Deliverable

Schema DDL (or ORM models) + an ER description + the index list with the query each serves + the migration plan (ordered, backward-compatible steps with rollback). Plus a short rationale: normalization choices, any deliberate denormalization and how it's kept consistent, and the access patterns that drove the design.

## Rules

- Money is `decimal`, time is `timestamptz` in UTC, ids are deliberate — these three mistakes are the most common and the most painful.
- Constraints in the DB, not just the app. The DB outlives every app that talks to it.
- No migration that isn't backward-compatible with running code and reversible.
- Index for real queries verified with `EXPLAIN`, not for hypothetical ones.
