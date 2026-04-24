# Data Agents Port Inventory

## Purpose

Short triage of what from `/home/user/Projetos/data-agents` is worth porting into AgentCodex.

## Ported

- `hooks/context_budget_hook.py`
  - value: strengthens local context-budget semantics already aligned with `context-optimizer`
  - native result: `agentcodex session-controls`

- `hooks/cost_guard_hook.py`
  - value: useful cost-tier heuristics for Databricks/Fabric operations
  - native result: `agentcodex session-controls`

- `tools/databricks_health_check.py`
  - value: operational platform validation for Databricks credentials and workspace reachability
  - native result: `agentcodex platform-health databricks`

- `tools/fabric_health_check.py`
  - value: operational platform validation for Fabric auth and API reachability
  - native result: `agentcodex platform-health fabric`

- `memory/decay.py`
- `memory/lint.py`
- parts of `memory/types.py`
- parts of `memory/extractor.py`
  - value: enriches memory lifecycle with decay, linting, extraction, and reviewable candidates
  - native result: `memory-lint`, `memory-extract`, `memory-review-candidates`, `memory-approve-candidates`

- `templates/pipeline-spec.md`
- `templates/star-schema-spec.md`
- `templates/cross-platform-spec.md`
- `templates/backlog.md`
  - value: useful enterprise data templates
  - native result: Codex-first templates under `.agentcodex/templates/`

- `kb/constitution.md`
- `kb/collaboration-workflows.md`
  - value: policy and workflow ideas
  - native result: `docs/policies/CONSTITUTION.md` and `docs/policies/WORKFLOW-ORCHESTRATION.md`

- `hooks/audit_hook.py`
- parts of `hooks/workflow_tracker.py`
  - value: compact audit and workflow visibility patterns
  - native result: `agentcodex audit-summary` and repo-local policy/workflow docs

## Port Next

- `memory/store.py`
- `memory/retrieval.py`
- `memory/compiler.py`
  - value: enriches memory lifecycle with consolidation/compilation after candidate approval
  - native target: the current AgentCodex memory subsystem behind the backend boundary

- richer platform/run audit classification
  - value: deeper platform-aware observability
  - native target: `audit-summary` and observability metrics

## Reference Only

- `config/logging_config.py`
- `config/mcp_servers.py`
- `config/snapshot.py`
  - value: reference for local config patterns

## Do Not Port Directly

- `.claude/CLAUDE.md`
- `main.py`
- `ui/*`
- `chainlit.md`
- `.chainlit/*`
- `agents/supervisor.py`
- `agents/*` tied to Claude Agent SDK orchestration

Reason:

- these are runtime-coupled to Claude SDK and UI surfaces that conflict with the Codex-first, `AGENTS.md`-first model of AgentCodex

## Current Decision

The best reuse path is:

1. keep porting repo-local operational patterns and policies
2. deepen memory only where it strengthens the current backend-boundary model
3. selectively enrich audit/guardrails and enterprise templates
4. continue avoiding Claude runtime wiring
