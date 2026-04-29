# AgentSpec Adherence Rerun - 2026-04-29

## Scope

Re-run AgentCodex adherence against the local AgentSpec checkout and the refreshed raw imports.

AgentSpec source checked:

- local checkout: `/home/user/Projetos/agentspec`
- git status: clean
- latest local commit: `67238c2 quality checks`

AgentCodex source checked:

- active command procedures: `docs/commands/`
- project-local command procedures: `.agentcodex/commands/`
- active roles: `docs/roles/`
- routing: `.agentcodex/routing/routing.json`
- raw AgentSpec imports: `.agentcodex/imports/agentspec/`

## Import Refresh

Commands run:

- `python3 scripts/import_upstreams.py agentspec`
- `python3 scripts/agentcodex.py generate-import-catalog`

Result:

- AgentSpec import refreshed with `933` files.
- Manifest preserved both source entries: `agentspec` and `ecc`.
- AgentSpec root scripts are now imported under `.agentcodex/imports/agentspec/scripts/`.
- AgentSpec plugin metadata is now imported under `.agentcodex/imports/agentspec/plugin_metadata/`.

## Command Coverage

AgentSpec command procedures found, excluding README files: `30`

AgentCodex active command procedures found: `37`

Coverage: `30/30`

Missing AgentSpec command procedures: none.

AgentCodex extra procedures beyond AgentSpec:

- `audit-summary`
- `judge`
- `memory-candidates`
- `orchestrate-workflow`
- `platform-health`
- `project-intake`
- `session-controls`

These are AgentCodex product additions, not adherence gaps.

## New Fix From This Rerun

The rerun found one remaining command-surface gap:

- AgentSpec had `/status`
- AgentCodex had executable `agentcodex status`
- AgentCodex did not yet have `docs/commands/status.md` or `.agentcodex/commands/status.md`

Applied fix:

- added `docs/commands/status.md`
- added `.agentcodex/commands/status.md`
- added `status.md` to `docs/COMMANDS.md`
- added `status.md` to `scripts/check_bootstrapped_project.py` required full-mode command procedures
- regenerated `docs/STATUS.md`
- rebuilt plugin runtime

## Role And Skill Coverage

AgentSpec imported agent docs: `60`

AgentCodex active role docs: `66`

Assessment:

- AgentCodex has at least equivalent role breadth by count.
- Some AgentSpec runtime skills are represented as Codex-native docs/manifests instead of loaded Claude skills.
- `agent-router` parity is documented through `docs/AGENT-ROUTER.md` and `.agentcodex/routing/routing.json`.
- `visual-explainer` and `excalidraw-diagram` remain imported reference material; visual command procedures are active under `docs/commands/`.

## Script And Plugin Metadata Coverage

AgentSpec imported scripts:

- `.agentcodex/imports/agentspec/scripts/generate-agent-router.py`
- `.agentcodex/imports/agentspec/scripts/judge.py`

AgentSpec imported plugin metadata:

- `.agentcodex/imports/agentspec/plugin_metadata/plugin.json`
- `.agentcodex/imports/agentspec/plugin_metadata/marketplace.json`

Assessment:

- The previous import tooling gap is closed.
- AgentCodex keeps these as raw upstream evidence and implements Codex-native equivalents where appropriate.

## Residual Differences

Intentional differences:

- AgentCodex uses `AGENTS.md`, `.codex/`, `docs/commands/`, and `.agentcodex/` instead of Claude plugin runtime paths.
- AgentCodex does not assume slash commands exist.
- AgentCodex visual outputs default to repo-local `.agentcodex/reports/visual/`, not `~/.agent/diagrams/`.
- `share` requires explicit approval before public upload/deployment.
- `memory` maps AgentSpec `.claude/storage/` behavior to AgentCodex memory lifecycle.

Product follow-up, not an adherence blocker:

- decide whether selected procedure-only commands need executable CLI facades
- run a fresh simulated plugin install and create a new project from zero
- optionally build native visual-generation templates/scripts if static procedures are not enough

## Validation

Commands run after this report:

- `python3 scripts/validate_agentcodex.py`
- `python3 -m unittest discover -s .agentcodex/tests -p 'test_*.py'`
- `python3 scripts/agentcodex.py check-project .`
- `python3 scripts/agentcodex.py validate-plugin`
- `python3 scripts/package_plugin.py`

Result:

- validation passes
- unit tests pass: `50 tests`
- project check passes
- plugin manifest passes
- package archive does not include Python cache files
- final command coverage remains `30/30`
