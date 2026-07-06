# Remediation & Hardening Playbook

The audit's payoff. Every finding must convert into an action with an expected effect and a verification step. Order the plan by **Priority (risk-reduction ÷ effort)** from the scoring engine — quick high-impact wins first, structural changes after, ongoing hygiene last.

Each action follows one shape: **What → How (exact) → Expected effect → Verify.**

---

## Tier 1 — Quick wins (do this week; hours of effort, large risk cut)

### Data-broker & people-search removal
The single highest-leverage action for most people: brokers are where a name+city becomes a home address.
- **How**: for each broker listing found, use its opt-out/removal page (most have one; it's often buried in the footer or privacy policy). In GDPR/CCPA jurisdictions, submit a formal erasure/do-not-sell request — it's a legal right, not a favor. Keep a tracker: broker · date requested · confirmation · date re-checked.
- **Effect**: removes the most discoverable Sensitivity-4/5 items.
- **Verify**: re-search the listing after the stated processing window (often 1–6 weeks); brokers re-list from fresh data feeds — this becomes a recurring monitoring task, not a one-time fix.
- Note: managed removal services exist and automate the long tail; describe them neutrally as an option, don't endorse a specific paid vendor.

### Credential-exposure response (from breach findings)
- **How**: for every breached account — change the password to a unique one, enable MFA (prefer an authenticator app or hardware key over SMS), and rotate that password *everywhere it was reused*. Move to a password manager so reuse ends structurally.
- **Effect**: breaks the account-takeover aggregation chain, usually the highest-Risk finding.
- **Verify**: re-query the breach service; confirm MFA is active on the critical accounts (email first — it's the reset hub for everything else).

### Lock down the over-shared account
Usually one or two accounts leak most of the personal detail.
- **How**: set post visibility to friends/private, remove location tags, prune the public bio (strip city/employer/DOB), review tagged-photo permissions, and turn off "searchable by phone/email."
- **Effect**: cuts Discoverability on a cluster of findings at once.
- **Verify**: view the profile logged-out (or from an unconnected account) — what a stranger sees is the truth, not what the settings page claims.

### Strip photo metadata & kill geotags
- **How**: remove EXIF from images before posting (platform strippers, or a batch tool on the subject's own files); turn off camera-app location tagging; delete or re-upload already-posted geotagged photos.
- **Effect**: closes a direct physical-location leak.
- **Verify**: download a recently-posted image and inspect EXIF — GPS fields should be absent.

### WHOIS privacy on personal domains
- **How**: enable the registrar's WHOIS privacy/proxy on any personal domain; if the registrar doesn't offer it, consider moving the domain.
- **Effect**: removes a home-address/phone leak that name-searches don't even need.
- **Verify**: run a public WHOIS lookup; registrant contact should show the proxy.

---

## Tier 2 — Structural (weeks; reduces future exposure)

### Search-result suppression / de-indexing
For high-sensitivity items that can't be deleted at source:
- **How**: request removal of outdated/sensitive personal info via search engines' dedicated removal tools (Google's "results about you" / outdated-content and personal-info removal flows; equivalent EU right-to-be-forgotten requests). For content on sites you don't control, send a removal request to the site owner/host first.
- **Effect**: drops Discoverability even where Removability at source is low.
- **Verify**: re-run the exact query after processing; confirm the URL no longer surfaces.

### Segregate identities
- **How**: separate personal from public/professional identity — distinct emails, distinct handles that don't cross-link, no reused avatar between a pseudonymous account and the real name. Where past reuse already linked them, decide whether to abandon or rename the exposed handle.
- **Effect**: breaks the pivot chain future adversaries rely on.
- **Verify**: attempt the username/avatar pivot yourself — it should dead-end.

### Prune the historical trail
- **How**: delete or lock old blogs, dormant accounts, stale forum posts, and abandoned profiles. For cached/archived copies, request removal from the archive after the live page is down.
- **Effect**: shrinks the "content authored by" surface, including the decade-old stuff the subject forgot.
- **Verify**: re-check cache/Wayback for the specific URLs.

### Alias/forwarding for exposure-prone contact
- **How**: use email aliases/masked emails and a secondary number for signups and public-facing use, keeping the primary identifiers off broker feeds and breach lists going forward.
- **Effect**: caps the growth rate of future exposure.

---

## Tier 3 — Behavioral & permanent-risk management

Some findings (Removability 1–2: legally-public records, already-circulated breach data, archived content beyond reach) can't be erased. Manage them:
- **Operational habits**: don't post real-time location; delay travel/event posts until after; keep routine-revealing activity (fitness routes, check-ins) private; assume anything posted is permanent.
- **Security-question hygiene**: never use answers that are publicly discoverable (pet/school/street names surfaced in the audit) — use random stored answers.
- **Phishing readiness**: knowing which email/phone is exposed and in which breaches tells the subject what impersonation to expect — brief them on it.

---

## Monitoring (make the gains stick)

Exposure regrows; a one-time audit decays. Stand up detection:
- **Self-search alerts**: standing alerts on `"First Last"`, key handles, email, and phone, so new mentions surface fast.
- **Breach notifications**: subscribe each identifier to a breach-notification service for automatic future-breach alerts.
- **Broker re-check cadence**: brokers re-list — schedule a quarterly re-check of the removed listings (the opt-out tracker is the worklist).
- **Re-audit**: full re-run every 6–12 months, or before a high-exposure event (job change, media appearance, public role, litigation).
- **Automate it**: the `automation-pro:workflow-automation` skill can turn the self-search + broker re-check into a scheduled change-detection job that alerts only when something *new* appears — so monitoring costs the subject near-zero ongoing effort.

---

## Reporting the plan

Present remediation as an **ordered, checkable action list**, not prose:

```
☐ [P25 🔴] Remove Radaris listing — opt-out at <url> — verify re-search in 3 wks
☐ [P25 🔴] Rotate reused password (found in Breach X) + MFA on primary email — verify on HIBP
☐ [P20 🟠] Set social profile to private + strip city from bio — verify logged-out
☐ [P12 🟡] WHOIS privacy on personal domain — verify public lookup
...
☐ [ongoing] Quarterly broker re-check · breach alerts on 3 emails · re-audit <date>
```

Give the subject the plan and let them execute the sensitive steps themselves (account changes, legal requests). The audit's job is to hand them a map and a to-do list that measurably shrinks their attack surface — and to make the "after" verifiably smaller than the "before."
