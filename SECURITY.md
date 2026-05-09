# Security Posture

This repository is designed to be safe to clone into a company repository as an agent-engineering guide.

## Clone Safety

- Markdown/YAML files in this repo are inert text and do not execute by themselves.
- The Python scripts use only the Python standard library; there are no package manager dependencies or install hooks.
- External GitHub repositories are never vendored, cloned, mirrored, or executed by the maintainer-only manual radar.
- Maintainer radar output stores metadata only: names, URLs, descriptions, topics, stars, and review status.
- Company/internal knowledge should not be committed into this guide repository.

## CI / Automation Boundaries

- `.github/workflows/validate.yml` has read-only repository permissions.
- `.github/workflows/weekly-repo-radar.yml` is maintainer-only and needs `contents: write` and `pull-requests: write` only to create a review branch and PR under `maintainer/radar/`.
- `.github/workflows/publish-user-distribution.yml` is maintainer-only and uses a source-repo `USER_DISTRIBUTION_TOKEN` secret only when a maintainer manually publishes a subset PR to a separate user distribution repository.
- The manual radar workflow uses the default `GITHUB_TOKEN`; do not add PATs, cloud keys, production secrets, or internal API credentials.
- The manual radar calls only the GitHub Search API and writes candidate review artifacts. It does not execute code from candidate repositories.
- The user distribution export is manifest-bounded by `distribution/user-export-manifest.yaml`; maintainer radar/update logic must stay out of exported user repositories.

## Company Adoption Checklist

Before enabling this in a company repository:

1. Review all GitHub Actions workflows.
2. Keep Actions disabled if your security team has not approved automatic jobs.
3. Do not run these workflows on privileged self-hosted runners for untrusted pull requests.
4. Keep `repos/registry.yaml` metadata-only; do not paste source code from third-party repositories.
5. Keep internal documents, secrets, customer data, and credentials out of `tasks/`, `sources/`, and `maintainer/radar/`.
6. If the company requires stricter control, disable `.github/workflows/weekly-repo-radar.yml` and run `maintainer/scripts/weekly_repo_radar.py` manually in a sandbox.

## Threat Model

| Threat | Current Control |
| --- | --- |
| Malicious external repo code execution | Repos are metadata-only; no clone/install/execute step. |
| Secret leakage | No secrets in repo; workflows should not receive company secrets. |
| Pull request CI abuse | Validation workflow uses read-only permissions. |
| Scheduled workflow write access | Weekly workflow writes only generated radar artifacts and opens a PR for review. |
| Markdown/script surprise execution | Markdown is inert; scripts are explicit and stdlib-only. |

## Non-Guarantee

No repository can be declared impossible to misuse. The safe operating assumption is: cloning is low-risk, but enabling workflows, adding secrets, using self-hosted runners, or pasting internal/company data changes the risk profile and requires company security review.
