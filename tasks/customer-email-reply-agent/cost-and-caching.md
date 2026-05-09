# Cost and Caching Plan: customer-email-reply-agent

## Token Efficiency Hard Gate

- Max input tokens per run: 12000 tokens including email, metadata, and retrieved policy snippets.
- Max output tokens per run: 2500 tokens including JSON and Markdown summary.
- Max total tokens per run: 14500 tokens.
- Cost ceiling per successful run: USD 0.25 equivalent in prototype pricing.
- Required cache hit-rate target: 60 percent for repeated policy snippets after the first week.
- Required context pruning rule: include only top 5 policy snippets, each summarized under 350 tokens, and discard unrelated CRM fields.
- Required summarization/compression trigger: summarize any policy document excerpt over 1200 tokens before model use.
- Stop condition when token or cost budget is exceeded: stop drafting, return handoff package with budget_exceeded reason.
- Cheaper model fallback: use a fast low-cost model for routine classification and extraction when confidence thresholds are met.
- Reduced-context fallback: use email summary plus top 2 policy snippets and require human review.

## Token Telemetry Requirements

- Track input tokens: record per run and per retrieved source group.
- Track output tokens: record JSON and Markdown token estimates separately.
- Track cache hits/misses: record policy cache key hash, hit flag, age, and invalidation reason.
- Track cost per run: estimate model and retrieval cost per message and aggregate daily.
