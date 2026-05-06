# Project Structure

AgentCodex had started to accumulate too many different concerns under `.agentcodex/` without one explicit taxonomy. This document is the canonical structure map.

## Top-Level Model

Use these categories, not just raw folders:

1. Control plane
2. Project runtime
3. Knowledge and routing
4. Bootstrap and distribution
5. Source reference

## 1. Control Plane

These directories hold resumable operational state, not project design content:

- `.agentcodex/reports/`
- `.agentcodex/history/`
- `.agentcodex/archive/`
- `.agentcodex/workflows/`
- `.agentcodex/state/`
- `.agentcodex/observability/`
- `.agentcodex/memory/`

Rule:
- if the artifact answers "what happened", "what is current", or "what was approved", it belongs here

## 2. Project Runtime

These directories define how a target project is executed or scaffolded:

- `.agentcodex/features/`
- `.agentcodex/ops/`
- `.agentcodex/commands/`
- `.agentcodex/templates/`

Rule:
- if the artifact is project-owned and expected to be edited as part of delivery, it belongs here

### Feature Content

Within `.agentcodex/features/<feature>/`, keep delivery artifacts inside the project-standard blocks:

- `definition/`
- `design/`
- `data/`
- `controls/`
- `metadata/`
- `execution/`
- `validation/`
- `operations/`
- `security/`
- `contracts/`
- `deploy/`
- `compliance/`
- `agents/`
- `kb/`

Rule:
- feature folders are for project delivery
- root `.agentcodex/` folders are for framework and control-plane surfaces

## 3. Knowledge And Routing

These directories are reusable framework intelligence, not feature-specific delivery state:

- `.agentcodex/kb/`
- `.agentcodex/routing/`
- `.agentcodex/roles/`
- `.agentcodex/registry/`
- `.agentcodex/maturity/`

Rule:
- if it teaches AgentCodex how to think or route, keep it here

## 4. Bootstrap And Distribution

These directories exist to install, package, or bootstrap AgentCodex itself:

- `.agentcodex/bootstrap/`
- `.codex/`
- `plugins/agentcodex/`
- `src/agentcodex_cli/`
- `scripts/`

Rule:
- do not confuse these with target-project delivery artifacts

## 5. Source Reference

These directories are upstream or derived reference layers:

- `.agentcodex/imports/`
- `.agentcodex/cache/`

Rule:
- imports are preserved source material
- cache is generated support material
- neither should be treated as active project delivery state

## Databricks Placement

Databricks was one of the places where this structure was least clear.

Use this split:

- reusable Databricks knowledge: `.agentcodex/kb/platforms/databricks/`
- Databricks operating overlays and profiles: `.agentcodex/ops/`
- target-project Databricks design and execution artifacts: `.agentcodex/features/<feature>/design/`, `execution/`, `security/`, `operations/`, `deploy/`
- Databricks runtime reports and readiness checks: `.agentcodex/reports/`
- Databricks imported source material: `.agentcodex/imports/data-agents/` and `.agentcodex/imports/agentspec/`

Do not mix:

- Databricks KB pages with project runtime manifests
- workspace failure reports with design artifacts
- imported upstream examples with project-owned delivery files

## Command

Use:

```bash
python3 scripts/agentcodex.py project-structure
```

This writes `.agentcodex/reports/project-structure.md` and summarizes the current layout by category.
