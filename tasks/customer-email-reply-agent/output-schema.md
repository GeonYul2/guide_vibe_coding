# Output Schema Contract: customer-email-reply-agent

## Format

Primary output is JSON object `customer_email_reply.v0.1` plus a Markdown summary for human review.

## Required Fields

- `schema_version`: must equal `customer-email-reply-agent.v0.1`.
- `message_id`: input email identifier.
- `classification`: one of `routine`, `needs_more_info`, `high_risk`, `out_of_scope`.
- `draft_reply`: proposed customer-facing text, empty when handoff is required.
- `policy_sources`: list of `{title, url_or_id, excerpt_summary, retrieved_at}`.
- `confidence`: number from 0.0 to 1.0.
- `handoff_required`: boolean.
- `handoff_reason`: clear reason when handoff is true.
- `sensitive_data_detected`: list of redacted data categories.
- `review_checklist`: list of human checks before sending.

## Validation Rules

The parser fails closed if required fields are missing, confidence is outside range, policy sources are absent for routine replies, or handoff is false for legal, refund exception, privacy, security, or policy-conflict cases. One repair attempt is allowed for formatting errors only.
