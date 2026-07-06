---
name: web-automation
description: Driving real websites with a browser (Playwright) — navigating, logging in, filling forms, clicking through flows, extracting data from JS-rendered pages, taking screenshots, and testing web UIs. Use when the user asks to automate a website, interact with a page, fill/submit forms, check something on a site that requires rendering or login, monitor a page, or when plain HTTP fetching returns empty/JS-shell content.
---

# Web Automation

Drive websites the way a careful human does: observe the page, act on what is actually there, verify the result of every action. The #1 cause of broken automation is acting on assumptions about a page instead of its current reality.

Detailed selector/waiting/download patterns: `references/playwright-patterns.md`.

## Tool choice (cheapest that works)

1. **Plain HTTP** (`curl`, `requests`) — if the data is in the raw HTML or an API. Always check first: `curl -s URL | grep -i "<target text>"`. If present, you don't need a browser.
2. **The site's API** — open DevTools-style thinking: many "scraping" jobs are one `fetch` to the JSON endpoint the page itself calls. Check Network-visible endpoints, `/api/`, embedded `__NEXT_DATA__`/`window.__INITIAL_STATE__` JSON in the HTML.
3. **Playwright** — when content is JS-rendered, requires interaction, or needs login. Python (`playwright.sync_api`) or Node — match the project's language; default to Python scripts run from the shell.

Setup when needed: `pip install playwright` (browser binaries may already exist — try launching before installing browsers; in managed environments respect `PLAYWRIGHT_BROWSERS_PATH`).

## Core working loop

Write automation **incrementally, interactively** — never a 200-line script in one shot:

1. **Launch & look.** Navigate, then dump reality before acting:
   ```python
   page.goto(url, wait_until="domcontentloaded")
   page.screenshot(path="step1.png", full_page=True)   # look at it
   print(page.title(), page.url)
   ```
   Read the screenshot / `page.content()` — cookie banners, login walls, and redirects live here, and they arrive before your target element does.
2. **Act on one step**, verify, screenshot, then extend the script to the next step. Each action gets a verification that it *worked* (URL changed, element appeared, text updated) — not just that it didn't throw.
3. **Handle the interstitials first**: cookie/consent banners, newsletter modals, "select your region" — dismiss them with conditional clicks (`if page.locator(...).is_visible(): ...click()`) before the main flow.
4. When the flow works end-to-end, harden it: replace sleeps with condition waits, add per-step try/except with a screenshot on failure, make it idempotent (safe to rerun after partial completion).

## Selectors — in order of durability

1. `page.get_by_role("button", name="Submit")` — role + accessible name (survives redesigns)
2. `page.get_by_label("Email")`, `get_by_placeholder`, `get_by_text` — user-visible anchors
3. `[data-testid=…]` / stable ids
4. CSS by semantic class — last resort; **never** auto-generated classes (`css-1x2y3z`), positional (`div:nth-child(4)`), or long copied selector chains — they break on the next deploy.

## Waiting — the discipline

- Never `time.sleep()` / `waitForTimeout` in final code. Playwright auto-waits on actions; for state, wait on conditions:
  `expect(locator).to_be_visible()`, `page.wait_for_url("**/dashboard")`, `page.wait_for_load_state("networkidle")` (sparingly), or wait for the specific response: `page.expect_response(lambda r: "/api/orders" in r.url)`.
- Flakiness = a race you haven't named. Find what you're actually waiting for and wait for *that*.

## Logins & sessions

- Credentials come from env vars or the user — **never hardcode into scripts or commit them**.
- Log in once, persist state, reuse: `context.storage_state(path="auth.json")` → `browser.new_context(storage_state="auth.json")`. Keep `auth.json` out of git (add to `.gitignore`).
- 2FA/CAPTCHA: stop and hand control to the user (headed browser or asking them for the code). **Never attempt to bypass CAPTCHAs or bot walls** — if a site actively blocks automation, report it and propose the site's API or official export instead.

## Extraction from pages

- Scope then extract: `rows = page.locator("table#orders tbody tr")`, loop `rows.nth(i)`, read cells relative to the row — never absolute selectors per cell.
- Prefer intercepting the underlying JSON (`page.expect_response`) over parsing rendered DOM — it's typed, complete, and stable.
- Write results incrementally (JSONL/CSV as you go), so a crash at item 900 of 1000 doesn't lose everything.

## Etiquette & safety

- Respect the site: throttle (1–2 req/s unless told otherwise), identify honestly, stop on 429/403 and back off. Check `robots.txt` and ToS for scraping jobs; surface conflicts to the user rather than silently proceeding.
- Destructive/outward actions on real sites (submitting orders, sending messages, deleting data, posting publicly) — confirm with the user before the *first* execution, and build a `--dry-run` mode for bulk operations.
- Screenshots on every failure path (`page.screenshot(path=f"error-{step}.png")`) — they turn "it broke" into a one-look diagnosis.

## Debugging a broken flow

1. Rerun headed or grab the failure screenshot + `page.content()` snapshot.
2. Diagnose which reality changed: element renamed? new modal? redirect? A/B variant? rate-limited (check status codes)?
3. Fix the selector/wait at the point of divergence — don't add sleeps, don't add blanket retries around the whole script. Retry only idempotent single steps, with backoff, max 2–3 attempts.
