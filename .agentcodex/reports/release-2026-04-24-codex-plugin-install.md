# Release Note

- date: `2026-04-24`
- release_scope: `codex plugin installation and publication readiness`
- repository: `agentcodex`
- author: `Codex`

## Summary

This release hardens and documents the Codex-native plugin distribution flow for AgentCodex.

The repository now supports:

- a published-plugin UX centered on Codex plugin/library installation
- a repository marketplace root at `marketplace.json`
- a home-local plugin installer at `scripts/install_codex_plugin.py`
- an optional local command shim at `scripts/install_codex_command_shim.py`
- legal pages for plugin publication:
  - `docs/PRIVACY.md`
  - `docs/TERMS.md`
  - `docs/PRIVACY-SHORT.md`
  - `docs/TERMS-SHORT.md`

## User-Facing Install Flow

For third parties without a local clone, the documented install path is:

```bash
codex plugin marketplace add https://github.com/ProjectDataengineerUK/agentcodex.git
```

Then in Codex:

1. install or enable `AgentCodex`
2. open the target repository
3. ask:

```text
Install AgentCodex in this repository.
```

Expected scaffold:

- `AGENTS.md`
- `.codex/`
- `.agentcodex/`

## Local Operator Shortcuts

For local machine setup and testing:

- `python3 scripts/install_codex_plugin.py`
- `python3 scripts/install_codex_plugin.py --uninstall`

Optional local shortcut layer:

- `python3 scripts/install_codex_command_shim.py`
- `codex install agentcodex`
- `codex uninstall agentcodex`

## Publication Metadata Status

Finalized in `plugins/agentcodex/.codex-plugin/plugin.json`:

- `homepage`
- `repository`
- `interface.websiteURL`
- `interface.privacyPolicyURL`
- `interface.termsOfServiceURL`
- `author.url`

Still pending by design:

- `author.email`

## Validation Executed

- `python3 scripts/agentcodex.py validate-plugin` -> passed
- `python3 scripts/agentcodex.py validate` -> passed
- `python3 -m py_compile scripts/install_codex_plugin.py` -> passed
- `python3 -m py_compile scripts/install_codex_command_shim.py` -> passed
- `python3 -m py_compile plugins/agentcodex/scripts/install_runtime.py scripts/sync_project.py` -> passed
- `python3 -m unittest discover -s .agentcodex/tests -p 'test_*safety.py'` -> passed
- `python3 scripts/package_plugin.py` -> generated `dist/plugins/agentcodex-plugin-0.1.0.tar.gz`
- `codex install agentcodex` -> executed successfully on the local machine after shim installation

## Notes

- `codex install agentcodex` is currently a local-machine shortcut implemented by a shim in `~/.local/bin/codex`
- it is not documented as a guaranteed public Codex registry install path for third parties
- the public install path remains marketplace-source registration plus Codex plugin/library installation
- managed install/sync behavior was hardened to preserve extra local files inside managed directories instead of deleting entire destination trees by default
