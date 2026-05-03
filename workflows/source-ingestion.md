# Workflow: Supplemental Source-Backed Technique Ingestion

Use this workflow when a YouTube video, article, talk, release note, internal post, or other non-GitHub source should inform this executable guide.

This is **supplemental**. The baseline discovery mechanism remains `workflows/weekly-repo-radar.md`, which searches GitHub repositories for reusable agent-engineering technique repos.

## Policy

- Store source metadata in `sources/registry.yaml`.
- Do not copy long transcripts, articles, or entire external repositories.
- Extract reusable techniques, gates, templates, and checklists.
- Mark speculative extraction as `candidate` until reviewed.
- Promote to mandatory only when the technique is broadly useful and has a clear enforcement point.

## Steps

1. Add source metadata to `sources/registry.yaml`.
2. Create or update a concise summary under `sources/summaries/` when enough source detail is available.
3. Extract techniques into `techniques/registry.yaml` with `source_refs`.
4. If the technique changes how every agent should behave, add it to `agent-playbook.yaml`, `templates/technique-selection.yaml`, and `techniques/taxonomy.yaml`.
5. If the technique needs a new enforcement point, add or update a required artifact template under `templates/`.
6. If it changes a build workflow, update files under `workflows/`.
7. Run script checks:

```bash
python3 -m py_compile scripts/*.py
python3 scripts/test_agent_guide.py
```

If you manually scaffold a sample task, fill all placeholders before running `scripts/validate_agent_task.py`.

## Current Seed Sources

The first seed sources are tracked in `sources/registry.yaml`:

- 실리콘밸리 엔지니어의 바이브코딩 테크닉
- Claw Code / harness engineering conversation
- Karpathy-style concise `CLAUDE.md` operating contract discussion

These are used as supplemental source references for:

- concise operating contracts
- minimal diff and scope control
- harness runtime design
- permissioned tool execution
- source-backed technique ingestion
