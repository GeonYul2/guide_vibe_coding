---
type: technique
id: llm_wiki_context_compilation
source: techniques/registry.yaml
---

# LLM Wiki Context Compilation

## When to Apply

The project has many interlinked Markdown/YAML/code artifacts that agents repeatedly need to understand.

## Selection Guidance

- Choose this technique when its trigger matches the task context.
- Prefer prerequisites first when they are listed below.
- Use peers to compare similar techniques rather than selecting blindly.
- Use "Commonly Used With" to assemble a complete technique bundle.

## Prerequisites / Before This

- [[wiki/techniques/retrieval_memory_governance|Retrieval and Memory Governance]]
- [[wiki/techniques/source_backed_technique_ingestion|Source-Backed Technique Ingestion]]

## Next / Enables

- [[wiki/techniques/wiki_first_source_verification|Wiki-First Source Verification]]

## Similar / Compare With

- [[wiki/techniques/obsidian_graph_knowledge_ops|Obsidian Graph Knowledge Operations]]
- [[wiki/techniques/retrieval_memory_governance|Retrieval and Memory Governance]]
- [[wiki/techniques/source_backed_technique_ingestion|Source-Backed Technique Ingestion]]
- [[wiki/techniques/wiki_first_source_verification|Wiki-First Source Verification]]

## Commonly Used With

- [[wiki/techniques/agent_readiness_scoring|Agent Readiness Scoring / Gap Map]]
- [[wiki/techniques/cost_budgeting|Cost Budgeting]]
- [[wiki/techniques/deep_interview|Deep Interview / Requirement Crystallization]]
- [[wiki/techniques/default_response_brevity|Default Response Brevity]]
- [[wiki/techniques/eval_regression_loop|Eval and Regression Loop]]
- [[wiki/techniques/failed_case_memory|Failed-Case Memory]]
- [[wiki/techniques/genai_telemetry_standardization|GenAI Telemetry Standardization]]
- [[wiki/techniques/guardrails_tripwires|Guardrails and Tripwires]]
- [[wiki/techniques/model_routing_fallback_policy|Model Routing and Fallback Policy]]
- [[wiki/techniques/observability_tracing|Observability and Trace Logging]]
- [[wiki/techniques/obsidian_graph_knowledge_ops|Obsidian Graph Knowledge Operations]]
- [[wiki/techniques/prompt_versioning|Prompt and Policy Versioning]]
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

wiki/index.md and wiki/*

## Operating Notes

Keep original files as source of truth, then compile a Markdown wiki with stable entry points, backlinks, and source references. Use the wiki to reduce repeated context loading, but verify important facts against source files before changing behavior.

## Source References

sources/registry.yaml#article-roboco-karpathy-llm-wiki-72-run-benchmark

## Canonical Source Nodes

- [[wiki/sources/techniques-registry|Techniques Registry Source]]
- [[wiki/sources/techniques-taxonomy|Techniques Taxonomy Source]]

## Verify Against

- [[wiki/index|Wiki Index]]
- [[wiki/technique-map|Technique Map]]
- `techniques/registry.yaml`
- `techniques/taxonomy.yaml`
- task-local `technique-selection.yaml`
