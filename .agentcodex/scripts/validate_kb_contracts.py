#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
REGISTRY_ROOT = ROOT / ".agentcodex" / "registry"
SCHEMAS_ROOT = REGISTRY_ROOT / "schemas"
CACHE_ROOT = ROOT / ".agentcodex" / "cache"
SOURCES_PATH = REGISTRY_ROOT / "sources.yaml"
REPOS_LOCK_PATH = REGISTRY_ROOT / "repos-lock.yaml"
SUMMARY_MANIFEST_PATH = CACHE_ROOT / "manifests" / "summary-refresh-manifest.json"
RETRIEVAL_INDEX_PATH = CACHE_ROOT / "manifests" / "retrieval-index.json"
SUMMARIES_ROOT = CACHE_ROOT / "summaries"
VALID_SUMMARY_FILES = {
    "overview.md": ["## Snapshot", "## Local Use"],
    "latest-notes.md": ["## Recent Signals"],
    "integration-notes.md": ["## Integration Guidance", "## Observed Surfaces"],
    "anti-patterns.md": ["## Avoid"],
}
VALID_TRUST = {"official", "public-trusted", "community-reviewed"}
VALID_INGEST = {"metadata-first", "docs-first", "summary-first"}
VALID_UPDATE_STRATEGY = {"periodic", "manual", "release-driven", "commit-watch"}
VALID_LOCK_STATUS = {"pending", "synced", "drifted", "blocked", "ignored"}
VALID_LAYERS = {"summaries", "manifests", "kb-pages", "docs-complementary", "upstream-raw"}
VALID_BUCKETS = {"platform", "control", "integration"}
RE_SOURCE_ID = re.compile(r"^[a-z0-9][a-z0-9-]*$")
RE_GITHUB_REPO = re.compile(r"^https://github\.com/[^/]+/[^/]+/?$")


def parse_iso_datetime(value: str) -> bool:
    try:
        datetime.fromisoformat(value.replace("Z", "+00:00"))
        return True
    except ValueError:
        return False


def parse_simple_yaml(path: Path) -> dict:
    data: dict = {}
    current_list_key: str | None = None
    current_item: dict | None = None
    current_nested_list_key: str | None = None
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.rstrip()
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        indent = len(line) - len(line.lstrip(" "))
        if indent == 0 and ":" in stripped:
            key, value = stripped.split(":", 1)
            key = key.strip()
            value = value.strip()
            current_list_key = None
            current_item = None
            current_nested_list_key = None
            if value == "":
                data[key] = []
                current_list_key = key
            elif value == "[]":
                data[key] = []
            else:
                data[key] = value
            continue
        if current_list_key and stripped.startswith("- "):
            if isinstance(data[current_list_key], list):
                if ":" in stripped[2:]:
                    key, value = stripped[2:].split(":", 1)
                    current_item = {key.strip(): value.strip()}
                    data[current_list_key].append(current_item)
                else:
                    data[current_list_key].append(stripped[2:].strip())
            continue
        if current_item is not None and ":" in stripped:
            key, value = stripped.split(":", 1)
            current_item[key.strip()] = value.strip()
    return data


def load_sources() -> dict:
    return parse_simple_yaml(SOURCES_PATH)


def load_repos_lock() -> dict:
    text = REPOS_LOCK_PATH.read_text(encoding="utf-8")
    if "entries:\n  []" in text:
        return {"version": parse_simple_yaml(REPOS_LOCK_PATH).get("version", ""), "description": parse_simple_yaml(REPOS_LOCK_PATH).get("description", ""), "entries": []}
    return parse_simple_yaml(REPOS_LOCK_PATH)


def validate_sources(errors: list[str]) -> None:
    if not SOURCES_PATH.exists():
        errors.append(f"Missing sources registry: {SOURCES_PATH}")
        return
    data = load_sources()
    if not isinstance(data.get("version"), str) or not data["version"]:
        errors.append("sources.yaml missing non-empty version")
    sources = data.get("sources", [])
    if not isinstance(sources, list):
        errors.append("sources.yaml sources must be a list")
        return
    seen: set[str] = set()
    for index, item in enumerate(sources):
        if not isinstance(item, dict):
            errors.append(f"sources.yaml entry {index} must be an object")
            continue
        for key in ("id", "name", "repo", "category", "trust", "ingest_mode", "update_strategy"):
            if not item.get(key):
                errors.append(f"sources.yaml entry {index} missing {key}")
        source_id = item.get("id", "")
        if source_id:
            if not RE_SOURCE_ID.match(source_id):
                errors.append(f"sources.yaml entry has invalid id: {source_id}")
            if source_id in seen:
                errors.append(f"sources.yaml duplicated id: {source_id}")
            seen.add(source_id)
        repo = item.get("repo", "")
        if repo and not RE_GITHUB_REPO.match(repo):
            errors.append(f"sources.yaml entry has invalid repo URL: {repo}")
        if item.get("trust") and item["trust"] not in VALID_TRUST:
            errors.append(f"sources.yaml entry {source_id} has invalid trust: {item['trust']}")
        if item.get("ingest_mode") and item["ingest_mode"] not in VALID_INGEST:
            errors.append(f"sources.yaml entry {source_id} has invalid ingest_mode: {item['ingest_mode']}")
        if item.get("update_strategy") and item["update_strategy"] not in VALID_UPDATE_STRATEGY:
            errors.append(f"sources.yaml entry {source_id} has invalid update_strategy: {item['update_strategy']}")


def parse_lock_entries(text: str) -> list[dict[str, str]]:
    entries: list[dict[str, str]] = []
    current: dict[str, str] | None = None
    in_entries = False
    for raw_line in text.splitlines():
        stripped = raw_line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if stripped == "entries:":
            in_entries = True
            continue
        if not in_entries:
            continue
        if stripped == "[]":
            return []
        if stripped.startswith("- "):
            if current:
                entries.append(current)
            current = {}
            remainder = stripped[2:].strip()
            if remainder and ":" in remainder:
                key, value = remainder.split(":", 1)
                current[key.strip()] = value.strip()
            continue
        if current is not None and ":" in stripped:
            key, value = stripped.split(":", 1)
            current[key.strip()] = value.strip()
    if current:
        entries.append(current)
    return entries


def validate_repos_lock(errors: list[str]) -> None:
    if not REPOS_LOCK_PATH.exists():
        errors.append(f"Missing repos lock: {REPOS_LOCK_PATH}")
        return
    text = REPOS_LOCK_PATH.read_text(encoding="utf-8")
    data = parse_simple_yaml(REPOS_LOCK_PATH)
    if not isinstance(data.get("version"), str) or not data["version"]:
        errors.append("repos-lock.yaml missing non-empty version")
    entries = parse_lock_entries(text)
    seen: set[str] = set()
    for index, item in enumerate(entries):
        for key in ("source_id", "observed_ref", "observed_at", "update_status", "notes"):
            if key not in item:
                errors.append(f"repos-lock.yaml entry {index} missing {key}")
        source_id = item.get("source_id", "")
        if source_id:
            if not RE_SOURCE_ID.match(source_id):
                errors.append(f"repos-lock.yaml has invalid source_id: {source_id}")
            if source_id in seen:
                errors.append(f"repos-lock.yaml duplicated source_id: {source_id}")
            seen.add(source_id)
        if item.get("observed_at") and not parse_iso_datetime(item["observed_at"]):
            errors.append(f"repos-lock.yaml invalid observed_at for {source_id}: {item['observed_at']}")
        if item.get("update_status") and item["update_status"] not in VALID_LOCK_STATUS:
            errors.append(f"repos-lock.yaml invalid update_status for {source_id}: {item['update_status']}")


def load_json(path: Path, errors: list[str]) -> dict | list | None:
    if not path.exists():
        errors.append(f"Missing JSON manifest: {path}")
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        errors.append(f"Invalid JSON in {path}: {exc}")
        return None


def validate_summary_refresh_manifest(errors: list[str]) -> None:
    data = load_json(SUMMARY_MANIFEST_PATH, errors)
    if not isinstance(data, dict):
        return
    if not parse_iso_datetime(str(data.get("generated_at", ""))):
        errors.append("summary-refresh-manifest.json invalid generated_at")
    if not isinstance(data.get("apply"), bool):
        errors.append("summary-refresh-manifest.json apply must be boolean")
    if not isinstance(data.get("sources"), list):
        errors.append("summary-refresh-manifest.json sources must be an array")
        return
    for index, item in enumerate(data["sources"]):
        if not isinstance(item, dict):
            errors.append(f"summary-refresh-manifest.json source {index} must be object")
            continue
        for key in ("source_id", "domain", "files"):
            if key not in item:
                errors.append(f"summary-refresh-manifest.json source {index} missing {key}")
        if "source_id" in item and item["source_id"] and not RE_SOURCE_ID.match(item["source_id"]):
            errors.append(f"summary-refresh-manifest.json invalid source_id: {item['source_id']}")
        if "domain" in item and item["domain"] and not RE_SOURCE_ID.match(item["domain"]):
            errors.append(f"summary-refresh-manifest.json invalid domain: {item['domain']}")
        files = item.get("files", [])
        if not isinstance(files, list):
            errors.append(f"summary-refresh-manifest.json files must be list for source {item.get('source_id', index)}")
            continue
        for file_path in files:
            if not isinstance(file_path, str) or not file_path.startswith(".agentcodex/cache/summaries/") or not file_path.endswith(".md"):
                errors.append(f"summary-refresh-manifest.json invalid summary file path: {file_path}")


def validate_retrieval_index(errors: list[str]) -> None:
    data = load_json(RETRIEVAL_INDEX_PATH, errors)
    if not isinstance(data, dict):
        return
    if not parse_iso_datetime(str(data.get("generated_at", ""))):
        errors.append("retrieval-index.json invalid generated_at")
    if not isinstance(data.get("scope"), str) or not data["scope"]:
        errors.append("retrieval-index.json missing non-empty scope")
    if not isinstance(data.get("entry_count"), int) or data["entry_count"] < 0:
        errors.append("retrieval-index.json invalid entry_count")
    retrieval_priority = data.get("retrieval_priority")
    if not isinstance(retrieval_priority, list) or not retrieval_priority:
        errors.append("retrieval-index.json retrieval_priority must be a non-empty list")
    else:
        observed_pairs = []
        for item in retrieval_priority:
            if not isinstance(item, dict):
                errors.append("retrieval-index.json retrieval_priority item must be object")
                continue
            if item.get("layer") not in VALID_LAYERS:
                errors.append(f"retrieval-index.json invalid layer in retrieval_priority: {item.get('layer')}")
            if not isinstance(item.get("priority"), int) or not (1 <= item["priority"] <= 5):
                errors.append(f"retrieval-index.json invalid priority in retrieval_priority: {item.get('priority')}")
            observed_pairs.append((item.get("layer"), item.get("priority")))
        expected_pairs = [
            ("summaries", 1),
            ("manifests", 2),
            ("kb-pages", 3),
            ("docs-complementary", 4),
            ("upstream-raw", 5),
        ]
        if observed_pairs != expected_pairs:
            errors.append("retrieval-index.json retrieval_priority does not match the expected fixed ordering")
    area_domains = data.get("area_domains")
    if not isinstance(area_domains, dict):
        errors.append("retrieval-index.json area_domains must be object")
    views = data.get("views")
    if not isinstance(views, dict):
        errors.append("retrieval-index.json views must be object")
    else:
        for key in ("by_domain", "by_platform", "by_control", "by_integration"):
            if key not in views or not isinstance(views[key], dict):
                errors.append(f"retrieval-index.json missing view {key}")
    entries = data.get("entries")
    if not isinstance(entries, list):
        errors.append("retrieval-index.json entries must be array")
        return
    if isinstance(data.get("entry_count"), int) and data["entry_count"] != len(entries):
        errors.append("retrieval-index.json entry_count does not match entries length")
    for index, item in enumerate(entries):
        if not isinstance(item, dict):
            errors.append(f"retrieval-index.json entry {index} must be object")
            continue
        for key in ("path", "layer", "priority", "domain", "source_id", "kind", "area", "bucket_tags", "snippet"):
            if key not in item:
                errors.append(f"retrieval-index.json entry {index} missing {key}")
        if item.get("layer") not in VALID_LAYERS:
            errors.append(f"retrieval-index.json entry {index} invalid layer: {item.get('layer')}")
        if not isinstance(item.get("priority"), int) or not (1 <= item["priority"] <= 5):
            errors.append(f"retrieval-index.json entry {index} invalid priority: {item.get('priority')}")
        if not isinstance(item.get("bucket_tags"), list):
            errors.append(f"retrieval-index.json entry {index} bucket_tags must be list")
        else:
            for tag in item["bucket_tags"]:
                if tag not in VALID_BUCKETS:
                    errors.append(f"retrieval-index.json entry {index} invalid bucket tag: {tag}")


def validate_summaries(errors: list[str]) -> None:
    if not SUMMARIES_ROOT.exists():
        return
    for path in sorted(SUMMARIES_ROOT.rglob("*.md")):
        if path.name not in VALID_SUMMARY_FILES:
            errors.append(f"Unexpected summary file name: {path}")
            continue
        relative_parts = path.relative_to(SUMMARIES_ROOT).parts
        if len(relative_parts) != 3:
            errors.append(f"Summary path must be <domain>/<source-id>/<file>: {path}")
            continue
        domain, source_id, filename = relative_parts
        if not RE_SOURCE_ID.match(domain):
            errors.append(f"Summary path has invalid domain: {path}")
        if not RE_SOURCE_ID.match(source_id):
            errors.append(f"Summary path has invalid source-id: {path}")
        text = path.read_text(encoding="utf-8", errors="replace")
        first_non_empty = next((line.strip() for line in text.splitlines() if line.strip()), "")
        if not first_non_empty.startswith("# "):
            errors.append(f"Summary missing top-level heading: {path}")
        if "source_id:" not in text:
            errors.append(f"Summary missing source_id bullet: {path}")
        for section in VALID_SUMMARY_FILES[filename]:
            if section not in text:
                errors.append(f"Summary missing section {section}: {path}")


def main() -> int:
    errors: list[str] = []
    validate_sources(errors)
    validate_repos_lock(errors)
    validate_summary_refresh_manifest(errors)
    validate_retrieval_index(errors)
    validate_summaries(errors)

    if errors:
        print("KB contract validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print("KB contract validation passed.")
    print(f"Validated sources registry: {SOURCES_PATH}")
    print(f"Validated repos lock: {REPOS_LOCK_PATH}")
    print(f"Validated manifests: {SUMMARY_MANIFEST_PATH.name}, {RETRIEVAL_INDEX_PATH.name}")
    print(f"Validated summaries root: {SUMMARIES_ROOT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
