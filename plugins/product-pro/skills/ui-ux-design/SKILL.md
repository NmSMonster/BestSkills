---
name: ui-ux-design
description: Designing usable, well-structured interfaces and user experiences — user flows, layout, visual hierarchy, interaction patterns, forms, and usability principles. Use when the user asks to design a UI/UX, improve a confusing interface, design a screen/flow/form, critique a design's usability, choose a UX pattern, or make something more intuitive. Grounded in usability heuristics and the user's goal, not decoration or trends.
---

# UI/UX Design

Good design is not how it looks — it's how well it lets a user accomplish their goal with the least friction and confusion. A beautiful interface that users can't figure out is a failed design; a plain one they breeze through is a success. Design the *experience* (the flow, the clarity, the reduction of effort) first; the visual polish serves it.

## Step 0 — User, goal, context

Before designing a pixel: **who** is the user, **what** are they trying to accomplish, and **in what context** (rushed, mobile, first-time, expert, stressed)? Design for their goal and mental model, not for the org chart or the database schema. The most common design failure is exposing the system's structure instead of the user's task.

## The flow before the screens

Design the **user flow** first — the sequence of steps to complete the goal — then the screens that serve it. 
- Map the path: entry → steps → success. Count the steps and cut every one you can (each step loses users). The best flow for "the user does X" is the one with the fewest decisions and least effort.
- Handle the unhappy paths: errors, empty states, edge cases, interruptions. A flow that only works when everything goes right isn't designed.
- Design the **first-run / empty state** deliberately — it's the user's first impression and where they learn the product; a blank screen with no guidance loses people at the start.

## Usability heuristics (the checklist good design passes)

Nielsen's heuristics, condensed to what to actually check:
1. **Visibility of system status** — always show what's happening: loading, saved, progress, current location. Never leave the user wondering if their click worked.
2. **Match the user's world** — use their language and concepts, not internal jargon or DB field names. Real-world metaphors where they help.
3. **User control & freedom** — undo, back, cancel, escape. Users make mistakes; let them recover without dread. No dead ends.
4. **Consistency & standards** — same thing looks/behaves the same everywhere; follow platform conventions (users spend most of their time in *other* apps and bring those expectations). Don't reinvent standard controls.
5. **Error prevention** — better than error messages. Constrain inputs, confirm destructive actions, use sensible defaults, make invalid states impossible (disable rather than allow-then-scold).
6. **Recognition over recall** — show options rather than making users remember them; keep needed info visible; don't force memory across steps.
7. **Flexibility** — shortcuts for experts, guidance for novices; both can use it.
8. **Aesthetic & minimalist** — every extra element competes for attention. Remove what isn't needed. Clarity comes from *less*.
9. **Good error messages** — plain language, say what went wrong and how to fix it, no codes or blame.
10. **Help** — ideally the UI needs none, but provide it where tasks are complex, in context.

## Visual hierarchy & layout

Guide the eye to what matters, in order of importance:
- **Hierarchy**: size, weight, color, contrast, and position signal importance. The most important thing (the primary action, the key info) should be the most prominent; secondary things recede. If everything shouts, nothing is heard.
- **One primary action per screen**, visually dominant. Secondary actions are visibly subordinate; destructive actions are separated and de-emphasized (and confirmed).
- **Whitespace** is not wasted space — it groups related things, separates unrelated ones, and gives the eye rest. Cramped UIs read as complex and stressful.
- **Grouping & proximity**: related elements close together, unrelated apart (Gestalt). Structure reflects meaning.
- **Alignment & consistency**: a consistent grid, spacing scale, and type scale make an interface feel calm and trustworthy; misalignment reads as broken.
- **Scannability**: people scan, not read. Clear headings, short chunks, obvious structure. Front-load the important.

## Forms (the most-used and most-abused UI)

- Only ask what you need — every field costs completion. Cut optional fields ruthlessly.
- One column, logical order, grouped sections. Labels above fields (not placeholder-as-label — it vanishes).
- Inline validation with helpful, specific errors at the field; show requirements up front, not after failure.
- Sensible defaults, smart input types (right keyboard on mobile, date pickers), forgiving formats (accept the phone number however they type it).
- Show progress for multi-step; let users save/resume long forms.

## Interaction & feedback

- Every action gets immediate feedback (visual state change, confirmation) — the user must know it registered.
- Affordances: things that are clickable *look* clickable; things that aren't, don't. Buttons look like buttons.
- Respect loading: skeletons/optimistic UI over blank screens or endless spinners; keep the user informed on anything slow.
- Motion with purpose (guide attention, show relationships), never gratuitous; respect reduced-motion.

## Accessibility & responsiveness are part of UX, not extras

- Design accessible from the start (see the `accessibility` skill): contrast, keyboard, screen readers, not-color-alone. An inaccessible design is an unusable design for many.
- Design responsive: the experience must work on the screens users actually use. Design mobile constraints early — they force the clarity that helps every screen size.

## Deliverable

For a design task: the user flow, then the screen/layout described (structure, hierarchy, primary action, states including empty/error/loading), the interaction and feedback, and the reasoning tied to the user's goal and the heuristics. Wireframe-level structure and rationale — not a color-picking exercise unless asked. For a critique: identify which heuristics the design violates and the user impact, prioritized by how much they hurt the goal, each with a concrete fix.

## Rules

- Design the flow and the user's goal first; visuals serve usability, not the reverse.
- Reduce steps, choices, and elements — friction and clutter are the enemies.
- One clear primary action per screen; consistent, conventional patterns; visible system status always.
- Design every state (empty, loading, error, success), not just the happy path.
- Prevent errors over explaining them; write human error messages; make recovery easy.
- Accessibility and responsiveness are requirements of good UX, not add-ons.
