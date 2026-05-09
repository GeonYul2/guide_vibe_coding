# Model Routing and Fallback Policy: GitHub Technique Radar Agent

Purpose: choose models by task risk, difficulty, cost, latency, and required quality.

## Routing Matrix

| Task Class | Default Model / Tier | Escalation Model / Tier | Max Input Tokens | Max Output Tokens | Max Cost | Latency Target | Quality Gate |
| --- | --- | --- | ---: | ---: | ---: | --- | --- |
| Query expansion and metadata scoring | deterministic Python | not applicable | 0 | 0 | USD 0.00 | under 2 minutes | Schema-valid candidates and stable scores |
| First-pass tag classification | cheap model or deterministic keyword rules | standard model for ambiguous top candidates | 20000 | 5000 | USD 0.50 | under 5 minutes | Tags match taxonomy and eval fixtures |
| Technique evidence summarization | standard model | frontier model for high-impact ambiguous candidate | 60000 | 15000 | USD 1.50 | under 10 minutes | Evidence is source-backed, concise, and non-copied |
| Final report synthesis | standard model or deterministic renderer | frontier model only for release-blocking inconsistencies | 20000 | 10000 | USD 0.50 | under 3 minutes | Markdown matches YAML and contains degraded status if needed |
| Guardrail or adoption decision | deterministic rules plus human handoff | human reviewer | 5000 | 1000 | USD 0.05 | immediate | No auto-adoption or prohibited-source access |

## Fallback Order

1. Primary path: GitHub API metadata, cached snippets, deterministic scoring, schema validation, and optional model summaries for top candidates.
2. Degraded but acceptable path: cached or metadata-only report with lower confidence and `watch` statuses for uncertain candidates.
3. Human handoff or safe stop: budget exceeded, rate-limited without fresh cache, prohibited source, invalid schema, or registry modification request.

## Retry Policy

- Retryable failures: transient network errors, 5xx GitHub responses, timeout, and malformed optional snippet payload when metadata remains valid.
- Non-retryable failures: prohibited source, invalid credentials, path outside allowlist, schema-breaking output, or direct adoption request.
- Max retries: two API retries per request and one model retry for invalid summary format.
- Backoff: exponential backoff starting at 2 seconds; obey `retry-after` and `x-ratelimit-reset` when provided.

## Budget Controls

- Per-run ceiling: USD 2.00 prototype target and USD 5.00 full maintainer maximum.
- Daily/weekly ceiling: USD 5.00 daily and USD 15.00 weekly.
- Stop condition: projected next call would exceed token, model-call, API, or cost budget.
- User-facing message when degraded: Radar completed in degraded mode with metadata-only evidence because budget, cache, or API limits prevented full summarization.
