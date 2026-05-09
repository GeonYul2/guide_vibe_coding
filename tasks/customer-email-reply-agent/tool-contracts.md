# Tool Contracts: customer-email-reply-agent

## Tool: Email Reader

Purpose: read inbound customer email text and limited metadata. Permission: read-only. Timeout: 5 seconds. Failure modes: unavailable, malformed message, unsupported attachment. Retry once for transient errors.

## Tool: Policy Search

Purpose: retrieve relevant approved policy snippets. Permission: read-only. Input includes normalized query and policy collection id. Output includes document id, title, snippet summary, timestamp, and confidence. Timeout: 8 seconds. Never fabricate missing policies.

## Tool: Review Queue Writer

Purpose: save draft and handoff package for a 상담원. Permission: internal draft write only. Idempotency key is message id plus schema version. External customer sending is forbidden and requires a separate human-owned system.
