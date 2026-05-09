# Security, Privacy, and Data Governance: GitHub Technique Radar Agent

Purpose: define how the agent protects company data, customer data, credentials, and logs.

## Data Classification

| Data Type | Classification | Allowed Use | Forbidden Use | Storage / Retention |
| --- | --- | --- | --- | --- |
| Public GitHub repository metadata | public | ranking, scoring, tags, and review artifacts | misrepresenting adoption or copying project content wholesale | retained in radar artifacts while useful |
| Public repository file snippets | public with copyright constraints | concise evidence extraction and source-backed summaries | long copied excerpts, vendoring, or unbounded storage | cache expires within thirty days; summaries retained |
| GitHub token | secret | authenticated API requests with least privilege | logs, artifacts, cache, prompts, or commits | environment only; rotate if exposed |
| CI logs and telemetry | internal operational | debugging, audit, budget tracking | storing secrets or unnecessary personal data | 30 to 90 days depending on event type |
| Human review notes | internal project data | adoption decisions and risk tracking | publishing private comments without approval | retained in PR or local registry as appropriate |

## Access Control

- Required permissions: read-only public GitHub API access for discovery; `contents:read` and PR creation only if workflow is explicitly configured for review PRs.
- Least-privilege rule: use the lowest scope token that can read public metadata; no private repo scopes for default operation.
- Credential/secret handling: read tokens from environment variables only, redact from logs, never write to cache or artifacts.
- Rotation or revocation plan: revoke token immediately if telemetry, cache, or output contains a token-like value; rerun with a new token after redaction.

## Privacy Controls

- PII detection/redaction: redact unnecessary emails, personal contact details, and token-like strings from fetched snippets and telemetry.
- Sensitive prompt/log redaction: store hashes or concise summaries for prompts containing external text; never store Authorization headers.
- Data deletion process: remove cache entries and generated artifacts with sensitive data, then document the incident in failure memory.
- Cross-border/regulated data constraint, if any: default source set is public GitHub data; do not add regulated or customer data sources without a new security review.

## Audit and Compliance

- Audit log fields: run id, actor or workflow id, source URL, allowed-source decision, output paths, changed files, token usage, cost estimate, guardrail events.
- Reviewer/owner: repository maintainer.
- Review cadence: with each radar PR review, plus immediate review after any guardrail or secret incident.
- Incident escalation: stop manual workflow, revoke affected credentials, remove sensitive artifacts, add regression case, and require maintainer approval before resuming.
