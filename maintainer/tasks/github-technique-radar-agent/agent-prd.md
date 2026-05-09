# Agent PRD: GitHub Technique Radar Agent

## Problem

Some third-party trending sites cannot be crawled or scraped without permission, but this guide still needs a compliant way to discover useful agent-engineering techniques from public repositories. The agent should turn GitHub-first discovery into a repeatable, reviewable update loop that improves this repository without copying external projects.

## Primary Users

- Maintainers of this Agent Engineering Guide.
- Coding agents using this repository to design or improve automation agents.
- Human reviewers deciding whether a discovered repository should become a watched, candidate, adopted, or rejected source.

## Desired Outcome

A weekly or manual GitHub-first radar run produces ranked repository candidates, concise technique evidence, structured metadata, and review instructions under `maintainer/radar/`, without using prohibited third-party trending-site data or violating third-party terms.

## Inputs

- `maintainer/radar-config.yaml` queries, filters, scoring factors, and review policy.
- GitHub REST or GraphQL public repository metadata.
- Previous radar outputs for star-delta comparison.
- Local registries: `repos/registry.yaml`, `techniques/registry.yaml`, `techniques/taxonomy.yaml`, and `sources/registry.yaml` when supplemental sources are explicitly provided.

## Outputs

- `maintainer/radar/YYYY-MM-DD.md` human-readable ranked report.
- `maintainer/radar/YYYY-MM-DD-candidates.yaml` structured candidate metadata.
- Optional concise summaries under `repos/summaries/` after review.
- No automatic modification of `repos/registry.yaml` or mandatory technique lists without human review.

## In Scope

- Discover repositories through GitHub APIs and configured GitHub search queries.
- Score candidates using public metadata, recent activity, topic/keyword relevance, and delta from prior radar snapshots.
- Extract reusable technique signals from repository metadata and selected lightweight files such as README, docs index, examples index, and release metadata.
- Deduplicate repositories across queries and previous registries.
- Produce review artifacts with evidence, risks, tags, and local application guidance.
- Respect GitHub API rate limits, secondary limits, and conditional request best practices.

## Non-Goals

- Recreating third-party proprietary rankings exactly.
- Crawling any site that forbids automated extraction.
- Vendoring, mirroring, or copying entire external repositories.
- Auto-promoting candidates into `repos/registry.yaml`.
- Adding new mandatory techniques without human review and enforcement updates.
- Performing vulnerability audits of candidate projects beyond lightweight risk notes.

## Autonomy Boundaries

### Agent May Do Autonomously

- Run local radar scripts and validators.
- Query GitHub public APIs within rate and budget limits.
- Create or update `maintainer/radar/` artifacts.
- Cache API responses and previous snapshots.
- Mark uncertain evidence as candidate, watch, or needs-review.

### Requires Human Approval

- Moving a candidate into `repos/registry.yaml` as adopted.
- Changing `techniques/registry.yaml`, `techniques/taxonomy.yaml`, required templates, or mandatory gates.
- Using credentials beyond a least-privilege GitHub token.
- Running production schedules or publishing review PRs from a new environment.

## Success Criteria

- A local dry run produces both radar output files with valid structured metadata.
- At least 95% of candidates include source URL, description, tags, score, evidence, risks, and suggested review status.
- Duplicate repositories are collapsed across queries.
- The run does not access prohibited third-party trending sites.
- The task validator passes before implementation starts.
- Radar outputs are small enough for human review and do not contain copied long-form third-party content.

## Failure Criteria

- The agent scrapes prohibited sources or bypasses robots/TOS restrictions.
- The agent exhausts GitHub primary or secondary limits without backoff.
- Output schema is invalid or missing required fields.
- Candidates are promoted without review.
- Token, API, or cost limits are exceeded without safe stop.

## Open Questions

- Whether the first prototype should use REST only or GraphQL plus REST; default is REST-first because the existing script already uses GitHub Search API patterns.
- Whether authenticated GitHub access is available in CI; default is optional `GITHUB_TOKEN` with unauthenticated degraded mode for small manual tests.
