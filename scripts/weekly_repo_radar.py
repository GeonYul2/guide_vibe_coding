#!/usr/bin/env python3
"""Generate a weekly GitHub repository radar report for agent-engineering technique repos.

Primary purpose: find hot GitHub repositories that teach or implement reusable
agent-engineering techniques (harnesses, evals, caching, observability, memory,
MCP/tools, prompt/workflow discipline). Videos/articles are supplemental sources;
GitHub repository discovery is the baseline refresh loop.

The script uses only Python stdlib. It queries the GitHub Search API,
deduplicates repositories across configured queries, scores candidates, compares
against previous radar star counts when available, and writes review artifacts
under repos/radar/ without modifying repos/registry.yaml.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "repos" / "radar-config.yaml"
RADAR_DIR = ROOT / "repos" / "radar"
GITHUB_SEARCH_URL = "https://api.github.com/search/repositories"

DEFAULT_QUERIES = [
    "agent harness stars:>50 pushed:>={year_start}",
    "agent eval framework stars:>100 pushed:>={year_start}",
    "structured outputs llm schema validation stars:>50 pushed:>={year_start}",
    "llm guardrails tripwires agent stars:>50 pushed:>={year_start}",
    "llm observability agents telemetry stars:>100 pushed:>={year_start}",
    "context engineering llm stars:>100 pushed:>={year_start}",
    "prompt caching token optimization llm agent stars:>50 pushed:>={year_start}",
    "llm cost optimization token budget agent stars:>50 pushed:>={year_start}",
    "prompt engineering workflow agent stars:>50 pushed:>={year_start}",
    "agentic engineering workflow stars:>50 pushed:>={year_start}",
    "mcp tools agent stars:>100 pushed:>={year_start}",
    "ai agent memory rag governance stars:>50 pushed:>={year_start}",
    "llm model routing fallback agent stars:>50 pushed:>={year_start}",
    "ai agent security privacy guardrails stars:>50 pushed:>={year_start}",
    "ai agent canary rollout monitoring stars:>20 pushed:>={year_start}",
    "claude code agents workflow stars:>100 pushed:>={year_start}",
]

DEFAULT_REQUIRED_ANY_KEYWORDS = [
    "agent",
    "agents",
    "agentic",
    "llm",
    "harness",
    "eval",
    "evaluation",
    "benchmark",
    "observability",
    "trace",
    "tracing",
    "telemetry",
    "schema",
    "schemas",
    "structured output",
    "structured outputs",
    "validation",
    "prompt",
    "workflow",
    "context",
    "token",
    "tokens",
    "cost",
    "budget",
    "optimization",
    "cache",
    "caching",
    "memory",
    "rag",
    "retrieval",
    "vector",
    "mcp",
    "tool",
    "tools",
    "framework",
    "sdk",
    "orchestration",
    "playbook",
    "patterns",
    "guide",
    "testing",
    "guardrails",
    "sandbox",
    "permission",
    "privacy",
    "security",
    "pii",
    "routing",
    "fallback",
    "canary",
    "rollout",
    "deployment",
]

DEFAULT_EXCLUDE_KEYWORDS = [
    "flight",
    "flights",
    "airline",
    "booking",
    "travel",
    "crypto trading",
    "dating",
    "game bot",
]

TECHNIQUE_KEYWORDS = {
    "harness": 4,
    "eval": 4,
    "evaluation": 4,
    "benchmark": 3,
    "test": 2,
    "testing": 3,
    "regression": 4,
    "observability": 4,
    "trace": 3,
    "tracing": 3,
    "monitoring": 2,
    "telemetry": 4,
    "schema": 4,
    "schemas": 4,
    "structured output": 5,
    "structured outputs": 5,
    "validation": 3,
    "parser": 2,
    "context": 3,
    "token": 4,
    "tokens": 4,
    "cost": 4,
    "budget": 3,
    "optimization": 3,
    "prompt caching": 5,
    "token optimization": 5,
    "cost optimization": 5,
    "cache": 3,
    "caching": 4,
    "compression": 3,
    "deduplication": 3,
    "memory": 3,
    "rag": 2,
    "retrieval": 3,
    "vector": 2,
    "governance": 3,
    "mcp": 3,
    "tool": 2,
    "tools": 2,
    "permission": 4,
    "sandbox": 3,
    "guardrail": 3,
    "guardrails": 3,
    "tripwire": 4,
    "tripwires": 4,
    "privacy": 4,
    "security": 4,
    "pii": 3,
    "routing": 3,
    "fallback": 3,
    "canary": 4,
    "rollout": 4,
    "deployment": 3,
    "workflow": 3,
    "orchestration": 3,
    "prompt": 3,
    "agentic engineering": 5,
    "harness engineering": 5,
    "context engineering": 4,
    "playbook": 4,
    "pattern": 3,
    "patterns": 3,
    "guide": 2,
    "awesome": 3,
    "framework": 2,
    "sdk": 2,
    "claude": 1,
    "codex": 1,
}

DOMAIN_APP_PENALTY_KEYWORDS = {
    "flight": 6,
    "flights": 6,
    "airline": 6,
    "booking": 6,
    "travel": 6,
    "shopping": 4,
    "dating": 5,
    "game": 3,
}


class RadarConfig(dict):
    """Tiny dict subclass for type clarity without depending on PyYAML."""


def parse_block_list(text: str, key: str) -> list[str]:
    """Parse a simple YAML list block named `key` from our owned config file."""
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
        match = re.match(r"\s*-\s*['\"]?(.*?)['\"]?\s*$", line)
        if match:
            block_indent = indent
            values.append(match.group(1))
        elif block_indent is not None and indent <= block_indent:
            break
    return values


def parse_config(path: Path) -> RadarConfig:
    if not path.exists():
        return RadarConfig(
            limit=10,
            queries=DEFAULT_QUERIES,
            required_any_keywords=DEFAULT_REQUIRED_ANY_KEYWORDS,
            exclude_keywords=DEFAULT_EXCLUDE_KEYWORDS,
            min_technique_score=3,
        )

    text = path.read_text(encoding="utf-8")
    limit_match = re.search(r"per_query_limit:\s*(\d+)", text)
    min_technique_match = re.search(r"min_technique_score:\s*(\d+)", text)
    return RadarConfig(
        limit=int(limit_match.group(1)) if limit_match else 10,
        queries=parse_block_list(text, "queries") or DEFAULT_QUERIES,
        required_any_keywords=parse_block_list(text, "required_any_keywords") or DEFAULT_REQUIRED_ANY_KEYWORDS,
        exclude_keywords=parse_block_list(text, "exclude_keywords") or DEFAULT_EXCLUDE_KEYWORDS,
        min_technique_score=int(min_technique_match.group(1)) if min_technique_match else 3,
    )


def render_queries(queries: list[str], run_date: dt.date) -> list[str]:
    values = {
        "year_start": f"{run_date.year}-01-01",
        "quarter_start": (run_date - dt.timedelta(days=90)).isoformat(),
        "month_start": (run_date - dt.timedelta(days=30)).isoformat(),
    }
    return [query.format(**values) for query in queries]


def github_get_json(url: str, token: str | None) -> dict[str, Any]:
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "agent-engineering-guide-weekly-radar",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    request = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def search_repositories(query: str, limit: int, token: str | None) -> list[dict[str, Any]]:
    params = urllib.parse.urlencode(
        {"q": query, "sort": "updated", "order": "desc", "per_page": max(1, min(limit, 100))}
    )
    payload = github_get_json(f"{GITHUB_SEARCH_URL}?{params}", token)
    return list(payload.get("items", []))


def repo_text(repo: dict[str, Any]) -> str:
    description = repo.get("description") or ""
    name = repo.get("name") or repo.get("full_name") or ""
    full_name = repo.get("full_name") or ""
    topics = " ".join(repo.get("topics") or [])
    return f"{full_name} {name} {description} {topics}".lower()


def days_since(iso_timestamp: str, today: dt.date) -> int:
    try:
        pushed = dt.datetime.fromisoformat(iso_timestamp.replace("Z", "+00:00")).date()
    except ValueError:
        return 9999
    return max(0, (today - pushed).days)


def keyword_score(text: str, weights: dict[str, int]) -> int:
    return sum(weight for keyword, weight in weights.items() if keyword in text)


def technique_match(repo: dict[str, Any], required_any: list[str], excluded: list[str], min_score: int) -> tuple[bool, int, list[str]]:
    text = repo_text(repo)
    reasons: list[str] = []
    required_hits = [keyword for keyword in required_any if keyword.lower() in text]
    excluded_hits = [keyword for keyword in excluded if keyword.lower() in text]
    score = keyword_score(text, TECHNIQUE_KEYWORDS) - keyword_score(text, DOMAIN_APP_PENALTY_KEYWORDS)

    if required_hits:
        reasons.append("required_any=" + ",".join(required_hits[:8]))
    if excluded_hits:
        reasons.append("excluded=" + ",".join(excluded_hits[:8]))
    reasons.append(f"technique_score={score}")

    is_match = bool(required_hits) and not excluded_hits and score >= min_score
    return is_match, score, reasons


def load_previous_stars(run_date: dt.date) -> dict[str, int]:
    """Read latest prior generated candidate YAML and return repo -> stars."""
    previous_files = []
    for path in RADAR_DIR.glob("*-candidates.yaml"):
        date_part = path.name.removesuffix("-candidates.yaml")
        try:
            file_date = dt.date.fromisoformat(date_part)
        except ValueError:
            continue
        if file_date < run_date:
            previous_files.append((file_date, path))
    if not previous_files:
        return {}

    _, latest = max(previous_files, key=lambda item: item[0])
    stars: dict[str, int] = {}
    current_name: str | None = None
    for line in latest.read_text(encoding="utf-8").splitlines():
        name_match = re.match(r"\s*- name:\s*(.*?)\s*$", line)
        if name_match:
            current_name = name_match.group(1).strip().strip('"')
            continue
        star_match = re.match(r"\s*stars:\s*(\d+)\s*$", line)
        if current_name and star_match:
            stars[current_name] = int(star_match.group(1))
            current_name = None
    return stars


def score_repo(candidate: dict[str, Any], today: dt.date) -> int:
    stars = int(candidate.get("stars") or 0)
    forks = int(candidate.get("forks") or 0)
    age_days = days_since(candidate.get("pushed_at") or "1970-01-01T00:00:00Z", today)
    star_delta = int(candidate.get("star_delta") or 0)
    technique_score = int(candidate.get("technique_score") or 0)
    matched_queries = candidate.get("matched_queries") or []

    recent_bonus = 50 if age_days <= 7 else 30 if age_days <= 30 else 10 if age_days <= 90 else 0
    star_score = min(100, stars // 100)
    fork_score = min(30, forks // 50)
    query_score = min(40, len(matched_queries) * 8)
    technique_bonus = min(70, max(0, technique_score) * 4)
    growth_bonus = min(80, max(0, star_delta) * 2)
    return star_score + fork_score + recent_bonus + query_score + technique_bonus + growth_bonus


def yaml_scalar(value: Any) -> str:
    if value is None:
        return ""
    text = str(value).replace("\n", " ").strip()
    if not text:
        return ""
    if any(ch in text for ch in [":", "#", "[", "]", "{", "}", ",", "&", "*", "?", "|"]):
        return json.dumps(text, ensure_ascii=False)
    return text


def build_candidates(
    queries: list[str],
    limit: int,
    token: str | None,
    today: dt.date,
    required_any_keywords: list[str],
    exclude_keywords: list[str],
    min_technique_score: int,
) -> tuple[list[dict[str, Any]], list[str]]:
    by_name: dict[str, dict[str, Any]] = {}
    errors: list[str] = []
    successful_queries = 0
    previous_stars = load_previous_stars(today)

    for query in queries:
        try:
            repos = search_repositories(query, limit, token)
            successful_queries += 1
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", "ignore")[:500].strip()
            errors.append(f"{query}: HTTP {exc.code} {detail}")
            continue
        except Exception as exc:  # noqa: BLE001 - CLI report should capture all source failures.
            errors.append(f"{query}: {type(exc).__name__}: {exc}")
            continue

        for repo in repos:
            full_name = repo.get("full_name")
            if not full_name:
                continue
            is_match, tech_score, reasons = technique_match(
                repo, required_any_keywords, exclude_keywords, min_technique_score
            )
            if not is_match:
                continue

            entry = by_name.setdefault(
                full_name,
                {
                    "name": full_name,
                    "url": repo.get("html_url"),
                    "description": repo.get("description") or "",
                    "stars": repo.get("stargazers_count") or 0,
                    "previous_stars": previous_stars.get(full_name),
                    "star_delta": 0,
                    "forks": repo.get("forks_count") or 0,
                    "open_issues": repo.get("open_issues_count") or 0,
                    "language": repo.get("language") or "",
                    "topics": repo.get("topics") or [],
                    "pushed_at": repo.get("pushed_at") or "",
                    "license": (repo.get("license") or {}).get("spdx_id") or "NOASSERTION",
                    "technique_score": tech_score,
                    "technique_match_reasons": reasons,
                    "matched_queries": [],
                },
            )
            if entry["previous_stars"] is not None:
                entry["star_delta"] = max(0, int(entry["stars"]) - int(entry["previous_stars"]))
            if query not in entry["matched_queries"]:
                entry["matched_queries"].append(query)

    candidates = list(by_name.values())
    for candidate in candidates:
        candidate["score"] = score_repo(candidate, today)
        candidate["status"] = "candidate"
        candidate["review_action"] = "human_review_required"
    candidates.sort(key=lambda item: (-int(item["score"]), -int(item["star_delta"]), -int(item["stars"]), item["name"]))

    if errors:
        print("Radar source warnings:", file=sys.stderr)
        for err in errors:
            print(f"- {err}", file=sys.stderr)
    if successful_queries == 0 and errors:
        raise SystemExit("All radar source queries failed; refusing to write an empty report from source errors.")
    return candidates, errors


def markdown_cell(value: Any, max_len: int = 120) -> str:
    """Escape untrusted GitHub metadata before writing a Markdown table cell."""
    rendered = str(value or "").replace("\n", " ").replace("\r", " ").strip()
    rendered = rendered[:max_len]
    return rendered.replace("|", "\\|").replace("<", "&lt;").replace(">", "&gt;")


def markdown_url(value: Any) -> str:
    """Allow only normal GitHub HTTPS URLs in generated Markdown links."""
    rendered = str(value or "")
    if rendered.startswith("https://github.com/"):
        return rendered.replace(")", "%29")
    return "https://github.com"

def write_yaml(path: Path, run_date: dt.date, candidates: list[dict[str, Any]], queries: list[str], source_errors: list[str]) -> None:
    lines = [
        "version: 0.1.0",
        f"generated_at: {run_date.isoformat()}",
        "primary_source: github_repositories",
        "supplemental_sources:",
        "  - youtube",
        "  - articles",
        "  - release_notes",
        "policy:",
        "  auto_vendor_repos: false",
        "  auto_modify_main_registry: false",
        "  human_review_required: true",
        f"source_status: {'partial' if source_errors else 'complete'}",
    ]
    if source_errors:
        lines.append("source_errors:")
        lines.extend(f"  - {json.dumps(error, ensure_ascii=False)}" for error in source_errors)
    else:
        lines.append("source_errors: []")
    lines.append("queries:")
    lines.extend(f"  - {json.dumps(query, ensure_ascii=False)}" for query in queries)
    lines.append("candidates:")
    for candidate in candidates:
        lines.extend(
            [
                f"  - name: {yaml_scalar(candidate['name'])}",
                f"    url: {yaml_scalar(candidate['url'])}",
                f"    status: {candidate['status']}",
                f"    score: {candidate['score']}",
                f"    technique_score: {candidate['technique_score']}",
                f"    stars: {candidate['stars']}",
                f"    previous_stars: {candidate['previous_stars'] if candidate['previous_stars'] is not None else 'null'}",
                f"    star_delta: {candidate['star_delta']}",
                f"    forks: {candidate['forks']}",
                f"    open_issues: {candidate['open_issues']}",
                f"    language: {yaml_scalar(candidate['language'])}",
                f"    license: {yaml_scalar(candidate['license'])}",
                f"    pushed_at: {yaml_scalar(candidate['pushed_at'])}",
                f"    description: {yaml_scalar(candidate['description'])}",
                "    topics:",
            ]
        )
        lines.extend(f"      - {yaml_scalar(topic)}" for topic in candidate["topics"][:20])
        lines.append("    technique_match_reasons:")
        lines.extend(f"      - {yaml_scalar(reason)}" for reason in candidate["technique_match_reasons"])
        lines.append("    matched_queries:")
        lines.extend(f"      - {json.dumps(query, ensure_ascii=False)}" for query in candidate["matched_queries"])
        lines.append("    review_action: human_review_required")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_markdown(path: Path, run_date: dt.date, candidates: list[dict[str, Any]], queries: list[str], source_errors: list[str]) -> None:
    top = candidates[:20]
    lines = [
        f"# Weekly Agent Technique Repository Radar — {run_date.isoformat()}",
        "",
        "Primary source: **GitHub repositories**. YouTube/articles/release notes are supplemental ingestion sources only.",
        "",
        "This report is generated automatically. It does **not** vendor external repositories and does **not** modify `repos/registry.yaml`.",
        "Human review is required before adopting any candidate.",
        "",
        f"Source status: **{'partial' if source_errors else 'complete'}**",
        "",
        "## Search Queries",
        "",
    ]
    lines.extend(f"- `{query}`" for query in queries)
    if source_errors:
        lines.extend(["", "## Source Warnings", ""])
        lines.extend(f"- {error}" for error in source_errors)
    lines.extend(
        [
            "",
            "## Top Technique Candidates",
            "",
            "| Rank | Score | Tech | Δ★ | Repo | Stars | Updated | License | Why review |",
            "| ---: | ---: | ---: | ---: | --- | ---: | --- | --- | --- |",
        ]
    )
    for idx, candidate in enumerate(top, 1):
        why = markdown_cell(candidate["description"] or "No description")
        repo_name = markdown_cell(candidate["name"], max_len=80)
        repo_url = markdown_url(candidate["url"])
        license_name = markdown_cell(candidate["license"], max_len=40)
        lines.append(
            f"| {idx} | {candidate['score']} | {candidate['technique_score']} | {candidate['star_delta']} | "
            f"[{repo_name}]({repo_url}) | {candidate['stars']} | {candidate['pushed_at'][:10]} | "
            f"{license_name} | {why} |"
        )
    lines.extend(
        [
            "",
            "## Review Checklist",
            "",
            "For each promising candidate:",
            "",
            "1. Confirm it is a reusable technique/pattern/tooling repo, not just a domain app.",
            "2. Read the README and license.",
            "3. Check recent commits, releases, issues, and maintainer activity.",
            "4. Identify the reusable technique, not just the repository name.",
            "5. Decide one of: `rejected`, `watch`, `candidate`, `adopted`.",
            "6. If adopted, update `repos/registry.yaml` with local application guidance.",
            "7. If it changes how agents should behave, update `techniques/registry.yaml` with a source reference.",
            "",
            "## Generated Files",
            "",
            f"- `{path.relative_to(ROOT)}`",
            f"- `repos/radar/{run_date.isoformat()}-candidates.yaml`",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Generate weekly agent technique repository radar artifacts")
    parser.add_argument("--date", default=dt.datetime.now(dt.UTC).date().isoformat(), help="Run date as YYYY-MM-DD")
    parser.add_argument("--limit", type=int, default=None, help="Override per-query result limit")
    args = parser.parse_args(argv)

    try:
        run_date = dt.date.fromisoformat(args.date)
    except ValueError as exc:
        raise SystemExit(f"Invalid --date: {args.date}") from exc

    config = parse_config(CONFIG)
    queries = render_queries(config["queries"], run_date)
    limit = args.limit if args.limit is not None else int(config["limit"])
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    candidates, source_errors = build_candidates(
        queries=queries,
        limit=limit,
        token=token,
        today=run_date,
        required_any_keywords=config["required_any_keywords"],
        exclude_keywords=config["exclude_keywords"],
        min_technique_score=int(config["min_technique_score"]),
    )

    RADAR_DIR.mkdir(parents=True, exist_ok=True)
    md_path = RADAR_DIR / f"{run_date.isoformat()}.md"
    yaml_path = RADAR_DIR / f"{run_date.isoformat()}-candidates.yaml"
    write_markdown(md_path, run_date, candidates, queries, source_errors)
    write_yaml(yaml_path, run_date, candidates, queries, source_errors)

    print(f"wrote {md_path.relative_to(ROOT)}")
    print(f"wrote {yaml_path.relative_to(ROOT)}")
    print(f"candidates: {len(candidates)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
