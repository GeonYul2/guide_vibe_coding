---
type: canonical-source
source: sources/registry.yaml
---

# Source Registry Bridge

This node connects generated wiki navigation to supplemental source summaries and the canonical source registry.

Canonical source file: `sources/registry.yaml`

## Source Summary Markdown Nodes

- [[sources/summaries/README|README.md]]
- [[sources/summaries/roboco-karpathy-llm-wiki-72-run-benchmark|roboco-karpathy-llm-wiki-72-run-benchmark.md]]
- [[sources/summaries/youtube-seed-sources|youtube-seed-sources.md]]

## Related Generated Nodes

- [[wiki/workflows/source-ingestion|Source Ingestion Workflow Wiki]]
- [[wiki/techniques/source_backed_technique_ingestion|Source-Backed Technique Ingestion]]
- [[wiki/techniques/wiki_first_source_verification|Wiki-First Source Verification]]

## Source Boundary

- Treat summary files as concise extraction notes, not copied source material.
- Verify source status and refs against `sources/registry.yaml`.
