# Tool Contracts: GitHub Technique Radar Agent

Repeat this section for each tool, API, script, database, browser, or internal system.

## Tool: GitHub REST Search API

- Purpose: Discover public repositories matching configured agent-engineering queries.
- Owner: GitHub; local usage owned by guide maintainer.
- Permission required: unauthenticated public access for small runs; optional least-privilege `GITHUB_TOKEN` for manual runs.
- Input schema: query string, sort field, order, per-page limit, page, API version header.
- Output schema: repository items with full name, URL, description, stars, forks, topics when available, pushed timestamp, open issues, license, and owner metadata.
- Timeout: 20 seconds per request.
- Retry policy: retry network failures up to two times with exponential backoff; obey `retry-after` and `x-ratelimit-reset`.
- Idempotency: read-only and safe to repeat with same query and timestamp.
- Rate limits: respect primary and secondary GitHub limits; authenticated requests preferred for manual runs.
- Secrets required: optional token via environment variable; never written to logs or artifacts.
- Error classes: rate limited, unauthorized, network timeout, malformed response, abuse detection, partial result.
- Fallback behavior: use cached response if fresh; otherwise reduce query count and mark run degraded.
- Human approval required when: new credential scope, private repository access, or write action is requested.
- Guardrail/tripwire link: GitHub API rate-budget tripwire in `guardrails.md`.
- Logging / redaction rules: log endpoint category, query hash, status, duration, and rate headers; redact token and full Authorization header.

## Tool: GitHub Repository Contents API

- Purpose: Fetch selected lightweight files such as README, docs index, package metadata, and release metadata for technique evidence.
- Owner: GitHub; local usage owned by guide maintainer.
- Permission required: public read or optional least-privilege token.
- Input schema: owner, repo, path from allowlist, ref, max bytes.
- Output schema: file path, encoding, decoded text snippet, SHA, size, URL.
- Timeout: 20 seconds per request.
- Retry policy: same as REST Search API.
- Idempotency: read-only.
- Rate limits: shared GitHub REST budget.
- Secrets required: optional token only.
- Error classes: not found, file too large, binary file, rate limited, decode error.
- Fallback behavior: rely on repository metadata and mark evidence as metadata-only.
- Human approval required when: fetching private repository content or expanding allowlist beyond lightweight source files.
- Guardrail/tripwire link: copied-content and private-data output guardrails.
- Logging / redaction rules: log file path and byte count; never log full large file content.

## Tool: `maintainer/scripts/weekly_repo_radar.py`

- Purpose: Execute configured discovery, scoring, and radar artifact generation.
- Owner: this repository.
- Permission required: local read/write to `maintainer/radar/` and cache directory; optional network access to GitHub.
- Input schema: config path, date, dry-run flag, per-query limit, output directory, optional cache path.
- Output schema: Markdown report, YAML candidates file, terminal summary, exit code.
- Timeout: 10 minutes local; 20 minutes manual workflow.
- Retry policy: delegates API retries to GitHub client; script-level retry is not automatic to avoid duplicate confusing reports.
- Idempotency: same date and config overwrites or updates the same radar files only when explicitly requested.
- Rate limits: enforced through GitHub client.
- Secrets required: optional `GITHUB_TOKEN`.
- Error classes: config invalid, API failure, schema invalid, output write failure, budget exceeded.
- Fallback behavior: dry-run with cached fixtures or reduced limit.
- Human approval required when: output path is outside allowed radar directory or registry modification is requested.
- Guardrail/tripwire link: local file write and registry modification tripwires.
- Logging / redaction rules: log run id, config version, counts, degraded status, and validation summary.

## Tool: `scripts/validate_agent_task.py`

- Purpose: Validate this task's required design artifacts before implementation claims.
- Owner: this repository.
- Permission required: local read access to task folder and guide config.
- Input schema: task directory path.
- Output schema: pass or failure lines with missing artifact and placeholder errors.
- Timeout: 30 seconds.
- Retry policy: no retry; fix artifacts then rerun.
- Idempotency: read-only.
- Rate limits: none.
- Secrets required: none.
- Error classes: missing directory, missing required file, placeholder remains, token gate incomplete.
- Fallback behavior: manual review against playbook if script unavailable.
- Human approval required when: none for read-only validation.
- Guardrail/tripwire link: pre-implementation gate.
- Logging / redaction rules: no sensitive fields expected.

## Tool: Local Cache Files

- Purpose: Store GitHub API responses, repository metadata summaries, ETags, and previous score snapshots for cost and rate-limit control.
- Owner: this repository maintainer.
- Permission required: local write to approved cache path.
- Input schema: cache key, source URL, response metadata, fetched timestamp, expiry timestamp, redacted response body.
- Output schema: cache hit or miss, cached payload, freshness status.
- Timeout: local file operations under 5 seconds.
- Retry policy: no retry beyond one re-read; corrupt cache is ignored and replaced.
- Idempotency: cache writes are keyed and replace stale entries.
- Rate limits: not applicable.
- Secrets required: none; tokens forbidden in cache.
- Error classes: corrupt cache, stale cache, permission denied, schema mismatch.
- Fallback behavior: live API request if budget allows; otherwise degraded stop.
- Human approval required when: cache path leaves repository or contains private data.
- Guardrail/tripwire link: privacy and cache invalidation rules.
- Logging / redaction rules: log key hash and freshness, not full content when content may contain accidental secrets.
