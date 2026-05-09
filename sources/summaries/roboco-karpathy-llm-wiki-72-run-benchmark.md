# Source Summary: ROBOCO Karpathy LLM Wiki 72-run benchmark

Source: https://roboco.io/posts/karpathy-llm-wiki-72-run-benchmark/

## Reusable patterns extracted

- LLM Wiki uses a three-layer contract: immutable raw sources, LLM-maintained Markdown wiki, and human-owned schema/instruction files such as `AGENTS.md`.
- It differs from stateless RAG by compiling cross-referenced knowledge once and reusing it across repeated queries.
- Daily operations are `ingest`, `query`, and `lint`: add sources with human checkpoint, answer through the index and linked pages, and regularly find stale/orphan/conflicting notes.
- Obsidian is useful as a local graph and backlink viewer for Markdown wiki pages, but the repo source of truth remains Git-controlled files.
- The recommended default is wiki-first with source verification: start at `wiki/index.md`, then verify important claims against source files, PRDs, code, or radar YAML.
- Direct read/grep remains better when the answer is clearly in one known source; GraphRAG-like graph tools can be a supplement for cross-component path questions.
- Citation discipline matters: wiki-derived answers should cite `[[Wiki Page]]` links and flag facts that require source verification or wiki updates.
- Benchmark context strategy in the target domain before treating wiki-first as universal.

## Candidate techniques promoted

- `llm_wiki_context_compilation`
- `wiki_first_source_verification`
- `obsidian_graph_knowledge_ops`

## Local application

This repository should keep executable source files as the source of truth and generate a `wiki/` layer for navigation, graph review, and lower-token LLM orientation. Obsidian should open the repository root as a vault so links between `wiki/`, `workflows/`, `templates/`, `tasks/`, and `maintainer/radar/` remain visible.
