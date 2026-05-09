# Workflow: Publish User Distribution

Purpose: publish only the user-facing automation-agent helper subset from this source/maintainer repository into a separate user distribution repository.

## Boundary

- Source repo keeps maintainer-only technique radar, discovery scripts, the full generated maintainer wiki, and publish automation.
- User distribution repo receives only paths declared in `distribution/user-export-manifest.yaml`.
- The user distribution does not receive `.github/workflows/weekly-repo-radar.yml`, `maintainer/`, `.omx/`, `.obsidian/`, the full generated maintainer `wiki/`, or sample tasks.
- The user distribution does receive the curated user wiki from `distribution/user/wiki/` as `wiki/` so cloned user repos can route intake and technique selection with less context.

## Local Export

```bash
python3 maintainer/scripts/export_user_distribution.py \
  --dest /path/to/user-distribution-checkout \
  --prune-excluded \
  --prune-stale
```

Use `--dry-run` first when the target checkout is not dedicated to this distribution. `--prune-stale` only removes paths recorded in the previous export stamp as copied by this exporter; unknown target files are preserved.

## GitHub PR Publish

Manual workflow: `.github/workflows/publish-user-distribution.yml`

Required secret in the source repo:

- `USER_DISTRIBUTION_TOKEN` — a GitHub token with permission to read/write the target distribution repository and open PRs.

Manual inputs:

- `target_repository`: target repo, for example `owner/agent-guide-user`
- `target_branch`: base branch, usually `main`
- `dry_run`: default `true`; set `false` only when the diff is expected
- `prune_excluded`: default `true`; removes legacy excluded paths from a dedicated distribution repo
- `prune_stale`: default `true`; removes previously exported paths no longer managed by the manifest

## Review Rules

1. Review the workflow dry-run diff first.
2. Confirm no maintainer/update logic is present in the target diff, and that `wiki/` contains only the curated user wiki.
3. Open a PR into the user distribution repository.
4. Do not give the user distribution repository radar credentials, PATs, or discovery workflows.
