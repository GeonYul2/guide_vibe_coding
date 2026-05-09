# Retrieval and Memory Governance: GitHub Technique Radar Agent

Purpose: prevent stale, private, or unsupported context from becoming hidden agent behavior.

## Source-of-Truth Hierarchy

1. Local control files: `agent-playbook.yaml`, `maintainer/radar-config.yaml`, `maintainer/workflows/weekly-repo-radar.md`, `techniques/registry.yaml`, and `techniques/taxonomy.yaml`.
2. GitHub official APIs and response headers for repository metadata, rate limits, and source file access.
3. Public repository files fetched through allowed GitHub API endpoints with byte and path limits.
4. Human-reviewed local registries and summaries.
5. Supplemental articles, videos, and release notes only through `workflows/source-ingestion.md`, not as a replacement for GitHub-first discovery.

## Retrieval Scope

- Allowed sources: GitHub REST or GraphQL APIs, public GitHub repository metadata, approved local registries, prior radar outputs, and explicitly registered supplemental sources.
- Forbidden sources: automated extraction from sites that prohibit scraping, private repositories without approval, copied full repositories, and unregistered third-party bulk datasets.
- Citation/source-reference requirement: every candidate must include a GitHub URL and concise evidence tied to metadata or allowed files.
- Freshness requirement: manual radar metadata should be no older than seven days; cached repository file snippets expire after thirty days or on changed SHA.

## Memory Types

| Memory Type | Stored Data | Retention | Owner | Deletion Rule |
| --- | --- | --- | --- | --- |
| session | run id, query hashes, candidate ids, errors, and validation status | duration of run plus local logs | radar maintainer | delete after report is reviewed or when logs exceed retention |
| long_term | prior radar candidate YAML, reviewed registry entries, concise summaries, score snapshots, ETags | retained in repo while useful for trend deltas and audits | repository maintainer | remove when source is rejected, stale, or no longer relevant |
| cache | API payloads, ETags, fetched timestamps, and reduced README snippets | seven to thirty days depending on data type | repository maintainer | invalidate on config change, repository SHA change, schema version bump, or privacy issue |

## Indexing and Invalidation

- Index update cadence: weekly manual run and manual dispatch when maintainers request a refresh.
- Cache/index invalidation trigger: query config change, schema version change, repository `pushed_at` change, README SHA change, expired TTL, or guardrail violation.
- Stale memory detection: compare generated timestamp, config version, source URL, and ETag or last modified metadata.
- Conflict resolution rule: local reviewed registry decisions override new automated scores; conflicting evidence is marked for human review rather than auto-updated.

## Privacy Controls

- PII/secret filtering rule: scan fetched text for token-like and secret-like patterns; do not store matches in artifacts.
- Redaction before storage: replace credentials, emails where unnecessary, and Authorization headers with redaction markers.
- Audit log requirement: record source URL, fetch time, cache status, schema version, and redaction count without storing secrets.
