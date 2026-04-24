#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from collections import defaultdict
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
from observability_runtime import ScriptRun
from source_domain_mapping import resolve_source_domain

AGENTCODEX_ROOT = ROOT / ".agentcodex"
CACHE_ROOT = AGENTCODEX_ROOT / "cache"
SUMMARIES_ROOT = CACHE_ROOT / "summaries"
MANIFESTS_ROOT = CACHE_ROOT / "manifests"
KB_ROOT = AGENTCODEX_ROOT / "kb"
DOCS_ROOT = ROOT / "docs"
IMPORTS_ROOT = AGENTCODEX_ROOT / "imports"
REGISTRY_ROOT = AGENTCODEX_ROOT / "registry"
DOMAINS_PATH = REGISTRY_ROOT / "domains.yaml"
REPORTS_ROOT = AGENTCODEX_ROOT / "reports"

INDEX_JSON_PATH = MANIFESTS_ROOT / "retrieval-index.json"
INDEX_MD_PATH = MANIFESTS_ROOT / "retrieval-index.md"
REPORT_PATH = REPORTS_ROOT / "index-build-report.md"

TEXT_FILE_SUFFIXES = {".md", ".json", ".yaml", ".yml", ".toml", ".txt"}
PRIORITY_ORDER = {
    "summaries": 1,
    "manifests": 2,
    "kb-pages": 3,
    "docs-complementary": 4,
    "upstream-raw": 5,
}
BUCKET_KEYWORDS = {
    "platform": {"platforms"},
    "control": {"controls"},
    "integration": {"integrations"},
}


def print_usage() -> int:
    print(
        "Usage: python3 .agentcodex/scripts/build_index.py "
        "[--domain <domain>] [--apply]"
    )
    return 1


def load_domains_registry() -> tuple[dict[str, dict[str, str]], dict[str, list[str]]]:
    domains: dict[str, dict[str, str]] = {}
    areas: dict[str, list[str]] = defaultdict(list)
    if not DOMAINS_PATH.exists():
        return domains, areas

    current: dict[str, str] | None = None
    for raw_line in DOMAINS_PATH.read_text(encoding="utf-8").splitlines():
        line = raw_line.rstrip()
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if stripped.startswith("- id:"):
            domain_id = stripped.split(":", 1)[1].strip()
            current = {"id": domain_id}
            domains[domain_id] = current
            continue
        if current is None:
            continue
        if re.match(r"^[a-z][a-z0-9-]*:", stripped):
            key, value = stripped.split(":", 1)
            current[key.strip()] = value.strip()

    for domain_id, payload in domains.items():
        area = payload.get("area", "")
        if area:
            areas[area].append(domain_id)
    return domains, areas


def normalize_domain(raw: str) -> str:
    return raw.strip().lower().replace("_", "-").replace(" ", "-")


def infer_bucket_tags(area: str, domain: str) -> list[str]:
    tags: list[str] = []
    if area:
        for bucket, areas in BUCKET_KEYWORDS.items():
            if area in areas:
                tags.append(bucket)
    if domain in {"azure", "databricks", "snowflake", "lakehouse"} and "platform" not in tags:
        tags.append("platform")
    if domain in {"governance", "access-control", "data-contracts", "data-quality"} and "control" not in tags:
        tags.append("control")
    if domain in {"mcp", "airbyte", "dbt", "openai-agents", "qdrant"} and "integration" not in tags:
        tags.append("integration")
    return sorted(tags)


def read_text_snippet(path: Path, word_limit: int = 30) -> str:
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""
    words = text.replace("\r", " ").replace("\n", " ").split()
    if not words:
        return ""
    return " ".join(words[:word_limit]) + (" ..." if len(words) > word_limit else "")


def summary_entries() -> list[dict]:
    entries: list[dict] = []
    if not SUMMARIES_ROOT.exists():
        return entries
    for path in sorted(SUMMARIES_ROOT.rglob("*.md")):
        relative = path.relative_to(ROOT)
        parts = path.relative_to(SUMMARIES_ROOT).parts
        if len(parts) < 3:
            continue
        domain, source_id, filename = resolve_source_domain(parts[0]), parts[1], parts[2]
        entries.append(
            {
                "path": str(relative),
                "layer": "summaries",
                "priority": PRIORITY_ORDER["summaries"],
                "domain": normalize_domain(domain),
                "source_id": source_id,
                "kind": filename.removesuffix(".md"),
                "area": "",
                "bucket_tags": [],
                "snippet": read_text_snippet(path),
            }
        )
    return entries


def manifest_entries() -> list[dict]:
    entries: list[dict] = []
    if not MANIFESTS_ROOT.exists():
        return entries
    for path in sorted(MANIFESTS_ROOT.glob("*")):
        if not path.is_file() or path.suffix.lower() not in TEXT_FILE_SUFFIXES:
            continue
        entries.append(
            {
                "path": str(path.relative_to(ROOT)),
                "layer": "manifests",
                "priority": PRIORITY_ORDER["manifests"],
                "domain": "global",
                "source_id": "",
                "kind": path.stem,
                "area": "",
                "bucket_tags": [],
                "snippet": read_text_snippet(path),
            }
        )
    return entries


def kb_entries(domain_registry: dict[str, dict[str, str]]) -> list[dict]:
    entries: list[dict] = []
    if not KB_ROOT.exists():
        return entries
    for path in sorted(KB_ROOT.rglob("*.md")):
        relative_parts = path.relative_to(KB_ROOT).parts
        if not relative_parts:
            continue
        domain = ""
        area = ""
        if relative_parts[0] in {"platforms", "controls", "metadata", "operations", "integrations", "patterns", "foundations"}:
            area = relative_parts[0]
            if len(relative_parts) >= 2 and relative_parts[1].lower() != "index.md":
                domain = normalize_domain(relative_parts[1])
        else:
            domain = normalize_domain(relative_parts[0])
            area = domain_registry.get(domain, {}).get("area", "")
        if not domain and path.name.lower() == "index.md":
            domain = area or "global"
        entries.append(
            {
                "path": str(path.relative_to(ROOT)),
                "layer": "kb-pages",
                "priority": PRIORITY_ORDER["kb-pages"],
                "domain": domain or "global",
                "source_id": "",
                "kind": path.stem.lower(),
                "area": area,
                "bucket_tags": infer_bucket_tags(area, domain or ""),
                "snippet": read_text_snippet(path),
            }
        )
    return entries


def docs_entries() -> list[dict]:
    entries: list[dict] = []
    if not DOCS_ROOT.exists():
        return entries
    for path in sorted(DOCS_ROOT.rglob("*.md")):
        entries.append(
            {
                "path": str(path.relative_to(ROOT)),
                "layer": "docs-complementary",
                "priority": PRIORITY_ORDER["docs-complementary"],
                "domain": "global",
                "source_id": "",
                "kind": path.stem.lower(),
                "area": "",
                "bucket_tags": [],
                "snippet": read_text_snippet(path),
            }
        )
    return entries


def upstream_entries() -> list[dict]:
    entries: list[dict] = []
    if not IMPORTS_ROOT.exists():
        return entries
    for path in sorted(IMPORTS_ROOT.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in TEXT_FILE_SUFFIXES:
            continue
        entries.append(
            {
                "path": str(path.relative_to(ROOT)),
                "layer": "upstream-raw",
                "priority": PRIORITY_ORDER["upstream-raw"],
                "domain": "global",
                "source_id": "",
                "kind": path.stem.lower(),
                "area": "",
                "bucket_tags": [],
                "snippet": read_text_snippet(path, word_limit=20),
            }
        )
    return entries


def filter_entries(entries: list[dict], selected_domain: str | None) -> list[dict]:
    if not selected_domain:
        return entries
    selected = normalize_domain(selected_domain)
    return [entry for entry in entries if entry.get("domain") == selected]


def build_views(entries: list[dict]) -> dict[str, dict[str, list[dict]]]:
    by_domain: dict[str, list[dict]] = defaultdict(list)
    by_platform: dict[str, list[dict]] = defaultdict(list)
    by_control: dict[str, list[dict]] = defaultdict(list)
    by_integration: dict[str, list[dict]] = defaultdict(list)

    for entry in sorted(entries, key=lambda item: (item["priority"], item["path"])):
        domain = entry["domain"]
        by_domain[domain].append(entry)
        tags = set(entry.get("bucket_tags", []))
        if "platform" in tags:
            by_platform[domain].append(entry)
        if "control" in tags:
            by_control[domain].append(entry)
        if "integration" in tags:
            by_integration[domain].append(entry)

    def slim(grouped: dict[str, list[dict]]) -> dict[str, list[dict]]:
        return {
            key: [
                {
                    "path": item["path"],
                    "layer": item["layer"],
                    "priority": item["priority"],
                    "kind": item["kind"],
                    "source_id": item["source_id"],
                }
                for item in values
            ]
            for key, values in sorted(grouped.items())
        }

    return {
        "by_domain": slim(by_domain),
        "by_platform": slim(by_platform),
        "by_control": slim(by_control),
        "by_integration": slim(by_integration),
    }


def build_index_document(entries: list[dict], selected_domain: str | None) -> dict:
    _, areas = load_domains_registry()
    return {
        "generated_at": datetime.now(UTC).isoformat(),
        "scope": normalize_domain(selected_domain) if selected_domain else "all",
        "retrieval_priority": [
            {"layer": layer, "priority": priority}
            for layer, priority in sorted(PRIORITY_ORDER.items(), key=lambda item: item[1])
        ],
        "area_domains": {key: sorted(value) for key, value in sorted(areas.items())},
        "entry_count": len(entries),
        "views": build_views(entries),
        "entries": entries,
    }


def build_markdown(index: dict) -> str:
    lines = [
        "# Retrieval Index",
        "",
        f"- generated_at: `{index['generated_at']}`",
        f"- scope: `{index['scope']}`",
        f"- entry_count: `{index['entry_count']}`",
        f"- freshness_state: `{'no_data' if index['entry_count'] == 0 else 'current'}`",
        "",
        "## Retrieval Priority",
        "",
    ]
    for item in index["retrieval_priority"]:
        lines.append(f"- `{item['priority']}` `{item['layer']}`")

    for section_name in ("by_domain", "by_platform", "by_control", "by_integration"):
        lines.extend(["", f"## {section_name.replace('_', ' ').title()}", ""])
        view = index["views"][section_name]
        if not view:
            lines.append("- no entries")
            continue
        for key, items in view.items():
            lines.append(f"### {key}")
            lines.append("")
            for item in items[:12]:
                source = f" source=`{item['source_id']}`" if item["source_id"] else ""
                lines.append(
                    f"- p{item['priority']} `{item['layer']}` `{item['path']}` kind=`{item['kind']}`{source}"
                )
            if len(items) > 12:
                lines.append(f"- ... {len(items) - 12} more")
            lines.append("")
    return "\n".join(lines)


def main() -> int:
    run = ScriptRun(ROOT, "build-index")
    args = sys.argv[1:]
    selected_domain: str | None = None
    apply = False

    i = 0
    while i < len(args):
        arg = args[i]
        if arg == "--domain":
            if i + 1 >= len(args):
                return print_usage()
            selected_domain = args[i + 1].strip()
            i += 2
            continue
        if arg == "--apply":
            apply = True
            i += 1
            continue
        return print_usage()

    domain_registry, _ = load_domains_registry()
    entries = []
    entries.extend(summary_entries())
    entries.extend(manifest_entries())
    entries.extend(kb_entries(domain_registry))
    entries.extend(docs_entries())
    entries.extend(upstream_entries())
    entries = filter_entries(entries, selected_domain)
    entries = sorted(entries, key=lambda item: (item["priority"], item["domain"], item["path"]))

    index = build_index_document(entries, selected_domain)
    markdown = build_markdown(index)

    REPORTS_ROOT.mkdir(parents=True, exist_ok=True)
    local_total = len([e for e in entries if e["layer"] in {"summaries", "manifests", "kb-pages", "docs-complementary"}])
    local_coverage = round((len([e for e in entries if e["layer"] in {"summaries", "manifests", "kb-pages"}]) / max(local_total, 1)), 4) if entries else 0.0
    source_inventory_coverage = round(
        len([e for e in entries if e["layer"] == "summaries"]) / max(len([e for e in entries if e["layer"] in {"summaries", "upstream-raw"}]), 1),
        4,
    ) if entries else 0.0
    REPORT_PATH.write_text(
        "\n".join(
            [
                "# Index Build Report",
                "",
                f"- generated_at: {index['generated_at']}",
                f"- scope: {index['scope']}",
                f"- entry_count: {index['entry_count']}",
                f"- summaries: {len([e for e in entries if e['layer'] == 'summaries'])}",
                f"- manifests: {len([e for e in entries if e['layer'] == 'manifests'])}",
                f"- kb_pages: {len([e for e in entries if e['layer'] == 'kb-pages'])}",
                f"- docs_complementary: {len([e for e in entries if e['layer'] == 'docs-complementary'])}",
                f"- upstream_raw: {len([e for e in entries if e['layer'] == 'upstream-raw'])}",
                f"- local_layer_coverage: {local_coverage}",
                f"- source_inventory_coverage: {source_inventory_coverage}",
                f"- freshness_state: {'no_data' if len(entries) == 0 else 'current'}",
                "",
            ]
        ),
        encoding="utf-8",
    )

    if apply:
        MANIFESTS_ROOT.mkdir(parents=True, exist_ok=True)
        INDEX_JSON_PATH.write_text(json.dumps(index, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
        INDEX_MD_PATH.write_text(markdown, encoding="utf-8")

    layer_counts = {
        "summaries": len([e for e in entries if e["layer"] == "summaries"]),
        "manifests": len([e for e in entries if e["layer"] == "manifests"]),
        "kb-pages": len([e for e in entries if e["layer"] == "kb-pages"]),
        "docs-complementary": len([e for e in entries if e["layer"] == "docs-complementary"]),
        "upstream-raw": len([e for e in entries if e["layer"] == "upstream-raw"]),
    }
    local_total = (
        layer_counts["summaries"]
        + layer_counts["manifests"]
        + layer_counts["kb-pages"]
        + layer_counts["docs-complementary"]
    )
    local_coverage = round(
        (layer_counts["summaries"] + layer_counts["manifests"] + layer_counts["kb-pages"]) / local_total,
        4,
    ) if local_total else 1.0
    summary_coverage = round(layer_counts["summaries"] / max(layer_counts["kb-pages"], 1), 4) if layer_counts["kb-pages"] else 0.0
    source_inventory_coverage = round(
        layer_counts["summaries"] / max(layer_counts["summaries"] + layer_counts["upstream-raw"], 1),
        4,
    ) if (layer_counts["summaries"] or layer_counts["upstream-raw"]) else 0.0
    freshness_state = "no_data" if len(entries) == 0 else "current"
    update_success_rate = round(
        (layer_counts["summaries"] + layer_counts["manifests"] + layer_counts["kb-pages"]) / max(local_total, 1),
        4,
    ) if local_total else 0.0
    run.metric("indexed_entries", len(entries))
    run.metric("coverage", local_coverage)
    run.metric("local_layer_coverage", local_coverage)
    run.metric("summary_coverage", summary_coverage)
    run.metric("source_inventory_coverage", source_inventory_coverage)
    run.metric("freshness", datetime.now(UTC).isoformat() if entries else "")
    run.metric("freshness_state", freshness_state)
    run.metric("update_success_rate", update_success_rate)
    for key, value in layer_counts.items():
        run.metric(f"entries_{key}", value)
    run.finalize(
        "success",
        {
            "apply": apply,
            "scope": index["scope"],
            "entry_count": len(entries),
            "freshness_state": freshness_state,
        },
    )

    print(
        f"{'Applied' if apply else 'Dry run'} index build for {index['entry_count']} entry(s). "
        f"Report: {REPORT_PATH.relative_to(ROOT)}"
    )
    if not apply:
        print("Use --apply to write retrieval-index.json and retrieval-index.md into .agentcodex/cache/manifests/.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
