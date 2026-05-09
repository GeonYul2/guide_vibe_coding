# Build Agent Flow

This is the token-saving map for `workflows/build-agent.md`. Verify details against the canonical workflow before implementation.

## Minimal Flow

1. Read `wiki/index.md` and this page.
2. Scaffold the task:

   ```bash
   python3 scripts/new_agent_task.py "<task-slug>"
   ```

3. Fill `intake-form.md` through the conversational intake loop.
4. Write `agent-prd.md` from the completed intake.
5. Use `wiki/technique-map.md` and `techniques/taxonomy.yaml` to classify the profile.
6. Fill `technique-selection.yaml`; every registry technique must be selected or rejected.
7. Complete the required gate artifacts from `templates/`.
8. Validate before implementation:

   ```bash
   python3 scripts/validate_agent_task.py tasks/<task-slug>
   ```

9. Implement only after validation passes, then rerun targeted tests/evals and the validator.

## Hard Stops

- Do not implement before required artifacts exist and contain non-placeholder content.
- Do not skip `cost-and-caching.md` token ceilings, cache target, pruning rule, fallback path, and token telemetry.
- Do not claim completion without validator output and test/eval evidence.
