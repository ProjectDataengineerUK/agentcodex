# Data Agents Import Automation - 2026-04-29

## Purpose

Make `/home/user/Projetos/data-agents` a first-class raw upstream source for AgentCodex, alongside AgentSpec and ECC.

## Implemented

- `scripts/import_upstreams.py` now supports:
  - `python3 scripts/agentcodex.py import-upstreams data-agents`
  - `python3 scripts/agentcodex.py import-upstreams all`
- `.agentcodex/imports/data-agents/` now stores the raw imported source material.
- `scripts/generate_import_catalog.py` now catalogs `data-agents` without assuming ECC-only directories such as `rules/`.
- `scripts/generate_data_agents_extension_registry.py` now generates a Codex-native extension registry without duplicating active AgentCodex roles, commands, or KB pages.
- `scripts/validate_agentcodex.py` now validates `.agentcodex/data-agents-extension.json` counts, source paths, native mappings, and no-duplicate policy.
- `docs/UPSTREAM-IMPORTS.md` documents the Data Agents source and refresh commands.
- `.agentcodex/tests/test_import_upstreams.py` covers the Data Agents import mapping.

## Imported Snapshot

Source:

- `/home/user/Projetos/data-agents`
- latest local commit checked during implementation: `968daaf Merge pull request #92 from ThomazRossito/dev`

Imported files:

- total: `502`

Catalog counts:

- agents registry docs: `13`
- command modules: `7`
- skills: `44`
- KB domains: `11`
- MCP servers: `14`
- hooks: `12`
- mirrored tests: `42`

## Imported Surfaces

- agents
- commands
- compression
- config
- evals
- hooks
- kb
- mcp_servers
- memory
- monitoring
- scripts
- skills
- templates
- tests
- tools
- ui
- utils
- wiki
- workflow
- github_workflows
- claude_commands
- chainlit
- README / PRODUCT / CHANGELOG / LICENSE / Makefile / pyproject / MCP config / env example / technical manual

## Refresh Procedure

Refresh only Data Agents:

```bash
python3 scripts/agentcodex.py import-upstreams data-agents
python3 scripts/agentcodex.py generate-import-catalog
python3 scripts/agentcodex.py generate-data-agents-extension
python3 scripts/agentcodex.py generate-roles
python3 scripts/agentcodex.py generate-routing
python3 scripts/validate_agentcodex.py
```

Refresh all imported upstreams:

```bash
python3 scripts/agentcodex.py import-upstreams all
python3 scripts/agentcodex.py generate-import-catalog
python3 scripts/agentcodex.py generate-data-agents-extension
python3 scripts/agentcodex.py generate-roles
python3 scripts/agentcodex.py generate-routing
python3 scripts/validate_agentcodex.py
```

## Native Codex Extension

- Registry: `.agentcodex/data-agents-extension.json`
- Human-readable summary: `docs/DATA-AGENTS-EXTENSION.md`
- New native roles added from distinct Data Agents behavior:
  - `docs/roles/business-monitor.md`
  - `docs/roles/semantic-modeler.md`
- Existing equivalent roles and commands are mapped instead of duplicated.

## Notes

- The raw import excludes Python cache files and PID files.
- The raw import is reference material, not runtime wiring.
- Existing normalized Data Agents material remains in AgentCodex KB and policy docs.
- Future Data Agents updates can now be pulled into `.agentcodex/imports/data-agents/` through the same import command used for AgentSpec and ECC.
