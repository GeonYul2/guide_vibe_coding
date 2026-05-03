#!/usr/bin/env python3
"""Validate required artifacts for an automation-agent task folder.

This intentionally uses only Python stdlib so the guide can run in constrained repos.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLAYBOOK = ROOT / "agent-playbook.yaml"
TECHNIQUE_REGISTRY = ROOT / "techniques" / "registry.yaml"

PLACEHOLDER_MARKERS = ["TODO", "<task-slug>", "<name>", "<short name>"]
MIN_BYTES = 80

TOKEN_EFFICIENCY_REQUIRED_FIELDS = [
    "Max input tokens per run",
    "Max output tokens per run",
    "Max total tokens per run",
    "Cost ceiling per successful run",
    "Required cache hit-rate target",
    "Required context pruning rule",
    "Required summarization/compression trigger",
    "Stop condition when token or cost budget is exceeded",
    "Cheaper model fallback",
    "Reduced-context fallback",
    "Track input tokens",
    "Track output tokens",
    "Track cache hits/misses",
    "Track cost per run",
]



def load_required_files() -> list[str]:
    """Extract required artifact paths from agent-playbook.yaml without requiring PyYAML."""
    if not PLAYBOOK.exists():
        return []
    return re.findall(r"^\s*-\s*path:\s*([a-zA-Z0-9_.-]+)\s*$", PLAYBOOK.read_text(encoding="utf-8"), flags=re.MULTILINE)


def load_mandatory_techniques() -> list[str]:
    """Extract technique ids from techniques/registry.yaml without requiring PyYAML."""
    if not TECHNIQUE_REGISTRY.exists():
        return []
    ids: list[str] = []
    for line in TECHNIQUE_REGISTRY.read_text(encoding="utf-8").splitlines():
        match = re.match(r"\s*- id:\s*([a-zA-Z0-9_-]+)\s*$", line)
        if match:
            ids.append(match.group(1))
    return ids


def fail(msg: str, errors: list[str]) -> None:
    errors.append(msg)


def validate_file(path: Path, errors: list[str]) -> None:
    if not path.exists():
        fail(f"missing required file: {path.name}", errors)
        return
    text = path.read_text(encoding="utf-8")
    if len(text.strip()) < MIN_BYTES:
        fail(f"too short or empty: {path.name}", errors)
    for marker in PLACEHOLDER_MARKERS:
        if marker in text:
            fail(f"placeholder remains in {path.name}: {marker}", errors)


def validate_token_efficiency_gate(path: Path, errors: list[str]) -> None:
    if not path.exists():
        return
    text = path.read_text(encoding="utf-8")
    if "## Token Efficiency Hard Gate" not in text:
        fail("cost-and-caching.md missing Token Efficiency Hard Gate section", errors)
    if "## Token Telemetry Requirements" not in text:
        fail("cost-and-caching.md missing Token Telemetry Requirements section", errors)

    for field in TOKEN_EFFICIENCY_REQUIRED_FIELDS:
        match = re.search(rf"^\s*-\s*{re.escape(field)}:[ \t]*(.*)$", text, flags=re.MULTILINE)
        if not match:
            fail(f"cost-and-caching.md missing token efficiency field: {field}", errors)
            continue
        value = match.group(1).strip()
        if not value or value == "TODO":
            fail(f"cost-and-caching.md has empty token efficiency field: {field}", errors)


def validate_technique_selection(path: Path, errors: list[str]) -> None:
    if not path.exists():
        return
    text = path.read_text(encoding="utf-8")
    mandatory_techniques = load_mandatory_techniques()
    missing = [tech for tech in mandatory_techniques if tech not in text]
    for tech in missing:
        fail(f"mandatory technique not considered in technique-selection.yaml: {tech}", errors)
    if "reason: TODO" in text:
        fail("technique-selection.yaml contains placeholder reasons", errors)
    if "selected:" not in text or "rejected:" not in text:
        fail("technique-selection.yaml must contain selected: and rejected:", errors)


def main(argv: list[str]) -> int:
    if len(argv) != 2 or argv[1] in {"-h", "--help"}:
        print("Usage: python3 scripts/validate_agent_task.py <task-dir>")
        return 0 if len(argv) == 2 else 2

    task_dir = Path(argv[1])
    errors: list[str] = []

    if not task_dir.exists() or not task_dir.is_dir():
        print(f"ERROR: task directory does not exist: {task_dir}")
        return 1

    required_files = load_required_files()
    if not required_files:
        print("ERROR: no required artifacts found in agent-playbook.yaml")
        return 1

    for name in required_files:
        validate_file(task_dir / name, errors)
    validate_technique_selection(task_dir / "technique-selection.yaml", errors)
    validate_token_efficiency_gate(task_dir / "cost-and-caching.md", errors)

    if errors:
        print("VALIDATION FAILED")
        for err in errors:
            print(f"- {err}")
        return 1

    print(f"VALIDATION PASSED: {task_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
