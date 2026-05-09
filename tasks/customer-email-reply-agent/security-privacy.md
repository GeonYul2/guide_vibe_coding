# Security and Privacy: customer-email-reply-agent

## Data Classification

Customer email content and CRM metadata are confidential. Payment identifiers, government ids, credentials, and health or legal details are restricted. Public help-center policy pages are public, while internal policies are confidential.

## Controls

Use least privilege: read-only email, read-only policy search, draft-only review queue writes. Redact sensitive data before logs and model prompts when feasible. Retain traces for 30 days with redaction; raw messages remain in the source email system.

## Audit

Security owner reviews blocked tool attempts, redaction failures, and handoff misses weekly during canary.
