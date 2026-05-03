#!/usr/bin/env python3
"""Repository-level completeness tests for the agent-engineering guide.

These tests intentionally use only stdlib and validate the guide as an executable
agent contract: registry consistency, taxonomy references, scaffolding, validator
behavior, and radar filtering/report generation.
"""
from __future__ import annotations

import importlib.util
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def assert_true(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def registry_ids() -> list[str]:
    return re.findall(r"^\s*- id:\s*([a-zA-Z0-9_-]+)\s*$", read("techniques/registry.yaml"), flags=re.MULTILINE)


def yaml_list_after_key(text: str, key: str) -> list[str]:
    values: list[str] = []
    in_block = False
    block_indent: int | None = None
    for line in text.splitlines():
        if re.match(rf"\s*{re.escape(key)}:\s*$", line):
            in_block = True
            block_indent = None
            continue
        if not in_block:
            continue
        if not line.strip():
            continue
        indent = len(line) - len(line.lstrip(" "))
        if block_indent is not None and indent < block_indent:
            break
        match = re.match(r"\s*-\s*([a-zA-Z0-9_./*-]+)\s*$", line)
        if match:
            block_indent = indent
            values.append(match.group(1))
        elif block_indent is not None and indent <= block_indent:
            break
    return values


def load_radar_module():
    path = ROOT / "scripts" / "weekly_repo_radar.py"
    spec = importlib.util.spec_from_file_location("weekly_repo_radar", path)
    assert_true(spec is not None and spec.loader is not None, "cannot load weekly_repo_radar module")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def filled_task_text(template_name: str) -> str:
    text = read(f"templates/{template_name}")
    text = text.replace("<task-slug>", "qa-complete-agent")
    text = text.replace("<name>", "qa-tool")
    text = text.replace("<short name>", "qa-failure")
    text = text.replace("TODO", "Concrete QA-filled content")
    text = text.replace(
        "reason: Concrete QA-filled content",
        "reason: required for repository completeness validation",
    )
    text = re.sub(r"(:)\n", r"\1 Concrete QA-filled content\n", text)
    return text


def run(cmd: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True)


def test_registry_playbook_template_consistency() -> None:
    ids = registry_ids()
    assert_true(ids, "technique registry has no ids")
    assert_true(len(ids) == len(set(ids)), "duplicate technique ids found")

    playbook = read("agent-playbook.yaml")
    mandatory = yaml_list_after_key(playbook, "mandatory_technique_consideration")
    missing_from_playbook = sorted(set(ids) - set(mandatory))
    extra_in_playbook = sorted(set(mandatory) - set(ids))
    assert_true(not missing_from_playbook, f"registry ids missing from playbook: {missing_from_playbook}")
    assert_true(not extra_in_playbook, f"unknown playbook technique ids: {extra_in_playbook}")

    technique_template = read("templates/technique-selection.yaml")
    missing_from_template = [tech_id for tech_id in ids if f"id: {tech_id}" not in technique_template]
    assert_true(not missing_from_template, f"registry ids missing from technique-selection template: {missing_from_template}")


def test_required_artifact_alignment() -> None:
    playbook = read("agent-playbook.yaml")
    required_from_playbook = re.findall(r"path:\s*([a-zA-Z0-9_.-]+)", playbook)
    assert_true(required_from_playbook, "playbook has no required artifact paths")

    for artifact in required_from_playbook:
        assert_true((ROOT / "templates" / artifact).exists(), f"missing template for {artifact}")

    new_script = read("scripts/new_agent_task.py")
    validator_script = read("scripts/validate_agent_task.py")
    assert_true("agent-playbook.yaml" in new_script, "new task scaffolder must read required artifacts from playbook")
    assert_true("agent-playbook.yaml" in validator_script, "validator must read required artifacts from playbook")
    assert_true("load_required_files" in new_script, "new task scaffolder missing dynamic required-file loader")
    assert_true("load_required_files" in validator_script, "validator missing dynamic required-file loader")


def test_production_grade_techniques_present() -> None:
    ids = set(registry_ids())
    expected_ids = {
        "structured_output_schema_validation",
        "guardrails_tripwires",
        "retrieval_memory_governance",
        "genai_telemetry_standardization",
        "model_routing_fallback_policy",
        "security_privacy_data_governance",
        "deployment_rollout_canary",
        "token_efficiency_budget_gate",
    }
    missing = sorted(expected_ids - ids)
    assert_true(not missing, f"missing production-grade technique ids: {missing}")

    playbook = read("agent-playbook.yaml")
    expected_artifacts = {
        "output-schema.md",
        "guardrails.md",
        "retrieval-memory.md",
        "telemetry.md",
        "model-routing.md",
        "security-privacy.md",
        "release-rollout.md",
    }
    missing_artifacts = [artifact for artifact in expected_artifacts if f"path: {artifact}" not in playbook]
    assert_true(not missing_artifacts, f"missing production-grade required artifacts: {missing_artifacts}")

    radar_config = read("repos/radar-config.yaml")
    for keyword in ["structured outputs", "guardrails", "telemetry", "model routing", "security privacy", "canary rollout"]:
        assert_true(keyword in radar_config, f"radar config missing discovery phrase: {keyword}")


def test_taxonomy_references_are_valid() -> None:
    ids = set(registry_ids())
    taxonomy = read("techniques/taxonomy.yaml")
    referenced = re.findall(r"^\s*-\s*([a-zA-Z0-9_]+)\s*$", taxonomy, flags=re.MULTILINE)
    # Filter out category/profile ids by only checking values that look like known technique ids or appear in technique-ish sections.
    unknown = sorted({item for item in referenced if item.endswith("_engineering") or item in ids} - ids)
    assert_true(not unknown, f"taxonomy references unknown techniques: {unknown}")

    # Stronger section-aware scan: any list item under techniques/must/should/optional must be a registry id.
    current_key: str | None = None
    bad_refs: list[str] = []
    for line in taxonomy.splitlines():
        key_match = re.match(r"\s*(techniques|must|should|optional):\s*$", line)
        if key_match:
            current_key = key_match.group(1)
            continue
        if current_key:
            if re.match(r"\S", line):
                current_key = None
                continue
            item_match = re.match(r"\s+-\s*([a-zA-Z0-9_]+)\s*$", line)
            if item_match and item_match.group(1) not in ids:
                bad_refs.append(f"{current_key}:{item_match.group(1)}")
    assert_true(not bad_refs, f"taxonomy has invalid technique refs: {bad_refs}")


def test_scaffold_and_validator_behavior() -> None:
    task_dir = ROOT / "tasks" / "qa-complete-agent"
    if task_dir.exists():
        shutil.rmtree(task_dir)
    try:
        result = run([sys.executable, "scripts/new_agent_task.py", "QA Complete Agent"])
        assert_true(result.returncode == 0, f"scaffolder failed: {result.stderr}\n{result.stdout}")
        assert_true(task_dir.exists(), "scaffolder did not create normalized task dir")

        placeholder_result = run([sys.executable, "scripts/validate_agent_task.py", str(task_dir)])
        assert_true(placeholder_result.returncode != 0, "validator should fail on placeholders")
        assert_true("placeholder remains" in placeholder_result.stdout, "placeholder failure not reported")

        required_artifacts = re.findall(r"path:\s*([a-zA-Z0-9_.-]+)", read("agent-playbook.yaml"))
        for artifact in required_artifacts:
            (task_dir / artifact).write_text(filled_task_text(artifact), encoding="utf-8")

        pass_result = run([sys.executable, "scripts/validate_agent_task.py", str(task_dir)])
        assert_true(pass_result.returncode == 0, f"validator should pass filled task: {pass_result.stdout}\n{pass_result.stderr}")
        assert_true("VALIDATION PASSED" in pass_result.stdout, "pass output missing")

        cost_file = task_dir / "cost-and-caching.md"
        original_cost = cost_file.read_text(encoding="utf-8")
        cost_file.write_text(original_cost.replace("- Max total tokens per run: Concrete QA-filled content", "- Max total tokens per run:"), encoding="utf-8")
        token_gate_result = run([sys.executable, "scripts/validate_agent_task.py", str(task_dir)])
        assert_true(token_gate_result.returncode != 0, "validator should fail on empty token hard-gate field")
        assert_true("empty token efficiency field: Max total tokens per run" in token_gate_result.stdout, "token hard-gate failure not reported")
        cost_file.write_text(original_cost, encoding="utf-8")

        missing = task_dir / "eval-spec.md"
        missing.unlink()
        missing_result = run([sys.executable, "scripts/validate_agent_task.py", str(task_dir)])
        assert_true(missing_result.returncode != 0, "validator should fail on missing required artifact")
        assert_true("missing required file: eval-spec.md" in missing_result.stdout, "missing file not reported")
    finally:
        if task_dir.exists():
            shutil.rmtree(task_dir)


def test_radar_config_filtering_and_report_generation() -> None:
    radar = load_radar_module()
    config = radar.parse_config(ROOT / "repos" / "radar-config.yaml")
    queries = radar.render_queries(config["queries"], radar.dt.date(2026, 5, 3))
    assert_true(queries, "radar has no queries")
    assert_true(all("{year_start}" not in query for query in queries), "query templates were not rendered")
    assert_true(any("agent" in query.lower() for query in queries), "radar queries are not agent-focused")

    technique_repo = {
        "full_name": "example/agent-harness-evals",
        "name": "agent-harness-evals",
        "description": "Reusable agent harness with eval regression tracing and MCP tool permissions",
        "topics": ["agent-harness", "evals", "mcp", "observability"],
    }
    is_match, score, reasons = radar.technique_match(
        technique_repo,
        config["required_any_keywords"],
        config["exclude_keywords"],
        int(config["min_technique_score"]),
    )
    assert_true(is_match, f"known technique repo should match: score={score}, reasons={reasons}")

    domain_app = {
        "full_name": "example/flight-agent",
        "name": "flight-agent",
        "description": "Agent-native flight search and booking app for travel",
        "topics": ["ai-agent", "booking", "travel"],
    }
    is_match, score, reasons = radar.technique_match(
        domain_app,
        config["required_any_keywords"],
        config["exclude_keywords"],
        int(config["min_technique_score"]),
    )
    assert_true(not is_match, f"domain app should be filtered: score={score}, reasons={reasons}")

    md_path = ROOT / "repos" / "radar" / "2099-01-01.md"
    yaml_path = ROOT / "repos" / "radar" / "2099-01-01-candidates.yaml"
    candidate = {
        "name": "example/agent-harness-evals",
        "url": "https://github.com/example/agent-harness-evals",
        "status": "candidate",
        "score": 123,
        "technique_score": 20,
        "stars": 1000,
        "previous_stars": 900,
        "star_delta": 100,
        "forks": 50,
        "open_issues": 2,
        "language": "Python",
        "license": "MIT",
        "pushed_at": "2099-01-01T00:00:00Z",
        "description": "Reusable agent harness with eval regression tracing",
        "topics": ["agent", "harness", "evals"],
        "technique_match_reasons": ["required_any=agent,harness", "technique_score=20"],
        "matched_queries": [queries[0]],
        "review_action": "human_review_required",
    }
    try:
        radar.write_markdown(md_path, radar.dt.date(2099, 1, 1), [candidate], queries, [])
        radar.write_yaml(yaml_path, radar.dt.date(2099, 1, 1), [candidate], queries, [])
        assert_true("Primary source: **GitHub repositories**" in md_path.read_text(encoding="utf-8"), "markdown missing GitHub-first statement")
        assert_true("primary_source: github_repositories" in yaml_path.read_text(encoding="utf-8"), "yaml missing primary source")
        assert_true("star_delta: 100" in yaml_path.read_text(encoding="utf-8"), "yaml missing star delta")
    finally:
        md_path.unlink(missing_ok=True)
        yaml_path.unlink(missing_ok=True)


def test_security_posture_contracts() -> None:
    validate_workflow = read(".github/workflows/validate.yml")
    assert_true("permissions:" in validate_workflow and "contents: read" in validate_workflow, "validate workflow must be read-only")

    weekly_workflow = read(".github/workflows/weekly-repo-radar.yml")
    assert_true("contents: write" in weekly_workflow and "pull-requests: write" in weekly_workflow, "weekly workflow write permissions must be explicit")

    security = read("SECURITY.md")
    assert_true("Markdown/YAML files" in security, "SECURITY.md missing clone safety statement")
    assert_true("does not execute code from candidate repositories" in security, "SECURITY.md missing external repo execution boundary")
    assert_true("do not add PATs" in security, "SECURITY.md missing secret guidance")

    dependency_manifests = [
        "package.json",
        "package-lock.json",
        "requirements.txt",
        "pyproject.toml",
        "Pipfile",
        "poetry.lock",
        "pnpm-lock.yaml",
        "yarn.lock",
    ]
    present = [name for name in dependency_manifests if (ROOT / name).exists()]
    assert_true(not present, f"unexpected dependency manifest(s) found: {present}")

    radar = load_radar_module()
    assert_true(radar.markdown_cell("<img src=x>|bad") == "&lt;img src=x&gt;\\|bad", "markdown cell escaping failed")
    assert_true(radar.markdown_url("javascript:alert(1)") == "https://github.com", "markdown URL allowlist failed")


def test_workflow_and_docs_contracts() -> None:
    workflow = read(".github/workflows/weekly-repo-radar.yml")
    assert_true("cron: '0 0 * * 1'" in workflow, "weekly radar cron missing or changed")
    assert_true("contents: write" in workflow and "pull-requests: write" in workflow, "workflow missing PR permissions")
    assert_true("scripts/weekly_repo_radar.py" in workflow, "workflow does not run radar script")

    agents = read("AGENTS.md")
    assert_true("GitHub repository discovery as the primary" in agents, "AGENTS missing GitHub-first policy")
    assert_true("1-2 sentences" in agents, "AGENTS missing response brevity policy")
    assert_true("readiness-scorecard.md" in agents, "AGENTS missing readiness scorecard gate")
    assert_true("output-schema.md" in agents, "AGENTS missing structured output schema gate")
    assert_true("guardrails.md" in agents, "AGENTS missing guardrails gate")
    assert_true("telemetry.md" in agents, "AGENTS missing telemetry gate")
    assert_true("security-privacy.md" in agents, "AGENTS missing security/privacy gate")
    assert_true("token efficiency budget gate" in agents.lower(), "AGENTS missing token efficiency hard gate")

    readme = read("README.md")
    assert_true("GitHub-first hot technique repository radar" in readme, "README missing GitHub-first framing")
    assert_true("1~2문장" in readme, "README missing Korean brevity guidance")
    assert_true("output schema" in readme, "README missing structured output gate")
    assert_true("security/privacy" in readme, "README missing security/privacy gate")
    assert_true("token-efficiency hard gate" in readme, "README missing token efficiency hard gate")
    assert_true("SECURITY.md" in readme, "README missing security posture doc")


def main() -> int:
    tests = [
        test_registry_playbook_template_consistency,
        test_required_artifact_alignment,
        test_production_grade_techniques_present,
        test_taxonomy_references_are_valid,
        test_scaffold_and_validator_behavior,
        test_radar_config_filtering_and_report_generation,
        test_security_posture_contracts,
        test_workflow_and_docs_contracts,
    ]
    failures: list[str] = []
    for test in tests:
        try:
            test()
            print(f"PASS {test.__name__}")
        except Exception as exc:  # noqa: BLE001 - report all test failures.
            failures.append(f"FAIL {test.__name__}: {exc}")
            print(failures[-1])
    if failures:
        print("\n".join(failures))
        return 1
    print(f"ALL TESTS PASSED ({len(tests)})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
