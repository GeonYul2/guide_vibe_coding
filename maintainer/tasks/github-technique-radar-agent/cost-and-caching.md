# Cost and Caching Plan: GitHub Technique Radar Agent

Purpose: token usage is operating cost. Implementation is blocked until this file defines measurable token, cache, routing, and telemetry limits.

## Token Efficiency Hard Gate

- Max input tokens per run: 120000 across all model-assisted summarization calls; zero model tokens for metadata-only dry runs.
- Max output tokens per run: 30000 across all generated summaries, classifications, and report text.
- Max total tokens per run: 150000 for a full maintainer run; 20000 for local smoke runs.
- Max model calls per run: 40 for full maintainer run; 5 for dry-run smoke test.
- Cost ceiling per successful run: USD 2.00 equivalent for prototype; USD 5.00 for full manual run unless explicitly raised.
- Cost ceiling per day/week/month: USD 5.00 per day, USD 15.00 per week, USD 40.00 per month for this agent.
- Required cache hit-rate target: at least 60% for repository metadata and 50% for README or documentation snippets after the second manual run.
- Required context pruning rule: include only repository metadata, top matched files, prior score snapshot, and at most 3000 characters of fetched text per candidate before summarization.
- Required summarization/compression trigger: summarize or discard any fetched text over 3000 characters and any candidate evidence bundle over 6000 characters.
- Stop condition when token or cost budget is exceeded: stop before the next model call, write degraded telemetry, and produce no complete radar claim unless schema-valid partial output is explicitly marked degraded.

## Cost Budget

- Expected model calls per run: 0 to 10 for metadata-only prototype; 10 to 30 for technique extraction on top candidates.
- Expected token range per run: 10000 to 80000 tokens for normal manual top-candidate summarization.
- Budget per run: USD 2.00 prototype target.
- Budget per day/week/month: USD 5.00 day, USD 15.00 week, USD 40.00 month.
- Stop condition when budget is exceeded: switch to metadata-only ranking and require human review for qualitative evidence.

## Context Strategy

- Required context: radar config, candidate metadata, matched queries, prior radar snapshot, selected lightweight file snippets, and schema contract.
- Optional context: release notes, package metadata, docs index, and human review notes.
- Context exclusion rules: no full repository trees, no full README dumps, no private data, no prohibited third-party trending-site content, no irrelevant issue threads.
- Context compression/summarization plan: deterministic metadata first; model summarizes only top candidates using capped snippets and a fixed rubric.
- Deduplication rule: normalize repository full name and content SHA before including context.
- Maximum retrieved chunks / files / messages: 3 files per candidate, 3000 characters per file, 25 candidates per full run for model-assisted extraction.

## Caching Strategy

- Cacheable inputs/context: GitHub search responses, repository metadata, selected file SHAs, decoded snippets, score snapshots, and model summaries keyed by source SHA plus rubric version.
- Cache key: `source_type:owner/repo:path_or_query:etag_or_sha:config_version:rubric_version` hashed for filesystem safety.
- Cache storage: repository-local cache directory or CI cache with tokens excluded; long-term reviewed outputs remain under `maintainer/radar/` and `repos/summaries/`.
- Invalidation rule: expire search metadata after seven days; expire file snippets after thirty days or immediately when SHA, query config, schema version, or rubric version changes.
- Stale-cache risk: stale stars or README evidence may misrank candidates; mitigate by refetching top candidates and marking stale evidence.
- Privacy/security constraints: no Authorization headers, tokens, private repository content, or detected secrets in cache.
- Prompt/prefix caching opportunity: stable system prompt, scoring rubric, schema instructions, and guardrail policy are reusable across candidate summaries.

## Fallback Strategy

- Cheaper model fallback: use deterministic metadata-only classification or a lower-cost model for first-pass tags; escalate only top ambiguous candidates.
- Reduced-context fallback: summarize only repository description, topics, license, stars, forks, pushed date, and matched query list.
- Retrieval-only or summary-only fallback: if model budget is unavailable, emit YAML with metadata evidence and `watch` status for uncertain candidates.
- Human handoff condition: budget exceeded, source conflict, adoption recommendation, license ambiguity, prohibited-source request, or repeated invalid output.

## Token Telemetry Requirements

- Track input tokens: record per model call and aggregate per run.
- Track output tokens: record per model call and aggregate per run.
- Track cache hits/misses: record by cache type, key hash, and freshness status.
- Track cost per run: estimate from model, input tokens, output tokens, and configured price table.
- Track budget-exceeded stops: event includes budget type, remaining candidates, and degraded output path.
- Dashboard or log query: filter by `agent=github-technique-radar-agent`, `run_id`, `event=model_call|cache|budget_stop|eval_result`.

## Optimization Checklist

- Remove irrelevant context before adding more context: required for every summarization bundle.
- Prefer structured compact output over prose: candidate YAML is canonical; Markdown is derived.
- Reuse stable system/developer prompts through caching: prompt prefix and rubric version are cache dimensions.
- Summarize or index long documents before full-context use: full-context use is forbidden for external repository files.
- Batch or deduplicate repeated requests: candidates are deduplicated by full name and file SHA.
- Use cheaper model tier when quality gate allows: deterministic or cheap first-pass extraction is the default.

## Related Contracts

- Model routing policy: model-routing.md
- Retrieval and memory governance: retrieval-memory.md
- Telemetry/cost events: telemetry.md
