---
type: technique
id: default_response_brevity
source: techniques/registry.yaml
---

# Default Response Brevity

## When to Apply

The agent communicates progress, results, blockers, or next steps to a human.

## Selection Guidance

- Choose this technique when its trigger matches the task context.
- Prefer prerequisites first when they are listed below.
- Use peers to compare similar techniques rather than selecting blindly.
- Use "Commonly Used With" to assemble a complete technique bundle.

## Prerequisites / Before This

- [[wiki/techniques/scope_control_and_minimal_diff|Scope Control and Minimal Diff Discipline]]

## Next / Enables

- [[wiki/techniques/prompt_versioning|Prompt and Policy Versioning]]

## Similar / Compare With

- [[wiki/techniques/concise_operating_contract|Concise Agent Operating Contract]]
- [[wiki/techniques/karpathy_claude_md_discipline|Karpathy CLAUDE.md Coding Discipline]]
- [[wiki/techniques/prompt_versioning|Prompt and Policy Versioning]]
- [[wiki/techniques/scope_control_and_minimal_diff|Scope Control and Minimal Diff Discipline]]

## Commonly Used With

- [[wiki/techniques/agent_readiness_scoring|Agent Readiness Scoring / Gap Map]]
- [[wiki/techniques/concise_operating_contract|Concise Agent Operating Contract]]
- [[wiki/techniques/cost_budgeting|Cost Budgeting]]
- [[wiki/techniques/deployment_rollout_canary|Deployment, Rollout, and Canary Strategy]]
- [[wiki/techniques/eval_regression_loop|Eval and Regression Loop]]
- [[wiki/techniques/failed_case_memory|Failed-Case Memory]]
- [[wiki/techniques/genai_telemetry_standardization|GenAI Telemetry Standardization]]
- [[wiki/techniques/guardrails_tripwires|Guardrails and Tripwires]]
- [[wiki/techniques/harness_engineering|Harness Engineering]]
- [[wiki/techniques/karpathy_claude_md_discipline|Karpathy CLAUDE.md Coding Discipline]]
- [[wiki/techniques/llm_wiki_context_compilation|LLM Wiki Context Compilation]]
- [[wiki/techniques/model_routing_fallback_policy|Model Routing and Fallback Policy]]
- [[wiki/techniques/observability_tracing|Observability and Trace Logging]]
- [[wiki/techniques/obsidian_graph_knowledge_ops|Obsidian Graph Knowledge Operations]]
- [[wiki/techniques/permissioned_tool_execution|Permissioned Tool Execution]]
- [[wiki/techniques/prompt_versioning|Prompt and Policy Versioning]]
- [[wiki/techniques/retrieval_memory_governance|Retrieval and Memory Governance]]
- [[wiki/techniques/scope_control_and_minimal_diff|Scope Control and Minimal Diff Discipline]]
- [[wiki/techniques/source_backed_technique_ingestion|Source-Backed Technique Ingestion]]
- [[wiki/techniques/standardized_intake_gate|Standardized Intake Quality Gate]]
- [[wiki/techniques/structured_output_schema_validation|Structured Output Schema Validation]]
- [[wiki/techniques/token_context_caching|Token / Context Caching]]
- [[wiki/techniques/token_efficiency_budget_gate|Token Efficiency Budget Gate]]
- [[wiki/techniques/tool_contracts|Tool Contract Design]]
- [[wiki/techniques/wiki_first_source_verification|Wiki-First Source Verification]]

## Required Output

AGENTS.md or task-local instruction file

## Operating Notes

Unless the human explicitly asks for detail, keep normal user-facing replies to one sentence by default. The first user-facing response in a new task or session must be exactly one sentence that declares brevity mode. Use two sentences only for safety, blockers, validation evidence, handoff, or requested artifacts.

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
