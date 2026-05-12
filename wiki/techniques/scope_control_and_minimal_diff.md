---
type: technique
id: scope_control_and_minimal_diff
source: techniques/registry.yaml
---

# Scope Control and Minimal Diff Discipline

## When to Apply

The agent edits code, docs, configs, prompts, or workflows.

## Selection Guidance

- Choose this technique when its trigger matches the task context.
- Prefer prerequisites first when they are listed below.
- Use peers to compare similar techniques rather than selecting blindly.
- Use "Commonly Used With" to assemble a complete technique bundle.

## Prerequisites / Before This

- [[wiki/techniques/karpathy_claude_md_discipline|Karpathy CLAUDE.md Coding Discipline]]

## Next / Enables

- [[wiki/techniques/default_response_brevity|Default Response Brevity]]

## Similar / Compare With

- [[wiki/techniques/agent_readiness_scoring|Agent Readiness Scoring / Gap Map]]
- [[wiki/techniques/concise_operating_contract|Concise Agent Operating Contract]]
- [[wiki/techniques/deep_interview|Deep Interview / Requirement Crystallization]]
- [[wiki/techniques/default_response_brevity|Default Response Brevity]]
- [[wiki/techniques/karpathy_claude_md_discipline|Karpathy CLAUDE.md Coding Discipline]]
- [[wiki/techniques/prompt_versioning|Prompt and Policy Versioning]]
- [[wiki/techniques/standardized_intake_gate|Standardized Intake Quality Gate]]

## Commonly Used With

- [[wiki/techniques/agent_readiness_scoring|Agent Readiness Scoring / Gap Map]]
- [[wiki/techniques/concise_operating_contract|Concise Agent Operating Contract]]
- [[wiki/techniques/default_response_brevity|Default Response Brevity]]
- [[wiki/techniques/deployment_rollout_canary|Deployment, Rollout, and Canary Strategy]]
- [[wiki/techniques/eval_regression_loop|Eval and Regression Loop]]
- [[wiki/techniques/failed_case_memory|Failed-Case Memory]]
- [[wiki/techniques/genai_telemetry_standardization|GenAI Telemetry Standardization]]
- [[wiki/techniques/guardrails_tripwires|Guardrails and Tripwires]]
- [[wiki/techniques/harness_engineering|Harness Engineering]]
- [[wiki/techniques/karpathy_claude_md_discipline|Karpathy CLAUDE.md Coding Discipline]]
- [[wiki/techniques/model_routing_fallback_policy|Model Routing and Fallback Policy]]
- [[wiki/techniques/observability_tracing|Observability and Trace Logging]]
- [[wiki/techniques/permissioned_tool_execution|Permissioned Tool Execution]]
- [[wiki/techniques/standardized_intake_gate|Standardized Intake Quality Gate]]
- [[wiki/techniques/structured_output_schema_validation|Structured Output Schema Validation]]
- [[wiki/techniques/token_efficiency_budget_gate|Token Efficiency Budget Gate]]
- [[wiki/techniques/tool_contracts|Tool Contract Design]]

## Required Output

implementation-plan.md

## Operating Notes

Require small reversible changes, no opportunistic refactors, explicit non-goals, and verification tied to the requested behavior.

## Source References

sources/registry.yaml#youtube-karpathy-65-line-claude-md, sources/registry.yaml#youtube-vibecoding-silicon-valley-techniques

## Canonical Source Nodes

- [[wiki/sources/techniques-registry|Techniques Registry Source]]
- [[wiki/sources/techniques-taxonomy|Techniques Taxonomy Source]]

## Verify Against

- [[wiki/index|Wiki Index]]
- [[wiki/technique-map|Technique Map]]
- `techniques/registry.yaml`
- `techniques/taxonomy.yaml`
- task-local `technique-selection.yaml`
