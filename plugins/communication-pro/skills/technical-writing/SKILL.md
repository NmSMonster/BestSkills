---
name: technical-writing
description: Writing clear technical documentation — READMEs, API docs, guides, tutorials, runbooks, architecture docs, RFCs, and ADRs. Use when the user asks to write or improve documentation, a README, setup/usage guide, API reference, design doc, or any explanation of how something technical works. Enforces writing for the reader's task, not the author's knowledge — with the right document type for the goal.
---

# Technical Writing

Documentation exists to get a specific reader to a specific outcome — install it, call the API, understand the design, recover the outage. It is judged by whether they succeed, not by how complete it feels. The universal failure is writing from what the author knows instead of what the reader needs to do.

## Step 0 — Reader and goal

Before writing, pin down: **who** reads this (their existing knowledge — a first-time user and a maintainer need opposite docs) and **what task** they're trying to complete. Every sentence then earns its place by serving that task or gets cut. If one document serves two very different readers/goals, split it — a README that's also an architecture treatise fails both.

## Step 1 — Pick the right document type

The single most common documentation mistake is mixing these four modes; each has a different shape (the Diátaxis distinction):

| Type | Reader wants | Shape |
|---|---|---|
| **Tutorial** | to learn by doing, first time | Guided, guaranteed-to-work happy path; no options, no theory; every step verified |
| **How-to / guide** | to accomplish a specific task | Goal-oriented steps; assumes basic competence; addresses real variations |
| **Reference** | to look up precise facts | Complete, consistent, dry; describes the machinery; optimized for scanning, not reading |
| **Explanation / design doc** | to understand *why* | Context, tradeoffs, alternatives, rationale; discursive |

Naming the mode before writing prevents the muddle where a tutorial drowns in reference detail or a reference tries to teach.

## Step 2 — Structure for scanning

Nobody reads docs linearly; they scan for their spot. Serve that:
- **Front-load the answer.** Most important info first — inverted pyramid. The reader may leave after the first screen; make it count.
- **Descriptive headings** that say the task ("Authenticate a request"), so the table of contents *is* a map. Readers navigate by heading.
- **Short paragraphs, one idea each.** Lists for steps and options. Tables for structured facts (params, flags, error codes).
- **Code you can copy and run** — complete, correct, tested. A snippet with a `...` placeholder or an undeclared import wastes the reader's next ten minutes. Show the expected output.
- **Progressive disclosure**: common case first, edge cases and advanced options later or linked. Don't make the 90% reader wade through the 10% path.

## Step 3 — Write clearly

- **Concrete over abstract.** "Returns `null` if the user isn't found" beats "handles the not-found case."
- **Active voice, present tense, second person.** "Send a POST to `/orders`" not "An order may be created by the sending of a request."
- **Define the one term the reader won't know; delete the jargon they don't need.** Don't show off vocabulary; don't dumb down real precision.
- **Say what breaks.** Prerequisites, gotchas, common errors, and what *not* to do save more time than any happy-path prose. A `⚠ Note:` at the point of danger is worth a page of caveats up front.
- **Consistent terminology.** Pick one name per concept and never vary it — "user"/"account"/"member" for the same thing forces the reader to guess if they're different.
- Cut ruthlessly: "in order to"→"to", "at this point in time"→"now", "it should be noted that"→delete. Every removed filler word raises the signal.

## Document-specific templates

**README** (the front door — a stranger's first 60 seconds):
```
# Project — one line: what it is and who it's for
Badges (build, version) if relevant
## What it does — 2–3 sentences, the problem it solves
## Install — copy-paste, working
## Quickstart — the smallest complete working example, with output
## Usage — the common tasks
## Configuration — options table
## Links — full docs, contributing, license
```
Lead with what it does and a working example. Save architecture and philosophy for later/linked.

**API reference** (per endpoint/function): purpose (1 line) · signature/params (name, type, required, meaning) · returns · errors/exceptions · a runnable example with real values · notes (auth, rate limits, idempotency). Consistency across entries lets readers scan.

**ADR (Architecture Decision Record)** — short, immutable, one per decision: Context (forces at play) · Decision (what we chose) · Consequences (good and bad, what we're now committed to) · Status (proposed/accepted/superseded). Records *why* for the engineer who inherits it in two years.

**RFC / design doc**: Problem & goals (and non-goals) · Proposed design · Alternatives considered and why rejected · Tradeoffs & risks · Rollout/migration · Open questions. The alternatives section is where the real thinking shows.

**Runbook** (for an incident, read under stress): symptom → diagnosis steps → fix steps, each command copy-pasteable, expected output shown, escalation path. Written so a tired on-call engineer at 3 a.m. can follow it without thinking.

## Quality bar

- [ ] A reader in the target audience can complete the task using only this doc.
- [ ] Every code example runs as written (test them) and shows expected output.
- [ ] The document is one mode (tutorial/how-to/reference/explanation), not a muddle.
- [ ] Headings alone convey the structure; the reader can find their section in seconds.
- [ ] Prerequisites, gotchas, and failure modes are stated, not just the happy path.
- [ ] No orphaned knowledge assumed — either the reader has it (stated) or it's defined/linked.
- [ ] Ruthlessly de-fluffed: no filler, no repetition, no showing off.

## Working method

Draft to the reader's task, then do a **reader pass**: read it as someone who knows nothing about the internals, and mark every place you'd get stuck, every undefined term, every step that assumes context. Fix those — that pass is where mediocre docs become good ones.
