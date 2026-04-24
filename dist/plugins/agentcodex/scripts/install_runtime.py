#!/usr/bin/env python3
from __future__ import annotations

import shutil
import sys
from pathlib import Path


SCRIPT_PATH = Path(__file__).resolve()
PLUGIN_ROOT = SCRIPT_PATH.parents[1]
REPO_ROOT = SCRIPT_PATH.parents[3] if len(SCRIPT_PATH.parents) > 3 else PLUGIN_ROOT
RUNTIME_ROOT = PLUGIN_ROOT / "runtime" / "agentcodex-runtime"


def resolve_args(args: list[str]) -> tuple[Path, str, bool, str | None] | None:
    mode = "install"
    with_codex = True
    profile: str | None = None
    positional: list[str] = []
    i = 0
    while i < len(args):
        arg = args[i]
        if arg == "--mode":
            if i + 1 >= len(args):
                return None
            mode = args[i + 1]
            i += 2
            continue
        if arg == "--profile":
            if i + 1 >= len(args):
                return None
            profile = args[i + 1]
            i += 2
            continue
        if arg == "--without-codex":
            with_codex = False
            i += 1
            continue
        positional.append(arg)
        i += 1
    if len(positional) != 1 or mode not in {"install", "sync"}:
        return None
    return Path(positional[0]).resolve(), mode, with_codex, profile


def runtime_source_root() -> Path:
    if (RUNTIME_ROOT / ".agentcodex" / "bootstrap").exists():
        return RUNTIME_ROOT
    if (REPO_ROOT / ".agentcodex" / "bootstrap").exists() and (REPO_ROOT / "docs" / "commands").exists():
        return REPO_ROOT
    raise RuntimeError(
        "Could not resolve AgentCodex runtime. Build the plugin runtime bundle or run from the source repository."
    )


def copy_file(src: Path, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, dest)


def sync_file(src: Path, dest: Path, mode: str, overwrite: bool = True) -> None:
    if dest.exists() and mode == "install" and not overwrite:
        return
    copy_file(src, dest)


def sync_tree(src: Path, dest: Path, mode: str) -> None:
    if dest.exists():
        if mode == "install":
            shutil.rmtree(dest)
        else:
            shutil.rmtree(dest)
    shutil.copytree(src, dest)


def copy_profile_overlay(source_root: Path, target: Path, profile: str) -> None:
    overlay_root = source_root / ".agentcodex" / "bootstrap" / "MATURITY_PROFILE_OVERLAYS" / profile
    if not overlay_root.exists():
        raise ValueError(profile)
    copy_file(overlay_root / "PROFILE.md", target / ".agentcodex" / "maturity" / "ACTIVE_PROFILE.md")
    sync_tree(overlay_root / "ops", target / ".agentcodex" / "ops", "sync")


def install_or_sync(target: Path, source_root: Path, mode: str, with_codex: bool, profile: str | None) -> None:
    target.mkdir(parents=True, exist_ok=True)
    managed_root = target / ".agentcodex"
    for relative in [
        "features",
        "reports",
        "archive",
        "history",
        "templates",
        "commands",
        "kb",
        "routing",
        "maturity",
        "ops",
    ]:
        (managed_root / relative).mkdir(parents=True, exist_ok=True)

    bootstrap_root = source_root / ".agentcodex" / "bootstrap"
    sync_file(bootstrap_root / "PROJECT_AGENTSCODEX_TEMPLATE.md", managed_root / "PROJECT_AGENTSCODEX.md", mode)
    sync_file(bootstrap_root / "PROJECT_AGENTS_TEMPLATE.md", target / "AGENTS.md", mode, overwrite=False)
    sync_file(
        bootstrap_root / "EXAMPLE_DEFINE_TEMPLATE.md",
        managed_root / "features" / "DEFINE_EXAMPLE_PROJECT_FEATURE.md",
        mode,
    )
    sync_tree(bootstrap_root / "PROJECT_STANDARD_FEATURE", managed_root / "features" / "example-project-standard", mode)
    sync_file(source_root / ".agentcodex" / "project-standard.json", managed_root / "project-standard.json", mode)
    sync_tree(source_root / ".agentcodex" / "templates", managed_root / "templates", mode)
    sync_tree(source_root / "docs" / "commands", managed_root / "commands", mode)
    sync_tree(source_root / ".agentcodex" / "kb", managed_root / "kb", mode)
    sync_file(source_root / ".agentcodex" / "routing" / "routing.json", managed_root / "routing" / "routing.json", mode)
    sync_tree(source_root / ".agentcodex" / "maturity", managed_root / "maturity", mode)

    if profile:
        copy_profile_overlay(source_root, target, profile)

    if with_codex:
        sync_tree(bootstrap_root / "codex", target / ".codex", mode)


def main() -> int:
    resolved = resolve_args(sys.argv[1:])
    if resolved is None:
        print(
            "Usage: python3 plugins/agentcodex/scripts/install_runtime.py "
            "<target-project-dir> [--mode install|sync] [--profile <profile-id>] [--without-codex]",
            file=sys.stderr,
        )
        return 1

    target, mode, with_codex, profile = resolved
    source_root = runtime_source_root()
    try:
        install_or_sync(target, source_root, mode, with_codex, profile)
    except ValueError:
        available = ", ".join(
            sorted(
                path.name
                for path in (source_root / ".agentcodex" / "bootstrap" / "MATURITY_PROFILE_OVERLAYS").iterdir()
                if path.is_dir()
            )
        )
        print(f"Unknown maturity profile: {profile}", file=sys.stderr)
        print(f"Available profiles: {available}", file=sys.stderr)
        return 1

    action = "Installed" if mode == "install" else "Synchronized"
    print(f"{action} AgentCodex runtime in {target}")
    if with_codex:
        print(f"Created or updated: {target / '.codex'}")
    print(f"Created or updated: {target / '.agentcodex'}")
    if not (target / "AGENTS.md").exists():
        print(f"Expected AGENTS.md missing at {target / 'AGENTS.md'}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
