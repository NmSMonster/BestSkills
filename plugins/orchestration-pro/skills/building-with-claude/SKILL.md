---
name: building-with-claude
description: Building applications and workflows powered by Claude (or any LLM) — prompt design, tool/function calling, agents, RAG, structured output, evaluation, and cost/latency control. Use when the user is building something that calls an LLM API, designing prompts or system prompts, building an agent or chatbot, doing RAG/retrieval, wiring tool use, getting reliable structured output, or debugging flaky LLM behavior. The meta-skill for making Claude build things with Claude.
---

# Building with Claude

Building reliable LLM-powered software is its own engineering discipline — the model is a probabilistic component, and the craft is engineering *around* that probability to get reliable behavior. This skill covers prompt design, the agentic patterns, and the evaluation loop that separates a demo from a product.

For exact current model IDs, pricing, parameters, and API/SDK specifics, load the `claude-api` skill (it holds the volatile facts you must not guess). This skill is the *methodology*.

## Prompt design — the foundation

- **Be explicit and specific.** The model isn't a mind-reader; ambiguity in the prompt becomes variance in the output. State the task, the format, the constraints, and what *not* to do. Vague prompt → inconsistent results.
- **Show, don't just tell.** A few good examples (few-shot) in the prompt beat paragraphs of instruction for teaching a format or style. Include an edge case in the examples.
- **Structure the prompt.** Separate role/system instructions, context/data, and the task. Use clear delimiters (XML tags work well with Claude — `<document>`, `<instructions>`) so the model knows what's data vs. what's command. This also hardens against prompt injection from within the data.
- **Give the model room to think** for reasoning-heavy tasks: ask it to work step by step / reason before answering. Don't force a one-token answer to a problem that needs working out.
- **System prompt sets durable behavior** (role, rules, tone, output contract); the user turn carries the specific request. Put the stable stuff in the system prompt.
- **Iterate empirically.** Prompt engineering is measured, not guessed — change one thing, test on real cases, keep what improves. (See evaluation below.)

## Structured output

When you need machine-parseable results:
- Ask for a specific schema and **use tool calling / structured-output mode** rather than hoping free text parses. Defining a tool with a JSON schema and letting the model "call" it is the reliable way to get typed output.
- Validate every output against the schema; handle the case where it doesn't conform (retry with the error, or repair). Never assume the JSON is well-formed in production.
- Keep schemas as simple as the task allows — deeply nested, ambiguous schemas raise error rates.

## Tool use / function calling

- **Define tools like good API design**: clear names, precise descriptions (the description is what the model uses to decide when to call — write it for the model), typed parameters, required vs. optional explicit. A vague tool description causes wrong/missed calls — the same rule as skill descriptions.
- Return tool results the model can use, including errors as structured data ("not found", "rate limited") so it can recover rather than hallucinate.
- Expect and handle: the model calling the wrong tool, calling with bad args, or not calling when it should. Validate args before executing; never execute a destructive tool call without the appropriate guardrail.

## Agentic patterns

- **Start simple.** A single well-prompted call with tools beats a multi-agent system for most tasks — reach for orchestration only when the task genuinely needs it. Complexity is a cost, not a feature.
- **The agent loop**: model → tool call → result → model, until done. Bound it (max iterations) so a confused agent can't loop forever; give it a way to signal completion.
- **Decompose** long tasks into steps with checkpoints rather than one giant prompt; sub-tasks to sub-agents when the work is separable and each piece is self-contained (mirrors `task-planning`'s delegation logic).
- **Context management**: the context window is finite and attention degrades over long contexts — keep only what's relevant, summarize history, retrieve on demand rather than stuffing everything in.

## RAG (retrieval-augmented generation)

- The quality ceiling is retrieval quality: if the right chunk isn't retrieved, the model can't use it. Invest in chunking (semantic, right-sized), embeddings, and re-ranking before blaming the model.
- **Ground the answer in retrieved context and ask for citations** to it — this cuts hallucination and makes answers checkable.
- Handle "not in the context": instruct the model to say it doesn't know rather than invent. Test that it actually does.
- Put retrieved documents in clearly delimited blocks; keep the user's untrusted input separate from instructions (injection defense).

## Evaluation — the difference between a demo and a product

You cannot improve what you don't measure, and "it looked good in my three tests" is not measurement.
- **Build an eval set**: real inputs with known-good outputs (or graded criteria), including the hard/edge cases. Even 20–50 cases beats vibes.
- **Grade automatically** where possible: exact match, schema validity, contains-required-facts; use an LLM-as-judge for open-ended quality (with a rubric — and validate the judge against human judgment on a sample).
- **Every prompt/model change is a measured experiment** against the eval set — did quality go up or down? This turns prompt engineering from guessing into engineering.
- Track regressions: a prompt tweak that fixes case A often breaks case B.

## Cost, latency, reliability (production concerns)

- **Right-size the model**: use the most capable model where quality matters; use a smaller/faster one for simple high-volume steps. Don't pay Opus prices for a classification a smaller model nails. Route by difficulty.
- **Prompt caching** for large stable prefixes (system prompt, retrieved docs reused across calls) cuts cost and latency substantially — structure prompts so the stable part is cacheable.
- **Stream** for perceived latency in user-facing apps.
- **Handle the API like any external API** (see `automation-pro:api-integration`): timeouts, retries with backoff on transient errors, rate-limit handling, graceful degradation. LLM APIs are flaky under load — engineer for it.
- Set `max_tokens` sanely; watch token usage; log prompts+outputs (minus PII) for debugging and eval-set growth.

## Debugging flaky LLM behavior

When output is wrong or inconsistent:
1. **Look at the actual full prompt** the model received (after all templating/retrieval) — the bug is usually there: missing context, ambiguous instruction, injection from data, a malformed example.
2. Isolate: is it the prompt, the retrieved context, the model, or the parsing? Test each.
3. Reduce variance: lower temperature for deterministic tasks; add examples; tighten the instruction; constrain with structured output.
4. Add the failing case to the eval set so the fix is measured and it never silently regresses.

## Rules

- Engineer around the probability: validate outputs, bound loops, handle the model being wrong — never assume the model did what you asked without checking.
- Measure changes against an eval set; don't ship prompt changes on vibes.
- Keep untrusted input separate from instructions; validate structured output; guardrail destructive tool calls.
- Start simple; add agentic complexity only when the task demands it.
- For current model IDs, prices, and API params, consult the `claude-api` skill — never guess volatile facts.
