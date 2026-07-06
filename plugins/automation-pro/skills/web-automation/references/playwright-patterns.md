# Playwright Patterns Reference

Copy-adapt snippets for common situations. Python `sync_api` shown; Node equivalents are mechanical.

## Skeleton (script you can grow)

```python
import sys
from playwright.sync_api import sync_playwright, expect

def run(step_dir="steps"):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        ctx = browser.new_context(viewport={"width": 1366, "height": 900})
        page = ctx.new_page()
        page.set_default_timeout(15_000)
        try:
            page.goto("https://example.com", wait_until="domcontentloaded")
            # ... steps ...
        except Exception:
            page.screenshot(path="error.png", full_page=True)
            print(f"URL at failure: {page.url}", file=sys.stderr)
            raise
        finally:
            ctx.close(); browser.close()

if __name__ == "__main__":
    run()
```

## Consent banners / modals (conditional dismiss)

```python
for sel in ['button:has-text("Accept all")', '[aria-label="Close"]', '#onetrust-accept-btn-handler']:
    loc = page.locator(sel).first
    if loc.is_visible():
        loc.click()
        break
```

## Login with persisted session

```python
import os, pathlib
AUTH = "auth.json"

def ensure_login(p):
    browser = p.chromium.launch(headless=True)
    if pathlib.Path(AUTH).exists():
        ctx = browser.new_context(storage_state=AUTH)
        page = ctx.new_page(); page.goto("https://app.example.com/dashboard")
        if "login" not in page.url:           # session still valid
            return browser, ctx, page
        ctx.close()
    ctx = browser.new_context(); page = ctx.new_page()
    page.goto("https://app.example.com/login")
    page.get_by_label("Email").fill(os.environ["APP_EMAIL"])
    page.get_by_label("Password").fill(os.environ["APP_PASSWORD"])
    page.get_by_role("button", name="Sign in").click()
    page.wait_for_url("**/dashboard")
    ctx.storage_state(path=AUTH)              # gitignore this file
    return browser, ctx, page
```

## Waiting on the real condition

```python
# navigation settled on the page you expect
page.wait_for_url("**/orders/**")

# element state
expect(page.get_by_role("alert")).to_contain_text("Saved")

# the API call behind the UI (best for data readiness)
with page.expect_response(lambda r: "/api/search" in r.url and r.status == 200) as resp:
    page.get_by_role("button", name="Search").click()
data = resp.value.json()
```

## Tables & lists (row-scoped extraction)

```python
rows = page.locator("table#orders tbody tr")
out = []
for i in range(rows.count()):
    row = rows.nth(i)
    out.append({
        "id":     row.locator("td").nth(0).inner_text().strip(),
        "status": row.locator("td").nth(2).inner_text().strip(),
    })
```

## Pagination (stop conditions that don't lie)

```python
while True:
    harvest(page)
    nxt = page.get_by_role("link", name="Next")
    if not nxt.is_visible() or nxt.is_disabled():
        break
    first_id = page.locator("tr td").first.inner_text()
    nxt.click()
    expect(page.locator("tr td").first).not_to_have_text(first_id)  # page actually changed
```

## Infinite scroll

```python
prev = -1
while True:
    n = page.locator(".item").count()
    if n == prev:
        break
    prev = n
    page.mouse.wheel(0, 4000)
    page.wait_for_timeout(500)   # acceptable in scroll probing only
```

## Downloads & uploads

```python
with page.expect_download() as dl:
    page.get_by_role("button", name="Export CSV").click()
dl.value.save_as("export.csv")

page.locator('input[type="file"]').set_input_files("report.pdf")
```

## New tab / popup

```python
with ctx.expect_page() as new_page_info:
    page.get_by_role("link", name="Open report").click()
report = new_page_info.value
report.wait_for_load_state()
```

## iframes

```python
frame = page.frame_locator('iframe[title="payment"]')
frame.get_by_label("Card number").fill("4242 4242 4242 4242")
```

## Embedded state instead of DOM scraping

```python
import json, re
html = page.content()
m = re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', html, re.S)
if m:
    state = json.loads(m.group(1))   # full typed data, no selectors needed
```

## Screenshot-per-step trail

```python
STEP = 0
def snap(page, name):
    global STEP; STEP += 1
    page.screenshot(path=f"steps/{STEP:02d}-{name}.png", full_page=True)
```

## Blocking noise for speed (careful: some sites need CSS for visibility checks)

```python
ctx.route("**/*.{png,jpg,jpeg,woff2,mp4}", lambda r: r.abort())
```

## Common failure signatures

| Symptom | Likely cause | Fix |
|---|---|---|
| `TimeoutError` on click | wrong selector, element in iframe, covered by modal | screenshot + `page.content()`, check iframes/modals |
| Empty extraction, works in real browser | content behind XHR you didn't wait for | `expect_response` on the data call |
| Works headed, fails headless | viewport-dependent layout, bot detection | set realistic viewport/UA; if bot wall → stop, use API |
| Flaky every ~5th run | race on navigation or animation | wait on URL/response/state, not time |
| Logged out mid-run | session expiry | re-run `ensure_login` on detection, refresh `auth.json` |
