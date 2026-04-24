#!/usr/bin/env python3
from __future__ import annotations

import json
import shutil
import sys
from collections import defaultdict
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
from observability_runtime import ScriptRun
from source_domain_mapping import normalize_source_category, resolve_source_domain

CACHE_ROOT = ROOT / ".agentcodex" / "cache"
REPO_METADATA_ROOT = CACHE_ROOT / "repo-metadata"
SUMMARIES_ROOT = CACHE_ROOT / "summaries"
MANIFESTS_ROOT = CACHE_ROOT / "manifests"
REPORTS_ROOT = ROOT / ".agentcodex" / "reports"
REPORT_PATH = REPORTS_ROOT / "summary-refresh-report.md"
MANIFEST_PATH = MANIFESTS_ROOT / "summary-refresh-manifest.json"


def print_usage() -> int:
    print(
        "Usage: python3 .agentcodex/scripts/refresh_summaries.py "
        "[--source <source-id>] [--domain <domain>] [--apply]"
    )
    return 1


def load_metadata_files() -> list[dict]:
    items: list[dict] = []
    if not REPO_METADATA_ROOT.exists():
        return items
    for path in sorted(REPO_METADATA_ROOT.glob("*.json")):
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue
        payload["_path"] = str(path)
        items.append(payload)
    return items


def normalize_domain(payload: dict) -> str:
    value = normalize_source_category(str(payload.get("category", "")))
    return resolve_source_domain(value) if value else "ai-data-engineering"


def remove_legacy_summary_dirs(payloads: list[dict]) -> list[str]:
    removed: list[str] = []
    for payload in payloads:
        category = normalize_source_category(str(payload.get("category", "")))
        domain = normalize_domain(payload)
        if not category or category == domain:
            continue
        legacy_dir = SUMMARIES_ROOT / category / payload["source_id"]
        if legacy_dir.exists():
            shutil.rmtree(legacy_dir)
            removed.append(str(legacy_dir.relative_to(ROOT)))
    return removed


def summarize_list(values: list[str], fallback: str, limit: int = 4) -> list[str]:
    cleaned = [value.strip() for value in values if value and value.strip()]
    if not cleaned:
        return [fallback]
    return cleaned[:limit]


def content_paths(payload: dict) -> list[str]:
    return [str(item.get("path", "")).strip() for item in payload.get("content_hits", []) if item.get("path")]


def content_summaries(payload: dict) -> list[str]:
    return [str(item.get("summary", "")).strip() for item in payload.get("content_hits", []) if item.get("summary")]


def changelog_summaries(payload: dict) -> list[str]:
    summaries = [str(item.get("summary", "")).strip() for item in payload.get("changelog_hits", []) if item.get("summary")]
    release = payload.get("release") or {}
    release_summary = str(release.get("body_summary", "")).strip()
    if release_summary:
        summaries.insert(0, release_summary)
    return summaries


def compact_text(text: str, word_limit: int = 45) -> str:
    words = text.replace("\r", " ").replace("\n", " ").split()
    if not words:
        return ""
    if len(words) <= word_limit:
        return " ".join(words)
    return " ".join(words[:word_limit]) + " ..."


def build_overview(payload: dict) -> str:
    repo_meta = payload.get("repo_metadata") or {}
    topics = repo_meta.get("topics") or []
    description = compact_text(str(repo_meta.get("description", "")).strip(), 30) or "No repository description captured."
    content = summarize_list(
        [compact_text(item, 28) for item in content_summaries(payload) if item],
        "No README or docs summary captured yet.",
        limit=3,
    )
    lines = [
        f"# {payload['name']} Overview",
        "",
        f"- source_id: `{payload['source_id']}`",
        f"- source_category: `{normalize_source_category(str(payload.get('category', '')) or 'unknown')}`",
        f"- domain: `{normalize_domain(payload)}`",
        f"- repo: `{payload.get('repo', '')}`",
        f"- observed_ref: `{payload.get('observed_ref', 'unknown') or 'unknown'}`",
        f"- observed_at: `{payload.get('observed_at', 'unknown') or 'unknown'}`",
        f"- trust: `{payload.get('trust', '')}`",
        f"- ingest_mode: `{payload.get('ingest_mode', '')}`",
        f"- update_strategy: `{payload.get('update_strategy', '')}`",
        "",
        "## Snapshot",
        "",
        f"- purpose: {description}",
        f"- topics: {', '.join(topics[:6]) if topics else 'No topics captured.'}",
        f"- default_branch: `{payload.get('default_branch', 'unknown') or 'unknown'}`",
        "",
        "## Codex Notes",
        "",
    ]
    lines.extend([f"- {item}" for item in content])
    lines.extend(
        [
            "",
            "## Local Use",
            "",
            "- Use this page as a short source fingerprint before reading upstream docs in depth.",
            "- Prefer this summary over replaying raw README text into the prompt.",
            "",
        ]
    )
    return "\n".join(lines)


def build_latest_notes(payload: dict) -> str:
    notes = summarize_list(
        [compact_text(item, 35) for item in changelog_summaries(payload) if item],
        "No release or changelog summary captured.",
        limit=4,
    )
    status = "needs follow-up" if payload.get("errors") else "captured"
    lines = [
        f"# {payload['name']} Latest Notes",
        "",
        f"- source_id: `{payload['source_id']}`",
        f"- sync_status: `{status}`",
        "",
        "## Recent Signals",
        "",
    ]
    lines.extend([f"- {item}" for item in notes])
    if payload.get("errors"):
        lines.extend(
            [
                "",
                "## Retrieval Gaps",
                "",
            ]
        )
        lines.extend([f"- {compact_text(error, 28)}" for error in payload["errors"][:4]])
    lines.append("")
    return "\n".join(lines)


def build_integration_notes(payload: dict) -> str:
    paths = content_paths(payload)
    has_examples = any(path.startswith(("examples", "example")) for path in paths)
    has_docs = any(path.startswith("docs") for path in paths)
    notes = [
        "Treat the repository as a reference boundary, not as implicit project policy.",
        "Pull only the narrow capability needed for the current design or implementation step.",
    ]
    if has_examples:
        notes.append("Example material exists; inspect examples before inventing local integration shape.")
    else:
        notes.append("No examples were detected in the lightweight scan; expect more design work before implementation.")
    if has_docs:
        notes.append("Docs directory exists; prefer targeted reads over full-doc replay.")
    else:
        notes.append("Top-level docs were not detected; rely on README plus official specs when needed.")

    lines = [
        f"# {payload['name']} Integration Notes",
        "",
        f"- source_id: `{payload['source_id']}`",
        f"- source_category: `{normalize_source_category(str(payload.get('category', '')) or 'unknown')}`",
        f"- domain: `{normalize_domain(payload)}`",
        "",
        "## Integration Guidance",
        "",
    ]
    lines.extend([f"- {note}" for note in notes])
    lines.extend(
        [
            "",
            "## Observed Surfaces",
            "",
        ]
    )
    observed = summarize_list(paths, "No lightweight content paths captured.", limit=6)
    lines.extend([f"- {item}" for item in observed])
    lines.append("")
    return "\n".join(lines)


def build_anti_patterns(payload: dict) -> str:
    paths = content_paths(payload)
    anti_patterns: list[str] = [
        "Do not paste long README or changelog sections directly into the prompt when this summary is enough.",
        "Do not assume the latest observed ref is safe for production without local validation and design fit.",
        "Do not turn upstream examples into local standards without an explicit decision record.",
    ]
    if not any(path.lower().startswith("readme") for path in paths):
        anti_patterns.append("Do not infer repository intent from directory names alone; the lightweight scan missed a README.")
    if not payload.get("release") and not payload.get("changelog_hits"):
        anti_patterns.append("Do not assume release cadence or stability; no release/changelog signal was captured.")
    if payload.get("errors"):
        anti_patterns.append("Do not treat this source as fully summarized yet; retrieval gaps were recorded during sync.")

    lines = [
        f"# {payload['name']} Anti-Patterns",
        "",
        f"- source_id: `{payload['source_id']}`",
        "",
        "## Avoid",
        "",
    ]
    lines.extend([f"- {item}" for item in anti_patterns[:6]])
    lines.append("")
    return "\n".join(lines)


def write_summary_files(payload: dict) -> list[str]:
    domain = normalize_domain(payload)
    target_dir = SUMMARIES_ROOT / domain / payload["source_id"]
    target_dir.mkdir(parents=True, exist_ok=True)
    files = {
        "overview.md": build_overview(payload),
        "latest-notes.md": build_latest_notes(payload),
        "integration-notes.md": build_integration_notes(payload),
        "anti-patterns.md": build_anti_patterns(payload),
    }
    written: list[str] = []
    for filename, content in files.items():
        path = target_dir / filename
        path.write_text(content, encoding="utf-8")
        written.append(str(path.relative_to(ROOT)))
    return written


def write_report(results: list[dict], removed_legacy_dirs: list[str]) -> None:
    REPORTS_ROOT.mkdir(parents=True, exist_ok=True)
    file_count = sum(len(item["files"]) for item in results)
    grouped: dict[str, list[dict]] = defaultdict(list)
    for result in results:
        grouped[result["domain"]].append(result)
    lines = [
        "# Summary Refresh Report",
        "",
        f"- generated_at: {datetime.now(UTC).isoformat()}",
        f"- source_count: {len(results)}",
        f"- summary_file_count: {file_count}",
        f"- source_domains: {len(grouped) if results else 0}",
        f"- freshness_state: {'no_data' if not results else 'current'}",
        f"- normalized_legacy_dirs_removed: {len(removed_legacy_dirs)}",
        "",
    ]
    if removed_legacy_dirs:
        lines.extend(["## Legacy Cleanup", ""])
        for path in removed_legacy_dirs:
            lines.append(f"- removed legacy summary path: `{path}`")
        lines.append("")
    for domain in sorted(grouped):
        lines.extend([f"## {domain}", ""])
        for item in grouped[domain]:
            lines.append(
                f"- `{item['source_id']}` category=`{item['source_category']}` -> {', '.join(item['files'])}"
            )
        lines.append("")
    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    run = ScriptRun(ROOT, "refresh-summaries")
    args = sys.argv[1:]
    selected_source: str | None = None
    selected_domain: str | None = None
    apply = False

    i = 0
    while i < len(args):
        arg = args[i]
        if arg == "--source":
            if i + 1 >= len(args):
                return print_usage()
            selected_source = args[i + 1].strip()
            i += 2
            continue
        if arg == "--domain":
            if i + 1 >= len(args):
                return print_usage()
            selected_domain = args[i + 1].strip().lower()
            i += 2
            continue
        if arg == "--apply":
            apply = True
            i += 1
            continue
        return print_usage()

    payloads = load_metadata_files()
    if selected_source:
        payloads = [item for item in payloads if item.get("source_id") == selected_source]
    if selected_domain:
        payloads = [item for item in payloads if normalize_domain(item) == selected_domain]

    results: list[dict] = []
    for payload in payloads:
        run.event("info", "refreshing summaries for source", source_id=payload["source_id"], domain=normalize_domain(payload))
        files = write_summary_files(payload) if apply else [
            str((SUMMARIES_ROOT / normalize_domain(payload) / payload["source_id"] / name).relative_to(ROOT))
            for name in ("overview.md", "latest-notes.md", "integration-notes.md", "anti-patterns.md")
        ]
        results.append(
            {
                "source_id": payload["source_id"],
                "source_category": normalize_source_category(str(payload.get("category", ""))),
                "domain": normalize_domain(payload),
                "files": files,
            }
        )

    manifest = {
        "generated_at": datetime.now(UTC).isoformat(),
        "apply": apply,
        "sources": results,
    }
    removed_legacy_dirs: list[str] = []
    if apply:
        removed_legacy_dirs = remove_legacy_summary_dirs(payloads)
        MANIFESTS_ROOT.mkdir(parents=True, exist_ok=True)
        MANIFEST_PATH.write_text(json.dumps(manifest, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    write_report(results, removed_legacy_dirs)
    source_count = len(results)
    generated_files = sum(len(item["files"]) for item in results)
    coverage = round(source_count / len(payloads), 4) if payloads else 0.0
    freshness_state = "no_data" if source_count == 0 else "current"
    update_success_rate = round(
        len([item for item in payloads if not item.get("errors")]) / len(payloads),
        4,
    ) if payloads else 0.0
    run.metric("sources_processed", source_count)
    run.metric("summary_files_generated", generated_files)
    run.metric("coverage", coverage)
    run.metric("summary_coverage", coverage)
    run.metric("source_inventory_coverage", coverage)
    run.metric("freshness", datetime.now(UTC).isoformat() if source_count else "")
    run.metric("freshness_state", freshness_state)
    run.metric("update_success_rate", update_success_rate)
    run.finalize(
        "success",
        {
            "apply": apply,
            "sources_processed": source_count,
            "summary_files_generated": generated_files,
            "freshness_state": freshness_state,
            "legacy_dirs_removed": len(removed_legacy_dirs),
        },
    )

    print(
        f"{'Applied' if apply else 'Dry run'} summary refresh for {len(results)} source(s). "
        f"Report: {REPORT_PATH.relative_to(ROOT)}"
    )
    if not apply:
        print("Use --apply to write summary files into .agentcodex/cache/summaries/.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
