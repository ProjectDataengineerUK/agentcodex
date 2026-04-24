#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
import urllib.parse
import urllib.request
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
from observability_runtime import ScriptRun

REGISTRY_ROOT = ROOT / ".agentcodex" / "registry"
REPORTS_ROOT = ROOT / ".agentcodex" / "reports"
REPOS_LOCK_PATH = REGISTRY_ROOT / "repos-lock.yaml"
SOURCES_PATH = REGISTRY_ROOT / "sources.yaml"
UPDATE_REPORT_PATH = REPORTS_ROOT / "update-report.md"


def print_usage() -> int:
    print(
        "Usage: python3 .agentcodex/scripts/check_updates.py "
        "[--source <source-id>] [--apply]"
    )
    return 1


def load_sources() -> list[dict[str, str]]:
    if not SOURCES_PATH.exists():
        raise SystemExit(f"Missing sources registry: {SOURCES_PATH}")

    items: list[dict[str, str]] = []
    current: dict[str, str] | None = None
    in_sources = False
    for raw_line in SOURCES_PATH.read_text(encoding="utf-8").splitlines():
        stripped = raw_line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if stripped == "sources:":
            in_sources = True
            continue
        if not in_sources:
            continue
        if stripped.startswith("- "):
            if current:
                items.append(current)
            current = {}
            remainder = stripped[2:].strip()
            if remainder:
                key, value = remainder.split(":", 1)
                current[key.strip()] = value.strip()
            continue
        if current is not None and ":" in stripped:
            key, value = stripped.split(":", 1)
            current[key.strip()] = value.strip()
    if current:
        items.append(current)
    return items


def load_repos_lock() -> tuple[str, str, list[dict[str, str]]]:
    if not REPOS_LOCK_PATH.exists():
        return "0.1.0", "observed upstream repository state for trusted public sources used by AgentCodex", []
    version = "0.1.0"
    description = ""
    entries: list[dict[str, str]] = []
    current: dict[str, str] | None = None
    in_entries = False
    for raw_line in REPOS_LOCK_PATH.read_text(encoding="utf-8").splitlines():
        stripped = raw_line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if stripped.startswith("version:"):
            version = stripped.split(":", 1)[1].strip()
            continue
        if stripped.startswith("description:"):
            description = stripped.split(":", 1)[1].strip()
            continue
        if stripped == "entries:":
            in_entries = True
            continue
        if not in_entries:
            continue
        if stripped.startswith("- "):
            if current:
                entries.append(current)
            current = {}
            remainder = stripped[2:].strip()
            if remainder:
                key, value = remainder.split(":", 1)
                current[key.strip()] = value.strip()
            continue
        if current is not None and ":" in stripped:
            key, value = stripped.split(":", 1)
            current[key.strip()] = value.strip()
    if current:
        entries.append(current)
    return version, description, entries


def save_repos_lock(version: str, description: str, entries: list[dict[str, str]]) -> None:
    lines = [
        f"version: {version}",
        f"description: {description}",
        "entries:",
    ]
    if not entries:
        lines.append("  []")
    else:
        for entry in sorted(entries, key=lambda item: item["source_id"]):
            lines.append(f"  - source_id: {entry['source_id']}")
            lines.append(f"    observed_ref: {entry['observed_ref']}")
            lines.append(f"    observed_at: {entry['observed_at']}")
            lines.append(f"    update_status: {entry['update_status']}")
            lines.append(f"    notes: {entry['notes']}")
    REPOS_LOCK_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def github_repo_parts(repo_url: str) -> tuple[str, str] | None:
    parsed = urllib.parse.urlparse(repo_url)
    if parsed.netloc not in {"github.com", "www.github.com"}:
        return None
    parts = [part for part in parsed.path.strip("/").split("/") if part]
    if len(parts) < 2:
        return None
    return parts[0], parts[1].removesuffix(".git")


def http_get_json(url: str) -> dict:
    request = urllib.request.Request(
        url,
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "AgentCodex/0.1.0",
        },
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def fetch_observed_state(source: dict[str, str]) -> dict[str, str]:
    repo_parts = github_repo_parts(source["repo"])
    if repo_parts is None:
        raise RuntimeError(f"Unsupported repository URL: {source['repo']}")
    owner, repo_name = repo_parts
    repo_api = f"https://api.github.com/repos/{owner}/{repo_name}"
    repo_data = http_get_json(repo_api)
    default_branch = repo_data.get("default_branch", "main")
    branch_data = http_get_json(f"{repo_api}/branches/{default_branch}")
    observed_ref = branch_data.get("commit", {}).get("sha", "")
    latest_release = ""
    try:
        release_data = http_get_json(f"{repo_api}/releases/latest")
        latest_release = release_data.get("tag_name", "")
    except Exception:
        latest_release = ""
    return {
        "default_branch": default_branch,
        "observed_ref": observed_ref,
        "latest_release": latest_release,
        "repo_updated_at": str(repo_data.get("updated_at", "")),
    }


def run_local_script(script_path: Path, args: list[str]) -> None:
    subprocess.run(
        [sys.executable, str(script_path), *args],
        cwd=str(ROOT),
        check=True,
    )


def apply_refresh_pipeline(changed_ids: list[str]) -> None:
    for source_id in changed_ids:
        run_local_script(
            ROOT / ".agentcodex" / "scripts" / "sync_sources.py",
            ["--source", source_id, "--apply", "--skip-lock-update"],
        )
    run_local_script(ROOT / ".agentcodex" / "scripts" / "refresh_summaries.py", ["--apply"])
    run_local_script(ROOT / ".agentcodex" / "scripts" / "build_index.py", ["--apply"])


def write_report(results: list[dict[str, str]], apply: bool) -> None:
    REPORTS_ROOT.mkdir(parents=True, exist_ok=True)
    changed = len([item for item in results if item["change_detected"] == "yes"])
    blocked = len([item for item in results if item["update_status"] == "blocked"])
    failed = len([item for item in results if item["update_status"] == "failed"])
    success_rate = round(
        len([item for item in results if item["update_status"] in {"synced", "drifted"}]) / len(results),
        4,
    ) if results else 0.0
    lines = [
        "# Update Report",
        "",
        f"- generated_at: {datetime.now(UTC).isoformat()}",
        f"- mode: {'apply' if apply else 'dry-run'}",
        f"- checked_sources: {len(results)}",
        f"- changed_sources: {changed}",
        f"- blocked_sources: {blocked}",
        f"- failed_sources: {failed}",
        f"- update_success_rate: {success_rate}",
        f"- freshness_state: {'no_data' if not results else 'current'}",
        "",
    ]
    if blocked:
        lines.extend(
            [
                "## Status Notes",
                "",
                "- `blocked` means the source could not be checked, usually because the network or upstream endpoint was unavailable.",
                "- `failed` means drift was detected or refresh was attempted, but the downstream refresh pipeline did not complete cleanly.",
                "- `synced` and `drifted` mean the upstream check itself completed successfully.",
                "",
            ]
        )
    for item in results:
        lines.extend(
            [
                f"## {item['source_id']}",
                "",
                f"- repo: {item['repo']}",
                f"- previous_ref: {item['previous_ref'] or 'none'}",
                f"- observed_ref: {item['observed_ref'] or 'unknown'}",
                f"- latest_release: {item['latest_release'] or 'none'}",
                f"- change_detected: {item['change_detected']}",
                f"- update_status: {item['update_status']}",
                f"- human_status: {human_status(item['update_status'])}",
                f"- notes: {item['notes']}",
                "",
            ]
        )
    UPDATE_REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")


def human_status(status: str) -> str:
    return {
        "blocked": "network-blocked",
        "failed": "refresh-failed",
        "synced": "upstream-synced",
        "drifted": "upstream-drifted",
    }.get(status, status)


def main() -> int:
    run = ScriptRun(ROOT, "check-updates")
    args = sys.argv[1:]
    selected_source: str | None = None
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
        if arg == "--apply":
            apply = True
            i += 1
            continue
        return print_usage()

    sources = load_sources()
    if selected_source:
        sources = [item for item in sources if item.get("id") == selected_source]

    version, description, lock_entries = load_repos_lock()
    lock_by_id = {item["source_id"]: item for item in lock_entries}
    updated_entries: dict[str, dict[str, str]] = {item["source_id"]: dict(item) for item in lock_entries}
    results: list[dict[str, str]] = []
    changed_ids: list[str] = []

    for source in sources:
        source_id = source["id"]
        previous = lock_by_id.get(source_id, {})
        now_iso = datetime.now(UTC).isoformat()
        run.event("info", "checking source update", source_id=source_id, repo=source["repo"])
        try:
            observed = fetch_observed_state(source)
            previous_ref = previous.get("observed_ref", "")
            change_detected = "yes" if observed["observed_ref"] and observed["observed_ref"] != previous_ref else "no"
            update_status = "drifted" if change_detected == "yes" else "synced"
            notes = (
                "new upstream ref detected"
                if change_detected == "yes"
                else "no upstream change detected"
            )
            updated_entries[source_id] = {
                "source_id": source_id,
                "observed_ref": observed["observed_ref"],
                "observed_at": now_iso,
                "update_status": update_status,
                "notes": notes,
            }
            if change_detected == "yes" or source_id not in lock_by_id:
                changed_ids.append(source_id)
            results.append(
                {
                    "source_id": source_id,
                    "repo": source["repo"],
                    "previous_ref": previous_ref,
                    "observed_ref": observed["observed_ref"],
                    "latest_release": observed["latest_release"],
                    "change_detected": change_detected,
                    "update_status": update_status,
                    "notes": notes,
                }
            )
        except Exception as exc:
            run.record_source_failure(source_id, str(exc), "check-updates")
            run.event("error", "source update check failed", source_id=source_id, error=str(exc))
            updated_entries[source_id] = {
                "source_id": source_id,
                "observed_ref": previous.get("observed_ref", ""),
                "observed_at": now_iso,
                "update_status": "blocked",
                "notes": str(exc).replace("\n", " "),
            }
            results.append(
                {
                    "source_id": source_id,
                    "repo": source["repo"],
                    "previous_ref": previous.get("observed_ref", ""),
                    "observed_ref": previous.get("observed_ref", ""),
                    "latest_release": "",
                    "change_detected": "unknown",
                    "update_status": "blocked",
                    "notes": str(exc).replace("\n", " "),
                }
            )

    apply_error: str | None = None
    if apply:
        try:
            if changed_ids:
                apply_refresh_pipeline(changed_ids)
            save_repos_lock(version, description, list(updated_entries.values()))
        except subprocess.CalledProcessError as exc:
            apply_error = f"refresh pipeline failed with exit code {exc.returncode}"
            run.event("error", "apply refresh pipeline failed", error=apply_error)
            for source_id in changed_ids:
                updated_entries[source_id] = {
                    "source_id": source_id,
                    "observed_ref": updated_entries.get(source_id, {}).get("observed_ref", lock_by_id.get(source_id, {}).get("observed_ref", "")),
                    "observed_at": updated_entries.get(source_id, {}).get("observed_at", datetime.now(UTC).isoformat()),
                    "update_status": "failed",
                    "notes": apply_error,
                }
            for item in results:
                if item["source_id"] in changed_ids:
                    item["update_status"] = "failed"
                    item["notes"] = apply_error

    write_report(results, apply=apply)
    blocked = len([item for item in results if item["update_status"] == "blocked"])
    changed = len([item for item in results if item["change_detected"] == "yes"])
    failed = len([item for item in results if item["update_status"] == "failed"])
    checked = len(results)
    success_rate = round(
        len([item for item in results if item["update_status"] in {"synced", "drifted"}]) / checked,
        4,
    ) if checked else 0.0
    freshness = datetime.now(UTC).isoformat() if checked else ""
    freshness_state = "no_data" if checked == 0 else "current"
    run.metric("sources_checked", checked)
    run.metric("sources_changed", changed)
    run.metric("sources_blocked", blocked)
    run.metric("sources_failed", failed)
    run.metric("coverage", round((checked - blocked - failed) / checked, 4) if checked else 0.0)
    run.metric("freshness", freshness)
    run.metric("freshness_state", freshness_state)
    run.metric("update_success_rate", success_rate)
    run.finalize(
        "failed" if apply_error else "success",
        {
            "apply": apply,
            "changed_sources": changed,
            "checked_sources": checked,
            "blocked_sources": blocked,
            "failed_sources": failed,
            "apply_error": apply_error or "",
            "freshness_state": freshness_state,
        },
    )
    if apply_error:
        print(f"Update check apply failed: {apply_error}", file=sys.stderr)
        return 1
    print(
        f"{'Applied' if apply else 'Dry run'} update check for {len(results)} source(s). "
        f"Changed: {len(changed_ids)}. Report: {UPDATE_REPORT_PATH.relative_to(ROOT)}"
    )
    if not apply:
        print("Use --apply to update repos-lock.yaml and refresh metadata, summaries, and retrieval index.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
