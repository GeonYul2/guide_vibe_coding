# Maintainer Tools

This folder is **not required** for ordinary users who clone the repo to design an automation agent.

Use it only when maintaining the playbook itself: discovering new agent-engineering repositories, reviewing technique candidates, updating source-backed techniques, or running the optional manual GitHub radar.

It also owns the user-distribution export/publish flow. Ordinary users should receive the exported subset, not this whole source/maintainer tree.

## Ordinary user path

From the repo root, users normally need only:

```bash
python3 scripts/new_agent_task.py "my-agent"
python3 scripts/validate_agent_task.py tasks/my-agent
```

They should follow `README.md`, `AGENTS.md`, `agent-playbook.yaml`, `workflows/build-agent.md`, `techniques/registry.yaml`, and `templates/`.

## Maintainer path

Run the optional radar only when refreshing techniques:

```bash
python3 maintainer/scripts/weekly_repo_radar.py --date "$(date -u +%F)" --limit 10
```

Maintainer-only files:

- `maintainer/scripts/weekly_repo_radar.py` — GitHub Search API radar generator
- `maintainer/scripts/export_user_distribution.py` — copies only manifest-selected user-facing files into a target checkout
- `scripts/generate_repo_score_report.py` — source-repo readiness scorer that emits `reports/repo-readiness-report.html`
- `maintainer/radar-config.yaml` — search/scoring/filter config
- `maintainer/radar/` — generated candidate review artifacts
- `maintainer/workflows/weekly-repo-radar.md` — review and promotion process
- `maintainer/workflows/publish-user-distribution.md` — export/publish process for the user-facing distribution repository
- `maintainer/tasks/github-technique-radar-agent/` — design artifacts for the radar agent itself

## User distribution export

Local dry run:

```bash
python3 maintainer/scripts/export_user_distribution.py \
  --dest /path/to/user-distribution-checkout \
  --dry-run
```

Publish path:

- Manifest: `distribution/user-export-manifest.yaml`
- User-facing overrides: `distribution/user/`
- Manual PR workflow: `.github/workflows/publish-user-distribution.yml`
- Required source-repo secret for PR publishing: `USER_DISTRIBUTION_TOKEN`

The export must not copy `maintainer/`, GitHub radar/update workflows, generated `wiki/`, `.omx/`, `.obsidian/`, or sample tasks into the user distribution.

## Repository readiness report

Generate a local HTML score report from the source/maintainer repository:

```bash
python3 scripts/generate_repo_score_report.py --run-tests
```

Output:

- `reports/repo-readiness-report.html` — local visual report
- `reports/repo-readiness-report.json` — machine-readable evidence

This report is maintainer-facing and is intentionally excluded from the user distribution. It treats sample/prototype task scores as portfolio visibility when their validators pass and their gate decisions explicitly bound live-use readiness.

## Two-repository publish boundary

Use two separate pushes:

1. Source/maintainer repo — commit and push source-of-truth changes here first.
2. User distribution repo — run `maintainer/scripts/export_user_distribution.py --prune-excluded --prune-stale` into the separate user checkout, review the diff, then push that repo separately.

Do not push generated maintainer-only reports, radar outputs, wiki, `.omx`, `.obsidian`, or sample tasks to the user distribution repo.

## Adoption rule

Radar candidates are never adopted automatically. A human maintainer reviews candidates, then updates `repos/registry.yaml`, `techniques/registry.yaml`, `techniques/taxonomy.yaml`, workflows, templates, and tests only when a reusable pattern is verified.
