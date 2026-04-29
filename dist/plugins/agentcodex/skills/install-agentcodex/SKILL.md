# Install AgentCodex

Use this skill when the user wants to install, sync, or validate AgentCodex in a repository without cloning the AgentCodex source repo manually.

## Purpose

Initialize AgentCodex project-local workflow state while keeping the runtime assets in the plugin by default.

The default behavior matches AgentSpec's plugin ergonomics: do not copy the full framework into every project.

Default lightweight install writes:

- `AGENTS.md`
- `.agentcodex/features/`
- `.agentcodex/reports/`
- `.agentcodex/archive/`
- `.agentcodex/history/`

Full install remains available when a team wants to vendor the runtime into the repository.

## Preferred commands

Install into the current repository:

```bash
python3 plugins/agentcodex/scripts/install_runtime.py .
```

Install with a maturity profile:

```bash
python3 plugins/agentcodex/scripts/install_runtime.py . --full --profile agentic-llm
```

Install the full bundled scaffold:

```bash
python3 plugins/agentcodex/scripts/install_runtime.py . --full --with-codex
```

Sync an existing repository to the latest bundled full scaffold:

```bash
python3 plugins/agentcodex/scripts/install_runtime.py . --sync --full
```

Validate a full vendored repository after install or sync:

```bash
python3 scripts/agentcodex.py check-project .
```

## Notes

- The installer resolves runtime assets from a bundled runtime directory when present.
- During local development inside the AgentCodex source repository, the installer can fall back to the canonical repo files.
- `check-project` expects a full vendored scaffold; lightweight installs are intentionally smaller.
- Prefer lightweight install unless the user explicitly asks for a full vendored scaffold.
