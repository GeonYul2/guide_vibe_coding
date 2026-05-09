# Conversational Intake

Use this page to start a new automation-agent task without dumping a long form into chat.

## Rule

Ask exactly one missing-field question per round, then write the answer into `tasks/<task-slug>/intake-form.md`.

## Question Order

1. What agent do you want to build, and what job should it finish for you?
2. Who will use it, and where does their current workflow hurt?
3. What input will the agent receive, and what output must it produce?
4. What may it do automatically, and what needs human approval?
5. What is explicitly forbidden or out of scope for version 1?
6. What are three success examples?
7. What are at least two failure, edge, unsafe, or ambiguous cases?
8. What tools, files, APIs, data, or credentials may it access?
9. What test, eval, log, metric, or checklist proves it works?

If one answer covers multiple fields, record all covered fields and ask only the next missing question.

## Artifact Contract

Canonical template: `templates/intake-form.md`

Required sections:

- Agent Idea
- Primary User
- Workflow Pain
- Input
- Output
- Allowed Actions
- Human Approval Required
- Forbidden / Non-Goals
- Success Examples
- Failure / Edge Cases
- Tools / Data Access
- Evidence of Success

Do not proceed to PRD synthesis or implementation while required fields are blank, vague, or marked unknown.
