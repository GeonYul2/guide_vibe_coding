---
type: canonical-source
source: repos/
---

# Repository Radar Bridge

This node connects generated wiki navigation to GitHub-first repository discovery artifacts.

Canonical config file: `maintainer/radar-config.yaml`, plus the maintainer-only scheduled workflow if enabled.

## Repository Markdown Nodes

- [[repos/README|README.md]]

## Radar Report Markdown Nodes

- [[maintainer/radar/2026-05-03|2026-05-03.md]]
- [[maintainer/radar/2026-05-09|2026-05-09.md]]

## Related Generated Nodes

- [[wiki/workflows/weekly-repo-radar|Weekly Repo Radar Workflow Wiki]]
- [[wiki/techniques/source_backed_technique_ingestion|Source-Backed Technique Ingestion]]

## Source Boundary

- Radar reports are review artifacts; humans promote reviewed repositories into `repos/registry.yaml`.
- Candidate YAML files are listed in generated indexes but are not Markdown graph nodes.
