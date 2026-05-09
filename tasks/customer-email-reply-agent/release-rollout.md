# Release and Rollout: customer-email-reply-agent

## Stages

1. Local fixture prototype: mocked email, policy search, and review queue.
2. Internal canary: 2 support agents review draft-only outputs for 50 emails.
3. Limited production assist: draft-only mode for one queue with daily quality review.

## Kill Switch

Disable the agent with `CUSTOMER_EMAIL_REPLY_AGENT_ENABLED=false` and route all messages to normal manual handling. Rollback removes review queue integration and preserves redacted traces for incident review.
