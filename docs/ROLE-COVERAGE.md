# Role Coverage

Status date: 2026-04-29

## Purpose

Track how the active AgentCodex role surface compares with the raw imported AgentSpec and ECC agent surfaces.

This file separates exact filename coverage from semantic coverage. Exact coverage is useful for auditing imported upstream files. Semantic coverage is useful for deciding whether AgentCodex really needs a new active role.

## Exact Coverage Snapshot

This snapshot uses raw filename stems.

- active AgentCodex roles in `docs/roles/`: 123
- imported AgentSpec files under `.agentcodex/imports/agentspec/agents/`: 60
- imported ECC agents under `.agentcodex/imports/ecc/agents/`: 48
- gross imported AgentSpec + ECC files: 108
- unique imported filename stems: 107
- exact upstream stems already active in AgentCodex: 96
- exact upstream stems not active in AgentCodex: 11
- AgentCodex-native role stems beyond exact upstream matches: 27

Notes:

- The AgentSpec count of 60 includes `README.md` and `_template.md`.
- If those two reference files are excluded, AgentSpec has 58 runnable agent documents, the gross imported runnable-agent count is 106, and the unique imported runnable-agent count is 105.
- Exact coverage intentionally does not treat `brainstorm-agent` and `workflow-brainstormer` as the same role.

## Semantic Coverage Snapshot

This snapshot recognizes current AgentCodex aliases and normalized ports.

- normalized upstream represented by active AgentCodex roles: 105
- normalized upstream still not represented as active roles: 0
- AgentCodex-native roles beyond normalized upstream matches: 21

Current normalized aliases:

- `brainstorm-agent` -> `workflow-brainstormer`
- `define-agent` -> `workflow-definer`
- `design-agent` -> `workflow-designer`
- `build-agent` -> `workflow-builder`
- `ship-agent` -> `workflow-shipper`
- `iterate-agent` -> `workflow-iterator`
- `the-planner` -> `planner`
- `code-explorer` -> `codebase-explorer`
- `code-cleaner` -> `refactor-cleaner`

## Exact Upstream Stems Not Active

These upstream filename stems do not have an exact same-named active role in `docs/roles/`. They are not duplicated because they are either reference files or normalized aliases already covered by an AgentCodex-native role name.

- `README`
- `_template`
- `brainstorm-agent`
- `build-agent`
- `code-cleaner`
- `code-explorer`
- `define-agent`
- `design-agent`
- `iterate-agent`
- `ship-agent`
- `the-planner`

## Current Decision

All runnable upstream AgentSpec and ECC agents are now represented as active AgentCodex roles without duplicating normalized aliases.

Do not add exact duplicate roles for the alias list above unless AgentCodex intentionally introduces an upstream-compatibility naming layer.

## AgentCodex-Native Roles

These active roles remain AgentCodex-specific or normalized ports beyond exact upstream filename matches.

- `azure-ai-architect`
- `context-optimizer`
- `data-governance-architect`
- `data-observability-engineer`
- `data-security-architect`
- `databricks-architect`
- `lineage-analyst`
- `memory-architect`
- `memory-governance-engineer`
- `memory-observability-engineer`
- `metadata-platform-engineer`
- `mosaic-ai-engineer`
- `platform-access-engineer`
- `schema-governance-engineer`
- `sentinel-analyzer`
- `sentinel-interpreter`
- `sentinel-runtime-watcher`
- `sentinel-security-watcher`
- `sentinel-supervisor`
- `snowflake-architect`
- `terraform-specialist`
- `workflow-brainstormer`
- `workflow-builder`
- `workflow-definer`
- `workflow-designer`
- `workflow-iterator`
- `workflow-shipper`

## Validation

After role-surface changes, run:

```bash
python3 scripts/generate_roles_manifest.py
python3 scripts/generate_routing_manifest.py
python3 scripts/generate_status_doc.py
python3 scripts/validate_agentcodex.py
python3 scripts/agentcodex.py check-project .
python3 -m unittest discover -s .agentcodex/tests -p 'test_*.py'
```
