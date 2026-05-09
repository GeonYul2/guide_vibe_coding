# Graph Links

## Core Build Flow

[[wiki/workflows/intake]] -> [[wiki/workflows/deep-interview]] -> [[wiki/workflows/build-agent]] -> [[wiki/techniques/standardized_intake_gate]] -> [[wiki/techniques/agent_readiness_scoring]]

## Technique Selection Map

[[wiki/technique-map]] -> [[wiki/techniques/standardized_intake_gate]] -> [[wiki/techniques/deep_interview]] -> [[wiki/techniques/structured_output_schema_validation]] -> [[wiki/techniques/eval_regression_loop]]

## Source-Backed Knowledge Flow

[[wiki/techniques/source_backed_technique_ingestion]] -> [[wiki/techniques/llm_wiki_context_compilation]] -> [[wiki/techniques/wiki_first_source_verification]] -> [[wiki/techniques/obsidian_graph_knowledge_ops]]

## Canonical Source Bridge

[[wiki/sources/techniques-registry]] -> [[wiki/techniques/standardized_intake_gate]]
[[wiki/sources/techniques-taxonomy]] -> [[wiki/technique-map]] -> [[wiki/techniques/deep_interview]]

## Root Vault Source Bridges

[[wiki/index]] -> [[wiki/sources/repo-root]] -> [[AGENTS]]
[[wiki/index]] -> [[wiki/sources/templates]] -> [[templates/agent-prd]]
[[wiki/index]] -> [[wiki/sources/source-registry]] -> [[sources/summaries/youtube-seed-sources]]
[[wiki/index]] -> [[wiki/sources/distribution]] -> [[distribution/user/AGENTS]]
[[wiki/index]] -> [[wiki/repos/radar]] -> [[maintainer/radar/2026-05-09]]
[[wiki/tasks/customer-email-reply-agent]] -> [[tasks/customer-email-reply-agent/model-routing]]
[[wiki/tasks/github-technique-radar-agent]] -> [[maintainer/tasks/github-technique-radar-agent/model-routing]]

## Discovery Flow

[[wiki/workflows/weekly-repo-radar]] -> [[wiki/techniques/source_backed_technique_ingestion]] -> [[wiki/techniques/wiki_first_source_verification]]

## Verification Flow

[[wiki/techniques/structured_output_schema_validation]] -> [[wiki/techniques/eval_regression_loop]] -> [[wiki/techniques/failed_case_memory]] -> [[wiki/techniques/observability_tracing]]

## Runtime and Cost Flow

[[wiki/techniques/agent_harness_runtime_design]] -> [[wiki/techniques/permissioned_tool_execution]] -> [[wiki/techniques/model_routing_fallback_policy]] -> [[wiki/techniques/token_efficiency_budget_gate]]
