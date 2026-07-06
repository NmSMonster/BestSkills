---
name: accessibility
description: Making web interfaces usable by everyone, including people with disabilities — semantic HTML, keyboard navigation, screen readers, ARIA, color contrast, and WCAG compliance. Use when the user asks to make something accessible, fix a11y issues, meet WCAG/ADA/Section 508 requirements, audit for accessibility, add keyboard/screen-reader support, or review UI for inclusivity. Accessibility is a requirement and often a legal one, not an optional nicety.
---

# Accessibility (a11y)

Accessibility means people with disabilities — visual, motor, auditory, cognitive — can actually use what you build. It's a requirement, frequently a legal one (ADA, Section 508, EN 301 549, WCAG), and it improves usability for *everyone* (keyboard users, mobile, bright sunlight, temporary injuries). The standard is **WCAG 2.1/2.2 Level AA**. The good news: most accessibility comes free from doing HTML correctly — the expensive part is retrofitting it later, so build it in.

## The foundation — semantic HTML (90% of accessibility)

The single highest-leverage practice: **use the right HTML element for the job.** Semantic elements come with accessibility built in — for free — that you'd otherwise have to reconstruct with ARIA and JS (badly).
- `<button>` for actions, `<a href>` for navigation — **not** `<div onclick>`. A real button is focusable, keyboard-activatable, and announced as a button automatically; a clickable div is none of those without a pile of ARIA and handlers.
- `<nav>`, `<main>`, `<header>`, `<footer>`, `<aside>` landmarks so screen-reader users can jump between regions.
- Headings (`<h1>`–`<h6>`) in a **logical, non-skipping hierarchy** — screen-reader users navigate by headings; they're the table of contents.
- `<label>` associated with every form input; `<ul>/<ol>` for lists; `<table>` with `<th>` for tabular data; `<fieldset>/<legend>` for grouped controls.
- The rule: **reach for ARIA only when semantic HTML can't express it.** "No ARIA is better than bad ARIA" — incorrect ARIA actively breaks the experience. Native elements first.

## Keyboard accessibility

Everything must work without a mouse — motor-impaired users, power users, and screen-reader users all navigate by keyboard.
- **Every interactive element is focusable and operable by keyboard** (Tab to reach, Enter/Space to activate). Native elements do this free; custom widgets need `tabindex`, key handlers, and correct roles.
- **Visible focus indicator** — never `outline: none` without a clear replacement. Users must see where they are.
- **Logical focus order** matching visual order (don't let it jump around).
- **No keyboard traps** — focus can always move on. For modals: trap focus *inside while open*, return it to the trigger on close, and close on Escape.
- Provide a **skip-to-content** link so keyboard users can bypass repeated nav.

## Screen readers & ARIA

- **Images**: meaningful `alt` text describing the content/purpose; empty `alt=""` for decorative images (so they're skipped). An image conveying info with no alt is invisible to blind users.
- **Accessible names** for every control: buttons with only an icon need an `aria-label` ("Close", "Search"). A screen reader announcing "button" with no name is useless.
- **Dynamic updates**: content that changes without a page load (notifications, live results, errors) needs `aria-live` regions so screen readers announce them — otherwise the change is silent.
- **State**: `aria-expanded`, `aria-selected`, `aria-checked`, `aria-disabled` on custom widgets so their state is conveyed. Keep ARIA state in sync with reality.
- **Roles** only when building a non-native widget (`role="dialog"`, `role="tab"`) — and then implement the *full* expected keyboard interaction pattern for that role (the WAI-ARIA Authoring Practices define them). A `role` without its interaction contract is a lie to the screen reader.

## Visual & cognitive

- **Color contrast**: text meets WCAG AA — **4.5:1** for normal text, **3:1** for large text and UI components/icons. Check it with a contrast tool; low-contrast "elegant" grey-on-white fails real users.
- **Don't convey information by color alone** — a red/green status needs a label or icon too (color-blind users). Error states need text, not just a red border.
- **Text resizes** to 200% without breaking layout; use relative units; don't disable zoom.
- **Respect `prefers-reduced-motion`** — cut animation for users who get motion sickness/vestibular issues.
- **Clear labels, error messages, and instructions** (cognitive accessibility); don't rely on placeholder text as the only label (it vanishes on input and often fails contrast).
- **Touch targets** large enough (~44px) and spaced.

## Forms (where accessibility most often breaks)

- Every input has a associated `<label>` (not just a placeholder).
- Errors: identified in text, associated with the field (`aria-describedby`), announced (live region), and not conveyed by color alone. Tell the user *what's wrong and how to fix it*.
- Required fields marked accessibly; grouped controls (radios) in a `<fieldset>`.

## Testing (don't guess — verify)

Accessibility must be tested, and automated tools catch only ~30–40%:
1. **Automated**: run axe DevTools / Lighthouse / WAVE — catches contrast, missing alt/labels, ARIA misuse. Necessary, not sufficient.
2. **Keyboard**: unplug the mouse. Tab through the whole flow — can you reach and operate everything, is focus visible, order logical, no traps, modals behave?
3. **Screen reader**: test with a real one (VoiceOver on Mac/iOS, NVGA/NVDA on Windows, TalkBack on Android) — is everything announced with a name, role, and state? This catches what automation can't.
4. **Zoom to 200% and check contrast**; test with reduced-motion on.

## Deliverable

For a build: accessible semantic markup with keyboard support and correct names/roles from the start. For an audit: findings prioritized by impact (blockers that make something *unusable* — unreachable controls, unlabeled inputs, keyboard traps — before minor contrast misses), each with the WCAG criterion, who it affects, and the fix. Note the coverage — what you tested (automated/keyboard/screen reader) and what you didn't.

## Rules

- Semantic HTML first; ARIA only when necessary and then complete/correct (bad ARIA is worse than none).
- Everything keyboard-operable with visible focus and no traps.
- Every image has appropriate alt; every control has an accessible name; every input has a label.
- Contrast meets AA; never convey meaning by color alone.
- Test with keyboard and a screen reader, not just an automated scan — automation misses most of it.
- Build it in from the start; retrofitting accessibility is far more expensive and worse.
