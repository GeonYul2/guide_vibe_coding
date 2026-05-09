#!/usr/bin/env python3
"""Export the user-facing agent-helper subset from the maintainer repo.

The manifest format is intentionally tiny YAML so this script stays stdlib-only:

include:
  - path/or/dir/
overrides:
  - source/path => destination/path
exclude:
  - path/to/remove/with/prune
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_MANIFEST = ROOT / "distribution" / "user-export-manifest.yaml"
STAMP_FILE = ".agent-guide-distribution.json"
MANIFEST_LIST_KEYS = {"include", "overrides", "exclude"}


@dataclass(frozen=True)
class CopyOperation:
    source: str
    dest: str
    override: bool = False


def parse_manifest(path: Path) -> dict[str, list[str]]:
    """Parse the small list-only manifest shape without a YAML dependency."""
    data: dict[str, list[str]] = {key: [] for key in MANIFEST_LIST_KEYS}
    current: str | None = None
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        stripped = raw_line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if not raw_line.startswith(" ") and stripped.endswith(":"):
            key = stripped[:-1]
            current = key if key in data else None
            continue
        if current and stripped.startswith("- "):
            data[current].append(stripped[2:].strip())
    return data


def clean_token(raw: str) -> str:
    token = raw.strip()
    if not token:
        raise ValueError("empty manifest path")
    if "\\" in token:
        raise ValueError(f"backslashes are not allowed in manifest paths: {raw}")
    path = Path(token.rstrip("/"))
    if path.is_absolute() or ".." in path.parts:
        raise ValueError(f"manifest path must stay inside repository: {raw}")
    return token


def path_for(root: Path, raw: str) -> Path:
    token = clean_token(raw)
    return root / token.rstrip("/")


def manifest_operations(manifest: dict[str, list[str]]) -> tuple[list[CopyOperation], list[str]]:
    operations: list[CopyOperation] = []
    for item in manifest["include"]:
        token = clean_token(item)
        operations.append(CopyOperation(source=token, dest=token.rstrip("/")))
    for item in manifest["overrides"]:
        if "=>" not in item:
            raise ValueError(f"override must use 'source => dest': {item}")
        src, dst = (part.strip() for part in item.split("=>", 1))
        operations.append(CopyOperation(source=clean_token(src), dest=clean_token(dst).rstrip("/"), override=True))
    excluded = [clean_token(item) for item in manifest["exclude"]]
    return operations, excluded


def ensure_outside_source(dest: Path, source_root: Path) -> None:
    resolved_dest = dest.resolve()
    resolved_source = source_root.resolve()
    if resolved_dest == resolved_source or resolved_source in resolved_dest.parents:
        raise SystemExit(
            f"Refusing to export into the source repository: {resolved_dest}\n"
            "Choose a sibling/temp checkout as --dest."
        )


def copy_path(src: Path, dst: Path, *, dry_run: bool) -> None:
    if not src.exists():
        raise FileNotFoundError(f"missing export source: {src}")
    if dry_run:
        print(f"COPY {'dir ' if src.is_dir() else 'file'} {src} -> {dst}")
        return
    if src.is_dir():
        if dst.exists():
            if dst.is_dir():
                shutil.rmtree(dst)
            else:
                dst.unlink()
        shutil.copytree(
            src,
            dst,
            ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".DS_Store"),
        )
        return
    dst.parent.mkdir(parents=True, exist_ok=True)
    if dst.exists() and dst.is_dir():
        shutil.rmtree(dst)
    shutil.copy2(src, dst)


def remove_path(path: Path, *, dry_run: bool) -> None:
    if not path.exists():
        return
    if dry_run:
        print(f"REMOVE {path}")
        return
    if path.is_dir():
        shutil.rmtree(path)
    else:
        path.unlink()


def git_revision(source_root: Path) -> str | None:
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            cwd=source_root,
            check=True,
            text=True,
            capture_output=True,
        )
    except Exception:  # noqa: BLE001 - stamp is best-effort only.
        return None
    return result.stdout.strip() or None


def write_stamp(dest: Path, manifest_path: Path, operations: list[CopyOperation], excluded: list[str], *, dry_run: bool) -> None:
    stamp = {
        "distribution": "agent-helper-user",
        "source_revision": git_revision(ROOT),
        "manifest": str(manifest_path.relative_to(ROOT)) if manifest_path.is_relative_to(ROOT) else str(manifest_path),
        "copied_paths": [op.dest for op in operations],
        "excluded_paths": excluded,
    }
    stamp_path = dest / STAMP_FILE
    if dry_run:
        print(f"WRITE {stamp_path}")
        return
    stamp_path.write_text(json.dumps(stamp, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def export_distribution(dest: Path, manifest_path: Path, *, dry_run: bool, prune_excluded: bool) -> None:
    manifest = parse_manifest(manifest_path)
    operations, excluded = manifest_operations(manifest)
    ensure_outside_source(dest, ROOT)

    if not dry_run:
        dest.mkdir(parents=True, exist_ok=True)

    if prune_excluded:
        for item in excluded:
            remove_path(path_for(dest, item), dry_run=dry_run)

    copied_dests: set[str] = set()
    for op in operations:
        if op.dest in excluded:
            raise ValueError(f"copy destination is excluded: {op.dest}")
        src = path_for(ROOT, op.source)
        dst = path_for(dest, op.dest)
        copy_path(src, dst, dry_run=dry_run)
        copied_dests.add(op.dest)

    write_stamp(dest, manifest_path, operations, excluded, dry_run=dry_run)
    print(
        f"Export {'planned' if dry_run else 'complete'}: {len(copied_dests)} paths "
        f"to {dest} ({'with' if prune_excluded else 'without'} prune)"
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Export user-facing agent-helper files to a target checkout.")
    parser.add_argument("--dest", required=True, type=Path, help="Target checkout/directory to receive the user distribution.")
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST, help="Export manifest path.")
    parser.add_argument("--dry-run", action="store_true", help="Print planned copy/remove operations without writing files.")
    parser.add_argument(
        "--prune-excluded",
        action="store_true",
        help="Remove manifest excluded paths from the target before copying. Use for dedicated distribution repos.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        export_distribution(args.dest, args.manifest, dry_run=args.dry_run, prune_excluded=args.prune_excluded)
    except Exception as exc:  # noqa: BLE001 - command-line tool should print concise failures.
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
