# YouTube Seed Sources — Initial Extraction

Status: supplemental seed; metadata verified, detailed transcript-level extraction pending. GitHub repository radar remains the primary refresh loop.

## Sources

- `youtube-vibecoding-silicon-valley-techniques`
- `youtube-claw-code-harness-engineering`
- `youtube-karpathy-65-line-claude-md`

## Extracted Technique Themes

### Concise operating contract

Enforcement point:

- `AGENTS.md`
- `agent-playbook.yaml`
- `templates/technique-selection.yaml`

Agent behavior:

- Prefer short, strict, project-local instructions.
- Make behavior constraints explicit.
- Verify before claiming completion.

### Scope control and minimal diff

Enforcement point:

- `techniques/registry.yaml#scope_control_and_minimal_diff`
- `templates/implementation-plan.md`

Agent behavior:

- Avoid opportunistic refactors.
- Keep changes small and reversible.
- State non-goals before implementation.

### Harness runtime design

Enforcement point:

- `techniques/registry.yaml#agent_harness_runtime_design`
- `templates/eval-spec.md`
- `templates/tool-contracts.md`

Agent behavior:

- Separate model prompting from execution harness.
- Define tool registry, runtime state, retries, permissions, and traces.
- Design harness/evals before implementation.

### Permissioned tool execution

Enforcement point:

- `techniques/registry.yaml#permissioned_tool_execution`
- `templates/tool-contracts.md`

Agent behavior:

- Define allowlists, approval gates, sandbox boundaries, timeouts, idempotency, and audit logs.

### Source-backed ingestion

Enforcement point:

- `workflows/source-ingestion.md`
- `sources/registry.yaml`
- `maintainer/radar-config.yaml`

Agent behavior:

- Register sources first.
- Extract reusable techniques only.
- Do not vendor external repositories or paste long transcripts.
