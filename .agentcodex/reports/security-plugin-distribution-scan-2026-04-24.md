# Security Scan Report

- generated_at: `2026-04-24`
- scope: `plugin distribution, local install wrappers, and publication metadata`
- repository: `agentcodex`
- analyst: `Codex`

## Objective

Review the plugin installation and publication surfaces added around AgentCodex distribution, with focus on:

- local command interception and wrapper behavior
- plugin manifest publication readiness
- destructive file operations in plugin install and sync flows
- marketplace-based distribution references

## Validation Executed

- `python3 scripts/agentcodex.py validate-plugin` -> `passed`
- `python3 scripts/agentcodex.py validate` -> `passed`
- `python3 -m py_compile scripts/install_codex_plugin.py` -> `passed`
- `python3 -m py_compile scripts/install_codex_command_shim.py` -> `passed`
- `codex plugin --help` -> delegated to the real Codex binary successfully
- `codex install agentcodex` -> executed successfully through the local shim on this machine

## Achados

### 1. Medio: local command shim shadows the real `codex` binary

Status atual: known and documented

Arquivos:

- `scripts/install_codex_command_shim.py`
- `README.md`

Descrição:

The local shortcut flow installs a new executable at `~/.local/bin/codex`, which takes precedence over the real Codex binary in the current `PATH` order.

Current behavior:

- intercepts only `install agentcodex` and `uninstall agentcodex`
- delegates all other commands to the real binary at `/home/user/.npm-global/bin/codex`

Risco:

This is acceptable as a local operator shortcut, but it should not be treated as a transparent or universal public install mechanism. On unmanaged machines it introduces a trust and maintainability boundary because command resolution now depends on a wrapper script under user control.

Recomendação:

- keep this path documented as local-only
- do not present it as the public third-party installation model
- prefer marketplace-source installation for external users

### 2. Medio: plugin install and sync flows still replace managed directories destructively

Status atual: mitigated

Arquivos:

- `plugins/agentcodex/scripts/install_runtime.py`
- `scripts/sync_project.py`

Descrição:

Managed trees are removed and recopied wholesale during install or sync operations.

Examples:

- `plugins/agentcodex/scripts/install_runtime.py:67`
- `plugins/agentcodex/scripts/install_runtime.py:69`
- `scripts/sync_project.py:168`
- `scripts/sync_project.py:227`

Risco:

This is primarily an operational safety issue rather than a remote exploit path. Local customizations inside managed directories can be removed during sync, especially in `.agentcodex`, `.codex`, and project-standard feature trees.

Correcao aplicada:

- `plugins/agentcodex/scripts/install_runtime.py` now updates managed tree contents in place instead of deleting destination directories first
- `scripts/sync_project.py` now refreshes managed trees file-by-file and preserves extra local files inside managed directories
- project-standard sync now updates expected files in place instead of replacing the full tree
- regression coverage added:
  - `.agentcodex/tests/test_install_runtime_safety.py`
  - `.agentcodex/tests/test_sync_project_safety.py`

Recomendação:

- keep destructive replacement behind an explicit future flag if it becomes necessary
- add broader tests for `.codex` and profile overlay edge cases

### 3. Baixo: manifest validation still depends on a public email decision

Status atual: open by design

Arquivo:

- `plugins/agentcodex/.codex-plugin/plugin.json`

Descrição:

The plugin manifest is otherwise publication-ready, but `author.email` remains intentionally unresolved to avoid exposing a personal contact.

Risco:

Low security risk. The main impact is publication readiness and operational contactability rather than direct compromise.

Recomendação:

- use a project alias or organizational mailbox
- avoid using a personal address if public exposure is not desired

## Pontos Revisados Sem Achado Relevante

- `scripts/validate_plugin_manifest.py`
- `plugins/agentcodex/.codex-plugin/plugin.json`
- `marketplace.json`
- `docs/PLUGIN-DISTRIBUTION.md`

## Status

- plugin manifest validation passed
- repository runtime validation passed
- public plugin metadata is mostly complete
- destructive sync/install behavior in managed directories was mitigated in the current pass
- local `codex install agentcodex` works, but only as a documented machine-local shim and not as a guaranteed public Codex install surface
