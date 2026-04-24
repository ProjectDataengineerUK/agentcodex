# Install AgentCodex

Use this skill when the user wants to install, sync, or validate AgentCodex in a repository without cloning the AgentCodex source repo manually.

## Purpose

Materialize the AgentCodex local runtime inside a target project by writing:

- `AGENTS.md`
- `.codex/`
- `.agentcodex/`

## Preferred commands

Install into the current repository:

```bash
python3 plugins/agentcodex/scripts/install_runtime.py .
```

Install with a maturity profile:

```bash
python3 plugins/agentcodex/scripts/install_runtime.py . --profile agentic-llm
```

Sync an existing repository to the latest bundled scaffold:

```bash
python3 plugins/agentcodex/scripts/install_runtime.py . --mode sync
```

Validate an existing repository after install or sync:

```bash
python3 scripts/agentcodex.py check-project .
```

## Notes

- The installer resolves runtime assets from a bundled runtime directory when present.
- During local development inside the AgentCodex source repository, the installer can fall back to the canonical repo files.
- Prefer `install_runtime.py` over directly copying files by hand so profile overlays and managed directories stay consistent.
