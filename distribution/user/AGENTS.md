# Agent Engineering Guide — User Distribution

This repository contains only the **user-facing automation-agent helper**. Maintainer-only GitHub radar, repository discovery, full maintainer generated wiki, and update/publish automation are intentionally excluded. A small curated `wiki/` is included for token-efficient orientation.

## Operating Contract

When an AI coding agent uses this repository to create, modify, or evaluate an automation agent, it must treat `agent-playbook.yaml` as the machine-readable control surface and follow `workflows/build-agent.md`.

## Mandatory Boot Sequence

1. Read `wiki/index.md` first when present to choose the smallest relevant context path.
2. Read `agent-playbook.yaml`.
3. Read `techniques/taxonomy.yaml`; read `techniques/registry.yaml` before final technique selection coverage.
4. Fill `tasks/<task-slug>/intake-form.md` using the conversational loop in `workflows/intake.md`.
5. Classify the task using `workflows/build-agent.md`.
6. If intent, scope, non-goals, approval boundaries, or success criteria are unclear, run `workflows/deep-interview.md` before planning or coding.
7. Create or update a task folder under `tasks/<task-slug>/` using `templates/`.
8. Run `python3 scripts/validate_agent_task.py tasks/<task-slug>` before claiming readiness or completion.

## Conversational Intake

Do not ask the human to fill the whole intake form at once. Ask one concise missing-field question per round, write each answer into `tasks/<task-slug>/intake-form.md`, and continue until all required intake fields are explicit.

## Implementation Gate

Implementation is blocked until all required artifacts listed in `agent-playbook.yaml` exist, contain non-placeholder content, and pass validation. For business automation agents, `cost-and-caching.md` must include max token ceilings, cache hit target, context pruning rule, fallback path, and token telemetry.

## Distribution Boundary

Do not run or assume maintainer-only technique discovery in this repo. If the task is to refresh global techniques, run GitHub radar, publish a distribution, or modify upstream update logic, use the source/maintainer repository instead of this user distribution.

## User Wiki Boundary

Use `wiki/` as the first-pass map for token-efficient technique routing. It is not authoritative: verify required gates against `AGENTS.md`, `agent-playbook.yaml`, `workflows/*.md`, `templates/*`, `techniques/taxonomy.yaml`, and `techniques/registry.yaml`.

## Response Brevity

Brevity is the default: keep routine progress and final chat concise, and place long rationale or plans in task artifacts unless the user asks for detail or a safety/blocker explanation requires expansion.
