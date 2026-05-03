# Telemetry and Trace Contract: <task-slug>

Purpose: make model, tool, retrieval, cache, cost, latency, and quality behavior observable without leaking secrets.

## Trace Events

| Event | Required Fields | Redaction Rule | Retention | Dashboard / Query |
| --- | --- | --- | --- | --- |
| model_call | TODO | TODO | TODO | TODO |
| tool_call | TODO | TODO | TODO | TODO |
| retrieval | TODO | TODO | TODO | TODO |
| cache | TODO | TODO | TODO | TODO |
| eval_result | TODO | TODO | TODO | TODO |
| handoff | TODO | TODO | TODO | TODO |

## Metrics

- Success rate metric: TODO
- Quality metric: TODO
- Latency metric: TODO
- Cost metric: TODO
- Guardrail/tripwire metric: TODO

## Correlation

- Run/session id format: TODO
- User/request id handling: TODO
- Tool-call correlation id: TODO
- Eval/regression id link: TODO

## Alerting

- Alert condition: TODO
- Owner: TODO
- First response action: TODO
