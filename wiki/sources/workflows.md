---
type: canonical-source
source: workflows/
---

# Workflow Source Bridge

This node connects generated workflow wiki pages to the canonical workflow Markdown files with exact Markdown links. Exact links are used because `wiki/workflows/*.md` mirrors can make Obsidian wikilink resolution ambiguous.

## Canonical Workflow Markdown Nodes

- [publish-user-distribution.md](../../maintainer/workflows/publish-user-distribution.md)
- [weekly-repo-radar.md](../../maintainer/workflows/weekly-repo-radar.md)
- [build-agent.md](../../workflows/build-agent.md)
- [deep-interview.md](../../workflows/deep-interview.md)
- [intake.md](../../workflows/intake.md)
- [source-ingestion.md](../../workflows/source-ingestion.md)

## Generated Workflow Wiki Nodes

- [[wiki/workflows/build-agent|Workflow: Build a New Automation Agent]]
- [[wiki/workflows/deep-interview|Workflow: Deep Interview]]
- [[wiki/workflows/intake|Workflow: Standardized Agent Intake]]
- [[wiki/workflows/source-ingestion|Workflow: Supplemental Source-Backed Technique Ingestion]]
- [[wiki/workflows/publish-user-distribution|Workflow: Publish User Distribution]]
- [[wiki/workflows/weekly-repo-radar|Workflow: Weekly GitHub Technique Repository Radar]]

## Related Generated Nodes

- [[wiki/index|Wiki Index]]
- [[wiki/sources/repo-root|Repository Root Source Bridge]]
- [[wiki/sources/maintainer|Maintainer Source Bridge]]

## Source Boundary

- Workflow source files remain canonical.
- Generated workflow wiki pages provide orientation and graph routing only.
