# Agent Engineering Guide — User Distribution

This repository contains only the **user-facing automation-agent helper**. Maintainer-only GitHub radar, repository discovery, generated wiki, and update/publish automation are intentionally excluded.

## Operating Contract

When an AI coding agent uses this repository to create, modify, or evaluate an automation agent, it must treat `agent-playbook.yaml` as the machine-readable control surface and follow `workflows/build-agent.md`.

## Mandatory Boot Sequence

1. Read `agent-playbook.yaml`.
2. Read `techniques/registry.yaml` and `techniques/taxonomy.yaml`.
3. Fill `tasks/<task-slug>/intake-form.md` using `workflows/intake.md`.
4. Classify the task using `workflows/build-agent.md`.
5. If intent, scope, non-goals, approval boundaries, or success criteria are unclear, run `workflows/deep-interview.md` before planning or coding.
6. Create or update a task folder under `tasks/<task-slug>/` using `templates/`.
7. Run `python3 scripts/validate_agent_task.py tasks/<task-slug>` before claiming readiness or completion.

## Implementation Gate

Implementation is blocked until all required artifacts listed in `agent-playbook.yaml` exist, contain non-placeholder content, and pass validation. For business automation agents, `cost-and-caching.md` must include max token ceilings, cache hit target, context pruning rule, fallback path, and token telemetry.

## Distribution Boundary

Do not run or assume maintainer-only technique discovery in this repo. If the task is to refresh global techniques, run GitHub radar, publish a distribution, or modify upstream update logic, use the source/maintainer repository instead of this user distribution.

## Response Brevity

Brevity is the default: keep routine progress and final chat concise, and place long rationale or plans in task artifacts unless the user asks for detail or a safety/blocker explanation requires expansion.
