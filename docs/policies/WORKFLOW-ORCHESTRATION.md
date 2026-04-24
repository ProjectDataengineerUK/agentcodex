# Workflow Orchestration

## Purpose

Define when AgentCodex should use a simple delegation versus a multi-step workflow with explicit handoff points.

## Delegation vs Workflow

| Mode | Use When | Requirement |
|------|----------|-------------|
| Simple Delegation | single-domain task with bounded output | no formal spec required |
| Workflow | multi-step, cross-domain, or cross-platform task | spec/template required |

## Workflow Rules

| ID | Rule |
|----|------|
| W1 | Use a template/spec before running a multi-step workflow. |
| W2 | Keep handoffs explicit and deterministic. |
| W3 | Preserve outputs of each major step in repo-local artifacts when the work is substantial. |
| W4 | Pause on failed prerequisite steps instead of blindly continuing. |
| W5 | Parallelize only steps that do not block each other. |

## Recommended Workflow Patterns

### WF-PIPELINE

Use for end-to-end data pipeline work.

Suggested flow:

1. `pipeline-architect`
2. `spark-engineer` or `dbt-specialist`
3. `data-quality-analyst`
4. `data-governance-architect` or `schema-governance-engineer`

Template:

- `.agentcodex/templates/data-pipeline-spec.md`

### WF-STAR-SCHEMA

Use for Gold-layer star schema work.

Suggested flow:

1. `schema-designer`
2. `sql-optimizer`
3. `data-quality-analyst`
4. semantic/modeling specialist if needed

Template:

- `.agentcodex/templates/star-schema-overview.md`

### WF-CROSS-PLATFORM

Use for Databricks/Fabric/Snowflake migration or interoperability work.

Suggested flow:

1. `data-platform-engineer`
2. platform-specific architect
3. governance/security specialist
4. observability specialist if runtime controls matter

Template:

- `.agentcodex/templates/cross-platform-operation.md`

### WF-BACKLOG-TO-DEFINE

Use for turning meeting/briefing material into an implementation-ready backlog.

Suggested flow:

1. `meeting-analyst`
2. `workflow-definer`
3. `planner`

Template:

- `.agentcodex/templates/business-backlog.md`

## Audit Expectations

- major workflows should update `.agentcodex/history/`
- health and control signals should be recoverable from repo-local reports
- command procedures should exist when a workflow becomes recurring

## Local Notes

- This document was informed by `collaboration-workflows.md` from `/home/user/Projetos/data-agents`, but normalized to AgentCodex roles and templates.
