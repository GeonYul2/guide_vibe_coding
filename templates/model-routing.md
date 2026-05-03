# Model Routing and Fallback Policy: <task-slug>

Purpose: choose models by task risk, difficulty, cost, latency, and required quality.

## Routing Matrix

| Task Class | Default Model / Tier | Escalation Model / Tier | Max Input Tokens | Max Output Tokens | Max Cost | Latency Target | Quality Gate |
| --- | --- | --- | ---: | ---: | ---: | --- | --- |
| TODO | TODO | TODO | TODO | TODO | TODO | TODO | TODO |

## Fallback Order

1. TODO: primary path
2. TODO: degraded but acceptable path
3. TODO: human handoff or safe stop

## Retry Policy

- Retryable failures: TODO
- Non-retryable failures: TODO
- Max retries: TODO
- Backoff: TODO

## Budget Controls

- Per-run ceiling: TODO
- Daily/weekly ceiling: TODO
- Stop condition: TODO
- User-facing message when degraded: TODO
