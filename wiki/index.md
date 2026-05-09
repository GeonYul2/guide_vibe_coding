# Agent Engineering LLM Wiki

This wiki is an Obsidian-compatible navigation and context-compilation layer. It is **not** the source of truth.

## Start Here

1. Read [[wiki/workflows/intake|Standardized Agent Intake]] for new tasks.
2. Use [[wiki/technique-map|Technique Map]] to compare similar techniques and choose bundles.
3. Read [[wiki/workflows/build-agent|Build a New Automation Agent]] for the implementation gate sequence.
4. Use [[wiki/graph-links|Graph Links]] to inspect core relationships.
5. Verify important claims against canonical source files before editing.

## Canonical Sources

- [[wiki/sources/repo-root|Repository Root Source Bridge]]
- [[AGENTS|AGENTS.md]]
- [[README|README.md]]
- [[SECURITY|SECURITY.md]]
- `agent-playbook.yaml`
- [[wiki/sources/techniques-registry|techniques/registry.yaml]]
- [[wiki/sources/techniques-taxonomy|techniques/taxonomy.yaml]]
- [[wiki/sources/workflows|workflows/*.md]]
- [[wiki/sources/templates|templates/*.md]]
- [[wiki/sources/source-registry|sources/registry.yaml and summaries]]
- [[wiki/sources/distribution|distribution/*.md]]
- [[wiki/sources/maintainer|maintainer/*.md]]
- [[wiki/repos/radar|maintainer/radar/*]]

## Techniques

- [[wiki/techniques/standardized_intake_gate|Standardized Intake Quality Gate]]
- [[wiki/techniques/deep_interview|Deep Interview / Requirement Crystallization]]
- [[wiki/techniques/harness_engineering|Harness Engineering]]
- [[wiki/techniques/eval_regression_loop|Eval and Regression Loop]]
- [[wiki/techniques/structured_output_schema_validation|Structured Output Schema Validation]]
- [[wiki/techniques/failed_case_memory|Failed-Case Memory]]
- [[wiki/techniques/guardrails_tripwires|Guardrails and Tripwires]]
- [[wiki/techniques/token_context_caching|Token / Context Caching]]
- [[wiki/techniques/retrieval_memory_governance|Retrieval and Memory Governance]]
- [[wiki/techniques/prompt_versioning|Prompt and Policy Versioning]]
- [[wiki/techniques/tool_contracts|Tool Contract Design]]
- [[wiki/techniques/observability_tracing|Observability and Trace Logging]]
- [[wiki/techniques/genai_telemetry_standardization|GenAI Telemetry Standardization]]
- [[wiki/techniques/cost_budgeting|Cost Budgeting]]
- [[wiki/techniques/token_efficiency_budget_gate|Token Efficiency Budget Gate]]
- [[wiki/techniques/model_routing_fallback_policy|Model Routing and Fallback Policy]]
- [[wiki/techniques/safety_handoff_boundaries|Safety and Human Handoff Boundaries]]
- [[wiki/techniques/security_privacy_data_governance|Security, Privacy, and Data Governance]]
- [[wiki/techniques/deployment_rollout_canary|Deployment, Rollout, and Canary Strategy]]
- [[wiki/techniques/concise_operating_contract|Concise Agent Operating Contract]]
- [[wiki/techniques/scope_control_and_minimal_diff|Scope Control and Minimal Diff Discipline]]
- [[wiki/techniques/agent_harness_runtime_design|Agent Harness Runtime Design]]
- [[wiki/techniques/permissioned_tool_execution|Permissioned Tool Execution]]
- [[wiki/techniques/source_backed_technique_ingestion|Source-Backed Technique Ingestion]]
- [[wiki/techniques/default_response_brevity|Default Response Brevity]]
- [[wiki/techniques/agent_readiness_scoring|Agent Readiness Scoring / Gap Map]]
- [[wiki/techniques/llm_wiki_context_compilation|LLM Wiki Context Compilation]]
- [[wiki/techniques/wiki_first_source_verification|Wiki-First Source Verification]]
- [[wiki/techniques/obsidian_graph_knowledge_ops|Obsidian Graph Knowledge Operations]]

## Workflows

- [[wiki/workflows/build-agent|Workflow: Build a New Automation Agent]]
- [[wiki/workflows/deep-interview|Workflow: Deep Interview]]
- [[wiki/workflows/intake|Workflow: Standardized Agent Intake]]
- [[wiki/workflows/source-ingestion|Workflow: Supplemental Source-Backed Technique Ingestion]]
- [[wiki/workflows/publish-user-distribution|Workflow: Publish User Distribution]]
- [[wiki/workflows/weekly-repo-radar|Workflow: Weekly GitHub Technique Repository Radar]]

## Tasks

- [[wiki/tasks/customer-email-reply-agent|customer-email-reply-agent]]
- [[wiki/tasks/github-technique-radar-agent|github-technique-radar-agent]]

## Source Bridges

- [[wiki/sources/repo-root|Repository Root Source Bridge]]
- [[wiki/sources/templates|Template Source Bridge]]
- [[wiki/sources/source-registry|Source Registry Bridge]]
- [[wiki/sources/distribution|Distribution Source Bridge]]
- [[wiki/sources/maintainer|Maintainer Source Bridge]]
- [[wiki/sources/workflows|Workflow Source Bridge]]
- [[wiki/repos/radar|Repository Radar Bridge]]

## Recent Radar Candidate Files

- `maintainer/radar/2026-05-03-candidates.yaml`
- `maintainer/radar/2026-05-09-candidates.yaml`

## Obsidian Usage

Open the repository root as an Obsidian vault. The committed `.obsidian/graph.json` filters graph view toward `path:wiki` while still allowing links to source files.
