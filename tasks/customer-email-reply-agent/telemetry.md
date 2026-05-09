# Telemetry: customer-email-reply-agent

## Events

- `email_received`: message id, size, language, redaction count.
- `retrieval`: policy query, source ids, freshness, latency, cache hit.
- `model_call`: task class, model tier, tokens, latency, cost.
- `schema_validation`: pass flag, error class, repair attempt count.
- `guardrail`: trigger, action, blocked tool, handoff reason.
- `review_queue_write`: idempotency key, status, latency.

## Redaction

Do not log raw customer text, email addresses, tokens, card numbers, national identifiers, or policy excerpts beyond short approved summaries.
