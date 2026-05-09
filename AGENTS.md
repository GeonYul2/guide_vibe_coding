# Agent Engineering Guide — Execution Contract

This repository is an **agent-executable playbook** for designing, building, and verifying automation agents. It is not a passive documentation library.

When an AI coding agent is asked to use this repository for an automation-agent task, it MUST treat this file as the control surface and follow the gates below before implementation.

## Mandatory Boot Sequence

1. Read `agent-playbook.yaml`.
2. Read `techniques/registry.yaml` and `techniques/taxonomy.yaml`.
3. For ordinary user tasks, do not run maintainer-only discovery. For refresh/discovery work only, read `maintainer/radar-config.yaml` and `maintainer/workflows/weekly-repo-radar.md`.
4. If supplemental source material such as YouTube videos, articles, or talks is involved, read `sources/registry.yaml` and `workflows/source-ingestion.md`.
5. Fill `intake-form.md` using `workflows/intake.md`, then classify the user's task using `workflows/build-agent.md`.
6. If the task intent, scope, non-goals, or success criteria are unclear, run `workflows/deep-interview.md` before planning or coding.
7. Create or update a task folder under `tasks/<task-slug>/` using `templates/`.
8. Run `python3 scripts/validate_agent_task.py tasks/<task-slug>` before claiming readiness or completion.

## Non-Negotiable Gates

For every new automation agent, the agent MUST produce these artifacts before implementation:

- `intake-form.md` — normalized first-input contract, missing-field follow-ups, and evidence boundary
- `agent-prd.md` — purpose, users, scope, non-goals, success criteria
- `technique-selection.yaml` — selected techniques and rejected techniques with reasons
- `output-schema.md` — structured output formats, schema versions, parser/repair/fail-closed rules
- `eval-spec.md` — harness, datasets/cases, acceptance thresholds, regression strategy
- `guardrails.md` — input/output/tool-call guardrails, tripwires, and handoff actions
- `tool-contracts.md` — tools/APIs, permissions, failure modes, timeouts, retries
- `retrieval-memory.md` — source hierarchy, RAG/memory scope, retention, freshness, invalidation
- `failure-cases.md` — known/expected failures and how they become regression cases
- `cost-and-caching.md` — hard token/cost ceiling, context pruning, caching strategy, invalidation rules
- `model-routing.md` — model choice, fallback, retry, escalation, and budget policy
- `telemetry.md` — trace events, metrics, redaction, retention, correlation, alerting
- `security-privacy.md` — data classification, secrets, PII, access control, audit rules
- `release-rollout.md` — staged rollout, canary, kill switch, rollback, post-deploy checks
- `readiness-scorecard.md` — readiness score, gap map, and implementation gate decision
- `implementation-plan.md` — small reversible implementation steps and verification commands

Every technique id in `techniques/registry.yaml` must be selected or rejected with a reason in `technique-selection.yaml`. Use `techniques/taxonomy.yaml` to prioritize techniques by agent context, but do not silently ignore registry techniques.

Implementation is blocked until the above artifacts exist and contain non-placeholder content. For business automation agents, implementation is also blocked if `cost-and-caching.md` lacks explicit max token ceilings, cache hit target, context pruning rule, fallback path, and token telemetry.

## Required Technique Defaults

Unless explicitly rejected with a reason in `technique-selection.yaml`, every automation-agent task must consider:

- standardized intake form / input quality gate
- deep interview / requirement crystallization
- harness engineering
- eval and regression loop
- structured output schema validation
- failed-case memory
- guardrails and tripwires
- token/context caching
- retrieval and memory governance
- prompt/version control
- tool contract design
- observability and trace logging
- GenAI telemetry standardization
- cost budget
- token efficiency budget gate: max tokens, cache target, pruning rule, and token telemetry
- model routing and fallback policy
- safety and human handoff boundaries
- security/privacy/data governance
- deployment, rollout, and canary strategy
- default response brevity unless the user asks for detail
- agent readiness scoring and gap map before implementation

## Default Response Brevity Policy

When the human has not explicitly asked for detailed explanation, long rationale, or expanded documentation, the agent should keep normal user-facing replies to 1-2 sentences. Expand only when needed for safety, blockers, validation evidence, handoff, or requested artifacts.

## Brevity Enforcement Rule

At the first user-facing response in a new task or session, if this brevity policy is active, the agent MUST treat concise chat as enabled by default and state it briefly instead of leaving it implicit. Use wording equivalent to: “Brevity mode is on: I’ll keep chat to 1–3 sentences and put long detail in files/artifacts unless you ask for detail.”

Enforce this as a working constraint: progress updates should be one short sentence; final reports should include only result, validation evidence, changed files, and remaining risks. Put long rationale, plans, and documentation into files/artifacts, not chat, unless the user explicitly asks for detail or a safety/blocker explanation requires expansion.

If verbosity instructions conflict, ask one concise clarification question, then enforce the chosen verbosity for the rest of the task.

## Primary Technique Discovery Policy

The baseline refresh mechanism for maintainers is GitHub-first repository discovery. Ordinary clone users who are building an automation agent do not need this path. Maintainers must be able to find hot GitHub repositories that contain reusable agent-engineering techniques, patterns, harnesses, eval systems, structured output/schema systems, caching/context tools, observability/telemetry, MCP/tooling, prompt/workflow discipline, memory/RAG governance, security/privacy, rollout/canary, or safety/permission designs.

YouTube videos, blog posts, talks, and release notes are supplemental sources. They may seed techniques, but they do not replace maintainer-reviewed GitHub repository discovery.

For discovery work:

1. Use `maintainer/scripts/weekly_repo_radar.py` and `maintainer/radar-config.yaml`.
2. Prioritize reusable technique repositories over domain-specific demo apps.
3. Record candidates under `maintainer/radar/`.
4. Promote reviewed repositories into `repos/registry.yaml` only after human review.
5. Promote a new mandatory technique only after a repository/source shows a reusable pattern and an enforcement point exists in this repo.

## Source Ingestion Policy

When a user provides videos, articles, talks, release notes, or external references:

1. Register the source in `sources/registry.yaml`.
2. Extract reusable techniques, not long copied content.
3. Link extracted techniques with `source_refs`.
4. Keep unverified or transcript-pending extraction marked as candidate/queued.
5. Use `workflows/source-ingestion.md` as the control process.

## External Repository Policy

Do not vendor, copy, or mirror entire external GitHub repositories into this repo.

External repositories must be tracked only as metadata in `repos/registry.yaml` plus optional concise summaries under `repos/summaries/`.

Technique discovery is manual-dispatch only via `.github/workflows/weekly-repo-radar.yml` or `maintainer/scripts/weekly_repo_radar.py`. It may create review artifacts and a PR under `maintainer/radar/`, but it must not directly adopt candidates into `repos/registry.yaml` without human review.

Each external repo entry should include:

- URL
- purpose
- tags
- last_checked date
- update cadence
- adoption status
- why it matters
- risks / maintenance notes
- local application guidance

## Verification Contract

Before declaring a task ready or complete, provide evidence:

- artifact validator output
- selected test/eval commands and results
- unresolved risks or explicit non-goals
- changed files

Do not claim completion if required artifacts are missing, placeholders remain, or validation was not run.
