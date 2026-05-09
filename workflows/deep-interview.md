# Workflow: Deep Interview

Purpose: turn a vague or incomplete `intake-form.md` into an implementation-ready specification.

## Rules

- Ask one question per round.
- Ask about intent and boundaries before implementation details.
- Do not start PRD synthesis or implementation until missing intake fields, non-goals, and success criteria are explicit.
- Prefer concrete examples, counterexamples, and tradeoff questions.
- If codebase facts can be discovered directly, inspect them instead of asking the user.

## Minimum Readiness Questions

1. What business or team workflow should this agent improve, and why does it need automation now?
2. Who is the primary user, and what exact output should they receive?
3. What actions may the agent take autonomously, and what actions require human approval?
4. What is explicitly out of scope for the first version?
5. What are three representative success cases and two failure/edge cases?
6. What data, tools, or systems can the agent access?
7. What should happen when the agent is uncertain, over budget, blocked, or receives unsafe input?
8. What measurable evidence proves the agent is working?

## Crystallized Output

Write the result back into `intake-form.md` first, then synthesize `agent-prd.md`:

- Problem
- Users
- Desired outcome
- Inputs / outputs
- In-scope behavior
- Non-goals
- Human approval boundaries
- Success criteria
- Failure criteria
- Open questions
