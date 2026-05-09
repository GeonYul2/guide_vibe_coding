#!/usr/bin/env python3
"""Generate an Obsidian-compatible LLM wiki from repo contracts.

The generated wiki is a navigation and context-compilation layer only. Canonical
source remains AGENTS.md, agent-playbook.yaml, techniques/*.yaml, workflows/*,
templates/*, tasks/*, distribution/*, and maintainer/* for maintainer-only
operations.
"""
from __future__ import annotations

import re
import shutil
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WIKI = ROOT / "wiki"
TECH_ID = r"[a-zA-Z0-9_]+"


def slug(text: str) -> str:
    return re.sub(r"[^a-zA-Z0-9_-]+", "-", text.strip().lower()).strip("-")


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def wiki_link(tech_id: str, label: str | None = None, prefix: str = "wiki/techniques/") -> str:
    label = label or tech_id
    return f"[[{prefix}{tech_id}|{label}]]"


def parse_techniques() -> list[dict[str, str]]:
    text = read(ROOT / "techniques" / "registry.yaml")
    blocks = re.split(r"\n\s*- id: ", text)
    techniques: list[dict[str, str]] = []
    for block in blocks[1:]:
        block = "id: " + block
        tid = re.search(r"^id:\s*([^\n]+)", block, flags=re.MULTILINE)
        name = re.search(r"^\s*name:\s*([^\n]+)", block, flags=re.MULTILINE)
        apply_when = re.search(r"^\s*apply_when:\s*([^\n]+)", block, flags=re.MULTILINE)
        output = re.search(r"^\s*output:\s*([^\n]+)", block, flags=re.MULTILINE)
        notes = re.search(r"^\s*notes:\s*>?\s*\n((?:\s{6,}.+\n?)*)", block, flags=re.MULTILINE)
        source_refs = re.findall(r"sources/registry.yaml#[a-zA-Z0-9_.-]+", block)
        if tid:
            techniques.append(
                {
                    "id": tid.group(1).strip(),
                    "name": name.group(1).strip() if name else tid.group(1).strip(),
                    "apply_when": apply_when.group(1).strip() if apply_when else "See registry.",
                    "output": output.group(1).strip() if output else "See registry.",
                    "notes": re.sub(r"\s+", " ", notes.group(1).strip()) if notes else "See registry.",
                    "source_refs": ", ".join(source_refs) if source_refs else "Registry-defined / local policy",
                }
            )
    return techniques


def yaml_list_after(lines: list[str], start_index: int, min_indent: int) -> list[str]:
    values: list[str] = []
    for line in lines[start_index + 1 :]:
        if not line.strip():
            continue
        indent = len(line) - len(line.lstrip(" "))
        if indent <= min_indent:
            break
        match = re.match(r"\s*-\s*(%s)\s*$" % TECH_ID, line)
        if match:
            values.append(match.group(1))
    return values


def parse_taxonomy(known_ids: set[str]) -> tuple[dict[str, list[str]], dict[str, dict[str, list[str]]]]:
    lines = read(ROOT / "techniques" / "taxonomy.yaml").splitlines()
    categories: dict[str, list[str]] = defaultdict(list)
    profiles: dict[str, dict[str, list[str]]] = defaultdict(lambda: {"must": [], "should": [], "optional": []})
    current_category: str | None = None
    current_profile: str | None = None
    current_priority: str | None = None
    mode: str | None = None

    for index, line in enumerate(lines):
        id_match = re.match(r"\s*- id:\s*([a-zA-Z0-9_]+)\s*$", line)
        if id_match:
            ident = id_match.group(1)
            # Category ids appear before agent_context_profiles; profile ids after.
            if mode != "profiles":
                current_category = ident
            else:
                current_profile = ident
            current_priority = None
            continue
        if re.match(r"agent_context_profiles:\s*$", line):
            mode = "profiles"
            current_category = None
            continue
        key_match = re.match(r"\s*(techniques|must|should|optional):\s*$", line)
        if key_match:
            key = key_match.group(1)
            if key == "techniques" and current_category:
                categories[current_category].extend([v for v in yaml_list_after(lines, index, len(line) - len(line.lstrip(" "))) if v in known_ids])
            elif key in {"must", "should", "optional"} and current_profile:
                current_priority = key
            continue
        item_match = re.match(r"\s*-\s*(%s)\s*$" % TECH_ID, line)
        if item_match and current_profile and current_priority and item_match.group(1) in known_ids:
            profiles[current_profile][current_priority].append(item_match.group(1))
    return dict(categories), dict(profiles)


def technique_relationships(
    techniques: list[dict[str, str]],
    categories: dict[str, list[str]],
    profiles: dict[str, dict[str, list[str]]],
) -> dict[str, dict[str, set[str]]]:
    ids = [tech["id"] for tech in techniques]
    rel: dict[str, dict[str, set[str]]] = {
        tid: {"prerequisites": set(), "next": set(), "peers": set(), "used_with": set()} for tid in ids
    }

    # Ordered operating chains make selection less ambiguous for agents.
    chains = [
        ["standardized_intake_gate", "deep_interview", "agent_readiness_scoring", "implementation_plan"],
        ["structured_output_schema_validation", "eval_regression_loop", "failed_case_memory", "observability_tracing"],
        ["tool_contracts", "permissioned_tool_execution", "agent_harness_runtime_design", "model_routing_fallback_policy"],
        ["retrieval_memory_governance", "llm_wiki_context_compilation", "wiki_first_source_verification", "obsidian_graph_knowledge_ops"],
        ["token_context_caching", "cost_budgeting", "token_efficiency_budget_gate", "model_routing_fallback_policy"],
        ["guardrails_tripwires", "safety_handoff_boundaries", "security_privacy_data_governance", "deployment_rollout_canary"],
        ["source_backed_technique_ingestion", "llm_wiki_context_compilation", "wiki_first_source_verification"],
        ["concise_operating_contract", "default_response_brevity", "prompt_versioning", "scope_control_and_minimal_diff"],
    ]
    known = set(ids)
    for chain in chains:
        present = [item for item in chain if item in known]
        for before, after in zip(present, present[1:]):
            rel[after]["prerequisites"].add(before)
            rel[before]["next"].add(after)

    # Category membership creates peer edges between similar techniques.
    for members in categories.values():
        members = [m for m in members if m in known]
        for tid in members:
            rel[tid]["peers"].update(set(members) - {tid})

    # Profile co-selection creates used-with edges; must techniques are especially strong.
    for profile in profiles.values():
        selected = [*profile.get("must", []), *profile.get("should", [])]
        selected = [s for s in selected if s in known]
        for tid in selected:
            rel[tid]["used_with"].update(set(selected) - {tid})

    return rel


def parse_workflows() -> list[Path]:
    return sorted((ROOT / "workflows").glob("*.md")) + sorted((ROOT / "maintainer" / "workflows").glob("*.md"))


def parse_tasks() -> list[Path]:
    return sorted(path for path in (ROOT / "tasks").glob("*/agent-prd.md")) + sorted(
        path for path in (ROOT / "maintainer" / "tasks").glob("*/agent-prd.md")
    )


def task_selected_techniques(task_dir: Path, known_ids: set[str]) -> list[str]:
    text = read(task_dir / "technique-selection.yaml")
    return [tid for tid in re.findall(r"id:\s*(%s)" % TECH_ID, text) if tid in known_ids]


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def reset_generated_wiki() -> None:
    """Clear generated wiki surfaces so moved or renamed sources do not leave stale graph nodes."""
    for directory in ["repos", "sources", "tasks", "techniques", "workflows"]:
        shutil.rmtree(WIKI / directory, ignore_errors=True)
    for filename in ["graph-links.md", "index.md", "llm-wiki-operations.md", "technique-map.md"]:
        (WIKI / filename).unlink(missing_ok=True)


def link_list(ids: list[str] | set[str], names: dict[str, str], prefix: str = "wiki/techniques/") -> str:
    ordered = sorted(ids)
    return "\n".join(f"- {wiki_link(tid, names.get(tid, tid), prefix)}" for tid in ordered) if ordered else "- None recorded."


def markdown_target(path: Path) -> str:
    return path.relative_to(ROOT).with_suffix("").as_posix()


def markdown_link(path: Path, label: str | None = None) -> str:
    target = markdown_target(path)
    return f"[[{target}|{label or path.name}]]"


def exact_markdown_link(from_page: Path, target: Path, label: str | None = None) -> str:
    """Return an exact relative Markdown link from a generated page to a canonical source file.

    Obsidian wikilinks such as [[workflows/build-agent]] can be ambiguous when a
    generated mirror also exists at wiki/workflows/build-agent.md. Markdown links
    with explicit relative paths force the edge to the root source file.
    """
    up = "../" * len(from_page.relative_to(ROOT).parent.parts)
    href = f"{up}{target.relative_to(ROOT).as_posix()}"
    return f"[{label or target.name}]({href})"


def markdown_link_list(paths: list[Path], empty: str = "- None recorded.") -> str:
    return "\n".join(f"- {markdown_link(path)}" for path in sorted(paths)) if paths else empty


def exact_markdown_link_list(from_page: Path, paths: list[Path], empty: str = "- None recorded.") -> str:
    return "\n".join(f"- {exact_markdown_link(from_page, path)}" for path in sorted(paths)) if paths else empty


def task_artifact_paths(task_dir: Path) -> list[Path]:
    return sorted(task_dir.glob("*.md"))


def generate() -> None:
    techniques = parse_techniques()
    known_ids = {tech["id"] for tech in techniques}
    names = {tech["id"]: tech["name"] for tech in techniques}
    categories, profiles = parse_taxonomy(known_ids)
    rel = technique_relationships(techniques, categories, profiles)
    workflows = parse_workflows()
    tasks = parse_tasks()
    reset_generated_wiki()
    workflow_names = {workflow.stem for workflow in workflows}
    root_docs = [path for path in [ROOT / "AGENTS.md", ROOT / "README.md", ROOT / "SECURITY.md"] if path.exists()]
    template_files = sorted((ROOT / "templates").glob("*.md"))
    source_summary_files = sorted((ROOT / "sources" / "summaries").glob("*.md"))
    distribution_files = sorted((ROOT / "distribution").rglob("*.md"))
    maintainer_files = sorted((ROOT / "maintainer").rglob("*.md"))
    radar_markdown_files = sorted((ROOT / "maintainer" / "radar").glob("*.md"))
    weekly_radar_related = (
        "- [[wiki/workflows/weekly-repo-radar|Weekly Repo Radar Workflow Wiki]]"
        if "weekly-repo-radar" in workflow_names
        else "- No weekly repo radar workflow page generated in the current tree."
    )

    technique_links = []
    for tech in techniques:
        tid = tech["id"]
        page = WIKI / "techniques" / f"{tid}.md"
        technique_links.append(f"- [[wiki/techniques/{tid}|{tech['name']}]]")
        write(
            page,
            f"""---
type: technique
id: {tid}
source: techniques/registry.yaml
---

# {tech['name']}

## When to Apply

{tech['apply_when']}

## Selection Guidance

- Choose this technique when its trigger matches the task context.
- Prefer prerequisites first when they are listed below.
- Use peers to compare similar techniques rather than selecting blindly.
- Use "Commonly Used With" to assemble a complete technique bundle.

## Prerequisites / Before This

{link_list(rel[tid]['prerequisites'], names)}

## Next / Enables

{link_list(rel[tid]['next'], names)}

## Similar / Compare With

{link_list(rel[tid]['peers'], names)}

## Commonly Used With

{link_list(rel[tid]['used_with'], names)}

## Required Output

{tech['output']}

## Operating Notes

{tech['notes']}

## Source References

{tech['source_refs']}

## Canonical Source Nodes

- [[wiki/sources/techniques-registry|Techniques Registry Source]]
- [[wiki/sources/techniques-taxonomy|Techniques Taxonomy Source]]

## Verify Against

- [[wiki/index|Wiki Index]]
- [[wiki/technique-map|Technique Map]]
- `techniques/registry.yaml`
- `techniques/taxonomy.yaml`
- task-local `technique-selection.yaml`
""",
        )

    workflow_links = []
    for wf in workflows:
        name = wf.stem
        title = read(wf).splitlines()[0].lstrip("# ") if read(wf).splitlines() else name
        source_path = wf.relative_to(ROOT).as_posix()
        page = WIKI / "workflows" / f"{name}.md"
        workflow_links.append(f"- [[wiki/workflows/{name}|{title}]]")
        write(
            page,
            f"""---
type: workflow
source: {source_path}
---

# {title}

Canonical source: {exact_markdown_link(page, wf, source_path)}

Canonical vault path: `{source_path}`

## Related Core Contracts

- [[wiki/index|Wiki Index]]
- [[wiki/technique-map|Technique Map]]
- [[wiki/techniques/standardized_intake_gate|Standardized Intake Quality Gate]]
- [[wiki/techniques/wiki_first_source_verification|Wiki-First Source Verification]]

## Verification Rule

Use this wiki page for orientation only. Before editing workflow behavior, read `{source_path}` directly.
""",
        )

    task_links = []
    for prd in tasks:
        task = prd.parent.name
        selected = task_selected_techniques(prd.parent, known_ids)
        artifact_paths = task_artifact_paths(prd.parent)
        task_source = prd.parent.relative_to(ROOT).as_posix()
        task_links.append(f"- [[wiki/tasks/{task}|{task}]]")
        write(
            WIKI / "tasks" / f"{task}.md",
            f"""---
type: task
task: {task}
source: {task_source}/
---

# Task: {task}

Canonical folder: `{task_source}/`

## Selected Techniques

{link_list(selected, names)}

## Required Task Artifacts

{markdown_link_list(artifact_paths)}

## Non-Markdown Task Contracts

- `{task_source}/technique-selection.yaml`

## Selection Verification

Before changing implementation, verify selected/rejected reasoning in `{task_source}/technique-selection.yaml`.
""",
        )

    category_sections = []
    for category, members in sorted(categories.items()):
        category_sections.append(f"## Category: {category}\n\n{link_list(members, names)}\n")

    profile_sections = []
    for profile, buckets in sorted(profiles.items()):
        profile_sections.append(
            f"## Profile: {profile}\n\n### Must\n\n{link_list(buckets.get('must', []), names)}\n\n"
            f"### Should\n\n{link_list(buckets.get('should', []), names)}\n\n"
            f"### Optional\n\n{link_list(buckets.get('optional', []), names)}\n"
        )

    write(
        WIKI / "technique-map.md",
        f"""# Technique Map

Use this page when choosing techniques for a task. It groups similar techniques and exposes must/should/optional bundles from `techniques/taxonomy.yaml`.

## Source Nodes

- [[wiki/sources/techniques-registry|Techniques Registry Source]]
- [[wiki/sources/techniques-taxonomy|Techniques Taxonomy Source]]

## Selection Rule

1. Start with the task profile.
2. Include all `must` techniques unless explicitly rejected with reason.
3. Compare peers before choosing among similar techniques.
4. Follow prerequisite and next-technique links on individual technique pages.

# Categories

{chr(10).join(category_sections)}

# Agent Context Profiles

{chr(10).join(profile_sections)}
""",
    )

    write(
        WIKI / "sources" / "techniques-registry.md",
        f"""---
type: canonical-source
source: techniques/registry.yaml
---

# Techniques Registry Source

This node exists to make the Obsidian graph connect generated technique notes back to their canonical source file.

Canonical source file: `techniques/registry.yaml`

## Generated Technique Pages

{link_list(known_ids, names)}

## Source Boundary

- Treat this page as a graph bridge and orientation note only.
- Verify technique IDs, names, triggers, outputs, notes, and source refs against `techniques/registry.yaml` before editing or claiming authority.
- Regenerate with `python3 scripts/generate_llm_wiki.py` after registry changes.
""",
    )

    write(
        WIKI / "sources" / "techniques-taxonomy.md",
        f"""---
type: canonical-source
source: techniques/taxonomy.yaml
---

# Techniques Taxonomy Source

This node exists to make the Obsidian graph connect generated technique relationship maps back to their canonical taxonomy file.

Canonical source file: `techniques/taxonomy.yaml`

## Generated Maps

- [[wiki/technique-map|Technique Map]]
- [[wiki/graph-links|Graph Links]]

## Technique Pages Using Taxonomy Relationships

{link_list(known_ids, names)}

## Source Boundary

- Treat this page as a graph bridge and orientation note only.
- Verify category membership, profile priorities, prerequisites, peers, and commonly-used-with relationships against `techniques/taxonomy.yaml`.
- Regenerate with `python3 scripts/generate_llm_wiki.py` after taxonomy changes.
""",
    )

    write(
        WIKI / "sources" / "repo-root.md",
        f"""---
type: canonical-source
source: repo-root
---

# Repository Root Source Bridge

This node connects the generated wiki graph to root-level repository documents that otherwise appear as isolated Markdown nodes when the repository root is opened as an Obsidian vault.

## Root Documents

{markdown_link_list(root_docs)}

## Related Generated Nodes

- [[wiki/index|Wiki Index]]
- [[wiki/sources/techniques-registry|Techniques Registry Source]]
- [[wiki/sources/techniques-taxonomy|Techniques Taxonomy Source]]
- [[wiki/sources/templates|Template Source Bridge]]
- [[wiki/sources/source-registry|Source Registry Bridge]]
- [[wiki/sources/distribution|Distribution Source Bridge]]
- [[wiki/sources/maintainer|Maintainer Source Bridge]]
- [[wiki/sources/workflows|Workflow Source Bridge]]
- [[wiki/repos/radar|Repository Radar Bridge]]

## Source Boundary

- Root documents remain canonical where they define project policy or overview.
- Generated wiki pages provide navigation only and must not replace direct source verification.
""",
    )

    write(
        WIKI / "sources" / "templates.md",
        f"""---
type: canonical-source
source: templates/
---

# Template Source Bridge

This node connects generated wiki navigation to canonical task artifact templates.

## Template Markdown Nodes

{markdown_link_list(template_files)}

## Related Generated Nodes

- [[wiki/index|Wiki Index]]
- [[wiki/workflows/build-agent|Build Agent Workflow Wiki]]

## Source Boundary

- Template files under `templates/` remain canonical for artifact shape.
- Regenerate the wiki after adding, removing, or renaming templates.
""",
    )

    workflow_source_page = WIKI / "sources" / "workflows.md"
    write(
        workflow_source_page,
        f"""---
type: canonical-source
source: workflows/
---

# Workflow Source Bridge

This node connects generated workflow wiki pages to the canonical workflow Markdown files with exact Markdown links. Exact links are used because `wiki/workflows/*.md` mirrors can make Obsidian wikilink resolution ambiguous.

## Canonical Workflow Markdown Nodes

{exact_markdown_link_list(workflow_source_page, workflows)}

## Generated Workflow Wiki Nodes

{chr(10).join(workflow_links) if workflow_links else '- None recorded.'}

## Related Generated Nodes

- [[wiki/index|Wiki Index]]
- [[wiki/sources/repo-root|Repository Root Source Bridge]]
- [[wiki/sources/maintainer|Maintainer Source Bridge]]

## Source Boundary

- Workflow source files remain canonical.
- Generated workflow wiki pages provide orientation and graph routing only.
""",
    )

    write(
        WIKI / "sources" / "source-registry.md",
        f"""---
type: canonical-source
source: sources/registry.yaml
---

# Source Registry Bridge

This node connects generated wiki navigation to supplemental source summaries and the canonical source registry.

Canonical source file: `sources/registry.yaml`

## Source Summary Markdown Nodes

{markdown_link_list(source_summary_files)}

## Related Generated Nodes

- [[wiki/workflows/source-ingestion|Source Ingestion Workflow Wiki]]
- [[wiki/techniques/source_backed_technique_ingestion|Source-Backed Technique Ingestion]]
- [[wiki/techniques/wiki_first_source_verification|Wiki-First Source Verification]]

## Source Boundary

- Treat summary files as concise extraction notes, not copied source material.
- Verify source status and refs against `sources/registry.yaml`.
""",
    )

    write(
        WIKI / "sources" / "distribution.md",
        f"""---
type: canonical-source
source: distribution/
---

# Distribution Source Bridge

This node connects the generated wiki graph to user-distribution override documents and export guidance.

## Distribution Markdown Nodes

{markdown_link_list(distribution_files)}

## Related Generated Nodes

- [[wiki/index|Wiki Index]]
- [[wiki/sources/repo-root|Repository Root Source Bridge]]
- [[wiki/sources/maintainer|Maintainer Source Bridge]]

## Source Boundary

- `distribution/` defines what the user-facing export receives.
- The user distribution must not include maintainer radar, discovery automation, generated wiki, or publish workflow logic.
- Verify exported files with `python3 maintainer/scripts/export_user_distribution.py --dry-run --dest <target>`.
""",
    )

    write(
        WIKI / "sources" / "maintainer.md",
        f"""---
type: canonical-source
source: maintainer/
---

# Maintainer Source Bridge

This node connects the generated wiki graph to maintainer-only Markdown artifacts used for optional repository radar operation and playbook maintenance.

## Maintainer Markdown Nodes

{markdown_link_list(maintainer_files)}

## Related Generated Nodes

- [[wiki/index|Wiki Index]]
- [[wiki/repos/radar|Repository Radar Bridge]]
- [[wiki/sources/repo-root|Repository Root Source Bridge]]
- [[wiki/sources/distribution|Distribution Source Bridge]]

## Source Boundary

- `maintainer/` is for playbook maintainers, not the ordinary automation-agent task path.
- Generated wiki pages may link to maintainer artifacts for graph completeness, but canonical behavior remains in the maintainer files themselves.
""",
    )

    write(
        WIKI / "repos" / "radar.md",
        f"""---
type: canonical-source
source: repos/
---

# Repository Radar Bridge

This node connects generated wiki navigation to GitHub-first repository discovery artifacts.

Canonical config file: `maintainer/radar-config.yaml`, plus the maintainer-only scheduled workflow if enabled.

## Repository Markdown Nodes

{markdown_link_list([path for path in [ROOT / "repos" / "README.md"] if path.exists()])}

## Radar Report Markdown Nodes

{markdown_link_list(radar_markdown_files)}

## Related Generated Nodes

{weekly_radar_related}
- [[wiki/techniques/source_backed_technique_ingestion|Source-Backed Technique Ingestion]]

## Source Boundary

- Radar reports are review artifacts; humans promote reviewed repositories into `repos/registry.yaml`.
- Candidate YAML files are listed in generated indexes but are not Markdown graph nodes.
""",
    )

    radar_files = sorted((ROOT / "maintainer" / "radar").glob("*-candidates.yaml"))
    radar_links = [f"- `maintainer/radar/{path.name}`" for path in radar_files[-10:]] or ["- No radar candidates yet."]
    root_vault_bridge_lines = [
        "[[wiki/index]] -> [[wiki/sources/repo-root]] -> [[AGENTS]]",
        "[[wiki/index]] -> [[wiki/sources/templates]] -> [[templates/agent-prd]]",
    ]
    if source_summary_files:
        root_vault_bridge_lines.append(
            f"[[wiki/index]] -> [[wiki/sources/source-registry]] -> [[{markdown_target(source_summary_files[-1])}]]"
        )
    if distribution_files:
        root_vault_bridge_lines.append(
            f"[[wiki/index]] -> [[wiki/sources/distribution]] -> [[{markdown_target(distribution_files[0])}]]"
        )
    if radar_markdown_files:
        root_vault_bridge_lines.append(f"[[wiki/index]] -> [[wiki/repos/radar]] -> [[{markdown_target(radar_markdown_files[-1])}]]")
    elif (ROOT / "repos" / "README.md").exists():
        root_vault_bridge_lines.append(f"[[wiki/index]] -> [[wiki/repos/radar]] -> [[{markdown_target(ROOT / 'repos' / 'README.md')}]]")
    for prd in tasks:
        task = prd.parent.name
        task_anchor = prd.parent / "model-routing.md" if (prd.parent / "model-routing.md").exists() else prd
        root_vault_bridge_lines.append(f"[[wiki/tasks/{task}]] -> [[{markdown_target(task_anchor)}]]")
    discovery_flow = (
        "[[wiki/workflows/weekly-repo-radar]] -> [[wiki/techniques/source_backed_technique_ingestion]] -> [[wiki/techniques/wiki_first_source_verification]]"
        if "weekly-repo-radar" in workflow_names
        else "[[wiki/repos/radar]] -> [[wiki/techniques/source_backed_technique_ingestion]] -> [[wiki/techniques/wiki_first_source_verification]]"
    )

    write(
        WIKI / "index.md",
        f"""# Agent Engineering LLM Wiki

This wiki is an Obsidian-compatible navigation and context-compilation layer. It is **not** the source of truth.

## Start Here

1. Read [[wiki/workflows/intake|Standardized Agent Intake]] for new tasks.
2. Use [[wiki/technique-map|Technique Map]] to compare similar techniques and choose bundles.
3. Read [[wiki/workflows/build-agent|Build a New Automation Agent]] for the implementation gate sequence.
4. Use [[wiki/graph-links|Graph Links]] to inspect core relationships.
5. Verify important claims against canonical source files before editing.

## Canonical Sources

- [[wiki/sources/repo-root|Repository Root Source Bridge]]
- {markdown_link(ROOT / "AGENTS.md", "AGENTS.md")}
- {markdown_link(ROOT / "README.md", "README.md")}
- {markdown_link(ROOT / "SECURITY.md", "SECURITY.md")}
- `agent-playbook.yaml`
- [[wiki/sources/techniques-registry|techniques/registry.yaml]]
- [[wiki/sources/techniques-taxonomy|techniques/taxonomy.yaml]]
- [[wiki/sources/workflows|workflows/*.md]]
- [[wiki/sources/templates|templates/*.md]]
- [[wiki/sources/source-registry|sources/registry.yaml and summaries]]
- [[wiki/sources/distribution|distribution/*.md]]
- [[wiki/sources/maintainer|maintainer/*.md]]
- [[wiki/repos/radar|maintainer/radar/*]]

## Techniques

{chr(10).join(technique_links)}

## Workflows

{chr(10).join(workflow_links)}

## Tasks

{chr(10).join(task_links) if task_links else '- No task pages generated yet.'}

## Source Bridges

- [[wiki/sources/repo-root|Repository Root Source Bridge]]
- [[wiki/sources/templates|Template Source Bridge]]
- [[wiki/sources/source-registry|Source Registry Bridge]]
- [[wiki/sources/distribution|Distribution Source Bridge]]
- [[wiki/sources/maintainer|Maintainer Source Bridge]]
- [[wiki/sources/workflows|Workflow Source Bridge]]
- [[wiki/repos/radar|Repository Radar Bridge]]

## Recent Radar Candidate Files

{chr(10).join(radar_links)}

## Obsidian Usage

Open the repository root as an Obsidian vault. The committed `.obsidian/graph.json` filters graph view toward `path:wiki` while still allowing links to source files.
""",
    )

    write(
        WIKI / "graph-links.md",
        f"""# Graph Links

## Core Build Flow

[[wiki/workflows/intake]] -> [[wiki/workflows/deep-interview]] -> [[wiki/workflows/build-agent]] -> [[wiki/techniques/standardized_intake_gate]] -> [[wiki/techniques/agent_readiness_scoring]]

## Technique Selection Map

[[wiki/technique-map]] -> [[wiki/techniques/standardized_intake_gate]] -> [[wiki/techniques/deep_interview]] -> [[wiki/techniques/structured_output_schema_validation]] -> [[wiki/techniques/eval_regression_loop]]

## Source-Backed Knowledge Flow

[[wiki/techniques/source_backed_technique_ingestion]] -> [[wiki/techniques/llm_wiki_context_compilation]] -> [[wiki/techniques/wiki_first_source_verification]] -> [[wiki/techniques/obsidian_graph_knowledge_ops]]

## Canonical Source Bridge

[[wiki/sources/techniques-registry]] -> [[wiki/techniques/standardized_intake_gate]]
[[wiki/sources/techniques-taxonomy]] -> [[wiki/technique-map]] -> [[wiki/techniques/deep_interview]]

## Root Vault Source Bridges

{chr(10).join(root_vault_bridge_lines)}

## Discovery Flow

{discovery_flow}

## Verification Flow

[[wiki/techniques/structured_output_schema_validation]] -> [[wiki/techniques/eval_regression_loop]] -> [[wiki/techniques/failed_case_memory]] -> [[wiki/techniques/observability_tracing]]

## Runtime and Cost Flow

[[wiki/techniques/agent_harness_runtime_design]] -> [[wiki/techniques/permissioned_tool_execution]] -> [[wiki/techniques/model_routing_fallback_policy]] -> [[wiki/techniques/token_efficiency_budget_gate]]
""",
    )

    write(
        WIKI / "llm-wiki-operations.md",
        """# LLM Wiki Operations

Source inspiration: `sources/summaries/roboco-karpathy-llm-wiki-72-run-benchmark.md`

## Contract

- Source of truth remains Git-controlled repo files.
- `wiki/` is generated orientation, not authority.
- Obsidian is the human graph viewer.
- Agents may start from `wiki/index.md`, but must verify important claims against source files before edits.

## Operations

### Ingest

Register sources in `sources/registry.yaml`, summarize reusable patterns under `sources/summaries/`, then update techniques/workflows/templates only with source refs.

### Query

Start at [[wiki/index]], follow links, then cite wiki pages and canonical files separately.

### Select Techniques

Start at [[wiki/technique-map]], pick the task profile, then inspect each candidate technique's prerequisites, peers, and commonly-used-with links.

### Lint

Run `python3 scripts/generate_llm_wiki.py`, then run repository tests and validator. Review Obsidian graph for orphaned pages or missing source coverage.
""",
    )


if __name__ == "__main__":
    generate()
    print(f"generated LLM wiki under {WIKI.relative_to(ROOT)}")
