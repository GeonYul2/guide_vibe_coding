# Cost and Caching Plan: <task-slug>

Purpose: token usage is operating cost. Implementation is blocked until this file defines measurable token, cache, routing, and telemetry limits.

## Token Efficiency Hard Gate

- Max input tokens per run:
- Max output tokens per run:
- Max total tokens per run:
- Max model calls per run:
- Cost ceiling per successful run:
- Cost ceiling per day/week/month:
- Required cache hit-rate target:
- Required context pruning rule:
- Required summarization/compression trigger:
- Stop condition when token or cost budget is exceeded:

## Cost Budget

- Expected model calls per run:
- Expected token range per run:
- Budget per run:
- Budget per day/week/month:
- Stop condition when budget is exceeded:

## Context Strategy

- Required context:
- Optional context:
- Context exclusion rules:
- Context compression/summarization plan:
- Deduplication rule:
- Maximum retrieved chunks / files / messages:

## Caching Strategy

- Cacheable inputs/context:
- Cache key:
- Cache storage:
- Invalidation rule:
- Stale-cache risk:
- Privacy/security constraints:
- Prompt/prefix caching opportunity:

## Fallback Strategy

- Cheaper model fallback:
- Reduced-context fallback:
- Retrieval-only or summary-only fallback:
- Human handoff condition:

## Token Telemetry Requirements

- Track input tokens:
- Track output tokens:
- Track cache hits/misses:
- Track cost per run:
- Track budget-exceeded stops:
- Dashboard or log query:

## Optimization Checklist

- Remove irrelevant context before adding more context:
- Prefer structured compact output over prose:
- Reuse stable system/developer prompts through caching:
- Summarize or index long documents before full-context use:
- Batch or deduplicate repeated requests:
- Use cheaper model tier when quality gate allows:

## Related Contracts

- Model routing policy: model-routing.md
- Retrieval and memory governance: retrieval-memory.md
- Telemetry/cost events: telemetry.md
