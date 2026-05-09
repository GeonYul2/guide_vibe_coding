# Guardrails: customer-email-reply-agent

## Input Guardrails

Detect sensitive data, legal threats, refund or compensation demands, account access requests, policy conflicts, and unsupported languages. Redact sensitive data before logging and route risky cases to human review.

## Output Guardrails

Do not promise refunds, compensation, legal conclusions, security remediation, or policy exceptions. Every routine reply must cite policy sources and include a human review checklist. If grounding is weak, produce a handoff instead of a confident answer.

## Tool Tripwires

SMTP sending, payment mutation, account permission changes, policy document edits, and raw sensitive-data persistence are blocked. Any attempt to access forbidden tools becomes a telemetry event and human handoff.
