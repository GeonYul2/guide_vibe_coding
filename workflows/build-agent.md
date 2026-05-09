# Workflow: Build a New Automation Agent

Use this workflow whenever a user wants to create, modify, or evaluate an automation agent.

## 0. Wiki-First Orientation

If `wiki/index.md` exists, read it first to choose the smallest relevant context path. Use the wiki only for orientation and token reduction; verify artifact requirements, technique IDs, and gate rules against canonical files before writing or claiming authority.

For technique selection, prefer this read order:

1. `wiki/index.md`
2. `wiki/technique-map.md`
3. `techniques/taxonomy.yaml`
4. only the needed entries in `techniques/registry.yaml`, then all registry IDs when filling final select/reject coverage

## 1. Task Scaffold

Read:

- `AGENTS.md`
- `agent-playbook.yaml`
- `techniques/registry.yaml`
- `techniques/taxonomy.yaml`

Create a task folder:

```bash
python3 scripts/new_agent_task.py "<task-slug>"
```

## 2. Standardized Intake Gate

Fill `intake-form.md` first. This is the normalized user-start contract and must cover:

- agent idea
- primary user
- workflow pain
- input and output
- allowed autonomous actions
- human approval required
- forbidden actions and non-goals
- success examples
- failure / edge cases
- tools / data access
- evidence of success

Use `workflows/intake.md` as a conversational Q&A loop: ask exactly one missing-field question per round, write each answer into `intake-form.md`, and do not ask the human to complete the whole form at once.

If any field is missing, vague, or marked `Unknown - follow up required`, run `workflows/deep-interview.md` before PRD synthesis, technique selection, or implementation.

Translate completed intake into `agent-prd.md`; do not skip the PRD.

## 3. Deep Interview Gate

If any of the following are unclear, run `workflows/deep-interview.md` before implementation:

- Why this agent should exist
- Who uses it
- Inputs and outputs
- Allowed actions and forbidden actions
- Success criteria
- Non-goals
- Human approval boundaries
- Failure handling expectations

## 4. Technique Selection Gate

Fill `technique-selection.yaml`.

Use `wiki/technique-map.md` when present to identify the likely task profile with fewer tokens, then verify against `techniques/taxonomy.yaml` to classify the agent context and prioritize must/should/optional techniques. Then, for every technique in `techniques/registry.yaml`:

- select it, or
- reject it with a concrete reason.

Do not silently ignore techniques.

## 5. Structured Output Gate

Fill `output-schema.md` before coding.

Minimum schema contract:

- output format and schema version
- required fields and validation rules
- parser/repair/fail-closed behavior
- valid and invalid golden examples
- eval cases that prove schema compliance

## 6. Harness / Eval Gate

Fill `eval-spec.md` before coding.

Minimum eval plan:

- happy path
- ambiguous input path
- tool failure path
- unsafe or out-of-scope request path
- invalid structured output path
- known regression cases

## 7. Guardrail Gate

Fill `guardrails.md`.

Define:

- input guardrails
- output guardrails
- tool-call tripwires
- human handoff triggers
- adversarial/unsafe eval cases

## 8. Tool Contract Gate

Fill `tool-contracts.md` for every API/script/database/browser/internal service.

Include:

- input schema
- output schema
- permissions
- timeout
- retry policy
- idempotency
- error classes
- human approval requirements

## 9. Retrieval and Memory Gate

Fill `retrieval-memory.md` when the agent uses sources, RAG, vector search, internal documents, or session/long-term memory.

Define:

- source-of-truth hierarchy
- allowed and forbidden sources
- citation/source-reference requirements
- retention and deletion rules
- freshness and invalidation rules
- privacy filters

## 10. Failure Memory Gate

Fill `failure-cases.md`.

Every observed failure must become one of:

- regression test
- explicit non-goal
- prompt/tool-contract update
- guardrail/tripwire update
- human handoff rule

## 11. Token Efficiency, Cost, Caching, and Model Routing Gate

Fill `cost-and-caching.md` and `model-routing.md`.

Define:

- max input/output/total tokens per run
- expected token/cost per run
- hard cost ceiling per successful run and per time window
- reusable context
- cache key and required cache hit-rate target
- context pruning, compression, and deduplication rule
- cache invalidation rule
- stale-cache risk
- model routing by task class
- token telemetry fields
- fallback behavior when budget or quality gates fail

## 12. Telemetry Gate

Fill `telemetry.md`.

Define:

- model/tool/retrieval/cache/eval/handoff trace events
- latency, cost, quality, success, and guardrail metrics
- redaction rules
- correlation ids
- alerts and owners

## 13. Security and Privacy Gate

Fill `security-privacy.md` when the agent touches company/customer/internal data, credentials, logs, or regulated information.

Define:

- data classification
- least-privilege access
- secret handling
- PII/sensitive log redaction
- retention/deletion
- audit owner and cadence

## 14. Release and Rollout Gate

Fill `release-rollout.md` when the agent will run outside a local prototype.

Define:

- local/internal canary/production stages
- entry and exit criteria
- kill switch
- rollback process
- post-deploy eval/monitoring checks

## 15. Implementation Plan Gate

Fill `implementation-plan.md` with small, reversible steps and verification commands.

## 16. Validate Before Implementation

Run:

```bash
python3 scripts/validate_agent_task.py tasks/<task-slug>
```

Implementation is blocked until validation passes.

## 17. Implement and Verify

After implementation:

- run targeted tests/evals
- add failed cases to `failure-cases.md`
- update `eval-spec.md` with new regression cases
- update `telemetry.md` and `release-rollout.md` if production behavior changed
- rerun validator
- report evidence, changed files, and known gaps
