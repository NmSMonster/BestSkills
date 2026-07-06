---
name: presentation-builder
description: Structuring talks and presentations that hold attention and land a point — narrative arc, slide design, and speaker delivery. Use when the user asks to build a presentation/talk/deck (non-investor; for investor decks use business-pro:pitch-deck), structure a talk, turn a document into slides, design slides that aren't bullet-walls, or prepare to present. Focuses on the argument and the audience, not decoration.
---

# Presentation Builder

A presentation is a *spoken argument with visual support* — not a document read aloud, and not slides that duplicate your speech. Most presentations fail because they're bullet-walls the presenter reads while the audience disengages. The fix: design the narrative first, then make slides that show what words can't.

(For fundraising/investor decks, use `business-pro:pitch-deck` — different genre with its own conventions.)

## Step 0 — Audience and the one takeaway

Before any slide: **who's in the room**, what they know, what they care about — and the **single sentence** you want them repeating afterward. If the audience remembers one thing, what is it? Everything serves that sentence or gets cut. A talk with three "main points" has none.

## Step 1 — Narrative before slides

Design the *argument*, not the deck. Talks that land follow a tension→resolution arc, not a topic list:
- **Hook** — open with a reason to care: a surprising fact, a sharp question, a concrete story, the stakes. Never open with "agenda" and "about me" — you have 30 seconds of attention; spend them on why this matters to *them*.
- **Tension** — the problem, gap, or question. Make the audience feel it before you resolve it. This is what keeps them listening.
- **Resolution** — your answer/insight/solution, built in logical steps, each earning the next.
- **Payoff** — the takeaway and the "so what / now what." End on the one sentence and a clear next step, not "any questions?" trailing off.

Write this as a sentence outline first (the talk track), get the arc right, *then* build slides. The slides serve the narrative; the narrative never serves the slides.

## Step 2 — Slides that help, not compete

The cardinal rule: **the audience can either read your slide or listen to you — not both.** So the slide must not duplicate your words.
- **One idea per slide.** If a slide has two messages, it's two slides. The headline states the *point* ("Latency dropped 60% after caching"), not the topic ("Performance").
- **Show, don't list.** Replace bullet-walls with: a chart that makes the trend obvious, a diagram of the system, one big number, a photo, a before/after. Visuals carry what prose can't; that's the entire reason for slides.
- **Minimal text.** A few words as an anchor, not sentences you'll read. If you need a paragraph, it belongs in a handout, not on screen. Kill the sub-sub-bullets.
- **Big and legible.** Large type (readable from the back), high contrast, one accent color, generous whitespace. The person in the last row is your design constraint.
- **Data slides** follow the `dataviz` skill: honest axes, the right chart, one message per chart, labeled directly. A chart the audience can't read in five seconds has failed.
- **Progressive reveal** for complex ideas — build a diagram piece by piece rather than dropping a finished tangle they'll read instead of listening.

## Step 3 — Delivery (the slides are half the talk)

- **Slides support you; you carry the content.** Never read them. The speaker notes hold what you *say* — which is richer than what's shown.
- **Signpost**: tell them the structure, mark transitions ("That's the problem — here's what we did"). Audiences follow a talk they can navigate.
- **One rehearsal changes everything** — run it out loud, time it, cut what drags. Most talks are too long; leave room to breathe and for questions.
- **Anticipate the top questions** and have backup slides in an appendix for the ones you can answer with a visual.
- Open strong, close on the takeaway. The first and last 30 seconds are what they remember — script those two verbatim even if nothing else.

## Deliverable

Depending on what the user needs:
- **Outline** — the narrative arc as a slide-by-slide sentence outline (headline + what each slide shows + speaker-note gist). Get this approved before building.
- **Slides** — Markdown (for Marp/reveal.js/Slidev), an HTML deck, or pptx structure. Each slide: point-headline, the one visual/idea, minimal anchor text, and speaker notes with the actual talk track.
- **Speaker notes** — per slide, what to *say* (more than what's shown), transitions, and timing.

## Quality bar

- [ ] There's one takeaway sentence, and the whole talk drives to it.
- [ ] The deck follows a tension→resolution arc, not a topic list.
- [ ] No slide is a bullet-wall the presenter would read aloud; each has one point-headline and shows more than it says.
- [ ] Data slides are honest and readable in five seconds.
- [ ] The open earns attention in 30 seconds; the close lands the takeaway + next step.
- [ ] Content lives in the speaker notes, not crammed on the slides.
