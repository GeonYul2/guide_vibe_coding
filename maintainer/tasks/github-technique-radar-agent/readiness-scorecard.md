# Agent Readiness Scorecard: GitHub Technique Radar Agent

Purpose: show whether this agent task is ready for implementation and what is missing.

## Summary

- Overall readiness score: 86 / 100
- Readiness status: ready-for-prototype
- Top missing items:
  - Confirm final CLI flags supported by `maintainer/scripts/weekly_repo_radar.py` before implementation changes.
  - Add fixture files and schema tests during implementation.
  - Decide whether GraphQL is needed after REST prototype evidence.

## Scoring Rubric

| Area | Weight | Score | Evidence | Missing / Risk | Required Before Implementation? |
| --- | ---: | ---: | --- | --- | --- |
| Intent and user outcome | 8 | 8 / 8 | PRD defines compliant GitHub-first radar outcome | none | yes |
| Scope and non-goals | 6 | 6 / 6 | Prohibited crawling, vendoring, and auto-adoption excluded | none | yes |
| Input/output schema | 8 | 6 / 8 | Candidate YAML schema and examples defined | implement validator fixtures | yes |
| Technique selection | 6 | 6 / 6 | Every registry technique selected with reason | none | yes |
| Harness and eval plan | 8 | 6 / 8 | Fixture, dry-run, and manual workflow modes defined | test fixtures not yet created | yes |
| Failure-case memory | 7 | 7 / 7 | Six initial failure cases recorded | expand with observed failures | yes |
| Guardrails and tripwires | 7 | 7 / 7 | Prohibited sources, vendoring, registry edits, and rate limits covered | none | yes |
| Tool contracts and permissions | 7 | 5 / 7 | GitHub APIs, script, validator, cache covered | final CLI contract may need alignment | yes |
| Retrieval and memory governance | 6 | 6 / 6 | Source hierarchy, freshness, cache, privacy rules defined | none | yes when retrieval/memory exists |
| Token efficiency, cost, caching, and model routing | 10 | 8 / 10 | Explicit token, cost, cache, fallback, and telemetry limits | price table can be refined later | yes |
| Telemetry and traceability | 7 | 5 / 7 | Required trace events and metrics defined | dashboard implementation pending | yes |
| Security and privacy | 7 | 7 / 7 | Token, cache, telemetry, and redaction rules defined | none | yes when company/customer/internal data exists |
| Release, rollout, and rollback | 6 | 4 / 6 | Local, canary, production, kill switch, and rollback planned | exact workflow flag may need implementation | yes when production/manual maintainer use exists |
| Human approval / handoff | 7 | 5 / 7 | Adoption and high-impact changes require human review | human review workflow still manual | yes |

## Readiness Map

```text
Intent             [green]
Scope              [green]
Schema             [yellow: fixtures pending]
Techniques         [green]
Eval/Harness       [yellow: implementation fixtures pending]
Failures           [green]
Guardrails         [green]
Tools/Auth         [yellow: final CLI alignment pending]
Retrieval/Memory   [green]
Token/Cost Gate    [green]
Telemetry          [yellow: dashboard pending]
Security/Privacy   [green]
Rollout/Rollback   [yellow: workflow flag pending]
Human Review       [green]
```

## Optional HTML Report

An HTML readiness map may be generated later from this scorecard for visual review, but it is not required for backend MVP implementation.

## Gate Decision

- Decision: proceed
- Reason: Required design gates are complete enough for a small REST-first prototype that only writes radar artifacts and task files.
- Required fixes before implementation:
  - Run task validator successfully.
  - Inspect current `maintainer/scripts/weekly_repo_radar.py` CLI and align implementation plan commands.
