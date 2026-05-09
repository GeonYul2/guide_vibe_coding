# Failure Cases: GitHub Technique Radar Agent

Each failure should become a regression case, explicit non-goal, prompt or tool update, guardrail or tripwire update, or human handoff rule.

### FC-001: Prohibited third-party scraping request

- Trigger: User or config asks the agent to crawl a prohibited third-party source that prohibits automated extraction.
- Observed/expected failure: Agent might attempt prohibited scraping to imitate third-party trending rankings.
- Root cause hypothesis: Discovery goal is confused with source permission.
- Desired handling: Block prohibited source and redirect to GitHub API discovery.
- Fix: Add source allowlist and prohibited-domain guardrail.
- Regression test/eval link: Out-of-scope and unsafe request case in `eval-spec.md`.
- Status: open

### FC-002: GitHub secondary rate limit

- Trigger: Too many GitHub API requests in a short period or concurrent query expansion.
- Observed/expected failure: API returns 403 or 429 and partial results could be mistaken for complete output.
- Root cause hypothesis: Missing backoff, cache, or concurrency limit.
- Desired handling: Honor retry headers, reduce concurrency, use cache, and mark run degraded if incomplete.
- Fix: Rate-limit-aware client and completion marker.
- Regression test/eval link: Tool failure case in `eval-spec.md`.
- Status: open

### FC-003: Domain demo outranks reusable technique repo

- Trigger: A high-star domain-specific demo matches broad agent keywords.
- Observed/expected failure: Radar highlights flashy demos instead of reusable agent-engineering patterns.
- Root cause hypothesis: Score overweights stars and underweights technique evidence.
- Desired handling: Apply required technique keywords, exclude keywords, and relevance scoring.
- Fix: Weighted scoring and fixture ranking threshold.
- Regression test/eval link: Ambiguous input case in `eval-spec.md`.
- Status: open

### FC-004: Duplicate repository across queries

- Trigger: Same repository appears under multiple configured searches.
- Observed/expected failure: Report contains duplicate candidates and inflated importance.
- Root cause hypothesis: Deduplication key missing or uses URL variants.
- Desired handling: Collapse by normalized `owner/repo`, preserve matched query list, and aggregate signals.
- Fix: Normalize repository full name before scoring.
- Regression test/eval link: Acceptance threshold for deduplication in `eval-spec.md`.
- Status: open

### FC-005: Long copied README excerpt

- Trigger: Technique evidence extraction copies large chunks from an external README.
- Observed/expected failure: Radar artifact violates concise-summary policy and becomes noisy.
- Root cause hypothesis: Summarizer lacks excerpt limit and source transformation rule.
- Desired handling: Store short paraphrased evidence bullets and source URLs only.
- Fix: Output guardrail limiting excerpt length and rejecting long copied text.
- Regression test/eval link: Output guardrail case in `guardrails.md`.
- Status: open

### FC-006: Candidate auto-promoted without review

- Trigger: Automated run edits `repos/registry.yaml` or mandatory technique files.
- Observed/expected failure: Unreviewed repository or technique changes become authoritative.
- Root cause hypothesis: Write permissions too broad or review gate missing.
- Desired handling: Block registry writes and require human review.
- Fix: Path allowlist and registry modification tripwire.
- Regression test/eval link: Guardrail tripwire case in `eval-spec.md`.
- Status: open
