# Source Evaluation Reference

Use this when deciding how much weight a source gets in triangulation and how to cite it.

## Quality tiers

**Tier 1 — Primary / authoritative.** Cite freely; one may suffice for a fact.
- Official documentation, changelogs, source code, specs, standards (RFC/ISO/W3C)
- Regulatory filings (SEC/EDGAR, Companies House, KRS), court records, patents
- Government statistics offices (Eurostat, GUS, BLS, OECD), central banks
- Peer-reviewed papers (check venue quality and citation count; a preprint is Tier 2 until reviewed)
- Direct data you can inspect (datasets, APIs, benchmarks you can rerun)

**Tier 2 — High-quality secondary.** Good for synthesis; verify surprising claims against Tier 1.
- Established journalism with editorial standards and named authors (FT, Reuters, Bloomberg, The Economist, major national outlets)
- Recognized industry analysts (Gartner, IDC, McKinsey) — solid on structure/trends, but note their commercial model when vendors are ranked
- Well-known expert practitioners writing in their proven domain
- Conference talks from named engineers about their own systems

**Tier 3 — Useful signal, never sole support.**
- Community: Stack Overflow, Reddit, Hacker News, GitHub issues — excellent for real-world problems and sentiment; sample widely, treat as anecdote
- Company engineering blogs — technically strong, structurally promotional
- Wikipedia — use its *references*, not the article, as your citation

**Tier 4 — Treat as claims requiring external confirmation.**
- Vendor marketing, sponsored "reports", press releases
- SEO content farms (recognizable: listicle format, no named author, affiliate links, generic stock imagery, "Top 10 X in 2026")
- Anonymous or single-purpose sites, AI-generated content mills

## Red flags (downgrade a tier or discard)

- No date, or silently updated content on time-sensitive claims
- No named author for factual/technical claims
- Statistics with no methodology or origin ("studies show")
- Circular sourcing: article cites article that cites the first article
- The domain's business model is selling what the article recommends (check "About", affiliate disclosures)
- Screenshots of data instead of links to data

## Independence test

Two sources are independent only if their information has different origins. Common failures:
- Wire-service story republished in 30 outlets = 1 source
- "Studies show" articles all tracing to one vendor survey = 1 source (Tier 4)
- Analyst report and press coverage of that analyst report = 1 source

Trace claims upstream until you hit the origin; weight the origin, not the echo count.

## Incentive checklist (run on every load-bearing source)

- Who pays this publisher, and does this article's conclusion serve that?
- Would the author suffer any consequence for being wrong?
- Is negative information about the subject present at all? (Its total absence signals filtering.)

## Citing well

- Always: title, link, publication date (and access date for volatile pages).
- Note the bias inline where it matters: "(vendor's own benchmark)".
- For volatile claims (pricing, features), quote the exact figure *and* its as-of date — the reader will land on a changed page.
