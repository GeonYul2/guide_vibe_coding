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
