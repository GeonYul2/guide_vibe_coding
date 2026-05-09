# Telemetry and Trace Contract: GitHub Technique Radar Agent

Purpose: make model, tool, retrieval, cache, cost, latency, and quality behavior observable without leaking secrets.

## Trace Events

| Event | Required Fields | Redaction Rule | Retention | Dashboard / Query |
| --- | --- | --- | --- | --- |
| model_call | run_id, model_tier, task_class, input_tokens, output_tokens, estimated_cost, cache_key_hash, latency_ms, result_status | redact prompts containing secrets; store summary hash instead of full external text | 30 days local or CI logs | `agent=github-technique-radar-agent event=model_call` |
| tool_call | run_id, tool_name, endpoint_category, query_hash, status_code, latency_ms, rate_remaining, retry_count | redact Authorization and token-like values | 30 days | `event=tool_call tool=github` |
| retrieval | run_id, source_url, owner_repo, path, etag_or_sha, bytes_used, freshness, allowed_source | do not store full file content in telemetry | 90 days for audit summary | `event=retrieval freshness=stale` |
| cache | run_id, cache_type, key_hash, hit_or_miss, age_seconds, invalidation_reason | key hash only; no token or raw content | 90 days | `event=cache hit_or_miss=miss` |
| eval_result | run_id, eval_id, fixture, passed, failures, duration_ms, schema_version | no sensitive fixture data unless already public and approved | retained with task artifacts | `event=eval_result passed=false` |
| handoff | run_id, trigger, candidate_url, required_owner, reason, changed_files | redact credentials and private notes | retained until review closed | `event=handoff` |
| budget_stop | run_id, budget_type, consumed, ceiling, remaining_candidates, degraded_output_path | no raw prompt content | 90 days | `event=budget_stop` |

## Metrics

- Success rate metric: percentage of runs producing schema-valid YAML and Markdown without degraded status.
- Quality metric: fixture ranking accuracy and percentage of candidates with complete evidence, risks, and local application fields.
- Latency metric: total run duration plus p95 GitHub API latency and p95 model-call latency.
- Cost metric: estimated cost per run, per candidate, and per adopted candidate after human review.
- Guardrail/tripwire metric: count of prohibited-source blocks, registry-write blocks, budget stops, and rate-limit degraded runs.

## Correlation

- Run/session id format: `gtra-YYYYMMDD-HHMMSS-shortsha`.
- User/request id handling: store only local actor or CI workflow id; do not store personal identifiers unless already part of GitHub audit metadata.
- Tool-call correlation id: `run_id:tool_name:sequence_number`.
- Eval/regression id link: use IDs from `eval-spec.md` and `failure-cases.md`.

## Alerting

- Alert condition: schema validation fails, prohibited-source access attempted, registry file changed during automated run, rate-limit failures exceed three consecutive runs, or cost exceeds budget.
- Owner: repository maintainer.
- First response action: stop schedule if needed, inspect run telemetry, revert unintended files, add or update failure case, then rerun dry-run validation.
