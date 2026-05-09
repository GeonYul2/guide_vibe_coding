---
type: canonical-source
source: distribution/
---

# Distribution Source Bridge

This node connects the generated wiki graph to user-distribution override documents and export guidance.

## Distribution Markdown Nodes

- [[distribution/user/AGENTS|AGENTS.md]]
- [[distribution/user/README|README.md]]
- [[distribution/user/SECURITY|SECURITY.md]]

## Related Generated Nodes

- [[wiki/index|Wiki Index]]
- [[wiki/sources/repo-root|Repository Root Source Bridge]]
- [[wiki/sources/maintainer|Maintainer Source Bridge]]

## Source Boundary

- `distribution/` defines what the user-facing export receives.
- The user distribution must not include maintainer radar, discovery automation, generated wiki, or publish workflow logic.
- Verify exported files with `python3 maintainer/scripts/export_user_distribution.py --dry-run --dest <target>`.
