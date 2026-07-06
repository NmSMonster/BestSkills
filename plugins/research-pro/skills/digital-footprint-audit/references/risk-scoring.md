# Risk Scoring Engine

Turns a pile of findings into a defensible, prioritized exposure posture. The goal is to separate the *critical few* from the *trivial many* so remediation effort goes where it cuts real risk. Score every finding; roll up to an overall posture.

## The three axes

Rate each finding 1–5 on each axis.

### Sensitivity — how much harm this datum enables
| Score | Meaning | Examples |
|---|---|---|
| 5 — Critical | Enables physical location, account takeover, or financial fraud | Home address, real-time location/routine, exposed password, government ID, financial account, answers to security questions |
| 4 — High | Strong lever for social engineering or impersonation | Phone number, personal email, DOB, employer+role+schedule, family members' identities, mother's maiden name |
| 3 — Moderate | Useful context for an adversary | City, general workplace, past addresses, education, non-public-facing photos |
| 2 — Low | Minor context | Professional bio, public role, published work |
| 1 — Negligible | Intended-public identity | Company name, public brand handle, published contact-us details |

### Discoverability — how easily an adversary finds it
| Score | Meaning |
|---|---|
| 5 | First page of a name search / broker front page — zero skill needed |
| 4 | Found via one obvious pivot (username search, reverse image) |
| 3 | Requires deliberate cross-source correlation |
| 2 | Buried, needs effort/tools to surface |
| 1 | Technically public but practically very hard to reach |

### Removability — can the subject actually reduce it
| Score | Meaning | Implication |
|---|---|---|
| 5 | Fully removable by the subject | Broker opt-out, delete own post, strip EXIF, tighten privacy setting |
| 4 | Removable via a process/request | GDPR/CCPA request, platform takedown, WHOIS privacy |
| 3 | Suppressible but not deletable | Push down in search, de-index request, minimize going forward |
| 2 | Mostly permanent | Cached/archived content, breach data already circulated |
| 1 | Irreversibly public | Legally-public record (some registries, court filings) |

## Priority score

For each finding compute a **remediation priority**:

```
Risk       = Sensitivity × Discoverability          (1–25: how dangerous it is right now)
Priority   = Risk × (Removability / 5)               (favor high-risk items you can actually fix)
```

- **Risk** ranks *danger*. **Priority** ranks *what to do first* — a Sensitivity-5 item that's irreversibly public (Removability 1) is a monitoring problem, not a fix; a Sensitivity-5 item that's a one-click broker removal (Removability 5) is the top of the action list.
- Sort the remediation plan by Priority descending. Sort the "known permanent risks" list by Risk descending (these feed the monitoring plan and behavioral advice instead of a fix).

## Aggregation multiplier

The whole is more dangerous than the parts. After scoring individually, look for **combinations** and score the *combination* as its own finding, at the sensitivity of what it unlocks:

- City + employer + routine post + gym check-in → **predictable physical pattern** → Sensitivity 5, even though each part was ≤3.
- Pet name + child name + street name across profiles → **security-question / password-guess kit** → Sensitivity 5.
- Personal email + a breach it appeared in + password reused elsewhere → **account-takeover chain** → Sensitivity 5.
- Pseudonymous account + reused avatar linking it to real name → **de-anonymization** → sensitivity of whatever the pseudonymous account contains.

Naming aggregation risks explicitly is the highest-value output of the audit — it's what a trained adversary sees and an untrained subject misses.

## Overall posture

Roll the findings into one headline rating (drives the executive summary):

| Posture | Definition |
|---|---|
| **Critical** | ≥1 finding at Risk ≥ 20 (e.g. exposed home address for a harassment target, or a live credential-reuse chain) |
| **High** | ≥1 finding at Risk 15–19, or several at 10–14 that aggregate |
| **Moderate** | Findings mostly Risk 6–12; removable; no physical-safety or ATO exposure |
| **Low** | Only intended-public identity exposed; nothing sensitive discoverable |

Always weight the posture by the **threat model** from Phase 0: the same home-address finding is Critical for a stalking/harassment target and Moderate for a sole trader whose address is their registered business. State that weighting in the summary — a score without the threat model is theater.

## Presenting scores

For each finding in the report:

```
[Finding]  Home address visible on Radaris listing
Sensitivity 5 · Discoverability 5 · Removability 5  →  Risk 25 · Priority 25  🔴 CRITICAL — fix first
Why (per threat model): direct physical-location exposure for a harassment target.
```

Use a small, consistent visual scale (🔴 Critical / 🟠 High / 🟡 Moderate / 🟢 Low). Numbers earn trust; the color lets the subject triage at a glance. Never inflate — a calm, accurate "Low" is as valuable as a red flag, and crying wolf on trivia buries the one finding that matters.
