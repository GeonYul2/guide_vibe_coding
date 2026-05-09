# User Agent Guide Wiki

This is the user-distribution wiki for token-efficient agent setup. It is a routing map, not the source of truth.

## Start Here

1. Read this page first.
2. For a new task, read [Conversational Intake](workflows/intake.md) and create `tasks/<task-slug>/intake-form.md`.
3. Use [Technique Map](technique-map.md) to choose the likely profile and first-pass technique bundle.
4. Verify gates and technique IDs against canonical files before writing final artifacts:
   - `AGENTS.md`
   - `agent-playbook.yaml`
   - `workflows/build-agent.md`
   - `workflows/intake.md`
   - `techniques/taxonomy.yaml`
   - `techniques/registry.yaml`
   - `templates/*`

## Token-Saving Read Path

For ordinary user tasks, avoid loading every file up front.

```text
wiki/index.md
  -> wiki/workflows/intake.md
  -> wiki/technique-map.md
  -> techniques/taxonomy.yaml
  -> relevant entries in techniques/registry.yaml
  -> templates needed for the current artifact
```

Before `technique-selection.yaml` is finalized, every technique ID in `techniques/registry.yaml` still must be selected or rejected with a concrete reason.

## User vs Maintainer Boundary

- This user repo builds and verifies automation-agent tasks.
- It does not run GitHub radar, maintainer discovery, publish workflows, or update the global technique catalog automatically.
- If the task is to refresh this guide itself, use the source/maintainer repository.

## Core Pages

- [Conversational Intake](workflows/intake.md)
- [Build Agent Flow](workflows/build-agent.md)
- [Technique Map](technique-map.md)
- [Graph Links](graph-links.md)
