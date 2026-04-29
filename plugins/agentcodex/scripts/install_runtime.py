#!/usr/bin/env python3
from __future__ import annotations

import shutil
import sys
from pathlib import Path


SCRIPT_PATH = Path(__file__).resolve()
PLUGIN_ROOT = SCRIPT_PATH.parents[1]
REPO_ROOT = SCRIPT_PATH.parents[3] if len(SCRIPT_PATH.parents) > 3 else PLUGIN_ROOT
RUNTIME_ROOT = PLUGIN_ROOT / "runtime" / "agentcodex-runtime"


def resolve_args(args: list[str]) -> tuple[Path, str, bool, str | None, str] | None:
    mode = "install"
    with_codex = False
    profile: str | None = None
    install_mode = "light"
    positional: list[str] = []
    i = 0
    while i < len(args):
        arg = args[i]
        if arg == "--mode":
            if i + 1 >= len(args):
                return None
            value = args[i + 1]
            if value in {"install", "sync"}:
                mode = value
            elif value in {"light", "full"}:
                install_mode = value
            else:
                return None
            i += 2
            continue
        if arg == "--sync":
            mode = "sync"
            i += 1
            continue
        if arg == "--full":
            install_mode = "full"
            i += 1
            continue
        if arg == "--light":
            install_mode = "light"
            i += 1
            continue
        if arg == "--profile":
            if i + 1 >= len(args):
                return None
            profile = args[i + 1]
            install_mode = "full"
            i += 2
            continue
        if arg == "--with-codex":
            with_codex = True
            i += 1
            continue
        if arg == "--without-codex":
            with_codex = False
            i += 1
            continue
        positional.append(arg)
        i += 1
    if len(positional) != 1 or mode not in {"install", "sync"}:
        return None
    return Path(positional[0]).resolve(), mode, with_codex, profile, install_mode


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


def sync_tree_contents(src: Path, dest: Path) -> None:
    dest.mkdir(parents=True, exist_ok=True)
    for path in sorted(src.rglob("*")):
        rel = path.relative_to(src)
        target = dest / rel
        if path.is_dir():
            target.mkdir(parents=True, exist_ok=True)
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(path, target)


def sync_tree(src: Path, dest: Path, mode: str) -> None:
    if not dest.exists():
        shutil.copytree(src, dest)
        return
    if mode == "install":
        sync_tree_contents(src, dest)
        return
    sync_tree_contents(src, dest)


def copy_profile_overlay(source_root: Path, target: Path, profile: str) -> None:
    overlay_root = source_root / ".agentcodex" / "bootstrap" / "MATURITY_PROFILE_OVERLAYS" / profile
    if not overlay_root.exists():
        raise ValueError(profile)
    copy_file(overlay_root / "PROFILE.md", target / ".agentcodex" / "maturity" / "ACTIVE_PROFILE.md")
    sync_tree(overlay_root / "ops", target / ".agentcodex" / "ops", "sync")


def install_or_sync(
    target: Path,
    source_root: Path,
    mode: str,
    with_codex: bool,
    profile: str | None,
    install_mode: str,
) -> None:
    target.mkdir(parents=True, exist_ok=True)
    managed_root = target / ".agentcodex"
    for relative in [
        "features",
        "reports",
        "archive",
        "history",
    ]:
        (managed_root / relative).mkdir(parents=True, exist_ok=True)

    bootstrap_root = source_root / ".agentcodex" / "bootstrap"
    sync_file(bootstrap_root / "PROJECT_AGENTSCODEX_TEMPLATE.md", managed_root / "PROJECT_AGENTSCODEX.md", mode)
    sync_file(bootstrap_root / "PROJECT_AGENTS_TEMPLATE.md", target / "AGENTS.md", mode, overwrite=False)

    if install_mode == "light":
        return

    for relative in [
        "templates",
        "commands",
        "kb",
        "routing",
        "maturity",
        "ops",
    ]:
        (managed_root / relative).mkdir(parents=True, exist_ok=True)

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
    if not sys.argv[1:] or sys.argv[1] in {"help", "--help", "-h"}:
        print(
            "Usage: python3 plugins/agentcodex/scripts/install_runtime.py "
            "<target-project-dir> [--mode install|sync|light|full] [--sync] [--full] "
            "[--profile <profile-id>] [--with-codex|--without-codex]"
        )
        return 0

    resolved = resolve_args(sys.argv[1:])
    if resolved is None:
        print(
            "Usage: python3 plugins/agentcodex/scripts/install_runtime.py "
            "<target-project-dir> [--mode install|sync|light|full] [--sync] [--full] "
            "[--profile <profile-id>] [--with-codex|--without-codex]",
            file=sys.stderr,
        )
        return 1

    target, mode, with_codex, profile, install_mode = resolved
    source_root = runtime_source_root()
    try:
        install_or_sync(target, source_root, mode, with_codex, profile, install_mode)
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
    print(f"{action} AgentCodex {install_mode} runtime in {target}")
    if with_codex:
        print(f"Created or updated: {target / '.codex'}")
    print(f"Created or updated: {target / '.agentcodex'}")
    if install_mode == "light":
        print("Runtime assets remain in the AgentCodex plugin/package. Use --full to vendor them into the project.")
    if not (target / "AGENTS.md").exists():
        print(f"Expected AGENTS.md missing at {target / 'AGENTS.md'}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
