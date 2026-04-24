#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
STATUS_DOC = ROOT / "docs" / "STATUS.md"
PROJECT_STANDARD = ROOT / ".agentcodex" / "project-standard.json"
MATURITY5_BASELINE = ROOT / ".agentcodex" / "maturity" / "maturity5-baseline.json"
ROLES_DIR = ROOT / "docs" / "roles"
COMMANDS_DIR = ROOT / "docs" / "commands"
CODEX_AGENTS_DIR = ROOT / ".codex" / "agents"
HISTORY_DIR = ROOT / ".agentcodex" / "history"
ADR_DIR = ROOT / "docs" / "adr"


def count_files(path: Path, pattern: str) -> int:
    if not path.exists():
        return 0
    return len(list(path.glob(pattern)))


def main() -> int:
    standard = json.loads(PROJECT_STANDARD.read_text(encoding="utf-8"))
    maturity = json.loads(MATURITY5_BASELINE.read_text(encoding="utf-8"))
    block_ids = [block["id"] for block in standard["blocks"]]
    maturity_profiles = maturity["profiles"]

    lines = [
        "# Status",
        "",
        "Generated status snapshot for AgentCodex.",
        "",
        "## Current Surface",
        "",
        f"- documented roles: {count_files(ROLES_DIR, '*.md')}",
        f"- command procedures: {count_files(COMMANDS_DIR, '*.md')}",
        f"- codex agents: {count_files(CODEX_AGENTS_DIR, '*.toml')}",
        f"- ADRs: {max(count_files(ADR_DIR, '*.md') - 1, 0)}",
        f"- history entries: {count_files(HISTORY_DIR, '*.md')}",
        "",
        "## Project Standard",
        "",
        f"- manifest: `.agentcodex/project-standard.json`",
        f"- version: {standard['version']}",
        f"- scaffold root: `{standard['feature_scaffold_root']}`",
        f"- total blocks: {len(block_ids)}",
        "",
        "Blocks:",
    ]
    lines.extend(f"- `{block_id}`" for block_id in block_ids)
    lines.extend(
        [
            "",
            "## Maturity 5 Baseline",
            "",
            "- manifest: `.agentcodex/maturity/maturity5-baseline.json`",
            f"- version: {maturity['version']}",
            f"- default profile: `{maturity['default_profile']}`",
            f"- profiles: {len(maturity_profiles)}",
            "",
            "Profiles:",
        ]
    )
    for profile in maturity_profiles:
        lines.append(f"- `{profile['id']}`: {profile['name']}")
    lines.extend(
        [
            "",
            "## Automation",
            "",
            "- `agentcodex refresh-all` refreshes generated artifacts and validates the repo",
            "- `agentcodex readiness-report <target-project-dir>` writes a project readiness report",
            "- `agentcodex ship-gate <target-project-dir>` enforces readiness before ship",
            "- `agentcodex control-plane-check <target-project-dir>` scores multi-agent, token, cost, and security/compliance readiness",
            "- `agentcodex maturity5-check <target-project-dir> [--profile <profile-id>]` evaluates the executable DataOps + LLMOps maturity baseline",
            "- `agentcodex install-local-automation` prepares repo-local git hooks when a `.git` root exists",
            "",
            "## Control Plane",
            "",
            "- `agentcodex control-plane-check <target-project-dir>` is the authoritative enterprise gate for `multi-agent`, `token`, `cost`, and `security`",
            "- `agentcodex enterprise-readiness <target-project-dir>` is a concise alias for the same control-plane evaluation",
            "- `fail` means a structural gap that blocks enterprise readiness",
            "- `warn` means the surface exists but still contains placeholder or incomplete operational content",
            "- `pass` means the evaluated control surface has no detected gaps in the current file-based checks",
            "",
        ]
    )

    STATUS_DOC.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote status doc: {STATUS_DOC}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
