# Implementation Plan: GitHub Technique Radar Agent

## Constraints

- Do not access or crawl prohibited third-party trending sites.
- Use GitHub APIs and local configured queries as the primary discovery source.
- Do not vendor external repositories.
- Do not auto-edit `repos/registry.yaml`, `techniques/registry.yaml`, or mandatory templates.
- Keep changes small, reversible, and validated.
- Respect GitHub rate limits and token/cost budgets.

## Steps

1. Validate this task folder and fix any artifact gaps.
2. Inspect `maintainer/scripts/weekly_repo_radar.py` to confirm current CLI, output schema, scoring, rate-limit, and cache behavior.
3. Add or adjust fixture-driven tests for deduplication, scoring, prohibited sources, rate-limit handling, and output schema.
4. Implement a REST-first radar improvement only where gaps exist: source allowlist, schema version field, degraded status, cache metadata, scoring weights, or validation hooks.
5. Run targeted tests and dry-run radar with a low per-query limit.
6. Review git diff to ensure only approved files changed.
7. Update failure cases, eval spec, telemetry, and rollout notes based on observed implementation evidence.
8. Rerun `python3 scripts/validate_agent_task.py tasks/github-technique-radar-agent` before claiming readiness or completion.

## Pre-Implementation Gate Checklist

- Required artifacts validated: pending validator run.
- Technique selection complete: yes, every registry technique is selected with a reason.
- Readiness score decision: 86 / 100, proceed with prototype after validator passes.

## Verification Commands

```bash
python3 scripts/validate_agent_task.py tasks/github-technique-radar-agent
python3 maintainer/scripts/weekly_repo_radar.py --help
python3 maintainer/scripts/weekly_repo_radar.py --dry-run --limit 3
python3 scripts/test_agent_guide.py
```

## Rollback Plan

- Revert task artifact changes if design direction is rejected.
- Revert radar script or config changes independently from task artifacts.
- Delete generated `maintainer/radar/` files from failed dry runs if schema-invalid or misleading.
- Restore cache by deleting local cache files; no external state should require rollback for prototype.

## Completion Evidence

- Validator output: to be recorded after gate run.
- Test/eval output: to be recorded after implementation tests.
- Remaining risks: CLI flags and fixture paths must be aligned with current script before coding changes.
