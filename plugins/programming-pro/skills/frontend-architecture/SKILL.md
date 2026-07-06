---
name: frontend-architecture
description: Structuring frontend/web applications well — component design, state management, data fetching, folder structure, performance, and framework patterns (React/Vue/Svelte/etc). Use when the user is building or refactoring a frontend, asks how to structure components or state, is dealing with prop-drilling/re-render/state-management problems, setting up a new frontend project, or making architectural decisions in a web app. Focuses on maintainable structure and correct state, not framework trivia.
---

# Frontend Architecture

Frontend complexity is mostly *state* complexity — where data lives, how it flows, and when things re-render. Get the state model and the component boundaries right and the app stays maintainable; get them wrong and no amount of clever code saves it. This skill is about those structural decisions, applicable across React/Vue/Svelte/Angular (examples lean React; principles are universal).

## Component design

- **Components have one responsibility.** A component that fetches data, manages form state, *and* renders a complex layout is three components. Split by responsibility, not by size.
- **Separate presentational from container/logic concerns.** "Dumb" components take props and render (reusable, testable, predictable); "smart" components/hooks hold state and data-fetching. This split makes the UI testable and the logic reusable.
- **Compose, don't configure.** A component with 15 boolean props (`isPrimary`, `isLarge`, `hasIcon`…) should be several components or use composition (children/slots). Prefer composition over a mega-component with a config object.
- **Props flow down, events flow up.** Keep data flow unidirectional and predictable. When prop-drilling gets deep (passing props through 4 layers that don't use them), that's the signal to lift state to context or a store — not to keep threading.
- **Keep components pure where possible**: same props → same render, side effects isolated (in effects/lifecycle, not in render).

## State — the core decision

Choose the *right kind of state in the right place*. Most frontend messes come from putting state in the wrong scope. Categorize every piece of state:

1. **Local UI state** (is this dropdown open, form input value) → keep it *local* to the component. Don't hoist it to a global store; that's the most common over-engineering.
2. **Shared client state** (current user, theme, cross-page UI) → lift to context or a lightweight store (Zustand, Pinia, Svelte stores). Reach for a store only when multiple distant components need the same state.
3. **Server state / cached data** (data from an API) → **this is not the same as client state, and treating it as such is the #1 frontend mistake.** Use a data-fetching/caching library (TanStack Query, SWR, RTK Query) that handles caching, revalidation, loading/error states, and staleness for you. Don't hand-roll `useEffect` + `useState` fetching with manual loading flags — you'll reimplement caching badly.
4. **URL state** (filters, current tab, pagination) → put it in the URL where it belongs, so it's shareable, bookmarkable, and survives refresh.
5. **Form state** → use a form library for anything nontrivial (validation, errors, submission) rather than wiring dozens of controlled inputs by hand.

Guiding rule: **keep state as local as possible, lift only when genuinely shared, and never conflate server data with client state.** Global-everything and prop-drill-everything are the two opposite failure modes; the truth is per-piece placement.

## Data fetching

- Handle the full lifecycle every time: loading, error, empty, and success — not just the happy path. A screen that shows nothing on error or spins forever on empty is a bug.
- Fetch at the right level; avoid waterfalls (sequential dependent fetches that could be parallel). Colocate data needs with the components that use them.
- Cache and revalidate (the query libraries do this) rather than refetching everything on every navigation.
- Optimistic updates for snappy UX where safe, with rollback on failure.

## Project structure

- **Organize by feature/domain, not by file type** for anything beyond a small app. `features/checkout/{components,hooks,api}` scales; a giant flat `components/` + `hooks/` + `utils/` with 200 files each does not — related code should live together.
- Shared/reusable primitives in a `shared` or `ui` layer; feature code imports from shared, not from sibling features (keep feature boundaries clean to avoid a tangle).
- Consistent conventions (naming, file layout, where types live) — a new contributor should predict where a file is.

## Performance (measure first — see performance-optimization)

Common frontend wins, applied after profiling, not preemptively:
- **Unnecessary re-renders**: memoize expensive components/values where the profiler shows churn; stabilize callback/object props; but don't `memo` everything reflexively — premature memoization adds noise and its own bugs.
- **Bundle size**: code-split by route (lazy-load), tree-shake, watch heavy dependencies (a date library or icon set can dwarf your app). Analyze the bundle.
- **Rendering long lists**: virtualize (windowing) lists of hundreds+ items.
- **Loading**: lazy-load below-the-fold, optimize images (right size/format, lazy), minimize render-blocking resources; measure Core Web Vitals.
- Perceived performance: skeletons/optimistic UI over spinners; don't block the whole page on one slow request.

## Cross-cutting

- **Accessibility is architecture, not polish** — semantic HTML, keyboard support, and ARIA where needed must be built in from the start (see the `accessibility` skill). Retrofitting it is far more expensive.
- **Type safety** (TypeScript): type the props, the API responses, the state. It catches a whole class of frontend bugs at build time.
- **Error boundaries** so one component's crash doesn't blank the whole app; graceful degradation.
- Keep business logic out of components where it can be plain testable functions/hooks.

## Deliverable

For a structure/architecture task: the component breakdown (responsibilities and boundaries), the state plan (each piece categorized and placed per the rules above), the data-fetching approach, and the folder structure — with the reasoning tied to how the app will grow. For a refactor: identify which failure mode is present (misplaced state, god-components, prop-drilling, server-state-as-client-state) and the incremental path out (pairs with `safe-refactoring`).

## Rules

- Categorize and place each piece of state; keep it as local as possible; never treat server data as client state.
- One responsibility per component; compose over configure; data down, events up.
- Handle loading/error/empty/success for every data dependency.
- Organize by feature at scale; keep feature boundaries clean.
- Optimize only what you've measured; build accessibility and types in from the start.
