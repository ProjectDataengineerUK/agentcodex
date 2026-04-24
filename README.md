# AgentCodex

AgentCodex is a Codex-first adaptation of AgentSpec built on ECC patterns.

It keeps the practical parts:

- explicit multi-step workflow
- KB-first execution
- specialist roles for data engineering
- file-based state instead of hidden runtime state

## Install

End-user flow:

1. Install the `AgentCodex` plugin in Codex.
2. Open your repository in Codex.
3. Ask Codex:

```text
Install AgentCodex in this repository.
```

This applies:

- `AGENTS.md`
- `.codex/`
- `.agentcodex/`

For a home-local Codex setup, prepare the plugin with:

```bash
python3 scripts/install_codex_plugin.py
```

That installs a local `AgentCodex` plugin entry for Codex and prepares the runtime bundle.

To remove the local plugin entry:

```bash
python3 scripts/install_codex_plugin.py --uninstall
```

## Quick Start

User prompt:

```text
Install AgentCodex in this repository.
```

## How It Works

AgentCodex combines:

- AgentSpec for workflow, domain structure, and KB-first guidance
- everything-claude-code (ECC) for Codex operating patterns and runtime conventions

Raw imported upstream material is preserved separately under:

- `.agentcodex/imports/agentspec/`
- `.agentcodex/imports/ecc/`

Current runtime surfaces:

- `AGENTS.md`
- `.codex/config.toml`
- `.codex/agents/*.toml`
- `.agentcodex/templates/`
- `.agentcodex/routing/routing.json`
- `.agentcodex/kb/`
- `.agentcodex/features/`
- `.agentcodex/history/`

## Distribution

AgentCodex is intended to be distributed as a Codex plugin.

For plugin packaging, publication, and legal page setup, see:

- `docs/PLUGIN-DISTRIBUTION.md`

## Credits

Primary upstream sources:

- AgentSpec: `https://github.com/luanmorenommaciel/agentspec`
- everything-claude-code (ECC): `https://github.com/affaan-m/everything-claude-code`

Both were verified locally as MIT-licensed.

Attribution details:

- `docs/CREDITS.md`
- `docs/PRIVACY.md`
- `docs/PRIVACY-SHORT.md`
- `docs/TERMS.md`
- `docs/TERMS-SHORT.md`
- `NOTICE`
- `LICENSE`

## Docs

Start here:

- `docs/PLUGIN-DISTRIBUTION.md`
- `docs/COMMANDS.md`
- `docs/ROUTING-GUIDE.md`
- `docs/CONTEXT-HISTORY.md`
- `docs/SESSION-HANDOFF.md`
- `docs/workflow/`
- `docs/roles/`
- `docs/CREDITS.md`
