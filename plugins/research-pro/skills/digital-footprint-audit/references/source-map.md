# Source Map & Collection Craft

The complete surface inventory for a footprint audit, with query craft per surface. Work top to bottom; record every check (including clean ones) in the findings log. Everything here uses **open, public, lawful** sources only — see the consent gate and sources restriction in SKILL.md.

## Pivot discipline (the core technique)

An audit is a graph traversal. Each identifier you confirm becomes a new seed you re-run through every relevant surface. Maintain a running **identifier ledger**:

| type | value | first seen (source) | confidence | pivoted? |
|---|---|---|---|---|
| handle | `janek_k` | github | confirmed | ✅ |
| email | j.k@… | WHOIS | probable | ⬜ |

Never leave a `confirmed` identifier un-pivoted — that's exactly the gap between a shallow check and a real audit. Stop when new pivots stop yielding new identifiers (saturation).

---

## 1. Search engines (breadth pass)

Run each query on at least two engines (Google + Bing/DuckDuckGo; add Yandex for image search — it is markedly stronger on faces). Record what appears on pages 1–2.

Query set (substitute the subject's seeds):
- `"First Last"` (quoted, exact)
- `"First Last" <city>` / `"First Last" <employer>` / `"First Last" <profession>`
- `"First Last" (email OR phone OR "@handle")`
- Maiden/former names, nicknames, and common misspellings
- Old identifiers: former employers, former cities, school/university

Operators worth knowing:
- `site:` — enumerate presence per platform (`site:reddit.com "handle"`).
- `filetype:pdf "First Last"` — resumes, member lists, meeting minutes, leaked docs often sit in PDFs/XLS.
- `intext:` / quotes — force exact phrase; kills fuzzy matches.
- `-` — exclude a common namesake to cut noise.
- Search the subject's **email local-part** and **phone** as quoted strings — they surface in scraped directories and paste sites.

Image search: reverse-search each public profile photo and avatar (Google Lens, Yandex, TinEye). Faces and reused avatars are the strongest cross-platform linker there is.

## 2. Username / handle enumeration

A reused handle is the spine of most footprints. For each handle in the ledger:
- Check presence across major platforms manually, and note the open-source enumeration tools that do this at scale (e.g. Sherlock, Maigret, WhatsMyName) — describe them to the user for their own self-audit; each queries *public* profile URLs only.
- For each hit, open the profile: is it the subject? What does it leak (real name, location, other linked accounts, activity times)?
- **Handle mutations**: people vary a base handle (`janek`, `janek_k`, `jkowalski`, `janek1990`). Generate plausible variants from the known ones and re-check.

## 3. Social & community platforms

Per platform, capture: display name, bio, location, linked accounts, public post history, tagged photos, follower/following that reveal relationships, and **metadata leakage** (post timestamps → timezone/routine; check-ins → places).
- Mainstream social (public-visibility posts only — as the subject themselves sees them; do not attempt to see private content).
- Professional networks (employer, role history, colleagues, email-format inference).
- Developer/creator platforms (code commits leak real names + emails via `git log`; ask the subject to run `git log --format='%an %ae'` on their own repos — a classic accidental email leak).
- Forums, Q&A, review sites, gaming profiles, Strava/fitness (routes and routines — a top physical-safety leak).

## 4. People-search & data brokers

These aggregate public + purchased records into profiles — the **most removable high-value exposure**, which is why they lead the remediation plan.
- Check what each broker *displays publicly* about the subject (name, age, relatives, past addresses, phone). Record the listing URL — you'll need it for the opt-out in the playbook.
- Coverage is regional: US (Spokeo, Whitepages, BeenVerified, Radaris, TruePeopleSearch, etc.), UK (192.com), and EU equivalents. In GDPR jurisdictions much broker activity is restricted and removal is a legal right — note that; it shapes remediation.
- **Do not purchase** "full reports." View only free public display; the point is to find what's exposed so it can be removed, not to buy a dossier.

## 5. Breach & credential exposure

Defensive check of the subject's *own* identifiers against breach-notification services.
- Query each of the subject's emails and phone numbers on Have I Been Pwned (and similar reputable notification services) for *breach membership* — which breaches exposed them and what data classes (passwords, addresses, etc.).
- **Never** obtain, open, or search the actual leaked credential dumps. Membership notification (defensive) is the line; possessing the dump is not.
- Every breach hit → an action item: rotate that password everywhere it was reused, enable MFA, assume that email is on spam/phishing lists.

## 6. Public & government records (jurisdiction-bound)

Only records that are *lawfully public* where the subject is, and only about the subject/their own entities:
- Business registries (PL: KRS/CEIDG; UK: Companies House; US: state SoS) — directorships, company addresses, filings.
- Domain WHOIS for the subject's own domains (privacy-proxy status is itself a finding — unproxied WHOIS can leak a home address).
- Court/property/voter records where those are public in-jurisdiction — handle with extra care; flag rather than transcribe sensitive values.
- Professional licenses, patents, academic publications, sanctions/PEP lists (relevant for executive/corporate mode).

## 7. Content authored by / about the subject

- **By**: old blogs, deleted-but-cached pages (Wayback Machine, Google cache), pastebins, comment history, uploaded documents. People forget what they published a decade ago; adversaries don't.
- **About**: news mentions, event attendee/speaker lists, org "team" pages, tagged/mentioned posts, wedding/obituary/school pages (rich in relatives and dates).

## 8. Technical & metadata leakage

- **EXIF**: download the subject's *own* publicly-posted photos and inspect metadata — GPS coordinates, device, timestamps. Geotagged photos are a top physical-location leak; most platforms strip EXIF but many blogs/forums/direct-hosted images don't.
- **Email/username inference**: corporate email format (`first.last@`) is usually derivable from one known address + the pattern; note it as a phishing-target finding.
- **Infra**: personal domains/servers, exposed home-lab services, S3 buckets tied to the subject's handle — DNS records and subdomains can leak internal names.

---

## Collection hygiene

- **Log negatives.** "Not found on X" is a genuine result and part of the posture.
- **Timestamp everything** — record the date of each check; volatile data changes weekly.
- **Confidence, not certainty.** Same-name ≠ same-person. Mark each finding confirmed / probable / possible, and say what would confirm it. Namesake collisions are the #1 error in footprint work — never merge two people on a name match alone.
- **Minimize retained sensitive data.** In working notes and the final report, mask what doesn't need to be in plaintext (`•••• last-4`, "[home address — secure appendix]"). The report is a dossier; treat it like one.
- **Stay in-band.** Public view only, no auth-bypass, no anti-bot evasion, no purchased leaks. If a source needs any of those, it's out of scope — note the exposure exists and move on.
