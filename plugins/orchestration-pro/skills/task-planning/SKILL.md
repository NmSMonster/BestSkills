---
name: task-planning
description: Planning and decomposing a complex, multi-step, or ambiguous task before executing — scoping, sequencing, identifying unknowns, deciding what to do yourself vs. delegate, and when to check with the user. Use when a request is large, vague, spans multiple steps or files, has unclear requirements, or when jumping straight to code would risk building the wrong thing. The meta-skill that decides how every other skill gets applied.
---

# Task Planning

The difference between a capable assistant and a beast is not raw skill — it's knowing *what to do in what order*, *what to figure out before starting*, and *when to stop and ask*. This skill runs before execution on any nontrivial task. Time spent planning is repaid many times over in work not thrown away.

## When to plan (and when not to)

- **Plan** when: the task is multi-step, touches many files/systems, has ambiguous requirements, is irreversible/expensive, or you notice yourself unsure where to start. 
- **Skip straight to doing** when: the task is small, clear, and reversible. Over-planning a one-line fix is its own failure — planning is a tool, not a ritual.
- The tell that you *should* have planned: you're deep in execution and realize you're building the wrong thing, or you've hit the third "oh wait, I also need to…". Stop and plan then.

## Step 1 — Understand before decomposing

Most failed tasks fail here — solving the wrong problem well.
- **Restate the goal** in your own words: what does *done* look like, observably? What decision or outcome does this serve? If you can't state the success condition, you're not ready to plan.
- **Surface the ambiguities.** List what's unclear or assumed. For each: can you resolve it by reading the code/context/docs yourself, or does only the user know? Resolve everything you can yourself first — don't outsource thinking you can do.
- **Find the constraints**: existing conventions, dependencies, non-negotiables, things you must not break. In a codebase, read before you plan — the right plan depends on what's already there.

## Step 2 — Decompose

Break the goal into steps that are each small, verifiable, and ordered by dependency:
- **Each step has an observable done-condition** ("endpoint returns 201 with the created object"), not a vague verb ("implement the API"). If a step can't be verified, it's too big or too vague — split it.
- **Sequence by dependency and by risk.** Do the step that *unblocks the most* and the step that *resolves the biggest unknown* early — you want to discover "this approach won't work" on day one, not day three. Front-load the risky/uncertain part (a spike, a proof-of-concept) before the bulk work that depends on it.
- **Identify the critical path** vs. parallelizable work.
- **Name the unknowns as their own steps** ("investigate whether library X supports Y"). An unknown is not a task you can estimate; it's a question you must answer first.

## Step 3 — Decide what to do yourself vs. delegate

For each chunk of work, pick the right executor:
- **Do it inline** when it needs the context you already have, is quick, or requires your judgment throughout.
- **Delegate to a subagent** (where available) when: it's a broad, self-contained search/investigation ("find everywhere X is used"), it's parallelizable independent work, or it would flood your context with detail you only need the conclusion of. A subagent starts cold — only delegate work that can be specified completely up front and whose *result* is what you need, not the process.
- **Don't delegate** work that needs the conversation's evolving context, tight back-and-forth, or decisions only you're positioned to make. The cost of a cold hand-off exceeds the benefit for tightly-coupled work.
- Match specialized work to the right **skill**: a debugging step invokes `systematic-debugging`, a schema step invokes `database-design`. Planning is partly routing to the right method.

## Step 4 — Decide when to check with the user

Calibrate this well — asking too much is annoying, asking too little builds the wrong thing:
- **Proceed without asking**: reversible actions that clearly follow from the request; obvious-default choices (mention them, don't ask).
- **Ask first**: genuine forks where the answer changes the whole approach and you can't infer it; irreversible/destructive/outward-facing actions; scope that seems to exceed what was requested.
- Prefer resolving ambiguity by **investigation** over asking. Only escalate what genuinely requires the user's knowledge or authority. When you do ask, batch the questions and give enough context to answer without digging.

## Step 5 — Plan the verification up front

Decide *how you'll know each step worked* before building it (this pairs with `self-verification`): the test, the command, the observable behavior. A plan without a verification strategy produces "I think it works." Also plan the **rollback**: for risky steps, how do you undo it?

## Step 6 — Right-size and present

- Match the plan's weight to the task. A sentence-long plan for a medium task; a structured breakdown for a big one. Don't produce a project-management artifact for a two-hour job.
- For substantial work, use a visible task list (todos) so progress is trackable and nothing is dropped — update it as you go, not at the end.
- Keep the plan alive: when execution reveals the plan was wrong (it often does), **re-plan** rather than forcing the original. A plan is a hypothesis about how to proceed, not a contract.

## Anti-patterns

- **Analysis paralysis**: planning a task small enough to just do. Bias to action on the reversible and small.
- **Big-bang plans** with no early verification — you find out at the end that step 2 was wrong.
- **Planning in a vacuum**: not reading the existing code/context first, so the plan collides with reality on contact.
- **Delegating tightly-coupled work** to subagents and paying the cold-start tax repeatedly.
- **Asking the user things you could find out** by reading — or *not* asking about a genuine fork and guessing wrong.
- Treating the plan as immutable when the ground has shifted.

## Deliverable

For a nontrivial task, briefly state: the goal (as a done-condition), the ordered steps (each verifiable), what you'll investigate vs. build vs. delegate, any genuine forks you need the user to decide, and how you'll verify. Then execute — updating the plan as reality teaches you. The plan serves the work; don't let it become the work.
