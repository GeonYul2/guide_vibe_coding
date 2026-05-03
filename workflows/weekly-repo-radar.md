# Workflow: Weekly GitHub Technique Repository Radar

Purpose: keep this guide current by discovering hot GitHub repositories that contain reusable agent-engineering techniques.

This is the **primary** refresh loop. YouTube videos, articles, talks, and release notes are supplemental source-ingestion inputs handled by `workflows/source-ingestion.md`.

## Implemented Automation

This repo uses GitHub Actions as the scheduler:

- Workflow: `.github/workflows/weekly-repo-radar.yml`
- Schedule: `0 0 * * 1` UTC, which is Monday 09:00 KST
- Manual trigger: `workflow_dispatch`
- Script: `scripts/weekly_repo_radar.py`
- Config: `repos/radar-config.yaml`
- Output:
  - `repos/radar/YYYY-MM-DD.md`
  - `repos/radar/YYYY-MM-DD-candidates.yaml`
- Review model: create a pull request for human review

GitHub Actions scheduled workflows use POSIX cron syntax in UTC and run from the latest commit on the default branch. This workflow also supports manual dispatch for ad-hoc refreshes.

## What Counts as a Candidate

Prioritize repositories that teach or implement reusable techniques, such as:

- agent harnesses and runtime loops
- eval, benchmark, regression, and test harness systems
- failed-case memory and feedback loops
- context engineering, compression, deduplication, and caching
- structured output, schema validation, parser/repair, and contract testing
- observability, tracing, telemetry, monitoring, and cost tracking
- MCP, tool registries, permission systems, and sandboxing
- prompt/version/workflow discipline
- memory, RAG, retrieval governance, and state patterns
- model routing, fallback, latency, and budget-control systems
- security, privacy, PII redaction, and data-governance patterns
- deployment, canary, rollout, rollback, and kill-switch patterns
- safety, handoff, policy, guardrail, and tripwire implementations
- concise operating-contract examples for coding agents

Deprioritize domain-specific demo apps unless they clearly expose reusable agent-engineering patterns.

## Guardrails

- Do not vendor external repositories.
- Do not auto-promote candidates into `repos/registry.yaml`.
- Do not auto-add mandatory techniques without human review.
- The scheduled job only creates review artifacts and opens a PR.

## Discovery Sources

The implementation uses GitHub Search API queries configured in `repos/radar-config.yaml`.

Candidate signals:

- recent commits/releases
- stars and forks
- star delta versus the previous generated radar when available
- issue/PR activity proxy via open issues
- technique keyword score
- relevance to automation agents
- license metadata
- language/topics/description match

## Classification Tags

Use tags such as:

- agent-framework
- evals
- harness
- caching
- observability
- telemetry
- structured-output
- schema-validation
- guardrails
- tripwires
- memory
- retrieval-governance
- model-routing
- security-privacy
- rollout-canary
- tool-use
- prompt-engineering
- workflow-orchestration
- browser-automation
- code-agent
- safety

## Weekly Review Procedure

1. Review the generated PR.
2. Open `repos/radar/YYYY-MM-DD.md` for the ranked overview.
3. Open `repos/radar/YYYY-MM-DD-candidates.yaml` for structured metadata.
4. For promising candidates, inspect the source repository manually.
5. Choose one status:
   - `rejected` — not useful, not reusable, or too risky
   - `watch` — revisit later
   - `candidate` — promising but not adopted
   - `adopted` — add to `repos/registry.yaml`
6. If a repository reveals a reusable technique, add the technique to `techniques/registry.yaml` with source refs.
7. If it should become mandatory for all agent tasks, update:
   - `agent-playbook.yaml`
   - `templates/technique-selection.yaml`
   - any required artifact template under `templates/`
   - `techniques/taxonomy.yaml`
   - `scripts/test_agent_guide.py`

## Adoption Output

Update `repos/registry.yaml` only after review:

```yaml
- name:
  url:
  tags: []
  status: candidate|watch|adopted|rejected
  last_checked: YYYY-MM-DD
  update_cadence: weekly|monthly|manual
  why_it_matters:
  local_application:
  risks:
  next_review:
```
