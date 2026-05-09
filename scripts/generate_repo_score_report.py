#!/usr/bin/env python3
"""Generate a local HTML readiness report for this agent-engineering guide repo.

The report applies the repository's `agent_readiness_scoring` technique at the
repository level: it reuses task readiness scorecards, required artifact gates,
registry/taxonomy consistency checks, and local validation evidence.

Only Python stdlib is used so the report can run in clone/user distributions.
"""
from __future__ import annotations

import argparse
import dataclasses
import datetime as dt
import html
import json
import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_HTML = ROOT / "reports" / "repo-readiness-report.html"
DEFAULT_JSON = ROOT / "reports" / "repo-readiness-report.json"


@dataclasses.dataclass
class Check:
    name: str
    passed: bool
    evidence: str
    files: list[str]
    risk: str = ""


@dataclasses.dataclass
class Area:
    name: str
    weight: float
    score: float
    evidence: list[str]
    gaps: list[str]
    files: list[str]


def rel(path: Path | str) -> str:
    path_obj = Path(path)
    if path_obj.is_absolute():
        try:
            return path_obj.relative_to(ROOT).as_posix()
        except ValueError:
            return path_obj.as_posix()
    return path_obj.as_posix()


def read_text(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def exists(path: str) -> bool:
    return (ROOT / path).exists()


def registry_ids() -> list[str]:
    if not exists("techniques/registry.yaml"):
        return []
    return re.findall(
        r"^\s*- id:\s*([a-zA-Z0-9_-]+)\s*$",
        read_text("techniques/registry.yaml"),
        flags=re.MULTILINE,
    )


def playbook_required_artifacts() -> list[str]:
    if not exists("agent-playbook.yaml"):
        return []
    return re.findall(
        r"^\s*-\s*path:\s*([a-zA-Z0-9_.-]+)\s*$",
        read_text("agent-playbook.yaml"),
        flags=re.MULTILINE,
    )


def playbook_mandatory_techniques() -> list[str]:
    if not exists("agent-playbook.yaml"):
        return []
    text = read_text("agent-playbook.yaml")
    match = re.search(r"^mandatory_technique_consideration:\s*$", text, flags=re.MULTILINE)
    if not match:
        return []
    tail = text[match.end() :]
    next_top_level = re.search(r"^[a-zA-Z_][a-zA-Z0-9_]*:\s*$", tail, flags=re.MULTILINE)
    block = tail[: next_top_level.start()] if next_top_level else tail
    return re.findall(r"^\s*-\s*([a-zA-Z0-9_-]+)\s*$", block, flags=re.MULTILINE)


def taxonomy_technique_refs() -> list[str]:
    if not exists("techniques/taxonomy.yaml"):
        return []
    refs: list[str] = []
    current_key: str | None = None
    for line in read_text("techniques/taxonomy.yaml").splitlines():
        key_match = re.match(r"\s*(techniques|must|should|optional):\s*$", line)
        if key_match:
            current_key = key_match.group(1)
            continue
        if current_key:
            if re.match(r"\S", line):
                current_key = None
                continue
            item_match = re.match(r"\s+-\s*([a-zA-Z0-9_]+)\s*$", line)
            if item_match:
                refs.append(item_match.group(1))
    return refs


def score_from_checks(name: str, weight: float, checks: list[Check]) -> Area:
    if not checks:
        return Area(name, weight, 0.0, [], ["No checks were defined."], [])
    passed = sum(1 for check in checks if check.passed)
    score = weight * passed / len(checks)
    evidence = [check.evidence for check in checks if check.passed]
    gaps = [check.risk or check.evidence for check in checks if not check.passed]
    files = sorted({path for check in checks for path in check.files})
    return Area(name, weight, score, evidence, gaps, files)


def command_result(cmd: list[str]) -> dict[str, object]:
    completed = subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True)
    output = (completed.stdout + "\n" + completed.stderr).strip()
    return {
        "cmd": " ".join(cmd),
        "returncode": completed.returncode,
        "passed": completed.returncode == 0,
        "output": output,
    }


def parse_scorecard(path: Path) -> dict[str, object]:
    text = path.read_text(encoding="utf-8")
    match = re.search(
        r"Overall readiness(?: score)?:\s*(\d+)\s*/\s*100",
        text,
        flags=re.IGNORECASE,
    )
    score = int(match.group(1)) if match else None
    title_match = re.search(r"^#\s+(.+)$", text, flags=re.MULTILINE)
    status_match = re.search(r"Readiness status:\s*([^\n]+)", text, flags=re.IGNORECASE)
    gate_match = re.search(r"## Gate Decision\s*\n\n(.+?)(?:\n## |\Z)", text, flags=re.IGNORECASE | re.DOTALL)
    return {
        "path": rel(path),
        "title": title_match.group(1).strip() if title_match else path.parent.name,
        "score": score,
        "status": status_match.group(1).strip() if status_match else "not explicitly stated",
        "gate_decision": " ".join(gate_match.group(1).split()) if gate_match else "not found",
    }


def scorecard_has_explicit_gate(card: dict[str, object]) -> bool:
    decision = str(card.get("gate_decision", "")).strip().lower()
    return bool(decision) and decision != "not found"


def discover_task_dirs() -> list[Path]:
    dirs: list[Path] = []
    for parent in [ROOT / "tasks", ROOT / "maintainer" / "tasks"]:
        if parent.exists():
            dirs.extend(sorted(path.parent for path in parent.glob("*/readiness-scorecard.md")))
    return dirs


def build_report(run_tests: bool) -> dict[str, object]:
    ids = registry_ids()
    mandatory = playbook_mandatory_techniques()
    required_artifacts = playbook_required_artifacts()
    taxonomy_refs = taxonomy_technique_refs()
    task_dirs = discover_task_dirs()

    validation_results = [command_result([sys.executable, "scripts/validate_agent_task.py", rel(task_dir)]) for task_dir in task_dirs]
    scorecards = [parse_scorecard(task_dir / "readiness-scorecard.md") for task_dir in task_dirs]
    numeric_scores = [item["score"] for item in scorecards if isinstance(item["score"], int)]
    average_task_score = sum(numeric_scores) / len(numeric_scores) if numeric_scores else 0.0
    validation_pass_ratio = (
        sum(1 for result in validation_results if result["passed"]) / len(validation_results)
        if validation_results
        else 0.0
    )

    full_test_result = command_result([sys.executable, "scripts/test_agent_guide.py"]) if run_tests else None

    registry_missing_from_playbook = sorted(set(ids) - set(mandatory))
    unknown_playbook_ids = sorted(set(mandatory) - set(ids))
    taxonomy_unknown_refs = sorted(set(taxonomy_refs) - set(ids))
    technique_template_text = read_text("templates/technique-selection.yaml") if exists("templates/technique-selection.yaml") else ""
    template_missing_ids = [tech_id for tech_id in ids if f"id: {tech_id}" not in technique_template_text]

    areas: list[Area] = []
    areas.append(
        score_from_checks(
            "Boot/control contract",
            12,
            [
                Check("playbook", exists("agent-playbook.yaml"), "agent-playbook.yaml exists and declares the execution contract.", ["agent-playbook.yaml"]),
                Check("agents", exists("AGENTS.md") and "Default Response Brevity" in read_text("AGENTS.md"), "AGENTS.md includes the repository operating contract and brevity policy.", ["AGENTS.md"]),
                Check("build workflow", exists("workflows/build-agent.md"), "workflows/build-agent.md is available for build/evaluate flows.", ["workflows/build-agent.md"]),
                Check("intake workflow", exists("workflows/intake.md"), "workflows/intake.md defines the standardized intake gate.", ["workflows/intake.md"]),
                Check("readme", exists("README.md") and "readiness-scorecard.md" in read_text("README.md"), "README.md documents readiness-scorecard use.", ["README.md"]),
                Check("security", exists("SECURITY.md"), "SECURITY.md is present for clone/runtime safety boundaries.", ["SECURITY.md"]),
            ],
        )
    )
    areas.append(
        score_from_checks(
            "Technique registry coverage",
            14,
            [
                Check("registry ids", bool(ids) and len(ids) == len(set(ids)), f"Registry has {len(ids)} unique technique ids.", ["techniques/registry.yaml"], "Technique ids are missing or duplicated."),
                Check("playbook coverage", not registry_missing_from_playbook and not unknown_playbook_ids, "Playbook mandatory technique list matches the registry.", ["agent-playbook.yaml", "techniques/registry.yaml"], f"Missing from playbook: {registry_missing_from_playbook}; unknown ids: {unknown_playbook_ids}"),
                Check("taxonomy refs", bool(taxonomy_refs) and not taxonomy_unknown_refs, "Taxonomy technique references resolve to registry ids.", ["techniques/taxonomy.yaml", "techniques/registry.yaml"], f"Unknown taxonomy refs: {taxonomy_unknown_refs}"),
                Check("selection template coverage", bool(ids) and not template_missing_ids, "Technique-selection template considers every registry technique.", ["templates/technique-selection.yaml", "techniques/registry.yaml"], f"Technique-selection template missing ids: {template_missing_ids}"),
            ],
        )
    )
    missing_templates = [artifact for artifact in required_artifacts if not exists(f"templates/{artifact}")]
    areas.append(
        score_from_checks(
            "Artifact templates and scaffolding",
            14,
            [
                Check("required artifacts", len(required_artifacts) >= 16, f"Playbook declares {len(required_artifacts)} required task artifacts.", ["agent-playbook.yaml"], "Required artifact list is missing or too small."),
                Check("templates", not missing_templates, "Every playbook-required artifact has a template.", ["templates/"], f"Missing templates: {missing_templates}"),
                Check("scaffolder", exists("scripts/new_agent_task.py") and "load_required_files" in read_text("scripts/new_agent_task.py"), "Task scaffolder reads artifact requirements from the playbook.", ["scripts/new_agent_task.py"], "Scaffolder is missing or hard-coded."),
                Check("validator", exists("scripts/validate_agent_task.py") and "load_required_files" in read_text("scripts/validate_agent_task.py"), "Task validator reads artifact requirements from the playbook.", ["scripts/validate_agent_task.py"], "Validator is missing or hard-coded."),
                Check("score validator", exists("scripts/validate_agent_task.py") and "validate_readiness_scorecard" in read_text("scripts/validate_agent_task.py"), "Validator enforces readiness-scorecard arithmetic.", ["scripts/validate_agent_task.py"], "Readiness-scorecard validation is absent."),
            ],
        )
    )
    task_governance_checks = [
        Check(
            "scorecards exist",
            bool(scorecards),
            f"{len(scorecards)} task scorecard(s) found; average task readiness is {average_task_score:.1f}/100.",
            [str(item["path"]) for item in scorecards] or ["tasks/"],
            "No task readiness scorecards were found.",
        ),
        Check(
            "numeric scores",
            len(numeric_scores) == len(scorecards) and bool(scorecards),
            "Every discovered task scorecard has a numeric readiness score.",
            [str(item["path"]) for item in scorecards],
            "At least one task scorecard is missing a numeric readiness score.",
        ),
        Check(
            "validators pass",
            validation_pass_ratio == 1.0 and bool(validation_results),
            f"{sum(1 for result in validation_results if result['passed'])}/{len(validation_results)} task validators passed.",
            [str(item["path"]) for item in scorecards],
            "At least one task validator failed; inspect validation evidence before using the task.",
        ),
        Check(
            "gate decisions explicit",
            all(scorecard_has_explicit_gate(card) for card in scorecards) and bool(scorecards),
            "Every task scorecard has an explicit gate decision, so prototype/live-readiness limits are visible.",
            [str(item["path"]) for item in scorecards],
            "At least one task scorecard lacks a gate decision.",
        ),
        Check(
            "lower scores bounded",
            all(
                not isinstance(card["score"], int)
                or int(card["score"]) >= 80
                or any(word in str(card["gate_decision"]).lower() for word in ["prototype", "not ready", "not proceed", "blocked"])
                for card in scorecards
            )
            and bool(scorecards),
            "Lower-scoring tasks are explicitly bounded as prototype/not-live-ready, so they are portfolio insight rather than a repo-control failure.",
            [str(item["path"]) for item in scorecards],
            "A lower-scoring task does not clearly state its prototype/not-live-ready boundary.",
        ),
    ]
    areas.append(
        score_from_checks(
            "Existing task scorecard governance",
            16,
            task_governance_checks,
        )
    )
    eval_checks = [
        Check("test suite", exists("scripts/test_agent_guide.py"), "Repository-level contract test suite exists.", ["scripts/test_agent_guide.py"]),
        Check("validator coverage", exists("scripts/test_agent_guide.py") and "test_scaffold_and_validator_behavior" in read_text("scripts/test_agent_guide.py"), "Tests cover scaffolding and validator behavior.", ["scripts/test_agent_guide.py"]),
        Check("existing scorecard coverage", exists("scripts/test_agent_guide.py") and "test_existing_task_readiness_scorecards_are_verifiable" in read_text("scripts/test_agent_guide.py"), "Tests verify existing task readiness scorecards.", ["scripts/test_agent_guide.py"]),
        Check("ci workflow", exists(".github/workflows/validate.yml") and "workflow_dispatch:" in read_text(".github/workflows/validate.yml"), "Manual validation workflow exists.", [".github/workflows/validate.yml"]),
    ]
    if run_tests and full_test_result is not None:
        eval_checks.append(
            Check(
                "fresh test run",
                bool(full_test_result["passed"]),
                f"Fresh test run passed: {full_test_result['cmd']}",
                ["scripts/test_agent_guide.py"],
                f"Fresh test run failed: {full_test_result['output'][-500:]}",
            )
        )
    else:
        eval_checks.append(
            Check(
                "fresh test run",
                False,
                "Fresh test run was skipped.",
                ["scripts/test_agent_guide.py"],
                "Run with --run-tests to include current test evidence.",
            )
        )
    areas.append(score_from_checks("Evaluation and verification harness", 14, eval_checks))
    areas.append(
        score_from_checks(
            "Wiki and source verification",
            10,
            [
                Check("wiki index", exists("wiki/index.md") and "not** the source of truth" in read_text("wiki/index.md"), "Wiki index exists and preserves source-of-truth boundary.", ["wiki/index.md"]),
                Check("technique map", exists("wiki/technique-map.md"), "Technique map exists for graph orientation.", ["wiki/technique-map.md"]),
                Check("registry source bridge", exists("wiki/sources/techniques-registry.md"), "Registry source bridge exists.", ["wiki/sources/techniques-registry.md"]),
                Check("task wiki", bool(list((ROOT / "wiki" / "tasks").glob("*.md"))) if exists("wiki/tasks") else False, "Task wiki pages exist.", ["wiki/tasks/"], "Task wiki pages are missing."),
                Check("obsidian graph", exists(".obsidian/graph.json"), "Obsidian graph configuration exists.", [".obsidian/graph.json"]),
            ],
        )
    )
    areas.append(
        score_from_checks(
            "Maintainer discovery/radar loop",
            10,
            [
                Check("radar script", exists("maintainer/scripts/weekly_repo_radar.py"), "Maintainer radar scoring script exists.", ["maintainer/scripts/weekly_repo_radar.py"]),
                Check("radar config", exists("maintainer/radar-config.yaml"), "Maintainer radar config exists.", ["maintainer/radar-config.yaml"]),
                Check("radar workflow", exists("maintainer/workflows/weekly-repo-radar.md"), "Maintainer radar workflow exists.", ["maintainer/workflows/weekly-repo-radar.md"]),
                Check("github workflow", exists(".github/workflows/weekly-repo-radar.yml") and "workflow_dispatch:" in read_text(".github/workflows/weekly-repo-radar.yml"), "Weekly radar GitHub workflow is manual-dispatchable.", [".github/workflows/weekly-repo-radar.yml"]),
                Check("radar artifacts", bool(list((ROOT / "maintainer" / "radar").glob("*-candidates.yaml"))) if exists("maintainer/radar") else False, "Radar candidate artifacts exist for review.", ["maintainer/radar/"], "Radar candidate artifacts are missing."),
            ],
        )
    )
    areas.append(
        score_from_checks(
            "Security, privacy, and distribution posture",
            8,
            [
                Check("security doc", exists("SECURITY.md") and "does not execute code from candidate repositories" in read_text("SECURITY.md"), "SECURITY.md documents external repository execution boundary.", ["SECURITY.md"]),
                Check("distribution manifest", exists("distribution/user-export-manifest.yaml"), "User distribution manifest exists.", ["distribution/user-export-manifest.yaml"]),
                Check("user distribution", exists("distribution/user/AGENTS.md") and exists("distribution/user/agent-playbook.yaml"), "User distribution overrides AGENTS/playbook.", ["distribution/user/AGENTS.md", "distribution/user/agent-playbook.yaml"]),
                Check("publish boundary", exists(".github/workflows/publish-user-distribution.yml") and "USER_DISTRIBUTION_TOKEN" in read_text(".github/workflows/publish-user-distribution.yml"), "Publish workflow requires explicit target token.", [".github/workflows/publish-user-distribution.yml"]),
            ],
        )
    )
    areas.append(
        score_from_checks(
            "HTML report operability",
            2,
            [
                Check("generator", exists("scripts/generate_repo_score_report.py"), "HTML report generator exists.", ["scripts/generate_repo_score_report.py"]),
                Check("output target", True, "Report can be emitted as a static local HTML file.", ["reports/repo-readiness-report.html"]),
            ],
        )
    )

    total_score = sum(area.score for area in areas)
    total_weight = sum(area.weight for area in areas)
    status = (
        "ready-for-maintainer-use"
        if total_score >= 90
        else "needs-focused-fixes"
        if total_score >= 75
        else "blocked"
    )
    top_gaps = [gap for area in areas for gap in area.gaps][:8]

    return {
        "generated_at": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
        "technique": {
            "id": "agent_readiness_scoring",
            "source": "techniques/registry.yaml",
            "wiki": "wiki/techniques/agent_readiness_scoring.md",
        },
        "summary": {
            "score": round(total_score, 1),
            "weight": round(total_weight, 1),
            "status": status,
            "top_gaps": top_gaps,
            "task_portfolio_average": round(average_task_score, 1),
        },
        "areas": [dataclasses.asdict(area) for area in areas],
        "scorecards": scorecards,
        "validation_results": validation_results,
        "test_result": full_test_result,
    }


def local_link(report_path: Path, target: str) -> str:
    target_path = ROOT / target
    try:
        return html.escape(Path("../" + target_path.relative_to(ROOT).as_posix()).as_posix())
    except ValueError:
        return html.escape(target)


def render_files(report_path: Path, files: list[str]) -> str:
    if not files:
        return ""
    links = []
    for file in files[:6]:
        display = html.escape(file)
        links.append(f'<a href="{local_link(report_path, file)}">{display}</a>')
    if len(files) > 6:
        links.append(f"<span>+{len(files) - 6} more</span>")
    return ", ".join(links)


def badge(score: float, weight: float) -> str:
    ratio = score / weight if weight else 0
    if ratio >= 0.9:
        return "green"
    if ratio >= 0.75:
        return "yellow"
    return "red"


def render_html(report: dict[str, object], output: Path) -> str:
    summary = report["summary"]  # type: ignore[index]
    areas: list[dict[str, object]] = report["areas"]  # type: ignore[assignment,index]
    scorecards: list[dict[str, object]] = report["scorecards"]  # type: ignore[assignment,index]
    validation_results: list[dict[str, object]] = report["validation_results"]  # type: ignore[assignment,index]
    test_result = report["test_result"]  # type: ignore[index]
    score = float(summary["score"])  # type: ignore[index]
    status = str(summary["status"])  # type: ignore[index]
    task_portfolio_average = float(summary["task_portfolio_average"])  # type: ignore[index]
    top_gaps: list[str] = summary["top_gaps"]  # type: ignore[assignment,index]
    generated_at = str(report["generated_at"])
    test_badge = "pass" if test_result and test_result["passed"] else "skipped/fail"

    area_rows = "\n".join(
        f"""
        <tr>
          <td><strong>{html.escape(str(area['name']))}</strong><span class="pill {badge(float(area['score']), float(area['weight']))}">{float(area['score']):.1f}/{float(area['weight']):.0f}</span></td>
          <td>{html.escape('; '.join(str(item) for item in area['evidence'][:3]))}</td>
          <td>{html.escape('; '.join(str(item) for item in area['gaps']) or 'No material gap found.')}</td>
          <td>{render_files(output, list(area['files']))}</td>
        </tr>
        """
        for area in areas
    )
    scorecard_rows = "\n".join(
        f"""
        <tr>
          <td><a href="{local_link(output, str(card['path']))}">{html.escape(str(card['path']))}</a></td>
          <td>{html.escape(str(card['title']))}</td>
          <td>{html.escape(str(card['score']))}/100</td>
          <td>{html.escape(str(card['status']))}</td>
          <td>{html.escape(str(card['gate_decision']))}</td>
        </tr>
        """
        for card in scorecards
    )
    validation_rows = "\n".join(
        f"""
        <tr>
          <td><code>{html.escape(str(result['cmd']))}</code></td>
          <td><span class="pill {'green' if result['passed'] else 'red'}">{'passed' if result['passed'] else 'failed'}</span></td>
        </tr>
        """
        for result in validation_results
    )
    gaps_list = "\n".join(f"<li>{html.escape(gap)}</li>" for gap in top_gaps) or "<li>No material gap found.</li>"
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Repository Readiness Score Report</title>
  <style>
    :root {{
      color-scheme: light dark;
      --bg: #0f172a;
      --panel: #111827;
      --text: #e5e7eb;
      --muted: #9ca3af;
      --line: #243244;
      --green: #22c55e;
      --yellow: #f59e0b;
      --red: #ef4444;
      --blue: #38bdf8;
    }}
    body {{ margin: 0; font-family: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; background: var(--bg); color: var(--text); }}
    main {{ max-width: 1180px; margin: 0 auto; padding: 32px 20px 56px; }}
    a {{ color: var(--blue); text-decoration: none; }}
    a:hover {{ text-decoration: underline; }}
    .hero {{ display: grid; grid-template-columns: minmax(180px, 240px) 1fr; gap: 24px; align-items: stretch; }}
    .card {{ background: linear-gradient(180deg, rgba(255,255,255,.04), rgba(255,255,255,.02)); border: 1px solid var(--line); border-radius: 18px; padding: 22px; box-shadow: 0 20px 50px rgba(0,0,0,.18); }}
    .score {{ font-size: 56px; font-weight: 800; line-height: 1; }}
    .muted {{ color: var(--muted); }}
    h1, h2 {{ letter-spacing: -0.025em; }}
    h1 {{ margin: 0 0 10px; font-size: 36px; }}
    h2 {{ margin: 34px 0 14px; }}
    table {{ width: 100%; border-collapse: collapse; overflow: hidden; border-radius: 14px; }}
    th, td {{ border-bottom: 1px solid var(--line); padding: 12px; text-align: left; vertical-align: top; }}
    th {{ color: var(--muted); font-size: 13px; text-transform: uppercase; letter-spacing: .06em; }}
    tr:hover td {{ background: rgba(255,255,255,.025); }}
    .pill {{ display: inline-block; margin-left: 8px; padding: 3px 8px; border-radius: 999px; font-size: 12px; font-weight: 700; color: #061019; }}
    .green {{ background: var(--green); }}
    .yellow {{ background: var(--yellow); }}
    .red {{ background: var(--red); color: #fff; }}
    .grid {{ display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 14px; }}
    .small {{ font-size: 13px; }}
    code {{ color: #bae6fd; }}
    @media (max-width: 860px) {{ .hero, .grid {{ grid-template-columns: 1fr; }} table {{ font-size: 13px; }} }}
  </style>
</head>
<body>
<main>
  <section class="hero">
    <div class="card">
      <div class="muted">Overall score</div>
      <div class="score">{score:.1f}</div>
      <div class="muted">/ 100</div>
      <p><span class="pill {badge(score, 100)}">{html.escape(status)}</span></p>
    </div>
    <div class="card">
      <h1>Repository Readiness Score Report</h1>
      <p>This report applies <a href="{local_link(output, 'wiki/techniques/agent_readiness_scoring.md')}"><code>agent_readiness_scoring</code></a> to the current repository using local control files, task scorecards, validator results, and optional test evidence.</p>
      <p class="muted small">Generated at {html.escape(generated_at)}. Fresh test evidence: <strong>{html.escape(test_badge)}</strong>.</p>
      <p class="small">Source technique: <a href="{local_link(output, 'techniques/registry.yaml')}">techniques/registry.yaml</a> · Validator: <a href="{local_link(output, 'scripts/validate_agent_task.py')}">scripts/validate_agent_task.py</a></p>
    </div>
  </section>

  <section class="grid">
    <div class="card small"><strong>Technique</strong><br><code>agent_readiness_scoring</code></div>
    <div class="card small"><strong>Task scorecards</strong><br>{len(scorecards)} found, validators {sum(1 for result in validation_results if result['passed'])}/{len(validation_results)} passed; portfolio average {task_portfolio_average:.1f}/100</div>
    <div class="card small"><strong>Report file</strong><br><code>{html.escape(rel(output))}</code></div>
  </section>

  <h2>Top gaps / risks</h2>
  <div class="card"><ul>{gaps_list}</ul></div>

  <h2>Weighted score areas</h2>
  <div class="card">
    <table>
      <thead><tr><th>Area</th><th>Evidence</th><th>Gap / risk</th><th>Files</th></tr></thead>
      <tbody>{area_rows}</tbody>
    </table>
  </div>

  <h2>Task readiness scorecards</h2>
  <div class="card">
    <table>
      <thead><tr><th>File</th><th>Title</th><th>Score</th><th>Status</th><th>Gate decision</th></tr></thead>
      <tbody>{scorecard_rows}</tbody>
    </table>
  </div>

  <h2>Validation evidence</h2>
  <div class="card">
    <table>
      <thead><tr><th>Command</th><th>Result</th></tr></thead>
      <tbody>{validation_rows}</tbody>
    </table>
    <p class="muted small">Full repository test command: <code>python3 scripts/test_agent_guide.py</code>{' passed during generation.' if test_result and test_result['passed'] else ' was not run or did not pass during generation.'}</p>
  </div>
</main>
</body>
</html>
"""


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Generate a static HTML readiness report for this repository.")
    parser.add_argument("--output", default=str(DEFAULT_HTML), help="HTML output path.")
    parser.add_argument("--json-output", default=str(DEFAULT_JSON), help="JSON evidence output path.")
    parser.add_argument("--run-tests", action="store_true", help="Run scripts/test_agent_guide.py and include fresh pass/fail evidence.")
    args = parser.parse_args(argv)

    output = Path(args.output)
    if not output.is_absolute():
        output = ROOT / output
    json_output = Path(args.json_output)
    if not json_output.is_absolute():
        json_output = ROOT / json_output

    report = build_report(run_tests=args.run_tests)
    output.parent.mkdir(parents=True, exist_ok=True)
    json_output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_html(report, output), encoding="utf-8")
    json_output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    summary = report["summary"]
    print(
        f"Generated {rel(output)} ({summary['score']}/100, {summary['status']}); "
        f"evidence JSON: {rel(json_output)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
