# AgentCodex

AgentCodex is a Codex-first adaptation of AgentSpec built on ECC patterns.

It keeps the practical parts:

- explicit multi-step workflow
- KB-first execution
- specialist roles for data engineering
- file-based state instead of hidden runtime state

## Install

For other users without this repository cloned, add the AgentCodex marketplace source:

```bash
codex plugin marketplace add https://github.com/ProjectDataengineerUK/agentcodex.git
```

Then install or enable `AgentCodex` from the Codex plugin/library surface, open your repository, and ask:

```text
Install AgentCodex in this repository.
```

This applies:

- `AGENTS.md`
- lightweight `.agentcodex/` workflow state directories

AgentCodex now follows the same default installation model as AgentSpec: runtime assets stay in the plugin/package, while the target project receives only minimal workflow state. To vendor the full runtime into a project, run:

```bash
agentcodex install <target-project-dir> --mode full --with-codex
```

Local shortcut on this machine:

- `codex install agentcodex` works on this machine because a local Codex command shim is installed in `~/.local/bin/codex`
- the shim delegates all other commands to the real Codex binary

If you need to install that shim manually:

```bash
python3 scripts/install_codex_command_shim.py
```

If you need to install the plugin without the shim:

```bash
python3 scripts/install_codex_plugin.py
```

To remove the local plugin entry:

```bash
python3 scripts/install_codex_plugin.py --uninstall
```

To remove the command shim:

```bash
python3 scripts/install_codex_command_shim.py --uninstall
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

Full vendored runtime surfaces:

- `AGENTS.md`
- `.codex/config.toml`
- `.codex/agents/*.toml`
- `.agentcodex/templates/`
- `.agentcodex/routing/routing.json`
- `.agentcodex/kb/`
- `.agentcodex/features/`
- `.agentcodex/history/`

In lightweight installs, most runtime surfaces remain in the installed plugin or package instead of being copied into the target repository.

## Distribution

AgentCodex is intended to be distributed as a Codex plugin.

For plugin packaging, publication, and legal page setup, see:

- `docs/PLUGIN-DISTRIBUTION.md`

Before publishing, validate plugin metadata readiness with:

```bash
python3 scripts/agentcodex.py validate-plugin
```

For marketplace-based installation tests, use:

```bash
codex plugin marketplace add https://github.com/ProjectDataengineerUK/agentcodex.git
```

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
