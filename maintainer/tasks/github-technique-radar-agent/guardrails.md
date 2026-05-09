# Guardrails and Tripwires: GitHub Technique Radar Agent

Purpose: define what the agent must block, clarify, sanitize, or escalate before it acts.

## Risk Boundaries

- Unsafe or forbidden requests: scraping sites that prohibit automated extraction, bypassing robots or terms, collecting secrets, or copying external repository contents wholesale.
- Out-of-scope requests: exact replication of proprietary ranking algorithms, auto-adoption of repositories, vulnerability certification, and production deployment without rollout approval.
- Sensitive data categories: GitHub tokens, private repository data, credentials in logs, maintainer emails beyond public metadata, and any accidental secrets found in repository content.
- Irreversible or high-impact actions: publishing PRs, editing main registries, adding mandatory techniques, changing manual workflows, or using elevated credentials.

## Input Guardrails

| Trigger | Detection Method | Action | User Message | Eval Case |
| --- | --- | --- | --- | --- |
| Request references prohibited third-party crawling, scraping, or automated extraction | Keyword and URL allowlist check | block | Prohibited third-party automated extraction is not allowed; use GitHub API discovery instead. | FC-001 |
| Request asks to vendor or mirror an external repository | Intent classification and file-count threshold | block | External repositories may be tracked only as metadata and summaries. | FC-006 |
| Request asks to auto-adopt a candidate | Registry write detection | handoff | Human review is required before adoption or mandatory technique promotion. | FC-006 |
| Missing or ambiguous discovery scope | Config validation detects empty query set or no target categories | clarify | Discovery scope needs query categories, but default radar config can be used for prototype. | HP-001 |
| Private token or secret appears in input | Secret pattern scan | sanitize | Secret-like values are redacted and are not stored in artifacts. | SP-001 |

## Output Guardrails

| Risk | Validation Rule | Action | Eval Case |
| --- | --- | --- | --- |
| Prohibited source in output | URL host must be GitHub or approved official source for the selected mode | fail closed | ISO-001 |
| Long copied third-party content | Evidence bullets capped at concise summaries and excerpt length threshold | fail closed and truncate | FC-005 |
| Unsupported adoption status | Status enum excludes direct adopted promotion in radar output | fail closed | FC-006 |
| Invalid candidate schema | YAML schema and required fields validation | fail closed | ISO-001 |
| Misleading complete report after API failure | Completion marker requires all configured queries to finish or degraded status to be explicit | fail closed | FC-002 |

## Tool-Call Tripwires

| Tool / Action | Tripwire | Required Approval | Rollback / Recovery |
| --- | --- | --- | --- |
| GitHub API | Remaining rate budget below configured floor or secondary limit response | No approval for safe stop; approval needed for higher-privilege credential | Backoff, cache partial metadata, mark run degraded |
| Local file write | Path outside `maintainer/radar/`, task folder, or approved summaries | Yes | Revert unintended diff and rerun validator |
| Registry modification | `repos/registry.yaml` or `techniques/*.yaml` write | Yes | Restore from git and record review requirement |
| Workflow change | `.github/workflows/*` modification | Yes | Revert workflow diff unless rollout gate approved |
| PR creation | Network write to GitHub | Yes | Close draft PR or revert branch if created in error |

## Human Handoff

- Handoff owner: repository maintainer or designated reviewer.
- Handoff trigger: adoption decision, mandatory technique change, credential escalation, production schedule change, schema-breaking change, or unresolved license/security concern.
- Required context to send with handoff: candidate URL, score, evidence, risks, local application guidance, relevant telemetry, and changed files.
