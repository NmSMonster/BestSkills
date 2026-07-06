---
name: financial-model
description: Building driver-based financial models — revenue projections, unit economics (CAC/LTV/margins), P&L, cash-flow and runway, break-even, scenarios, and SaaS/e-commerce/services metrics. Use when the user asks for financial projections, a budget model, pricing analysis, burn/runway calculation, "can this business make money", or a spreadsheet model for a plan or pitch.
---

# Financial Model

A financial model is a calculator for decisions, not a prophecy. Its worth is the clarity of its assumptions and the ease of changing them. **Drivers → calculations → outputs**, strictly separated: every number is either an input someone can defend or a formula anyone can audit. A hardcoded number inside a formula is a landmine.

## Architecture (any tool)

Build in a spreadsheet (xlsx via openpyxl, or Google-Sheets-ready CSV) unless the user prefers code (then: a Python model that *exports* to xlsx — decision-makers live in spreadsheets).

Three layers, three tabs/sections, color-coded by convention (inputs blue, formulas black):
1. **Assumptions** — every driver, one place: value, unit, source/rationale next to each ("€49/mo — current pricing page"; "3% MoM churn — industry benchmark for SMB SaaS, unvalidated ⚠").
2. **Model** — monthly time series (months as columns), formulas referencing only assumptions and prior periods. Monthly for 24–36 months; annual summaries derived, never modeled directly.
3. **Outputs** — the dashboard: revenue, gross margin, EBITDA/net, cash balance, runway, break-even month, headline unit economics, scenario table.

## Revenue: model the engine, not the curve

Never type a revenue line that grows X%/month — model *how* revenue is generated:

- **SaaS/subscription**: `new customers (by channel: spend ÷ CAC, or funnel: traffic × conversion) → +adds −churn → ending customers × ARPU`. Track MRR movements (new/expansion/churned). Cohort logic if retention varies by age.
- **E-commerce/transactional**: `sessions × conversion × AOV`, minus returns; repeat-purchase rate drives the second year.
- **Services**: `billable people × utilization × rate × hours` — capacity-constrained, so hiring plan drives revenue.
- **Marketplace**: `transactions × take rate`, with both sides' acquisition modeled.

Growth then emerges from drivers (marketing spend, sales hires, conversion) — which is exactly what makes the model answer questions ("what if CAC rises 30%?").

## Costs

- **COGS/variable** (scale with revenue): hosting per user, payment fees (~2–3%), support per customer, shipping/materials. → **Gross margin**; sanity-check vs. sector norms (SaaS 70–85%, e-comm 25–50%, services 30–60%) and explain deviations.
- **Opex (mostly headcount)**: model people individually or by role×month with fully-loaded cost (salary × 1.2–1.35 for taxes/benefits/tools — country-dependent; for Poland use ~×1.2 on UoP gross). Hiring tied to triggers ("support hire per 500 customers"), not dates pulled from air.
- **Timing ≠ P&L**: cash-flow needs payment terms (B2B invoices paid in 30–60 days, annual prepays, inventory bought ahead of sales, VAT flows). Cash kills companies that are profitable on paper — model the **cash line and its trough**; runway = cash ÷ current net burn, and funding need = |trough| × 1.3–1.5 buffer.

## Unit economics (compute, don't assert)

- **Contribution margin** = price − variable cost per unit.
- **CAC** = fully-loaded acquisition cost ÷ new customers, *per channel* — blended CAC hides dying channels.
- **LTV** = contribution margin per customer per month ÷ monthly churn (or cohort-based if you have data). State the churn source.
- Health gates: **LTV:CAC ≥ 3** (with *honest* LTV), **CAC payback < 12–18 months** (B2B) / < 6 (B2C). Failing gates is a finding to report, not to massage: say which driver must move how far to pass.

## Scenarios & sensitivity

- Three scenarios — **base / downside / upside** — varying only the 3–5 real uncertainty drivers (growth, churn, CAC, pricing), not everything. Downside = "channels underperform 40%, churn +50%": show runway impact.
- **One-way sensitivity** on each key driver (±20%) → rank by impact on cash/profit. The top-2 drivers are where the user should spend validation effort — say so explicitly.

## Sanity-check battery (run before delivering)

- [ ] Cross-foots: customers × ARPU ≈ revenue; headcount × cost ≈ payroll; cash flow ties to P&L − timing items.
- [ ] No hardcodes inside formulas (spot-check by changing an assumption → outputs move).
- [ ] Implied endpoints pass the laugh test: year-3 market share vs. SOM, revenue per employee (typ. €100–300k), support load per agent.
- [ ] Growth % declines as base grows (constant high %-growth forever = red flag).
- [ ] Every assumption labeled: validated / benchmark / guess ⚠.

## Deliverable

The model file + a one-page memo: headline outputs (revenue Y1–3, break-even month, cash trough & funding need, LTV:CAC), the 3 assumptions that matter most and their validation status, scenario table, and what the model says about the decision at hand. Never hand over a spreadsheet without the memo — models don't speak for themselves.
