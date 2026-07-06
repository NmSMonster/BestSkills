---
name: digital-footprint-audit
description: Comprehensive OSINT self-audit — map everything publicly discoverable about YOURSELF (or a person/organization that has explicitly authorized it), score the exposure and its real-world risk, then produce a prioritized remediation and monitoring plan. Use when the user wants to audit their own digital footprint, find what's exposed about them online, do pre-employment/pre-publicity privacy hardening, check for doxxing exposure, run a personal or executive privacy review, or reduce their attack surface. This is a DEFENSIVE, consent-gated skill: it exists to help people find and shrink their own exposure, not to profile third parties.
---

# Digital Footprint Audit

A footprint audit answers one question to a professional standard: **"If a determined adversary targeted me/us with only public information, what could they assemble, and how do I shut it down?"** The output is not a pile of links — it is a scored exposure map plus a remediation plan that measurably shrinks the attack surface.

This skill runs the same tradecraft a privacy-focused threat-intel team or a protective-intelligence detail would run — but pointed *inward*, at the subject's own exposure, to defend it.

## ⛔ Consent gate — resolve BEFORE any collection

This skill operates only in one of these modes. Establish which one applies in the first exchange; if none does, stop and explain why.

1. **Self-audit** — the user is auditing their own footprint. Default and always allowed.
2. **Authorized audit** — the user has explicit authorization to audit a specific person (signed consent, e.g. an executive-protection or penetration-testing engagement) OR an organization/brand they represent. Ask the user to confirm the authorization exists; record it in the report header.
3. **Public-entity / corporate audit** — the subject is a company, brand, or public-facing organizational identity. Allowed.

**Hard stops — refuse and offer the defensive alternative instead:**
- Building a profile of a private third party the user has not been authorized to audit ("my ex", "this person", "a girl I met") — regardless of stated reason.
- Anything whose goal is to *locate, contact, confront, monitor, or pressure* a person rather than to *defend* a footprint.
- Circumventing access controls: logging into others' accounts, guessing passwords, social-engineering, buying leaked data, scraping behind authentication, or defeating a site's anti-bot measures.
- Compiling minors' information beyond a parent auditing their own child's exposure.

If a request drifts toward these mid-audit, name it and stop. A self-audit and a stalking tool touch some of the same sources — the dividing line is **whose footprint, with whose consent, toward defense vs. targeting.** Hold that line without apology.

## Sources restriction

Only **open, public, lawful** sources: public web and search engines, the subject's own accounts as *they themselves* can view them, public records that are lawfully public in the relevant jurisdiction, and reputable breach-notification services (HIBP-style) that the subject queries about *their own* identifiers. No paid data-broker "full reports," no leaked credential dumps, no authenticated scraping of others.

## The audit pipeline

Run these phases in order. Depth scales to stakes — a routine personal check is a couple of hours; an executive protective-intelligence audit is a multi-day effort. Load the reference files as you reach each phase.

### Phase 0 — Scope & seed
- Confirm mode (above) and record it.
- Collect **seed identifiers** the subject knowingly provides about themselves: full name + variants/maiden/aliases, usernames/handles, email addresses, phone numbers, home city, employer, personal domains, profile photos. These are the pivots; everything downstream expands from them.
- Set the **threat model**: what is the subject actually defending against? (doxxing/harassment, stalking/physical safety, credential stuffing & account takeover, social engineering of them or their company, pre-publicity/pre-hiring scrutiny, corporate espionage). The threat model decides what counts as high-risk — a home address is catastrophic for a harassment target and trivial for a registered business.

### Phase 1 — Collect (breadth first)
Sweep every surface category, recording each finding as you go. **Full source checklist and query craft:** `references/source-map.md`.
- Search-engine presence (name, name+city, name+employer, in quotes; image search on profile photos).
- Social & community accounts (via username enumeration across platforms).
- People-search & data-broker listings (what they *display publicly* — the removable exposure).
- Breach exposure (subject's own emails/phones against breach-notification services).
- Public & government records lawfully public in-jurisdiction (business registries, court/property where public, domain WHOIS).
- Content the subject created (posts, commits, docs, forum history, old blogs) and content *about* them (mentions, tags, press).
- Technical/metadata leakage (EXIF geolocation in published photos, usernames reused as email locals, exposed personal domains/servers).

### Phase 2 — Correlate & pivot
This is where scattered data becomes a profile — which is exactly what an adversary does, so you must do it to know the true exposure.
- **Pivot** on each new identifier: a username found on one site → search it everywhere; a reused email → breach check + account discovery; a photo → reverse image → other profiles.
- **Correlate** across sources to flag *aggregation risk*: individually-harmless facts that combine into something dangerous (gym check-ins + a commute photo + an "at the office" post = a predictable daily pattern; a pet's name across two sites = a probable security-question answer).
- Note **linkage**: which "anonymous" or pseudonymous accounts are tied back to the real identity, and by what thread (reused handle, avatar, writing style, cross-post).

### Phase 3 — Score the exposure
Rate every finding for **sensitivity × discoverability × removability**, and roll up to an overall posture. **Scoring rubric and the risk matrix:** `references/risk-scoring.md`.
- Flag the **critical few** first: anything enabling physical location, account takeover, financial fraud, or impersonation.
- Distinguish *what's out there* from *what's easily removable* — the remediation plan is built from the removable, high-sensitivity items.

### Phase 4 — Remediate & harden
Turn findings into an ordered action plan the subject can actually execute. **Removal procedures, opt-outs, and hardening playbook:** `references/remediation-playbook.md`.
- Order by **(risk reduction ÷ effort)** — quick, high-impact wins first (broker opt-outs, locking down the one over-shared account, killing EXIF), structural changes later.
- Each action: what to do, exact where/how (link or steps), expected effect, and how to verify it worked.

### Phase 5 — Monitor
Exposure regrows — brokers re-list, new breaches land, new posts leak. Set up ongoing detection (self-search alerts, breach-notification subscriptions, periodic re-audit cadence). The `automation-pro:workflow-automation` skill can turn this into a scheduled change-detection job.

## Deliverable

Produce a single structured report:

```
# Digital Footprint Audit — <subject>
Mode: <self / authorized / public-entity>   Authorization: <stated basis>
Date: <date>   Threat model: <what we're defending against>

## Executive summary
Overall exposure posture (Critical/High/Moderate/Low) in 4–6 sentences:
the 3 things an adversary could do today, and the 3 actions that cut the most risk.

## Exposure map
Per surface category: what was found, where, sensitivity, and removability.

## Critical findings (the "fix this week" list)
Ranked. Each: finding → why it's dangerous under the threat model → exact fix → verification.

## Aggregation risks
Individually-harmless items that combine into real risk; break the linkage.

## Remediation plan
Prioritized by risk-reduction ÷ effort. Quick wins → structural → ongoing.

## Monitoring plan
What to watch, how, cadence, and the re-audit date.

## Appendix — full findings log
Every source checked (incl. "nothing found" — negative results are results), with links & dates.
```

## Operating rules

- **Everything logged with source + date.** Footprint data is volatile; an undated finding is unverifiable next month.
- **Report facts, not inferences dressed as facts.** "Reused handle `x` appears on 4 platforms" is a finding; "therefore they live at…" is a hypothesis — label it.
- **Store the audit securely.** The report itself is a concentrated dossier — the single most dangerous document produced. Tell the subject to keep it encrypted/access-controlled and never to share it casually. Offer to keep working files in the scratchpad and to avoid restating raw sensitive values (full numbers, addresses) in plaintext where masking suffices ("home address on broker X — [REDACTED in report; see secure appendix]").
- **No fabrication and no filler.** If a surface is clean, say so. A short honest audit beats a padded one.
- **Defensive framing end to end.** Every finding pairs with a defense. The purpose is to shrink the surface, never to demonstrate how to exploit it.
