---
name: literature-review
description: Structured review and synthesis of academic papers, technical reports, or a body of documents on a topic — thematic synthesis, evidence tables, and gap analysis. Use when the user asks for a literature review, a survey of academic research or papers, a state-of-the-art summary, a related-work section, an evidence table across studies, or synthesis across a set of provided papers/PDFs. For a general researched answer to a topic rather than a formal synthesis of the scholarly literature, use deep-research instead.
---

# Literature Review

A literature review synthesizes *across* sources by theme and evidence strength — it is not a stack of per-paper summaries. The reader should finish knowing what the field agrees on, where it disagrees, and what remains open.

## Phase 1 — Scope

- Define the review question precisely (population/system, intervention/method, outcome — adapt PICO to the domain).
- Set inclusion criteria before searching: time window, study/document types, venues, language. Write them down; apply them consistently.
- Decide the deliverable with the user: narrative review (default), systematic-style with methods section, related-work section for a paper, or annotated bibliography.

## Phase 2 — Gather

- Search scholarly sources (Google Scholar, arXiv, PubMed, ACL Anthology, SSRN — whichever fit the field) with multiple query formulations, including the field's competing terminologies.
- **Snowball**: from each key paper, follow references backward (its citations) and forward (papers citing it — Scholar's "cited by"). Two rounds of snowballing from 3 seed papers beats twenty raw searches.
- Prefer: peer-reviewed > preprints > technical reports > blog posts, but recent preprints are often where the state of the art lives in fast fields — include them, labeled.
- Identify the 3–5 **anchor papers** (foundational or most-cited) — misreading these poisons the review.
- Stop gathering when new searches return papers you've already seen (saturation), not at an arbitrary count.

## Phase 3 — Extract

For every included paper, capture into an **evidence table** (build it as you read, in a file):

| Paper (year) | Method/design | Data/sample & size | Key finding | Effect/metrics | Limitations | Venue/citations |

Reading discipline:
- Abstract + figures + conclusions first; read methods carefully for any paper whose finding you'll rely on.
- Record what the paper **actually showed**, not what its abstract implies. Note when conclusions outrun the data (small n, no baseline comparison, cherry-picked benchmark).
- Note conflicts of interest and funding for load-bearing results.
- Never cite a paper you only saw cited elsewhere — abstracts and citation chains routinely distort claims. If you can't access it, mark it "(not directly reviewed)".

## Phase 4 — Synthesize by theme

1. Cluster findings into 3–7 **themes** (methods families, schools of thought, problem aspects) — these become your section headings, never the paper names.
2. Within each theme, characterize:
   - **Consensus**: what multiple independent groups replicate.
   - **Contested**: where results conflict — and *why* (different datasets? metrics? definitions? eras?). Diagnosing the disagreement is the highest-value synthesis.
   - **Trajectory**: how the theme evolved; what superseded what.
3. Weigh, don't count: one strong replication outweighs five weak papers. Note replication status explicitly where a field has known issues.
4. **Gap analysis**: questions no included work answers, populations/settings untested, methods not yet applied. This section is what makes a review useful for deciding what to do next.

## Deliverable

```
# Review: <question>
## Summary — the state of knowledge in one paragraph
## Methods — search terms, sources, inclusion criteria, N included (for systematic-style)
## Themes — per theme: consensus / contested / trajectory, with inline citations (Author, Year)
## Evidence table — the extraction table
## Gaps & open questions
## References — full list, links/DOIs, access dates
```

## Quality bar

- Every claim in the synthesis traces to ≥1 named paper; contested claims show both sides.
- Recency handled honestly: state the search cutoff date; flag fields moving faster than the newest included work.
- Your own analytical voice is present (comparisons, diagnoses of conflicts) and clearly distinguishable from reported findings.
