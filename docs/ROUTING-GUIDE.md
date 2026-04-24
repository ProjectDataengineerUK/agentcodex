# Routing Guide

## Purpose

This document is the Codex-native replacement for AgentSpec's Claude-oriented `agent-router`.

It tells AgentCodex which role to prefer based on task shape, workflow phase, and domain.

## Primary Routing Rules

### Workflow Phase Routing

| Situation | Preferred Role |
|---|---|
| idea is vague, options need comparison | `workflow-brainstormer` |
| requirements are unclear or incomplete | `workflow-definer` |
| architecture or file manifest is needed | `workflow-designer` |
| implementation should start from a defined design | `workflow-builder` |
| evidence gathering before changes | `explorer` |
| final bug/risk/test review | `reviewer` |

### Data Engineering Routing

| Task Shape | Preferred Role |
|---|---|
| feature planning, implementation sequencing, phased refactors | `planner` |
| meeting notes, transcript synthesis, discussion consolidation | `meeting-analyst` |
| KB creation, KB audit, knowledge organization | `kb-architect` |
| repo exploration, onboarding, architecture walkthrough | `codebase-explorer` |
| explicit code review and regression inspection | `code-reviewer` |
| security-focused review and vulnerability inspection | `security-reviewer` |
| build failure, type error, compiler or config breakage | `build-error-resolver` |
| high-level system architecture and technical trade-offs | `architect` |
| feature implementation architecture and file blueprinting | `code-architect` |
| context reduction, token budget, response depth, long-session recovery | `context-optimizer` |
| dead code cleanup and post-refactor consolidation | `refactor-cleaner` |
| documentation refresh and codemap maintenance | `doc-updater` |
| library docs lookup and current API reference questions | `docs-lookup` |
| code documentation, API docs, docstrings, README authoring | `code-documenter` |
| test-first workflow and verification-led implementation | `tdd-guide` |
| test generation and coverage expansion after implementation | `test-generator` |
| PR test coverage review and behavioral test-gap analysis | `pr-test-analyzer` |
| Python implementation for typed modules and utilities | `python-developer` |
| lightweight prompt or mini-spec generation for quick tasks | `prompt-crafter` |
| prompt optimization and structured LLM output implementation | `llm-specialist` |
| performance bottlenecks and runtime optimization | `performance-optimizer` |
| silent fallbacks, swallowed errors, and hidden failure modes | `silent-failure-hunter` |
| orchestration, DAGs, task dependencies | `pipeline-architect` |
| multi-agent AI systems, RAG architecture, memory, guardrails | `genai-architect` |
| memory architecture, semantic/episodic/procedural memory design | `memory-architect` |
| memory retention, access policy, ownership, sensitivity, audit rules | `memory-governance-engineer` |
| memory telemetry, tracing, hit rate, backend failures, access denials | `memory-observability-engineer` |
| production Sentinel supervision, quarantine policy, approval boundaries | `sentinel-supervisor` |
| runtime watcher design across compute, environments, pipelines, and functionality | `sentinel-runtime-watcher` |
| security watcher design, suspicious access monitoring, security quarantine triggers | `sentinel-security-watcher` |
| diagnosis from watcher outputs, anomaly chains, trend regression, diff analysis | `sentinel-analyzer` |
| production incident interpretation, recommended actions, severity/confidence reporting | `sentinel-interpreter` |
| cross-platform data platform strategy and platform comparison | `data-platform-engineer` |
| star schema, dimensional modeling, grain | `schema-designer` |
| dbt models, tests, macros, incremental logic | `dbt-specialist` |
| Spark jobs, partitioning, distributed transforms | `spark-engineer` |
| validation rules, expectations, trust checks | `data-quality-analyst` |
| uncertain DE choice requiring local domain validation | `domain-researcher` |

## Secondary Routing Rules

### Use `explorer` when

- current codebase behavior is unclear
- file ownership is unclear
- dependency impact must be traced
- a migration may affect multiple modules

### Use `reviewer` when

- implementation is done and risks need inspection
- a plan may introduce regressions
- testing is weak or missing
- a migration could silently break behavior

### Use `domain-researcher` when

- a data-engineering decision needs evidence
- the team is choosing between two platform patterns
- local domain docs should be checked before implementation

## Domain And Control Routing

| Domain or Control | Preferred Role | Explore First | Review With | Research With |
|---|---|---|---|---|
| `governance` | `data-governance-architect` | `explorer` | `reviewer` | `domain-researcher` |
| `lineage` | `lineage-analyst` | `explorer` | `reviewer` | `domain-researcher` |
| `observability` | `data-observability-engineer` | `explorer` | `reviewer` | `domain-researcher` |
| `sentinel` | `sentinel-supervisor` | `explorer` | `reviewer` | `domain-researcher` |
| `access-control` | `platform-access-engineer` | `explorer` | `security-reviewer` | `domain-researcher` |
| `data-contracts` | `schema-governance-engineer` | `explorer` | `reviewer` | `domain-researcher` |
| `mcp` | `docs-lookup` | `explorer` | `reviewer` | `domain-researcher` |
| `memory` | `memory-architect` | `explorer` | `reviewer` | `domain-researcher` |

## Platform Routing

| Platform | Preferred Role | Explore First | Review With | Research With |
|---|---|---|---|---|
| `azure` | `azure-ai-architect` | `explorer` | `reviewer` | `domain-researcher` |
| `databricks` | `databricks-architect` | `explorer` | `reviewer` | `domain-researcher` |
| `snowflake` | `snowflake-architect` | `explorer` | `reviewer` | `domain-researcher` |

## Control Routing

| Control | Preferred Role | Explore First | Review With | Research With |
|---|---|---|---|---|
| `governance` | `data-governance-architect` | `explorer` | `reviewer` | `domain-researcher` |
| `lineage` | `lineage-analyst` | `explorer` | `reviewer` | `domain-researcher` |
| `observability` | `data-observability-engineer` | `explorer` | `reviewer` | `domain-researcher` |
| `access-control` | `platform-access-engineer` | `explorer` | `security-reviewer` | `domain-researcher` |
| `data-contracts` | `schema-governance-engineer` | `explorer` | `reviewer` | `domain-researcher` |
| `memory-governance` | `memory-governance-engineer` | `explorer` | `reviewer` | `domain-researcher` |
| `memory-observability` | `memory-observability-engineer` | `explorer` | `reviewer` | `domain-researcher` |
| `sentinel-supervision` | `sentinel-supervisor` | `explorer` | `reviewer` | `domain-researcher` |
| `sentinel-security` | `sentinel-security-watcher` | `explorer` | `security-reviewer` | `domain-researcher` |

## Escalation Rules

### Workflow Escalations

- `workflow-builder` escalates to `workflow-designer` when the design is incomplete.
- `workflow-designer` escalates to `workflow-definer` when requirements are too vague.
- `workflow-definer` escalates to `workflow-brainstormer` when the problem framing is still unstable.

### Domain Escalations

- `dbt-specialist` escalates to `schema-designer` when the data model itself is unclear.
- `meeting-analyst` escalates to `planner` or workflow roles when discussion must become an implementation plan.
- `kb-architect` escalates to `domain-researcher` or the relevant specialist when structure is clear but content accuracy is domain-sensitive.
- `codebase-explorer` escalates to `planner` or specialists once exploration turns into design or implementation.
- `security-reviewer` escalates to `code-reviewer` or `reviewer` when the dominant issue is broader quality rather than security.
- `build-error-resolver` escalates to `planner` or `refactor-cleaner` when the smallest viable fix is no longer small.
- `architect` escalates to `planner` or workflow design roles when system architecture depends on unresolved scope.
- `code-architect` escalates to `planner` or workflow design roles when implementation structure depends on unresolved scope.
- `context-optimizer` escalates to `workflow-iterator` or `planner` when token reduction depends on better workflow structure rather than shorter answers.
- `refactor-cleaner` escalates to `planner` when cleanup turns into architecture change.
- `docs-lookup` escalates to specialists after the current-library facts are gathered.
- `code-documenter` escalates to `doc-updater` or `codebase-explorer` when documentation needs broader repository context.
- `tdd-guide` escalates to workflow roles when scope is not clear enough to support test-first work.
- `test-generator` escalates to `tdd-guide` or domain specialists when test generation exposes missing requirements or weak contracts.
- `pr-test-analyzer` escalates to `test-generator` or `tdd-guide` when the next step is creating tests instead of reviewing them.
- `python-developer` escalates to specialists when the dominant issue is domain-specific rather than generic Python implementation.
- `prompt-crafter` escalates to `workflow-definer`, `planner`, or `genai-architect` when a quick prompt is not enough.
- `llm-specialist` escalates to `genai-architect` when the issue is system architecture rather than prompt implementation.
- `performance-optimizer` escalates to `code-architect` or `planner` when optimization requires structural redesign.
- `silent-failure-hunter` escalates to `code-reviewer` or `security-reviewer` depending on the dominant failure mode.
- `data-platform-engineer` escalates to `lakehouse-architect` or cloud specialists when platform strategy becomes implementation-specific.
- `genai-architect` escalates to `ai-data-engineer` when retrieval-data design dominates the problem.
- `spark-engineer` escalates to `pipeline-architect` when orchestration dominates the problem.
- `pipeline-architect` escalates to `data-quality-analyst` when quality gates are the main unresolved risk.

## File Pattern Hints

These hints are advisory:

| Pattern | Preferred Role |
|---|---|
| `.agentcodex/kb/**/*` | `kb-architect` |
| `.agentcodex/memory/**/*` | `memory-architect` |
| `.agentcodex/cache/memory/**/*` | `memory-observability-engineer` |
| `.agentcodex/reports/memory/**/*` | `memory-observability-engineer` |
| `.agentcodex/history/**/*` | `context-optimizer` |
| `*.py` | `python-developer` |
| `package.json` | `build-error-resolver` |
| `docs/**/*.md` | `doc-updater` |
| `README.md` | `code-documenter` |
| `src/**/*` | `code-architect` |
| `tests/**/*` | `test-generator` |
| `models/**/*.sql` | `dbt-specialist` |
| `agents/**/*` | `genai-architect` |
| `dags/**/*.py` | `pipeline-architect` |
| `jobs/**/*.py` | `spark-engineer` |
| `notes/**/*` | `meeting-analyst` |
| `prompts/**/*` | `llm-specialist` |
| `schemas/**/*` | `schema-designer` |
| `tests/data/**/*` | `data-quality-analyst` |
| `tsconfig*.json` | `build-error-resolver` |
| `transcripts/**/*` | `meeting-analyst` |
| `.agentcodex/kb/platforms/snowflake/**/*` | `snowflake-architect` |

## Routing Philosophy

1. Route by the dominant problem, not by file extension alone.
2. Use `explorer` before specialist execution when the codebase context is weak.
3. Use `reviewer` after meaningful implementation or migration.
4. Use `domain-researcher` when local domain guidance should decide the path.
