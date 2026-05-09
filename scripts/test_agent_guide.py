#!/usr/bin/env python3
"""Repository-level completeness tests for the agent-engineering guide.

These tests intentionally use only stdlib and validate the guide as an executable
agent contract: registry consistency, taxonomy references, scaffolding, validator
behavior, and radar filtering/report generation.
"""
from __future__ import annotations

import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEST_TASK_PREFIX = "qa-complete-agent-"


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
    path = ROOT / "maintainer" / "scripts" / "weekly_repo_radar.py"
    spec = importlib.util.spec_from_file_location("weekly_repo_radar", path)
    assert_true(spec is not None and spec.loader is not None, "cannot load weekly_repo_radar module")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_export_module():
    path = ROOT / "maintainer" / "scripts" / "export_user_distribution.py"
    spec = importlib.util.spec_from_file_location("export_user_distribution", path)
    assert_true(spec is not None and spec.loader is not None, "cannot load export_user_distribution module")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def filled_task_text(template_name: str, task_slug: str = "qa-complete-agent") -> str:
    if template_name == "readiness-scorecard.md":
        return f"""# Agent Readiness Scorecard: {task_slug}

Purpose: show whether this agent task is ready for implementation and what is missing.

## Summary

- Overall readiness score: 100 / 100
- Readiness status: ready-for-implementation
- Top missing items:
  - All required smoke-test fields are intentionally filled for validator coverage.

## Scoring Rubric

| Area | Weight | Score | Evidence | Missing / Risk | Required Before Implementation? |
| --- | ---: | ---: | --- | --- | --- |
| Intent and user outcome | 8 | 8 / 8 | Filled smoke artifact | Covered by validator test | yes |
| Scope and non-goals | 6 | 6 / 6 | Filled smoke artifact | Covered by validator test | yes |
| Input/output schema | 8 | 8 / 8 | Filled smoke artifact | Covered by validator test | yes |
| Technique selection | 6 | 6 / 6 | Filled smoke artifact | Covered by validator test | yes |
| Harness and eval plan | 8 | 8 / 8 | Filled smoke artifact | Covered by validator test | yes |
| Failure-case memory | 7 | 7 / 7 | Filled smoke artifact | Covered by validator test | yes |
| Guardrails and tripwires | 7 | 7 / 7 | Filled smoke artifact | Covered by validator test | yes |
| Tool contracts and permissions | 7 | 7 / 7 | Filled smoke artifact | Covered by validator test | yes |
| Retrieval and memory governance | 6 | 6 / 6 | Filled smoke artifact | Covered by validator test | yes when retrieval/memory exists |
| Token efficiency, cost, caching, and model routing | 10 | 10 / 10 | Filled smoke artifact | Covered by validator test | yes |
| Telemetry and traceability | 7 | 7 / 7 | Filled smoke artifact | Covered by validator test | yes |
| Security and privacy | 7 | 7 / 7 | Filled smoke artifact | Covered by validator test | yes when company/customer/internal data exists |
| Release, rollout, and rollback | 6 | 6 / 6 | Filled smoke artifact | Covered by validator test | yes when production/scheduled use exists |
| Human approval / handoff | 7 | 7 / 7 | Filled smoke artifact | Covered by validator test | yes |

## Readiness Map

```text
Intent             [green]
Scope              [green]
Schema             [green]
Techniques         [green]
Eval/Harness       [green]
Failures           [green]
Guardrails         [green]
Tools/Auth         [green]
Retrieval/Memory   [green]
Token/Cost Gate    [green]
Telemetry          [green]
Security/Privacy   [green]
Rollout/Rollback   [green]
Human Review       [green]
```

## Gate Decision

- Decision: proceed
- Reason: Smoke fixture is fully populated for validator coverage.
- Required fixes before implementation:
  - Keep score arithmetic valid.
"""
    text = read(f"templates/{template_name}")
    text = text.replace("<task-slug>", task_slug)
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

    assert_true("intake-form.md" in required_from_playbook, "playbook must require standardized intake form")
    for artifact in required_from_playbook:
        assert_true((ROOT / "templates" / artifact).exists(), f"missing template for {artifact}")

    new_script = read("scripts/new_agent_task.py")
    validator_script = read("scripts/validate_agent_task.py")
    assert_true("agent-playbook.yaml" in new_script, "new task scaffolder must read required artifacts from playbook")
    assert_true("agent-playbook.yaml" in validator_script, "validator must read required artifacts from playbook")
    assert_true("load_required_files" in new_script, "new task scaffolder missing dynamic required-file loader")
    assert_true("load_required_files" in validator_script, "validator missing dynamic required-file loader")
    assert_true("validate_intake_form" in validator_script, "validator must enforce intake completeness")
    assert_true("INTAKE_REQUIRED_SECTIONS" in validator_script, "validator missing intake section contract")


def test_production_grade_techniques_present() -> None:
    ids = set(registry_ids())
    expected_ids = {
        "standardized_intake_gate",
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

    radar_config = read("maintainer/radar-config.yaml")
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
    task_slug = f"{TEST_TASK_PREFIX}{os.getpid()}"
    task_dir = ROOT / "tasks" / task_slug
    if task_dir.exists():
        shutil.rmtree(task_dir)
    try:
        result = run([sys.executable, "scripts/new_agent_task.py", f"QA Complete Agent {os.getpid()}"])
        assert_true(result.returncode == 0, f"scaffolder failed: {result.stderr}\n{result.stdout}")
        assert_true(task_dir.exists(), "scaffolder did not create normalized task dir")
        assert_true((task_dir / "intake-form.md").exists(), "scaffolder did not create required intake form")

        placeholder_result = run([sys.executable, "scripts/validate_agent_task.py", str(task_dir)])
        assert_true(placeholder_result.returncode != 0, "validator should fail on placeholders")
        assert_true("placeholder remains" in placeholder_result.stdout, "placeholder failure not reported")

        required_artifacts = re.findall(r"path:\s*([a-zA-Z0-9_.-]+)", read("agent-playbook.yaml"))
        for artifact in required_artifacts:
            (task_dir / artifact).write_text(filled_task_text(artifact, task_slug), encoding="utf-8")

        pass_result = run([sys.executable, "scripts/validate_agent_task.py", str(task_dir)])
        assert_true(pass_result.returncode == 0, f"validator should pass filled task: {pass_result.stdout}\n{pass_result.stderr}")
        assert_true("VALIDATION PASSED" in pass_result.stdout, "pass output missing")

        readiness_file = task_dir / "readiness-scorecard.md"
        original_readiness = readiness_file.read_text(encoding="utf-8")
        readiness_file.write_text(original_readiness.replace("- Overall readiness score: 100 / 100", "- Overall readiness score: 99 / 100"), encoding="utf-8")
        score_result = run([sys.executable, "scripts/validate_agent_task.py", str(task_dir)])
        assert_true(score_result.returncode != 0, "validator should fail on readiness score mismatch")
        assert_true("summary score 99 does not match row total 100" in score_result.stdout, "readiness score mismatch not reported")
        readiness_file.write_text(original_readiness, encoding="utf-8")

        cost_file = task_dir / "cost-and-caching.md"
        original_cost = cost_file.read_text(encoding="utf-8")
        cost_file.write_text(original_cost.replace("- Max total tokens per run: Concrete QA-filled content", "- Max total tokens per run:"), encoding="utf-8")
        token_gate_result = run([sys.executable, "scripts/validate_agent_task.py", str(task_dir)])
        assert_true(token_gate_result.returncode != 0, "validator should fail on empty token hard-gate field")
        assert_true("empty token efficiency field: Max total tokens per run" in token_gate_result.stdout, "token hard-gate failure not reported")
        cost_file.write_text(original_cost, encoding="utf-8")

        intake_file = task_dir / "intake-form.md"
        original_intake = intake_file.read_text(encoding="utf-8")
        intake_file.write_text(original_intake.replace("## Evidence of Success\n\nConcrete QA-filled content", "## Evidence of Success\n\nnone"), encoding="utf-8")
        intake_result = run([sys.executable, "scripts/validate_agent_task.py", str(task_dir)])
        assert_true(intake_result.returncode != 0, "validator should fail on unresolved intake answers")
        assert_true("intake-form.md unresolved intake answer: Evidence of Success" in intake_result.stdout, "intake failure not reported")
        intake_file.write_text(original_intake, encoding="utf-8")

        missing = task_dir / "eval-spec.md"
        missing.unlink()
        missing_result = run([sys.executable, "scripts/validate_agent_task.py", str(task_dir)])
        assert_true(missing_result.returncode != 0, "validator should fail on missing required artifact")
        assert_true("missing required file: eval-spec.md" in missing_result.stdout, "missing file not reported")
    finally:
        if task_dir.exists():
            shutil.rmtree(task_dir)


def test_existing_task_readiness_scorecards_are_verifiable() -> None:
    scorecards = sorted((ROOT / "tasks").glob("*/readiness-scorecard.md")) + sorted(
        (ROOT / "maintainer" / "tasks").glob("*/readiness-scorecard.md")
    )
    for scorecard in scorecards:
        task_dir = scorecard.parent
        if task_dir.parent == ROOT / "tasks" and task_dir.name.startswith(TEST_TASK_PREFIX):
            continue
        result = run([sys.executable, "scripts/validate_agent_task.py", str(task_dir)])
        assert_true(result.returncode == 0, f"task validator failed for {task_dir.relative_to(ROOT)}: {result.stdout}\n{result.stderr}")


def test_radar_config_filtering_and_report_generation() -> None:
    radar = load_radar_module()
    config = radar.parse_config(ROOT / "maintainer" / "radar-config.yaml")
    queries = radar.render_queries(config["queries"], radar.dt.date(2026, 5, 3))
    assert_true(queries, "radar has no queries")
    assert_true(all("{year_start}" not in query for query in queries), "query templates were not rendered")
    assert_true(any("agent" in query.lower() for query in queries), "radar queries are not agent-focused")

    query_plans = radar.render_query_plans(config, radar.dt.date(2026, 5, 3))
    assert_true(len(query_plans) > len(queries), "dynamic query plans should expand beyond static queries")
    assert_true(any(plan["source"].startswith("dynamic:") for plan in query_plans), "dynamic query plans missing")
    assert_true(any("created:>=" in plan["query"] for plan in query_plans), "new-repo created window queries missing")

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

    md_path = ROOT / "maintainer" / "radar" / "2099-01-01.md"
    yaml_path = ROOT / "maintainer" / "radar" / "2099-01-01-candidates.yaml"
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
        md_text = md_path.read_text(encoding="utf-8")
        assert_true("기본 출처: **GitHub 저장소**" in md_text, "markdown missing Korean GitHub-first statement")
        assert_true("동적 신선도/성장률 쿼리" in md_text, "markdown missing dynamic search explanation")
        assert_true("## 처음 시작하는 사람용 프롬프트" in md_text, "markdown missing beginner starter prompt")
        assert_true("가상 프로젝트" in md_text and "후보 중에서" in md_text, "starter prompt missing beginner-safe practice context")
        assert_true("정확도 체크 방법" in md_text and "외부 저장소 설치, production 배포, registry 수정" in md_text, "starter prompt missing accuracy/safety check")
        assert_true("| 순위 | 점수 | 테크닉 | Δ★ | 저장소 | Stars | 생성일 | 업데이트 | 발견 출처 | 라이선스 | 리뷰 이유 |" in md_text, "markdown table header should be Korean and match generated columns")
        assert_true("primary_source: github_repositories" in yaml_path.read_text(encoding="utf-8"), "yaml missing primary source")
        assert_true("star_delta: 100" in yaml_path.read_text(encoding="utf-8"), "yaml missing star delta")
    finally:
        md_path.unlink(missing_ok=True)
        yaml_path.unlink(missing_ok=True)


def test_user_distribution_export_contracts() -> None:
    exporter = load_export_module()
    manifest_text = read("distribution/user-export-manifest.yaml")
    assert_true("maintainer/" in manifest_text, "user distribution manifest must exclude maintainer tree")
    assert_true("reports/" in manifest_text, "user distribution manifest must exclude generated reports")
    assert_true("weekly-repo-radar.yml" in manifest_text, "user distribution manifest must exclude radar workflow")
    assert_true("publish-user-distribution.yml" in manifest_text, "user distribution manifest must exclude publish workflow")
    assert_true("generate_repo_score_report.py" in manifest_text, "user distribution manifest must exclude source-repo score reporter")
    assert_true("distribution/user/AGENTS.md => AGENTS.md" in manifest_text, "user distribution must override AGENTS.md")
    assert_true("--prune-stale" in read("maintainer/workflows/publish-user-distribution.md"), "publish workflow docs must document stale export pruning")

    source_playbook = read("agent-playbook.yaml")
    user_playbook = read("distribution/user/agent-playbook.yaml")
    assert_true(
        re.findall(r"path:\s*([a-zA-Z0-9_.-]+)", source_playbook)
        == re.findall(r"path:\s*([a-zA-Z0-9_.-]+)", user_playbook),
        "user playbook required artifacts must stay aligned with source playbook",
    )
    assert_true(
        yaml_list_after_key(source_playbook, "mandatory_technique_consideration")
        == yaml_list_after_key(user_playbook, "mandatory_technique_consideration"),
        "user playbook mandatory technique list must stay aligned with source playbook",
    )

    with tempfile.TemporaryDirectory(prefix="agent-guide-user-export-") as tmp:
        target = Path(tmp) / "target"
        # Simulate an older full-repo export that must be cleaned from a dedicated
        # distribution repo when --prune-excluded is used.
        (target / "maintainer").mkdir(parents=True)
        (target / "maintainer" / "old.txt").write_text("legacy", encoding="utf-8")
        (target / ".github" / "workflows").mkdir(parents=True)
        (target / ".github" / "workflows" / "weekly-repo-radar.yml").write_text("legacy", encoding="utf-8")
        (target / ".github" / "workflows" / "validate.yml").write_text("legacy", encoding="utf-8")
        (target / ".github" / "workflows" / "publish-user-distribution.yml").write_text("legacy", encoding="utf-8")
        (target / "wiki").mkdir()
        (target / "wiki" / "index.md").write_text("legacy", encoding="utf-8")

        result = run(
            [
                sys.executable,
                "maintainer/scripts/export_user_distribution.py",
                "--dest",
                str(target),
                "--prune-excluded",
            ]
        )
        assert_true(result.returncode == 0, f"user distribution export failed: {result.stdout}\n{result.stderr}")

        assert_true((target / "AGENTS.md").exists(), "export missing user AGENTS.md")
        assert_true((target / ".gitignore").exists(), "export missing user .gitignore")
        assert_true((target / "README.md").exists(), "export missing user README.md")
        assert_true((target / "SECURITY.md").exists(), "export missing user SECURITY.md")
        assert_true((target / "agent-playbook.yaml").exists(), "export missing user playbook")
        assert_true((target / "workflows" / "build-agent.md").exists(), "export missing build workflow")
        assert_true(not (target / "workflows" / "source-ingestion.md").exists(), "user distribution must not include source ingestion update workflow")
        assert_true((target / "templates" / "intake-form.md").exists(), "export missing templates")
        assert_true((target / "techniques" / "registry.yaml").exists(), "export missing technique registry")
        assert_true((target / "scripts" / "new_agent_task.py").exists(), "export missing scaffolder")
        assert_true((target / "scripts" / "validate_agent_task.py").exists(), "export missing validator")
        assert_true(not (target / "scripts" / "test_agent_guide.py").exists(), "user distribution must not include maintainer tests")
        assert_true(not (target / "scripts" / "generate_llm_wiki.py").exists(), "user distribution must not include wiki generator")
        assert_true(not (target / "maintainer").exists(), "user distribution must prune maintainer tree")
        assert_true(not (target / ".github" / "workflows" / "weekly-repo-radar.yml").exists(), "user distribution must prune radar workflow")
        assert_true(not (target / ".github" / "workflows" / "publish-user-distribution.yml").exists(), "user distribution must prune publish workflow")
        assert_true(not (target / "wiki").exists(), "user distribution must prune generated wiki")
        assert_true(not (target / "reports").exists(), "user distribution must prune generated reports")
        assert_true(not (target / "scripts" / "generate_repo_score_report.py").exists(), "user distribution must not include source-repo score reporter")
        assert_true(not (target / "tasks" / "customer-email-reply-agent").exists(), "user distribution must not include sample task")
        assert_true((target / ".agent-guide-distribution.json").exists(), "export missing distribution stamp")

        stale_managed_path = target / "legacy-copied.md"
        stale_managed_path.write_text("old managed export", encoding="utf-8")
        unknown_local_path = target / "local-user-note.md"
        unknown_local_path.write_text("preserve user-owned file", encoding="utf-8")
        stamp_path = target / ".agent-guide-distribution.json"
        stamp = json.loads(stamp_path.read_text(encoding="utf-8"))
        stamp["copied_paths"] = list(stamp["copied_paths"]) + ["legacy-copied.md"]
        stamp_path.write_text(json.dumps(stamp, indent=2), encoding="utf-8")

        stale_result = run(
            [
                sys.executable,
                "maintainer/scripts/export_user_distribution.py",
                "--dest",
                str(target),
                "--prune-stale",
            ]
        )
        assert_true(stale_result.returncode == 0, f"user distribution stale prune failed: {stale_result.stdout}\n{stale_result.stderr}")
        assert_true(not stale_managed_path.exists(), "stale previously-copied export path must be pruned")
        assert_true(unknown_local_path.exists(), "stale prune must preserve unknown target files")

        exported_agents = (target / "AGENTS.md").read_text(encoding="utf-8")
        assert_true("maintainer-only technique discovery" in exported_agents, "user AGENTS missing discovery boundary")
        assert_true("source/maintainer repository" in exported_agents, "user AGENTS missing source-repo handoff")


def test_security_posture_contracts() -> None:
    validate_workflow = read(".github/workflows/validate.yml")
    assert_true("permissions:" in validate_workflow and "contents: read" in validate_workflow, "validate workflow must be read-only")

    weekly_workflow = read(".github/workflows/weekly-repo-radar.yml")
    assert_true("contents: write" in weekly_workflow and "pull-requests: write" in weekly_workflow, "weekly workflow write permissions must be explicit")

    publish_workflow = read(".github/workflows/publish-user-distribution.yml")
    assert_true("workflow_dispatch:" in publish_workflow, "publish workflow must remain manually dispatched")
    assert_true("push:" not in publish_workflow and "pull_request:" not in publish_workflow and "schedule:" not in publish_workflow, "publish workflow must not auto-run")
    assert_true("permissions:" in publish_workflow and "contents: read" in publish_workflow, "publish workflow must have read-only source permissions")
    assert_true("USER_DISTRIBUTION_TOKEN" in publish_workflow, "publish workflow must require an explicit target-repo token")
    assert_true("export_user_distribution.py" in publish_workflow, "publish workflow must use manifest-bounded exporter")
    assert_true("--prune-stale" in publish_workflow, "publish workflow must support stale export pruning")
    assert_true("git commit -F" in publish_workflow, "publish workflow must use commit-message files, not unindented multiline -m strings")

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
    assert_true("workflow_dispatch:" in workflow, "weekly radar must remain manual-dispatchable")
    assert_true("schedule:" not in workflow and "cron:" not in workflow, "weekly radar must not run automatically")
    assert_true("contents: write" in workflow and "pull-requests: write" in workflow, "workflow missing PR permissions")
    assert_true("maintainer/scripts/weekly_repo_radar.py" in workflow, "workflow does not run maintainer radar script")
    assert_true("git commit -F" in workflow, "weekly workflow must use commit-message files, not unindented multiline -m strings")
    for workflow_file in sorted((ROOT / ".github" / "workflows").glob("*.yml")):
        text = workflow_file.read_text(encoding="utf-8")
        top_level_lore_trailers = re.findall(r"^(Constraint|Rejected|Confidence|Scope-risk|Directive|Tested|Not-tested):", text, flags=re.MULTILINE)
        assert_true(not top_level_lore_trailers, f"workflow has invalid top-level commit trailer keys: {workflow_file.name}")

    validate_workflow = read(".github/workflows/validate.yml")
    assert_true("workflow_dispatch:" in validate_workflow, "validate workflow must remain manual-dispatchable")
    assert_true("push:" not in validate_workflow and "pull_request:" not in validate_workflow, "validate workflow must not auto-run for clone/import users")

    agents = read("AGENTS.md")
    assert_true(
        "GitHub-first repository discovery" in agents or "GitHub repository discovery as the primary" in agents,
        "AGENTS missing GitHub-first policy",
    )
    assert_true("1-2 sentences" in agents, "AGENTS missing response brevity policy")
    assert_true("readiness-scorecard.md" in agents, "AGENTS missing readiness scorecard gate")
    assert_true("output-schema.md" in agents, "AGENTS missing structured output schema gate")
    assert_true("guardrails.md" in agents, "AGENTS missing guardrails gate")
    assert_true("telemetry.md" in agents, "AGENTS missing telemetry gate")
    assert_true("security-privacy.md" in agents, "AGENTS missing security/privacy gate")
    assert_true("token efficiency budget gate" in agents.lower(), "AGENTS missing token efficiency hard gate")
    assert_true("maintainer-only discovery" in agents, "AGENTS must keep discovery out of ordinary user path")

    build_workflow = read("workflows/build-agent.md")
    intake_workflow = read("workflows/intake.md")
    assert_true("Standardized Intake Gate" in build_workflow, "build workflow missing standardized intake gate")
    assert_true("Missing fields must trigger" in intake_workflow or "missing fields" in intake_workflow.lower(), "intake workflow missing follow-up rule")

    readme = read("README.md")
    assert_true("기본 사용자 경로" in readme and "maintainer/" in readme, "README must separate user path from maintainer tools")
    assert_true("intake-form.md" in readme, "README missing standardized intake guidance")
    assert_true("1~2문장" in readme, "README missing Korean brevity guidance")
    assert_true("output schema" in readme, "README missing structured output gate")
    assert_true("security/privacy" in readme, "README missing security/privacy gate")
    assert_true("token-efficiency hard gate" in readme, "README missing token efficiency hard gate")
    assert_true("SECURITY.md" in readme, "README missing security posture doc")
    assert_true("maintainer/scripts/weekly_repo_radar.py" in readme, "README missing optional maintainer radar path")
    assert_true("distribution/user-export-manifest.yaml" in readme, "README missing user distribution manifest path")
    assert_true("publish-user-distribution" in readme, "README missing user distribution publish path")

    maintainer_readme = read("maintainer/README.md")
    assert_true("export_user_distribution.py" in maintainer_readme, "maintainer README missing export script")
    assert_true("--prune-stale" in maintainer_readme, "maintainer README missing stale export pruning guidance")
    assert_true("USER_DISTRIBUTION_TOKEN" in maintainer_readme, "maintainer README missing publish secret boundary")



def test_llm_wiki_obsidian_contracts() -> None:
    generator = read("scripts/generate_llm_wiki.py")
    assert_true("Source of truth remains" in generator, "wiki generator must preserve source-of-truth boundary")
    assert_true((ROOT / "wiki" / "index.md").exists(), "wiki index missing")
    assert_true((ROOT / "wiki" / "graph-links.md").exists(), "wiki graph links missing")
    assert_true((ROOT / "wiki" / "technique-map.md").exists(), "wiki technique map missing")
    assert_true((ROOT / "wiki" / "llm-wiki-operations.md").exists(), "wiki operations page missing")
    assert_true((ROOT / "wiki" / "sources" / "techniques-registry.md").exists(), "wiki registry source node missing")
    assert_true((ROOT / "wiki" / "sources" / "techniques-taxonomy.md").exists(), "wiki taxonomy source node missing")
    assert_true((ROOT / "wiki" / "sources" / "repo-root.md").exists(), "wiki repo root source bridge missing")
    assert_true((ROOT / "wiki" / "sources" / "templates.md").exists(), "wiki template source bridge missing")
    assert_true((ROOT / "wiki" / "sources" / "workflows.md").exists(), "wiki workflow source bridge missing")
    assert_true((ROOT / "wiki" / "sources" / "source-registry.md").exists(), "wiki source registry bridge missing")
    assert_true((ROOT / "wiki" / "sources" / "maintainer.md").exists(), "wiki maintainer source bridge missing")
    assert_true((ROOT / "wiki" / "sources" / "distribution.md").exists(), "wiki distribution source bridge missing")
    assert_true((ROOT / "wiki" / "repos" / "radar.md").exists(), "wiki repository radar bridge missing")
    assert_true((ROOT / ".obsidian" / "graph.json").exists(), "Obsidian graph config missing")
    graph_config = read(".obsidian/graph.json")
    assert_true("path:wiki/sources" in graph_config, "Obsidian graph config missing source node color group")
    assert_true("path:maintainer" in graph_config, "Obsidian graph config missing maintainer color group")
    assert_true('"showOrphans": false' in graph_config, "Obsidian graph should hide unlinked orphan dots by default")
    assert_true('"hideUnresolved": true' in graph_config, "Obsidian graph should hide unresolved link dots by default")
    wiki_index = read("wiki/index.md")
    assert_true("not** the source of truth" in wiki_index, "wiki index missing authority boundary")
    assert_true("Open the repository root as an Obsidian vault" in wiki_index, "wiki index missing Obsidian connection guidance")
    assert_true("[[wiki/technique-map|Technique Map]]" in wiki_index, "wiki index missing technique map link")
    assert_true("[[wiki/sources/repo-root|Repository Root Source Bridge]]" in wiki_index, "wiki index missing repo root source bridge")
    assert_true("[[wiki/sources/distribution|distribution/*.md]]" in wiki_index, "wiki index missing distribution source bridge")
    assert_true("[[wiki/sources/maintainer|maintainer/*.md]]" in wiki_index, "wiki index missing maintainer source bridge")
    assert_true("[[wiki/sources/workflows|workflows/*.md]]" in wiki_index, "wiki index missing workflow source bridge")
    assert_true("[[wiki/sources/techniques-registry|techniques/registry.yaml]]" in wiki_index, "wiki index missing registry source node link")
    assert_true("[[AGENTS|AGENTS.md]]" in wiki_index, "wiki index missing AGENTS root document link")
    assert_true("[[wiki/techniques/llm_wiki_context_compilation" in wiki_index, "wiki index missing LLM wiki technique link")
    source_summary = read("sources/summaries/roboco-karpathy-llm-wiki-72-run-benchmark.md")
    assert_true("wiki-first with source verification" in source_summary, "LLM wiki source summary missing verification pattern")
    technique_map = read("wiki/technique-map.md")
    assert_true("# Agent Context Profiles" in technique_map, "technique map missing profile bundles")
    assert_true("[[wiki/techniques/structured_output_schema_validation" in technique_map, "technique map missing technique links")
    eval_page = read("wiki/techniques/eval_regression_loop.md")
    assert_true("## Similar / Compare With" in eval_page, "technique page missing peer comparison section")
    assert_true("[[wiki/techniques/structured_output_schema_validation" in eval_page, "eval technique missing peer/prerequisite links")
    assert_true("[[wiki/sources/techniques-registry" in eval_page, "technique page missing registry source bridge")
    source_node = read("wiki/sources/techniques-registry.md")
    assert_true("Canonical source file: `techniques/registry.yaml`" in source_node, "registry source node missing canonical path")
    assert_true("[[wiki/techniques/llm_wiki_context_compilation" in source_node, "registry source node missing technique backlinks")
    distribution_node = read("wiki/sources/distribution.md")
    assert_true("[[distribution/user/README|README.md]]" in distribution_node, "distribution bridge missing user README link")
    assert_true("must not include maintainer radar" in distribution_node, "distribution bridge missing export boundary")
    repo_root_node = read("wiki/sources/repo-root.md")
    assert_true("[[README|README.md]]" in repo_root_node and "[[SECURITY|SECURITY.md]]" in repo_root_node, "repo root bridge missing root docs")
    template_node = read("wiki/sources/templates.md")
    assert_true("[[templates/agent-prd|agent-prd.md]]" in template_node, "template bridge missing template links")
    workflow_node = read("wiki/sources/workflows.md")
    assert_true("](../../workflows/build-agent.md)" in workflow_node, "workflow bridge missing exact root workflow Markdown link")
    assert_true("[[wiki/workflows/build-agent" in workflow_node, "workflow bridge missing generated workflow wiki link")
    workflow_page = read("wiki/workflows/build-agent.md")
    assert_true("](../../workflows/build-agent.md)" in workflow_page, "workflow wiki page missing exact canonical source link")
    maintainer_node = read("wiki/sources/maintainer.md")
    if (ROOT / "maintainer" / "README.md").exists():
        assert_true("[[maintainer/README|README.md]]" in maintainer_node, "maintainer bridge missing README link")
    task_prds = sorted((ROOT / "tasks").glob("*/agent-prd.md"))
    assert_true(bool(task_prds), "expected at least one task PRD for wiki task bridge coverage")
    for task_prd in task_prds:
        task_slug = task_prd.parent.name
        task_page = read(f"wiki/tasks/{task_slug}.md")
        assert_true("## Selected Techniques" in task_page, f"task page missing selected technique section: {task_slug}")
        assert_true("[[wiki/techniques/llm_wiki_context_compilation" in task_page, f"task page missing selected technique edges: {task_slug}")
        if (task_prd.parent / "model-routing.md").exists():
            assert_true(
                f"[[tasks/{task_slug}/model-routing|model-routing.md]]" in task_page,
                f"task page missing canonical artifact links: {task_slug}",
            )
    all_wiki_text = "\n".join(page.read_text(encoding="utf-8") for page in (ROOT / "wiki").rglob("*.md"))
    canonical_markdown = [
        page
        for page in ROOT.rglob("*.md")
        if not any(part in {".git", ".omx", ".obsidian", "wiki"} for part in page.relative_to(ROOT).parts)
    ]
    for page in canonical_markdown:
        target = page.relative_to(ROOT).with_suffix("").as_posix()
        assert_true(
            f"[[{target}" in all_wiki_text or f"{target}.md)" in all_wiki_text,
            f"canonical markdown not linked from wiki bridge: {target}",
        )
    for page in (ROOT / "wiki").rglob("*.md"):
        page_text = page.read_text(encoding="utf-8")
        for raw_target in re.findall(r"\[\[([^\]|#]+)", page_text):
            target = raw_target.strip()
            assert_true((ROOT / f"{target}.md").exists(), f"wiki link target missing in {page.relative_to(ROOT)}: {target}")
        for raw_target in re.findall(r"\]\(([^)]+\.md)\)", page_text):
            target = (page.parent / raw_target).resolve()
            assert_true(target.exists(), f"markdown link target missing in {page.relative_to(ROOT)}: {raw_target}")
    registry = read("techniques/registry.yaml")
    for tech_id in ["llm_wiki_context_compilation", "wiki_first_source_verification", "obsidian_graph_knowledge_ops"]:
        assert_true(f"id: {tech_id}" in registry, f"missing LLM wiki technique: {tech_id}")


def test_repo_score_report_generation() -> None:
    reporter = ROOT / "scripts" / "generate_repo_score_report.py"
    assert_true(reporter.exists(), "repo score report generator missing")
    with tempfile.TemporaryDirectory(prefix="agent-guide-score-report-") as tmp:
        html_path = Path(tmp) / "repo-readiness-report.html"
        json_path = Path(tmp) / "repo-readiness-report.json"
        result = run(
            [
                sys.executable,
                "scripts/generate_repo_score_report.py",
                "--output",
                str(html_path),
                "--json-output",
                str(json_path),
            ]
        )
        assert_true(result.returncode == 0, f"score report generator failed: {result.stdout}\n{result.stderr}")
        assert_true(html_path.exists(), "score report HTML not generated")
        assert_true(json_path.exists(), "score report JSON not generated")
        html_text = html_path.read_text(encoding="utf-8")
        report = json.loads(json_path.read_text(encoding="utf-8"))
        assert_true("agent_readiness_scoring" in html_text, "score report missing technique id")
        assert_true(report["summary"]["score"] >= 95, f"repo readiness score unexpectedly low: {report['summary']['score']}")
        assert_true(
            report["summary"]["task_portfolio_average"] < report["summary"]["score"],
            "task portfolio average should remain visible as separate evidence",
        )
        assert_true(
            any(area["name"] == "Existing task scorecard governance" for area in report["areas"]),
            "score report missing task scorecard governance area",
        )

def main() -> int:
    tests = [
        test_registry_playbook_template_consistency,
        test_required_artifact_alignment,
        test_production_grade_techniques_present,
        test_taxonomy_references_are_valid,
        test_scaffold_and_validator_behavior,
        test_existing_task_readiness_scorecards_are_verifiable,
        test_radar_config_filtering_and_report_generation,
        test_user_distribution_export_contracts,
        test_security_posture_contracts,
        test_workflow_and_docs_contracts,
        test_llm_wiki_obsidian_contracts,
        test_repo_score_report_generation,
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
