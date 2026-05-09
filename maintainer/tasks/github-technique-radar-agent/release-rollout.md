# Release, Rollout, and Canary Plan: GitHub Technique Radar Agent

Purpose: prevent prototype behavior from being silently promoted to production automation.

## Release Stages

| Stage | Audience / Traffic | Entry Criteria | Exit Criteria | Owner |
| --- | --- | --- | --- | --- |
| local | maintainer or coding agent dry run | required artifacts validated and dry-run command available | schema-valid fixture output and no prohibited-source access | repository maintainer |
| internal_canary | manual GitHub API run with low limits | local stage passed, token budget configured, cache enabled | two successful low-limit runs with reviewed candidate quality | repository maintainer |
| production | manual maintainer GitHub Actions run creating review artifacts or PR | canary passed, kill switch documented, telemetry and guardrails active | four consecutive successful maintainer runs with acceptable quality and no budget incidents | repository maintainer |

## Kill Switch and Rollback

- Kill switch location: disable `.github/workflows/weekly-repo-radar.yml`, set workflow schedule off, or set a `RADAR_DISABLED=1` environment flag if implemented.
- Rollback command/process: revert the commit or PR that changed radar script, config, schema, or schedule; keep reviewed prior radar artifacts unless they contain bad data.
- Data/state recovery plan: delete corrupt cache, restore last known valid radar output from git, and rerun with fixture mode before live mode.
- User communication plan: PR or issue comment states failure reason, changed files, degraded status, and next review action.

## Post-Deploy Monitoring

- Canary eval command: `python3 maintainer/scripts/weekly_repo_radar.py --dry-run --limit 3` followed by schema validation for generated candidate YAML.
- Success threshold: schema-valid outputs, no forbidden source, no unapproved registry diff, and at least 80% reviewer acceptance of top candidates during canary.
- Failure threshold: any prohibited-source attempt, secret leak, registry auto-edit, repeated API budget failure, or invalid output in two consecutive runs.
- Review window: weekly for manual runs and immediately after script, config, or schema changes.

## Change Management

- Approval owner: repository maintainer.
- Release notes location: radar PR description or `maintainer/radar/YYYY-MM-DD.md` summary section.
- Prompt/schema/tool contract version bump required when: candidate YAML fields change, scoring rubric changes materially, model summarization prompt changes, or tool permissions expand.
