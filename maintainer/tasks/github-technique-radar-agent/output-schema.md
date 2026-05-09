# Output Schema Contract: GitHub Technique Radar Agent

Purpose: make every machine-consumed agent output parseable, versioned, and testable before implementation.

## Output Formats

- Primary format: YAML candidate file at `maintainer/radar/YYYY-MM-DD-candidates.yaml`.
- Secondary format, if any: Markdown review report at `maintainer/radar/YYYY-MM-DD.md`.
- Human-readable companion output: concise terminal summary listing output paths, candidate counts, rate-limit status, and validation result.

## Schema Version

- Current schema version: `radar_candidates.v1`.
- Backward compatibility policy: additive fields allowed; removing or renaming fields requires schema version bump and fixture migration.
- Migration owner: repository maintainer reviewing the radar PR.

## Required Fields

| Field | Type | Required? | Description | Validation Rule |
| --- | --- | --- | --- | --- |
| schema_version | string | yes | Candidate file schema identifier | Must equal `radar_candidates.v1` for the first implementation |
| generated_at | string | yes | UTC ISO-8601 timestamp | Must parse as UTC timestamp |
| config_version | string | yes | Version from `maintainer/radar-config.yaml` | Non-empty string |
| source_policy | string | yes | Discovery source policy | Must state GitHub API only and no prohibited third-party crawling |
| candidates | list | yes | Ranked repository candidates | One or more entries for successful full run; empty allowed only for dry-run fixtures |
| candidates[].rank | integer | yes | Rank after scoring | Positive integer, unique within file |
| candidates[].name | string | yes | Repository full name | Matches `owner/repo` |
| candidates[].url | string | yes | GitHub repository URL | Starts with `https://github.com/` |
| candidates[].matched_queries | list | yes | Config query labels or strings that matched | Non-empty list |
| candidates[].score | number | yes | Composite relevance score | Greater than or equal to zero |
| candidates[].signals | mapping | yes | Stars, forks, pushed date, star delta, keyword score, topic hits | Required numeric or nullable fields documented in tool contract |
| candidates[].tags | list | yes | Classification tags | Values from weekly radar classification set when possible |
| candidates[].evidence | list | yes | Short source-backed reasons | One to five concise bullets, no long copied text |
| candidates[].risks | list | yes | Maintenance, license, relevance, or security caveats | Empty list allowed only with explicit `no obvious risk found` item |
| candidates[].suggested_status | string | yes | Review recommendation | One of `rejected`, `watch`, `candidate`, `adopted-review-needed` |
| candidates[].local_application | string | yes | How this repo could improve the guide | Non-empty, concise text |

## Invalid Output Handling

- Parser behavior: load YAML, validate required fields, type checks, enum checks, URL shape, rank uniqueness, and no long copied excerpts.
- Repair attempt limit: one deterministic repair pass for missing nullable signal fields; no model repair for source URLs or review status.
- Fail-closed condition: missing schema version, invalid repository URL, duplicate ranks, prohibited source, or malformed YAML.
- Human handoff condition: candidate looks important but evidence conflicts, license is unclear, API result is incomplete, or adoption would modify registries.

## Golden Examples

### Valid Example

```yaml
schema_version: radar_candidates.v1
generated_at: '2026-05-09T00:00:00Z'
config_version: 0.4.0
source_policy: GitHub API only; prohibited third-party scraping is excluded.
candidates:
  - rank: 1
    name: example/agent-evals
    url: https://github.com/example/agent-evals
    matched_queries:
      - agent eval framework stars:>100 pushed:>=2026-01-01
    score: 8.7
    signals:
      stars: 1200
      forks: 90
      open_issues: 12
      pushed_at: '2026-05-08T12:00:00Z'
      star_delta_from_previous_radar: 80
      technique_keyword_score: 5
    tags:
      - evals
      - harness
    evidence:
      - Provides reusable eval harness patterns for agent regressions.
      - Recent activity suggests active maintenance.
    risks:
      - License and API stability require human review.
    suggested_status: candidate
    local_application: Compare fixture and regression design with this guide's eval templates.
```

### Invalid Example

```yaml
schema_version: radar_candidates.v1
candidates:
  - rank: 1
    name: prohibited-source-derived/list
    url: https://blocked.example/repositories
    suggested_status: adopted
```

Expected validation error: prohibited source URL, missing required fields, and attempted adoption without review.

## Eval Links

- Schema validation eval cases: `eval-spec.md` cases HP-001 and ISO-001.
- Regression cases from failures: `failure-cases.md` FC-001 through FC-006.
