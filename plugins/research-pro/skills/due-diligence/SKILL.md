---
name: due-diligence
description: Structured background research on a company, vendor, investment, partner, or organization before a commitment — legitimacy, financials, ownership, reputation, legal, and red flags. Use when the user is vetting a company/vendor/supplier/partner, considering an investment or acquisition, checking if a business is legitimate, evaluating a counterparty, or asks "should we do business with X". Uses public records and lawful sources on organizations and their public-facing principals.
---

# Due Diligence

Due diligence answers one question with evidence: **"What am I actually getting into, and what could go wrong?"** The deliverable is a risk-weighted verdict — proceed / proceed-with-conditions / walk away — backed by verified facts and an explicit list of red flags. The goal is to find the problems *before* the money moves, not after.

Scope: this is research on **organizations and their public-facing business identity** (and named principals in their business capacity) using public, lawful sources — registries, filings, court records, reputable reporting. It is not covert surveillance of private individuals; for personal-exposure work see `research-pro:digital-footprint-audit` (which is consent-gated).

## Step 0 — Frame the risk

Set the decision and its stakes — a $500 tooling purchase and a $5M acquisition warrant very different depth. Establish:
- What's being decided and what's at risk (money, data, reputation, dependency, legal liability).
- The **dealbreakers** up front: what facts, if true, mean automatic no (insolvency, fraud history, sanctions, no legal existence).
- Depth: vendor check (hours) vs. investment/M&A diligence (deep, multi-workstream).

## The diligence workstreams

Work these in order; stop early only if a dealbreaker surfaces.

### 1. Existence & legitimacy (do this first — it's cheap and disqualifying)
- **Legal registration**: does the entity actually exist? Company registry (PL: KRS/CEIDG, UK: Companies House, US: state SoS) — legal name, registration number, status (active/dissolved/insolvent), incorporation date, registered address.
- Red flags: not registered, dissolved/struck-off, registered days ago for a "established 20 years" claim, virtual-office-only address shared by hundreds of shell entities, name mismatch with what they told you.

### 2. Ownership & structure
- Who owns and controls it: directors, shareholders, ultimate beneficial owner (UBO). Follow the chain through holding companies.
- Red flags: hidden/obscured ownership, opaque offshore layering with no business reason, directors linked to prior failed/fraudulent entities, frequent recent ownership changes, the same individuals behind a web of shells.

### 3. Financial health
- For entities that file: accounts/annual returns from the registry — revenue trend, profitability, assets vs. liabilities, going-concern notes, auditor changes, late filings.
- Signals of distress: negative equity, shrinking revenue, mounting liabilities, late or overdue filings, qualified audit opinion, a recent auditor resignation.
- For private/unfiling entities: proxy signals — headcount trend (LinkedIn), hiring/layoffs, funding history, payment behavior (trade references, credit reports where available), office moves.

### 4. Legal & regulatory
- Litigation history (court records where public), judgments, liens, bankruptcies.
- Regulatory standing: required licenses held and current; enforcement actions, fines, consent decrees.
- **Sanctions & watchlists**: screen the entity and principals against sanctions lists (OFAC, EU, UN), PEP lists, and debarment lists — a hit here is usually a hard stop.
- Red flags: pattern of litigation (esp. as defendant on the same issue), unpaid judgments, revoked licenses, any sanctions/enforcement hit.

### 5. Reputation & track record
- Customer/counterparty experience: reviews (read the critical ones), BBB/trade complaints, references — and *check* references, don't just collect them.
- Press: coverage good and bad; search "[company] fraud/lawsuit/scam/complaint/data breach" explicitly — you're hunting for the bad news, because that's the point.
- For vendors handling your data: security posture (breach history, certifications like SOC 2/ISO 27001, a real security page vs. marketing).
- Red flags: pattern of the same complaint, unresolved disputes, a breach with a bad response, fabricated/only-5-star reviews, key people with a history of failed ventures or misconduct.

### 6. Operational fit (for vendors/partners)
- Can they actually deliver: capacity, key-person dependency, subcontracting, business continuity.
- Contractual risk: lock-in, data ownership/portability, SLA teeth, termination terms, liability caps.
- Concentration risk: are you becoming dependent on someone who could fail or squeeze you?

## Verification discipline

- **Verify claims against independent records**, don't accept the counterparty's self-description. "Founded 2005, 200 employees, $50M revenue" → check registry date, headcount proxy, filed accounts. Gaps between claim and record are themselves findings.
- Triangulate (see `research-pro:deep-research` methodology): a fact matters when independent sources confirm it. One glowing testimonial is marketing; a registry filing is evidence.
- **Same-name ≠ same-entity.** Confirm you're researching the right legal entity (registration number, not just a trading name) — the #1 error is attributing another company's record.
- Date everything; note what you *couldn't* verify (private financials, unavailable records) as explicit gaps, not as clean bills of health.

## Deliverable

```
# Due diligence: <entity>, for <decision>
Date · Depth · Sources

## Verdict — Proceed / Proceed with conditions / Walk away — with the reason in 3–5 sentences
## Red flags — ranked; each with evidence and severity (dealbreaker / serious / watch)
## Findings by workstream — existence, ownership, financials, legal, reputation, operational
   (each: what was verified, the source, and the risk read)
## Conditions / mitigations — if "proceed with conditions", exactly what to require
   (escrow, shorter term, audit rights, references, insurance, phased commitment)
## Gaps — what couldn't be verified and how it limits confidence
## Sources — dated, annotated
```

## Rules

- Lead with the verdict and the red flags — that's what the decision needs.
- Every material claim traces to a verifiable source; label the counterparty's own claims as unverified until checked.
- Absence of red flags after a *thorough* search is a finding ("no litigation or sanctions found as of <date>"); absence after a shallow one is not — state which you did.
- A dealbreaker (no legal existence, sanctions hit, active fraud proceedings) ends the analysis — surface it immediately, don't bury it under completeness.
- Public, lawful sources only. Report facts and rated risks; flag inferences as inferences.
