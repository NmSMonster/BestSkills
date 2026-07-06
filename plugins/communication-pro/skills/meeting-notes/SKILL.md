---
name: meeting-notes
description: Turning a meeting transcript, recording, or rough notes into structured output people actually use — decisions, action items with owners, and a scannable summary. Use when the user gives you a transcript/notes and wants a summary, minutes, action items, or follow-up; or wants help preparing an agenda. Optimizes for decisions and accountability, not a verbatim retelling.
---

# Meeting Notes

Meeting notes have one job: make sure the decisions and commitments survive the meeting. Nobody re-reads a wall of "then Alice said, then Bob said." The valuable output is **what was decided, who owns what by when, and what's still open** — everything else is compression fodder.

## The extraction priority

From any transcript or rough notes, pull these four things in order of value:

1. **Decisions** — what was actually decided (and by whom, if it matters). The single most-lost artifact from meetings. State each as a clear resolution: "Decided: ship with Postgres, not Mongo — [reason]." If a decision was implied but never made explicit, flag it: "Seemed agreed but not confirmed: …".
2. **Action items** — every commitment, as `owner → task → due date`. An action item without an owner is a wish; without a date, it's a someday. If the transcript didn't assign an owner or date, mark it `[owner?]` / `[date?]` so the user chases it — don't silently drop it.
3. **Open questions / blockers** — unresolved issues, disagreements parked for later, dependencies. These are what the next meeting is for; surfacing them prevents the "wait, didn't we need to figure out X?" three weeks later.
4. **Key context / discussion** — the *why* behind decisions, and important information shared. Compressed hard — the reasoning that a future reader needs, not the play-by-play.

## Deliverable format

```
# <Meeting> — <date>
Attendees: … · Purpose: one line

## TL;DR
2–4 sentences: what was decided and what happens next. The part most people read.

## Decisions
- **Decided:** <decision> — <one-line rationale> (<who>, if relevant)

## Action items
| Owner | Action | Due |
|-------|--------|-----|
| Alice | Draft the migration plan | Fri Jul 11 |
| [?]   | Confirm budget with finance | [date?] |

## Open questions / blockers
- <unresolved item> — <who's affected / what it's waiting on>

## Notes (context)
Compressed discussion, grouped by topic — the reasoning worth keeping.
```

Put the TL;DR and action items at the **top** — they're what gets read and acted on. Bury nothing that requires action.

## Working method

- **Attribute decisions and actions**, summarize discussion. Who *decided* and who *owns* matters; who said each sentence in the debate usually doesn't.
- **Group by topic, not chronology.** A meeting that jumped between three subjects should produce three clean sections, not a timeline. Readers think in topics.
- **Distinguish decided / discussed / deferred.** "We talked about X" is not "we decided X." Precision here prevents people acting on a non-decision or ignoring a real one.
- **Neutral and accurate.** Don't editorialize or soften a hard decision. If there was genuine disagreement, note that it was contested and how it resolved — that context matters later.
- **Flag the gaps.** Missing owners, vague dates, decisions that seemed unfinished — surface them as `⚠` so the user can close them, rather than producing tidy notes that hide the loose ends.
- **Keep names/quotes only where they carry weight** (a commitment, a key rationale, a specific concern raised). Strip the rest.

## If asked to prepare (not just summarize)

**Agenda**: for each item — topic, desired outcome (decide / discuss / inform), owner, time box. An agenda whose items don't have a *desired outcome* produces a meeting with no decisions. Send pre-reads so the meeting is for deciding, not for reading.

**Pre-meeting brief**: the decision(s) needed, the options, and the info required to decide — so the meeting converges instead of wandering.

## Rules

- Never invent an action item, owner, or decision that isn't in the source. If it's ambiguous, mark it ambiguous — fabricated accountability is worse than a flagged gap.
- Compression is the value: a good summary is a fraction of the transcript. If your notes are as long as the meeting, you've transcribed, not summarized.
- Preserve exact numbers, dates, names, and commitments verbatim; compress the connective discussion freely.
- If the transcript is unclear on something load-bearing (who owns a critical action), say so explicitly rather than guessing.
