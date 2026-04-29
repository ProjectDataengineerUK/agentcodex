# AgentSpec Adherence Report - 2026-04-29

## Source Checked

- upstream repo: `https://github.com/luanmorenommaciel/agentspec`
- local checkout: `/home/user/Projetos/agentspec`
- branch: `main`
- latest verified commit: `67238c2 quality checks`
- notable current AgentSpec feature: `15b3723 feat: v3.2 - Judge Layer + --judge flag + Python hardening + Makefile (#13)`

The local AgentSpec checkout was fetched from `origin/main` and no newer commit was present beyond `67238c2`.

## Applied In This Pass

### Judge Layer V0

Ported AgentSpec's Judge Layer into AgentCodex as a Codex-native command and script.

Files added:

- `scripts/judge.py`
- `docs/commands/judge.md`
- `.agentcodex/commands/judge.md`
- `docs/JUDGE.md`
- `.agentcodex/tests/test_judge.py`

Files updated:

- `src/agentcodex_cli/dispatcher.py`
- `docs/COMMANDS.md`
- `scripts/check_bootstrapped_project.py`
- `docs/STATUS.md`

AgentCodex-specific adaptation:

- ledger path changed from `.claude/storage/judge-ledger.jsonl` to `.agentcodex/storage/judge-ledger.jsonl`
- command path is `python3 scripts/agentcodex.py judge ...`
- phase prompts support `generic`, `define`, `design`, and `build`
- command remains opt-in and advisory

## Validation

Commands run:

- `python3 scripts/validate_agentcodex.py`
- `python3 -m unittest discover -s .agentcodex/tests -p 'test_judge.py'`
- `python3 -m unittest discover -s .agentcodex/tests -p 'test_*.py'`
- `python3 scripts/agentcodex.py judge --ledger`
- `python3 scripts/agentcodex.py check-project .`

Results:

- validation passed
- judge unit tests passed
- full repo-local unittest suite passed: `47 tests`
- `judge --ledger` works without requiring an API key
- full project check passed

## Remaining AgentSpec Surfaces To Port

High priority:

- `/create-pr`: workflow closeout and PR creation procedure - ported in deep pass
- `/sql-review`: SQL-specific review surface using `sql-optimizer` - ported in deep pass
- `/lakehouse`: table format and catalog guidance using `lakehouse-architect` - ported in deep pass
- `/migrate`: legacy ETL migration procedure - ported in deep pass

Medium priority:

- `/readme-maker`: README generation procedure - ported in medium pass
- `/memory`: AgentSpec-style session insight capture, mapped to AgentCodex memory lifecycle - ported in medium pass
- AgentSpec `agent-router` skill parity against AgentCodex routing manifests - documented in medium pass

Visual explainer track:

- `/generate-web-diagram` - ported in visual pass
- `/generate-slides` - ported in visual pass
- `/generate-visual-plan` - ported in visual pass
- `/diff-review` - ported in visual pass
- `/plan-review` - ported in visual pass
- `/project-recap` - ported in visual pass
- `/fact-check` - ported in visual pass
- `/share` - ported in visual pass
- `visual-explainer` skill - retained as imported reference material
- `excalidraw-diagram` skill - retained as imported reference material

Import tooling gap:

- `scripts/import_upstreams.py` imports AgentSpec root scripts such as `scripts/judge.py` - fixed in import tooling pass
- `scripts/import_upstreams.py` imports plugin metadata under `plugin/.claude-plugin/` - fixed in import tooling pass
- partial import updates preserve existing ECC manifest entries when importing only AgentSpec - fixed in import tooling pass

## Recommended Next Pass

Close the remaining productization gap:

1. Optional CLI facades for high-value procedure-only commands if documentation is not enough.
2. Fresh simulated install from packaged plugin, then create a new project from zero.

## Deep Pass - High Priority Commands

Completed after the first Judge Layer pass:

- `docs/commands/sql-review.md`
- `.agentcodex/commands/sql-review.md`
- `docs/commands/lakehouse.md`
- `.agentcodex/commands/lakehouse.md`
- `docs/commands/migrate.md`
- `.agentcodex/commands/migrate.md`
- `docs/commands/create-pr.md`
- `.agentcodex/commands/create-pr.md`

AgentCodex-specific strengthening:

- `sql-review` requires dialect/runtime classification, grain and join checks, PII review, dbt checks, evidence-based findings, and concrete fixes.
- `lakehouse` requires workload/platform classification, table-format tradeoffs, catalog/governance model, maintenance policy, rollback, and validation checks.
- `migrate` requires legacy behavior inventory, target-stack justification, source-to-target mapping, parity validation, cutover, and rollback.
- `create-pr` is intentionally non-mutating until explicit user approval; it drafts branch, commit, PR body, tests, and risk evidence before running git/GitHub write commands.

Files updated:

- `docs/COMMANDS.md`
- `scripts/check_bootstrapped_project.py`
- `docs/STATUS.md`

Validation after deep pass:

- `python3 scripts/validate_agentcodex.py`
- `python3 scripts/agentcodex.py check-project .`

## Medium Pass - Core AgentSpec Surfaces

Completed after the high-priority command pass:

- `docs/commands/readme-maker.md`
- `.agentcodex/commands/readme-maker.md`
- `docs/commands/memory.md`
- `.agentcodex/commands/memory.md`
- `docs/AGENT-ROUTER.md`

AgentCodex-specific adaptation:

- `readme-maker` is a Codex-native evidence-first README procedure using `code-documenter`, `codebase-explorer`, and `reviewer`.
- `memory` maps AgentSpec's `.claude/storage/` behavior to the existing AgentCodex repo-local memory lifecycle under `.agentcodex/memory/` and `.agentcodex/reports/memory/`.
- `agent-router` parity is documented against `.agentcodex/routing/routing.json` instead of loading a Claude skill or `${CLAUDE_PLUGIN_ROOT}` runtime path.
- `scripts/check_bootstrapped_project.py` now treats `memory.md` and `readme-maker.md` as required full-mode command procedures.
- `scripts/package_plugin.py` now excludes Python cache files from packaged plugin archives.

Files updated:

- `docs/COMMANDS.md`
- `docs/STATUS.md`
- `scripts/check_bootstrapped_project.py`
- `scripts/package_plugin.py`
- `plugins/agentcodex/runtime/agentcodex-runtime/`
- `dist/plugins/agentcodex-plugin-0.1.0.tar.gz`

Validation after medium pass:

- `python3 scripts/validate_agentcodex.py`
- `python3 -m unittest discover -s .agentcodex/tests -p 'test_*.py'`
- `python3 scripts/agentcodex.py check-project .`
- `python3 scripts/agentcodex.py validate-plugin`
- `PYTHONPATH=src python3 -m agentcodex_cli.cli help`

## Import Tooling Pass

Completed after the medium-priority command pass:

- `scripts/import_upstreams.py` now imports AgentSpec `scripts/` into `.agentcodex/imports/agentspec/scripts/`.
- `scripts/import_upstreams.py` now imports AgentSpec `plugin/.claude-plugin/` into `.agentcodex/imports/agentspec/plugin_metadata/`.
- partial imports preserve existing manifest entries for sources that were not refreshed.
- `.agentcodex/tests/test_import_upstreams.py` covers the new mapping and manifest-preservation behavior.

Verification:

- `python3 scripts/import_upstreams.py agentspec`
- `python3 scripts/agentcodex.py generate-import-catalog`
- `python3 scripts/validate_agentcodex.py`
- `python3 -m unittest discover -s .agentcodex/tests -p 'test_*.py'` passed with `50 tests`
- `python3 scripts/agentcodex.py check-project .`

## Visual Explainer Pass

Completed after the import tooling pass:

- `docs/commands/generate-web-diagram.md`
- `.agentcodex/commands/generate-web-diagram.md`
- `docs/commands/generate-visual-plan.md`
- `.agentcodex/commands/generate-visual-plan.md`
- `docs/commands/generate-slides.md`
- `.agentcodex/commands/generate-slides.md`
- `docs/commands/diff-review.md`
- `.agentcodex/commands/diff-review.md`
- `docs/commands/plan-review.md`
- `.agentcodex/commands/plan-review.md`
- `docs/commands/project-recap.md`
- `.agentcodex/commands/project-recap.md`
- `docs/commands/fact-check.md`
- `.agentcodex/commands/fact-check.md`
- `docs/commands/share.md`
- `.agentcodex/commands/share.md`

AgentCodex-specific adaptation:

- visual outputs default to repo-local `.agentcodex/reports/visual/` instead of user-global `~/.agent/diagrams/`
- each visual command requires a verified fact sheet before presenting claims
- `share` is explicit-approval-only for public upload/deployment and includes sensitivity review
- visual/excalidraw skills remain imported reference material, not Claude runtime assumptions
- `scripts/check_bootstrapped_project.py` now treats the visual procedures as required full-mode command procedures

Validation after visual pass:

- `python3 scripts/validate_agentcodex.py`
- `python3 -m unittest discover -s .agentcodex/tests -p 'test_*.py'` passed with `50 tests`
- `python3 scripts/agentcodex.py check-project .`
- `python3 scripts/agentcodex.py validate-plugin`
- packaged plugin archive regenerated without `__pycache__` or `.pyc` entries
