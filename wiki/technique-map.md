# Technique Map

Use this page when choosing techniques for a task. It groups similar techniques and exposes must/should/optional bundles from `techniques/taxonomy.yaml`.

## Source Nodes

- [[wiki/sources/techniques-registry|Techniques Registry Source]]
- [[wiki/sources/techniques-taxonomy|Techniques Taxonomy Source]]

## Selection Rule

1. Start with the task profile.
2. Include all `must` techniques unless explicitly rejected with reason.
3. Compare peers before choosing among similar techniques.
4. Follow prerequisite and next-technique links on individual technique pages.

# Categories

## Category: context_cost_and_memory

- [[wiki/techniques/cost_budgeting|Cost Budgeting]]
- [[wiki/techniques/model_routing_fallback_policy|Model Routing and Fallback Policy]]
- [[wiki/techniques/observability_tracing|Observability and Trace Logging]]
- [[wiki/techniques/retrieval_memory_governance|Retrieval and Memory Governance]]
- [[wiki/techniques/token_context_caching|Token / Context Caching]]
- [[wiki/techniques/token_efficiency_budget_gate|Token Efficiency Budget Gate]]

## Category: discovery_and_update

- [[wiki/techniques/source_backed_technique_ingestion|Source-Backed Technique Ingestion]]

## Category: harness_and_runtime

- [[wiki/techniques/agent_harness_runtime_design|Agent Harness Runtime Design]]
- [[wiki/techniques/deployment_rollout_canary|Deployment, Rollout, and Canary Strategy]]
- [[wiki/techniques/harness_engineering|Harness Engineering]]
- [[wiki/techniques/model_routing_fallback_policy|Model Routing and Fallback Policy]]
- [[wiki/techniques/permissioned_tool_execution|Permissioned Tool Execution]]
- [[wiki/techniques/tool_contracts|Tool Contract Design]]

## Category: intake_and_scope

- [[wiki/techniques/agent_readiness_scoring|Agent Readiness Scoring / Gap Map]]
- [[wiki/techniques/deep_interview|Deep Interview / Requirement Crystallization]]
- [[wiki/techniques/karpathy_claude_md_discipline|Karpathy CLAUDE.md Coding Discipline]]
- [[wiki/techniques/scope_control_and_minimal_diff|Scope Control and Minimal Diff Discipline]]
- [[wiki/techniques/standardized_intake_gate|Standardized Intake Quality Gate]]

## Category: llm_wiki_and_graph

- [[wiki/techniques/llm_wiki_context_compilation|LLM Wiki Context Compilation]]
- [[wiki/techniques/obsidian_graph_knowledge_ops|Obsidian Graph Knowledge Operations]]
- [[wiki/techniques/retrieval_memory_governance|Retrieval and Memory Governance]]
- [[wiki/techniques/source_backed_technique_ingestion|Source-Backed Technique Ingestion]]
- [[wiki/techniques/wiki_first_source_verification|Wiki-First Source Verification]]

## Category: observability_and_operations

- [[wiki/techniques/deployment_rollout_canary|Deployment, Rollout, and Canary Strategy]]
- [[wiki/techniques/eval_regression_loop|Eval and Regression Loop]]
- [[wiki/techniques/genai_telemetry_standardization|GenAI Telemetry Standardization]]
- [[wiki/techniques/observability_tracing|Observability and Trace Logging]]

## Category: operating_contracts

- [[wiki/techniques/concise_operating_contract|Concise Agent Operating Contract]]
- [[wiki/techniques/default_response_brevity|Default Response Brevity]]
- [[wiki/techniques/karpathy_claude_md_discipline|Karpathy CLAUDE.md Coding Discipline]]
- [[wiki/techniques/prompt_versioning|Prompt and Policy Versioning]]
- [[wiki/techniques/scope_control_and_minimal_diff|Scope Control and Minimal Diff Discipline]]

## Category: quality_and_evals

- [[wiki/techniques/eval_regression_loop|Eval and Regression Loop]]
- [[wiki/techniques/failed_case_memory|Failed-Case Memory]]
- [[wiki/techniques/guardrails_tripwires|Guardrails and Tripwires]]
- [[wiki/techniques/harness_engineering|Harness Engineering]]
- [[wiki/techniques/structured_output_schema_validation|Structured Output Schema Validation]]

## Category: safety_security_and_governance

- [[wiki/techniques/guardrails_tripwires|Guardrails and Tripwires]]
- [[wiki/techniques/observability_tracing|Observability and Trace Logging]]
- [[wiki/techniques/permissioned_tool_execution|Permissioned Tool Execution]]
- [[wiki/techniques/safety_handoff_boundaries|Safety and Human Handoff Boundaries]]
- [[wiki/techniques/security_privacy_data_governance|Security, Privacy, and Data Governance]]
- [[wiki/techniques/source_backed_technique_ingestion|Source-Backed Technique Ingestion]]

## Category: schemas_and_outputs

- [[wiki/techniques/eval_regression_loop|Eval and Regression Loop]]
- [[wiki/techniques/structured_output_schema_validation|Structured Output Schema Validation]]
- [[wiki/techniques/tool_contracts|Tool Contract Design]]


# Agent Context Profiles

## Profile: coding_agent

### Must

- [[wiki/techniques/concise_operating_contract|Concise Agent Operating Contract]]
- [[wiki/techniques/eval_regression_loop|Eval and Regression Loop]]
- [[wiki/techniques/failed_case_memory|Failed-Case Memory]]
- [[wiki/techniques/guardrails_tripwires|Guardrails and Tripwires]]
- [[wiki/techniques/harness_engineering|Harness Engineering]]
- [[wiki/techniques/karpathy_claude_md_discipline|Karpathy CLAUDE.md Coding Discipline]]
- [[wiki/techniques/permissioned_tool_execution|Permissioned Tool Execution]]
- [[wiki/techniques/scope_control_and_minimal_diff|Scope Control and Minimal Diff Discipline]]
- [[wiki/techniques/standardized_intake_gate|Standardized Intake Quality Gate]]
- [[wiki/techniques/structured_output_schema_validation|Structured Output Schema Validation]]
- [[wiki/techniques/token_efficiency_budget_gate|Token Efficiency Budget Gate]]
- [[wiki/techniques/tool_contracts|Tool Contract Design]]

### Should

- [[wiki/techniques/agent_readiness_scoring|Agent Readiness Scoring / Gap Map]]
- [[wiki/techniques/default_response_brevity|Default Response Brevity]]
- [[wiki/techniques/deployment_rollout_canary|Deployment, Rollout, and Canary Strategy]]
- [[wiki/techniques/genai_telemetry_standardization|GenAI Telemetry Standardization]]
- [[wiki/techniques/model_routing_fallback_policy|Model Routing and Fallback Policy]]
- [[wiki/techniques/observability_tracing|Observability and Trace Logging]]

### Optional

- [[wiki/techniques/security_privacy_data_governance|Security, Privacy, and Data Governance]]
- [[wiki/techniques/token_context_caching|Token / Context Caching]]

## Profile: document_knowledge_agent

### Must

- [[wiki/techniques/deep_interview|Deep Interview / Requirement Crystallization]]
- [[wiki/techniques/eval_regression_loop|Eval and Regression Loop]]
- [[wiki/techniques/failed_case_memory|Failed-Case Memory]]
- [[wiki/techniques/guardrails_tripwires|Guardrails and Tripwires]]
- [[wiki/techniques/llm_wiki_context_compilation|LLM Wiki Context Compilation]]
- [[wiki/techniques/prompt_versioning|Prompt and Policy Versioning]]
- [[wiki/techniques/retrieval_memory_governance|Retrieval and Memory Governance]]
- [[wiki/techniques/safety_handoff_boundaries|Safety and Human Handoff Boundaries]]
- [[wiki/techniques/security_privacy_data_governance|Security, Privacy, and Data Governance]]
- [[wiki/techniques/source_backed_technique_ingestion|Source-Backed Technique Ingestion]]
- [[wiki/techniques/standardized_intake_gate|Standardized Intake Quality Gate]]
- [[wiki/techniques/structured_output_schema_validation|Structured Output Schema Validation]]
- [[wiki/techniques/token_efficiency_budget_gate|Token Efficiency Budget Gate]]
- [[wiki/techniques/wiki_first_source_verification|Wiki-First Source Verification]]

### Should

- [[wiki/techniques/agent_readiness_scoring|Agent Readiness Scoring / Gap Map]]
- [[wiki/techniques/genai_telemetry_standardization|GenAI Telemetry Standardization]]
- [[wiki/techniques/observability_tracing|Observability and Trace Logging]]
- [[wiki/techniques/token_context_caching|Token / Context Caching]]

### Optional

- [[wiki/techniques/model_routing_fallback_policy|Model Routing and Fallback Policy]]
- [[wiki/techniques/tool_contracts|Tool Contract Design]]

## Profile: research_or_radar_agent

### Must

- [[wiki/techniques/default_response_brevity|Default Response Brevity]]
- [[wiki/techniques/eval_regression_loop|Eval and Regression Loop]]
- [[wiki/techniques/llm_wiki_context_compilation|LLM Wiki Context Compilation]]
- [[wiki/techniques/observability_tracing|Observability and Trace Logging]]
- [[wiki/techniques/prompt_versioning|Prompt and Policy Versioning]]
- [[wiki/techniques/retrieval_memory_governance|Retrieval and Memory Governance]]
- [[wiki/techniques/source_backed_technique_ingestion|Source-Backed Technique Ingestion]]
- [[wiki/techniques/standardized_intake_gate|Standardized Intake Quality Gate]]
- [[wiki/techniques/structured_output_schema_validation|Structured Output Schema Validation]]
- [[wiki/techniques/token_efficiency_budget_gate|Token Efficiency Budget Gate]]
- [[wiki/techniques/wiki_first_source_verification|Wiki-First Source Verification]]

### Should

- [[wiki/techniques/agent_readiness_scoring|Agent Readiness Scoring / Gap Map]]
- [[wiki/techniques/cost_budgeting|Cost Budgeting]]
- [[wiki/techniques/genai_telemetry_standardization|GenAI Telemetry Standardization]]
- [[wiki/techniques/model_routing_fallback_policy|Model Routing and Fallback Policy]]
- [[wiki/techniques/obsidian_graph_knowledge_ops|Obsidian Graph Knowledge Operations]]
- [[wiki/techniques/token_context_caching|Token / Context Caching]]

### Optional

- [[wiki/techniques/guardrails_tripwires|Guardrails and Tripwires]]
- [[wiki/techniques/safety_handoff_boundaries|Safety and Human Handoff Boundaries]]
- [[wiki/techniques/security_privacy_data_governance|Security, Privacy, and Data Governance]]

## Profile: sql_or_data_agent

### Must

- [[wiki/techniques/deep_interview|Deep Interview / Requirement Crystallization]]
- [[wiki/techniques/eval_regression_loop|Eval and Regression Loop]]
- [[wiki/techniques/failed_case_memory|Failed-Case Memory]]
- [[wiki/techniques/harness_engineering|Harness Engineering]]
- [[wiki/techniques/observability_tracing|Observability and Trace Logging]]
- [[wiki/techniques/retrieval_memory_governance|Retrieval and Memory Governance]]
- [[wiki/techniques/safety_handoff_boundaries|Safety and Human Handoff Boundaries]]
- [[wiki/techniques/security_privacy_data_governance|Security, Privacy, and Data Governance]]
- [[wiki/techniques/standardized_intake_gate|Standardized Intake Quality Gate]]
- [[wiki/techniques/structured_output_schema_validation|Structured Output Schema Validation]]
- [[wiki/techniques/token_efficiency_budget_gate|Token Efficiency Budget Gate]]
- [[wiki/techniques/tool_contracts|Tool Contract Design]]

### Should

- [[wiki/techniques/agent_readiness_scoring|Agent Readiness Scoring / Gap Map]]
- [[wiki/techniques/cost_budgeting|Cost Budgeting]]
- [[wiki/techniques/genai_telemetry_standardization|GenAI Telemetry Standardization]]
- [[wiki/techniques/model_routing_fallback_policy|Model Routing and Fallback Policy]]
- [[wiki/techniques/token_context_caching|Token / Context Caching]]

### Optional

- [[wiki/techniques/deployment_rollout_canary|Deployment, Rollout, and Canary Strategy]]
- [[wiki/techniques/permissioned_tool_execution|Permissioned Tool Execution]]

## Profile: workflow_automation_agent

### Must

- [[wiki/techniques/agent_harness_runtime_design|Agent Harness Runtime Design]]
- [[wiki/techniques/deep_interview|Deep Interview / Requirement Crystallization]]
- [[wiki/techniques/failed_case_memory|Failed-Case Memory]]
- [[wiki/techniques/guardrails_tripwires|Guardrails and Tripwires]]
- [[wiki/techniques/observability_tracing|Observability and Trace Logging]]
- [[wiki/techniques/permissioned_tool_execution|Permissioned Tool Execution]]
- [[wiki/techniques/safety_handoff_boundaries|Safety and Human Handoff Boundaries]]
- [[wiki/techniques/security_privacy_data_governance|Security, Privacy, and Data Governance]]
- [[wiki/techniques/standardized_intake_gate|Standardized Intake Quality Gate]]
- [[wiki/techniques/structured_output_schema_validation|Structured Output Schema Validation]]
- [[wiki/techniques/token_efficiency_budget_gate|Token Efficiency Budget Gate]]
- [[wiki/techniques/tool_contracts|Tool Contract Design]]

### Should

- [[wiki/techniques/agent_readiness_scoring|Agent Readiness Scoring / Gap Map]]
- [[wiki/techniques/cost_budgeting|Cost Budgeting]]
- [[wiki/techniques/deployment_rollout_canary|Deployment, Rollout, and Canary Strategy]]
- [[wiki/techniques/eval_regression_loop|Eval and Regression Loop]]
- [[wiki/techniques/genai_telemetry_standardization|GenAI Telemetry Standardization]]
- [[wiki/techniques/model_routing_fallback_policy|Model Routing and Fallback Policy]]

### Optional

- [[wiki/techniques/retrieval_memory_governance|Retrieval and Memory Governance]]
- [[wiki/techniques/token_context_caching|Token / Context Caching]]
