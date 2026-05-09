---
type: canonical-source
source: maintainer/
---

# Maintainer Source Bridge

This node connects the generated wiki graph to maintainer-only Markdown artifacts used for optional repository radar operation and playbook maintenance.

## Maintainer Markdown Nodes

- [[maintainer/README|README.md]]
- [[maintainer/radar/2026-05-03|2026-05-03.md]]
- [[maintainer/radar/2026-05-09|2026-05-09.md]]
- [[maintainer/tasks/github-technique-radar-agent/agent-prd|agent-prd.md]]
- [[maintainer/tasks/github-technique-radar-agent/cost-and-caching|cost-and-caching.md]]
- [[maintainer/tasks/github-technique-radar-agent/eval-spec|eval-spec.md]]
- [[maintainer/tasks/github-technique-radar-agent/failure-cases|failure-cases.md]]
- [[maintainer/tasks/github-technique-radar-agent/guardrails|guardrails.md]]
- [[maintainer/tasks/github-technique-radar-agent/implementation-plan|implementation-plan.md]]
- [[maintainer/tasks/github-technique-radar-agent/intake-form|intake-form.md]]
- [[maintainer/tasks/github-technique-radar-agent/model-routing|model-routing.md]]
- [[maintainer/tasks/github-technique-radar-agent/output-schema|output-schema.md]]
- [[maintainer/tasks/github-technique-radar-agent/readiness-scorecard|readiness-scorecard.md]]
- [[maintainer/tasks/github-technique-radar-agent/release-rollout|release-rollout.md]]
- [[maintainer/tasks/github-technique-radar-agent/retrieval-memory|retrieval-memory.md]]
- [[maintainer/tasks/github-technique-radar-agent/security-privacy|security-privacy.md]]
- [[maintainer/tasks/github-technique-radar-agent/telemetry|telemetry.md]]
- [[maintainer/tasks/github-technique-radar-agent/tool-contracts|tool-contracts.md]]
- [[maintainer/workflows/publish-user-distribution|publish-user-distribution.md]]
- [[maintainer/workflows/weekly-repo-radar|weekly-repo-radar.md]]

## Related Generated Nodes

- [[wiki/index|Wiki Index]]
- [[wiki/repos/radar|Repository Radar Bridge]]
- [[wiki/sources/repo-root|Repository Root Source Bridge]]
- [[wiki/sources/distribution|Distribution Source Bridge]]

## Source Boundary

- `maintainer/` is for playbook maintainers, not the ordinary automation-agent task path.
- Generated wiki pages may link to maintainer artifacts for graph completeness, but canonical behavior remains in the maintainer files themselves.
