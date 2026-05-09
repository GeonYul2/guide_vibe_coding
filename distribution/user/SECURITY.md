# Security Posture — User Distribution

This user distribution is designed to be safe to copy into a repository as an automation-agent guide.

## Included

- Markdown/YAML execution contracts and templates.
- Python standard-library scripts for task scaffolding and artifact validation.
- Metadata-only source and repository registries.

## Excluded

- Maintainer GitHub radar and repository discovery automation.
- GitHub Actions workflows.
- Generated wiki/Obsidian state.
- Local OMX/runtime state.
- External repository vendoring, cloning, installation, or execution.

## Adoption Checklist

1. Review `AGENTS.md` and `agent-playbook.yaml` before using this guide in a company repo.
2. Keep internal documents, secrets, customer data, and credentials out of committed task artifacts unless your security policy explicitly allows it.
3. Keep external repository references metadata-only.
4. If you need technique discovery or distribution publishing, use the source/maintainer repository rather than adding those workflows here.
