# LLM Wiki Operations

Source inspiration: `sources/summaries/roboco-karpathy-llm-wiki-72-run-benchmark.md`

## Contract

- Source of truth remains Git-controlled repo files.
- `wiki/` is generated orientation, not authority.
- Obsidian is the human graph viewer.
- Agents may start from `wiki/index.md`, but must verify important claims against source files before edits.

## Operations

### Ingest

Register sources in `sources/registry.yaml`, summarize reusable patterns under `sources/summaries/`, then update techniques/workflows/templates only with source refs.

### Query

Start at [[wiki/index]], follow links, then cite wiki pages and canonical files separately.

### Select Techniques

Start at [[wiki/technique-map]], pick the task profile, then inspect each candidate technique's prerequisites, peers, and commonly-used-with links.

### Lint

Run `python3 scripts/generate_llm_wiki.py`, then run repository tests and validator. Review Obsidian graph for orphaned pages or missing source coverage.
