# Workflow: Standardized Agent Intake

Purpose: make every new automation-agent task start from the same minimum-quality input before PRD, technique selection, or implementation work begins.

## When to Use

Use this workflow at the start of every new task under `tasks/<task-slug>/`.

## Required Artifact

Create and complete:

```text
tasks/<task-slug>/intake-form.md
```

Use `templates/intake-form.md` as the source template.

## Conversational Intake Protocol

Do **not** ask the user to fill the full intake form in one message.

Run intake as a question-answer loop:

1. Create the task folder and `intake-form.md` from the template.
2. Extract any answers already present in the user's first message or discoverable from local repository context.
3. Ask exactly **one** missing-field question per round.
4. After each answer, immediately update the matching section in `intake-form.md`.
5. Prefer concrete examples over abstract labels; ask for examples, counterexamples, or approval boundaries when a field is vague.
6. Stop asking only when every minimum intake field below is explicit enough for PRD synthesis and validation.

Question order:

1. What agent do you want to build, and what job should it finish for you?
2. Who will use it, and where does their current workflow hurt?
3. What input will the agent receive, and what output must it produce?
4. What may it do automatically, and what needs human approval?
5. What is explicitly forbidden or out of scope for version 1?
6. What are three success examples?
7. What are at least two failure, edge, unsafe, or ambiguous cases?
8. What tools, files, APIs, data, or credentials may it access?
9. What test, eval, log, metric, or checklist proves it works?

If one answer covers multiple fields, record all covered fields and ask the next missing question. Do not re-ask information already answered.

## Minimum Intake Fields

Every intake must answer or explicitly mark follow-up for:

1. Agent Idea
2. Primary User
3. Workflow Pain
4. Input
5. Output
6. Allowed Actions
7. Human Approval Required
8. Forbidden / Non-Goals
9. Success Examples
10. Failure / Edge Cases
11. Tools / Data Access
12. Evidence of Success

## Quality Rules

- Do not leave blank fields.
- Do not leave `TODO` placeholders.
- If the user does not know an answer, write `Unknown - follow up required` and ask through `workflows/deep-interview.md`. Missing fields must trigger deep interview before validation can pass.
- Do not start implementation until Forbidden / Non-Goals and Evidence of Success are explicit.
- Translate intake answers into `agent-prd.md`; do not treat the intake form as a replacement for the PRD.
- Never dump the full 12-field intake checklist into chat as the first response. Keep the chat conversational and put the completed structure in the artifact.

## Handoff to Deep Interview

Run `workflows/deep-interview.md` when any of these are missing or vague:

- user and workflow pain
- input/output contract
- allowed autonomous actions
- human approval boundary
- forbidden/non-goal scope
- success examples or evidence
- failure/edge cases
- tool/data access boundary

## Handoff to Technique Selection

After intake is complete, use it to classify the agent context with `techniques/taxonomy.yaml` and fill `technique-selection.yaml`.
