# Technique Map

Use this page to narrow technique selection before reading larger canonical YAML files. Final authority remains `techniques/taxonomy.yaml`, `techniques/registry.yaml`, and task-local `technique-selection.yaml`.

## Selection Algorithm

1. Pick the closest profile below.
2. Treat profile `must` techniques as selected unless there is a concrete rejection reason.
3. Consider `should` techniques next; reject irrelevant ones with reasons.
4. Review `optional` techniques only if their trigger matches the task.
5. Before final validation, ensure every technique ID in `techniques/registry.yaml` appears in `technique-selection.yaml` as selected or rejected.

## Always Consider First

- `standardized_intake_gate`
- `deep_interview` when intent, scope, non-goals, approval boundary, or success evidence is unclear
- `structured_output_schema_validation` when output is machine-consumed
- `eval_regression_loop` and `failed_case_memory` for behavior proof
- `token_efficiency_budget_gate` for business or repeated automation
- `karpathy_claude_md_discipline` for coding agents, AGENTS.md/CLAUDE.md rules, and refactoring work
- `tool_contracts`, `permissioned_tool_execution`, `guardrails_tripwires`, and `safety_handoff_boundaries` when tools or external side effects are involved

## Profile: Coding / Refactoring Agent

Must:

- `standardized_intake_gate`
- `concise_operating_contract`
- `karpathy_claude_md_discipline`
- `scope_control_and_minimal_diff`
- `structured_output_schema_validation`
- `harness_engineering`
- `eval_regression_loop`
- `failed_case_memory`
- `tool_contracts`
- `permissioned_tool_execution`
- `guardrails_tripwires`
- `token_efficiency_budget_gate`

Should:

- `observability_tracing`
- `genai_telemetry_standardization`
- `model_routing_fallback_policy`
- `deployment_rollout_canary`
- `default_response_brevity`
- `agent_readiness_scoring`

Optional:

- `token_context_caching`
- `security_privacy_data_governance`

## Profile: Workflow Automation Agent

Must:

- `standardized_intake_gate`
- `deep_interview`
- `structured_output_schema_validation`
- `tool_contracts`
- `permissioned_tool_execution`
- `safety_handoff_boundaries`
- `guardrails_tripwires`
- `security_privacy_data_governance`
- `agent_harness_runtime_design`
- `observability_tracing`
- `failed_case_memory`
- `token_efficiency_budget_gate`

Should:

- `eval_regression_loop`
- `deployment_rollout_canary`
- `model_routing_fallback_policy`
- `cost_budgeting`
- `genai_telemetry_standardization`
- `agent_readiness_scoring`

Optional:

- `token_context_caching`
- `retrieval_memory_governance`

## Profile: Document / Knowledge Agent

Must:

- `standardized_intake_gate`
- `deep_interview`
- `structured_output_schema_validation`
- `prompt_versioning`
- `retrieval_memory_governance`
- `llm_wiki_context_compilation`
- `wiki_first_source_verification`
- `eval_regression_loop`
- `failed_case_memory`
- `safety_handoff_boundaries`
- `guardrails_tripwires`
- `security_privacy_data_governance`
- `source_backed_technique_ingestion`
- `token_efficiency_budget_gate`

Should:

- `token_context_caching`
- `observability_tracing`
- `genai_telemetry_standardization`
- `agent_readiness_scoring`

Optional:

- `tool_contracts`
- `model_routing_fallback_policy`

## Profile: SQL / Data / Analytics Agent

Must:

- `standardized_intake_gate`
- `deep_interview`
- `structured_output_schema_validation`
- `tool_contracts`
- `harness_engineering`
- `eval_regression_loop`
- `failed_case_memory`
- `retrieval_memory_governance`
- `observability_tracing`
- `security_privacy_data_governance`
- `safety_handoff_boundaries`
- `token_efficiency_budget_gate`

Should:

- `token_context_caching`
- `cost_budgeting`
- `model_routing_fallback_policy`
- `genai_telemetry_standardization`
- `agent_readiness_scoring`

Optional:

- `permissioned_tool_execution`
- `deployment_rollout_canary`

## Profile: Research / Source Tracking Agent

Must:

- `standardized_intake_gate`
- `source_backed_technique_ingestion`
- `llm_wiki_context_compilation`
- `wiki_first_source_verification`
- `structured_output_schema_validation`
- `retrieval_memory_governance`
- `observability_tracing`
- `eval_regression_loop`
- `prompt_versioning`
- `default_response_brevity`
- `token_efficiency_budget_gate`

Should:

- `cost_budgeting`
- `token_context_caching`
- `obsidian_graph_knowledge_ops`
- `genai_telemetry_standardization`
- `model_routing_fallback_policy`
- `agent_readiness_scoring`

Optional:

- `safety_handoff_boundaries`
- `guardrails_tripwires`
- `security_privacy_data_governance`

## Final Coverage Check

Open `templates/technique-selection.yaml`, move irrelevant techniques from `selected` to `rejected`, and replace every placeholder reason. Then run:

```bash
python3 scripts/validate_agent_task.py tasks/<task-slug>
```
