#!/usr/bin/env python3
"""Scaffold a new automation-agent task folder from playbook-declared templates."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEMPLATES = ROOT / "templates"
TASKS = ROOT / "tasks"
PLAYBOOK = ROOT / "agent-playbook.yaml"


def load_required_files() -> list[str]:
    """Extract required artifact paths from agent-playbook.yaml without PyYAML."""
    if not PLAYBOOK.exists():
        raise SystemExit(f"Missing playbook: {PLAYBOOK.relative_to(ROOT)}")
    text = PLAYBOOK.read_text(encoding="utf-8")
    files = re.findall(r"^\s*-\s*path:\s*([a-zA-Z0-9_.-]+)\s*$", text, flags=re.MULTILINE)
    if not files:
        raise SystemExit("No required_artifacts found in agent-playbook.yaml")
    return files


def slugify(raw: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9._-]+", "-", raw.strip().lower()).strip("-._")
    if not slug:
        raise SystemExit("Task slug cannot be empty")
    return slug


def main(argv: list[str]) -> int:
    if len(argv) != 2 or argv[1] in {"-h", "--help"}:
        print("Usage: python3 scripts/new_agent_task.py <task-slug>")
        return 0 if len(argv) == 2 else 2

    slug = slugify(argv[1])
    task_dir = TASKS / slug
    task_dir.mkdir(parents=True, exist_ok=True)

    for name in load_required_files():
        src = TEMPLATES / name
        if not src.exists():
            raise SystemExit(f"Missing template for required artifact: {src.relative_to(ROOT)}")
        dst = task_dir / name
        if dst.exists():
            print(f"skip existing: {dst.relative_to(ROOT)}")
            continue
        text = src.read_text(encoding="utf-8").replace("<task-slug>", slug)
        dst.write_text(text, encoding="utf-8")
        print(f"created: {dst.relative_to(ROOT)}")

    print(f"\nNext: fill placeholders, then run: python3 scripts/validate_agent_task.py {task_dir.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
