#!/usr/bin/env python3
from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
IMPORTS_ROOT = ROOT / ".agentcodex" / "imports"

AGENTSPEC_ROOT = Path("/home/user/Projetos/agentspec")
ECC_ROOT = Path("/home/user/Projetos/everything-claude-code")


AGENTSPEC_IMPORTS = {
    "agents": "plugin/agents",
    "commands": "plugin/commands",
    "skills": "plugin/skills",
    "kb": "plugin/kb",
    "sdd": "plugin/sdd",
    "claude": ".claude",
    "plugin_extras_skills": "plugin-extras/skills",
    "plugin_hooks": "plugin/hooks",
    "docs": "docs",
    "readme": "README.md",
    "claude_md": "CLAUDE.md",
}

ECC_IMPORTS = {
    "agents_md": "AGENTS.md",
    "agents": "agents",
    "commands": "commands",
    "skills": "skills",
    "rules": "rules",
    "contexts": "contexts",
    "codex": ".codex",
    "docs": "docs",
    "docs_pt_br": "docs/pt-BR",
    "scripts_ci": "scripts/ci",
    "schemas": "schemas",
    "manifests": "manifests",
    "readme": "README.md",
    "commands_quick_ref": "COMMANDS-QUICK-REF.md",
}


def safe_remove(path: Path) -> None:
    if path.is_dir():
        shutil.rmtree(path)
    elif path.exists():
        path.unlink()


def copy_path(source_root: Path, rel_source: str, dest_root: Path, name: str) -> dict:
    source = source_root / rel_source
    destination = dest_root / name
    if not source.exists():
        return {"name": name, "status": "missing", "source": str(source)}

    safe_remove(destination)
    if source.is_dir():
        shutil.copytree(source, destination)
        file_count = sum(1 for p in destination.rglob("*") if p.is_file())
        return {
            "name": name,
            "status": "copied",
            "type": "directory",
            "source": str(source),
            "destination": str(destination.relative_to(ROOT)),
            "files": file_count,
        }

    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, destination)
    return {
        "name": name,
        "status": "copied",
        "type": "file",
        "source": str(source),
        "destination": str(destination.relative_to(ROOT)),
        "files": 1,
    }


def import_source(source_name: str, source_root: Path, mapping: dict[str, str]) -> dict:
    target_root = IMPORTS_ROOT / source_name
    target_root.mkdir(parents=True, exist_ok=True)
    results = []
    total_files = 0

    for name, rel_source in mapping.items():
        result = copy_path(source_root, rel_source, target_root, name)
        results.append(result)
        total_files += result.get("files", 0)

    return {
        "source": source_name,
        "root": str(source_root),
        "target_root": str(target_root.relative_to(ROOT)),
        "total_files": total_files,
        "imports": results,
    }


def main() -> int:
    if len(sys.argv) != 2 or sys.argv[1] not in {"all", "agentspec", "ecc"}:
        print("Usage: python3 scripts/import_upstreams.py [all|agentspec|ecc]")
        return 1

    IMPORTS_ROOT.mkdir(parents=True, exist_ok=True)
    mode = sys.argv[1]
    manifest: dict[str, object] = {"version": "0.1.0", "imports": []}

    if mode in {"all", "agentspec"}:
        manifest["imports"].append(import_source("agentspec", AGENTSPEC_ROOT, AGENTSPEC_IMPORTS))
    if mode in {"all", "ecc"}:
        manifest["imports"].append(import_source("ecc", ECC_ROOT, ECC_IMPORTS))

    manifest_path = IMPORTS_ROOT / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote import manifest: {manifest_path}")
    for item in manifest["imports"]:
        print(f"Imported {item['source']} -> {item['target_root']} ({item['total_files']} files)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
