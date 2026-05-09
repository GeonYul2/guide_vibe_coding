# Implementation Plan: customer-email-reply-agent

## Steps

1. Confirm policy source, CRM metadata, review queue, and email access boundaries through deep interview.
2. Build fixture dataset with routine, ambiguous, privacy, legal, refund, and retrieval-failure emails.
3. Implement schema validator and guardrail classifier before draft generation.
4. Implement mocked policy retrieval and draft-only review queue writer.
5. Run fixture evals and convert every failure into `failure-cases.md`.
6. Add telemetry for retrieval, model calls, schema validation, guardrails, handoff, and costs.
7. Run canary only after validator and fixture evals pass.

## Verification Commands

- `python3 scripts/validate_agent_task.py tasks/customer-email-reply-agent`
- Future harness command: `python3 scripts/test_customer_email_reply_agent.py`
