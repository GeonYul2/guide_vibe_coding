---
type: technique
id: prompt_versioning
source: techniques/registry.yaml
---

# Prompt and Policy Versioning

## When to Apply

Prompts, system policies, rubrics, or examples influence behavior.

## Selection Guidance

- Choose this technique when its trigger matches the task context.
- Prefer prerequisites first when they are listed below.
- Use peers to compare similar techniques rather than selecting blindly.
- Use "Commonly Used With" to assemble a complete technique bundle.

## Prerequisites / Before This

- [[wiki/techniques/default_response_brevity|Default Response Brevity]]

## Next / Enables

- None recorded.

## Similar / Compare With

- [[wiki/techniques/concise_operating_contract|Concise Agent Operating Contract]]
- [[wiki/techniques/default_response_brevity|Default Response Brevity]]
- [[wiki/techniques/karpathy_claude_md_discipline|Karpathy CLAUDE.md Coding Discipline]]
- [[wiki/techniques/scope_control_and_minimal_diff|Scope Control and Minimal Diff Discipline]]

## Commonly Used With

- [[wiki/techniques/agent_readiness_scoring|Agent Readiness Scoring / Gap Map]]
- [[wiki/techniques/cost_budgeting|Cost Budgeting]]
- [[wiki/techniques/deep_interview|Deep Interview / Requirement Crystallization]]
- [[wiki/techniques/default_response_brevity|Default Response Brevity]]
- [[wiki/techniques/eval_regression_loop|Eval and Regression Loop]]
- [[wiki/techniques/failed_case_memory|Failed-Case Memory]]
- [[wiki/techniques/genai_telemetry_standardization|GenAI Telemetry Standardization]]
- [[wiki/techniques/guardrails_tripwires|Guardrails and Tripwires]]
- [[wiki/techniques/llm_wiki_context_compilation|LLM Wiki Context Compilation]]
- [[wiki/techniques/model_routing_fallback_policy|Model Routing and Fallback Policy]]
- [[wiki/techniques/observability_tracing|Observability and Trace Logging]]
- [[wiki/techniques/obsidian_graph_knowledge_ops|Obsidian Graph Knowledge Operations]]
- [[wiki/techniques/retrieval_memory_governance|Retrieval and Memory Governance]]
- [[wiki/techniques/safety_handoff_boundaries|Safety and Human Handoff Boundaries]]
- [[wiki/techniques/security_privacy_data_governance|Security, Privacy, and Data Governance]]
- [[wiki/techniques/source_backed_technique_ingestion|Source-Backed Technique Ingestion]]
- [[wiki/techniques/standardized_intake_gate|Standardized Intake Quality Gate]]
- [[wiki/techniques/structured_output_schema_validation|Structured Output Schema Validation]]
- [[wiki/techniques/token_context_caching|Token / Context Caching]]
- [[wiki/techniques/token_efficiency_budget_gate|Token Efficiency Budget Gate]]
- [[wiki/techniques/wiki_first_source_verification|Wiki-First Source Verification]]

## Required Output

implementation-plan.md

## Operating Notes

See registry.

## Source References

Registry-defined / local policy

## Canonical Source Nodes

- [[wiki/sources/techniques-registry|Techniques Registry Source]]
- [[wiki/sources/techniques-taxonomy|Techniques Taxonomy Source]]

## Verify Against

- [[wiki/index|Wiki Index]]
- [[wiki/technique-map|Technique Map]]
- `techniques/registry.yaml`
- `techniques/taxonomy.yaml`
- task-local `technique-selection.yaml`
