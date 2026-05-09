# Readiness Scorecard: customer-email-reply-agent

## Summary

Overall readiness: 72 / 100 for prototype design. The intake, PRD, technique selection, schema, guardrails, and token gate are explicit enough for planning, but implementation should wait for real policy source ownership and CRM/review-queue contracts.

## Gap Map

- Intent and users: clear enough for prototype.
- Inputs and outputs: clear with simulated assumptions.
- Tool contracts: draft contracts exist; real systems need confirmation.
- Evals: fixture plan exists; dataset must be built.
- Security: high importance due to customer data and PII.
- Release: draft-only canary required before production use.

## Scoring Rubric

| Area | Weight | Score | Evidence | Missing / Risk | Required Before Implementation? |
| --- | ---: | ---: | --- | --- | --- |
| Intent and user outcome | 8 | 7 / 8 | Intake and PRD define the customer email reply workflow | Real support-team owner confirmation pending | yes |
| Scope and non-goals | 6 | 5 / 6 | Automatic external sending and unsupported commitments are excluded | Final production boundaries need owner signoff | yes |
| Input/output schema | 8 | 6 / 8 | Reply draft, evidence, confidence, and handoff fields are defined | Parser fixtures and schema implementation pending | yes |
| Technique selection | 6 | 6 / 6 | Every registry technique is selected or rejected with a reason | no gap in artifact | yes |
| Harness and eval plan | 8 | 5 / 8 | Fixture plan covers policy, ambiguity, and unsafe cases | Dataset must be built | yes |
| Failure-case memory | 7 | 5 / 7 | Known policy and safety failures are documented | Needs observed production-like failures | yes |
| Guardrails and tripwires | 7 | 6 / 7 | Refund, legal, security, and PII handoff rules are defined | Runtime enforcement pending | yes |
| Tool contracts and permissions | 7 | 4 / 7 | Draft contracts for email, policy search, and review queue exist | Real CRM and queue contracts need confirmation | yes |
| Retrieval and memory governance | 6 | 4 / 6 | Source hierarchy and freshness rules are drafted | Policy source ownership is unresolved | yes when retrieval/memory exists |
| Token efficiency, cost, caching, and model routing | 10 | 8 / 10 | Token ceilings, cache target, pruning, fallback, and telemetry are explicit | Pricing and live cache metrics pending | yes |
| Telemetry and traceability | 7 | 4 / 7 | Trace events and quality metrics are defined | Dashboard and alert routing pending | yes |
| Security and privacy | 7 | 5 / 7 | PII, logs, and access rules are covered | Formal security review pending | yes when company/customer/internal data exists |
| Release, rollout, and rollback | 6 | 3 / 6 | Canary and kill-switch plan exists | Production rollout criteria need approval | yes when production/scheduled use exists |
| Human approval / handoff | 7 | 4 / 7 | Handoff boundaries are described | Reviewer roster and SLA pending | yes |

## Gate Decision

Ready for prototype artifact design, not ready for live integration or automatic external sending.
