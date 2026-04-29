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

- `kb/databricks/`
- `skills/databricks/databricks-spark-declarative-pipelines/`
- `skills/databricks/databricks-jobs/`
- `skills/databricks/databricks-bundles/`
- `skills/databricks/databricks-unity-catalog/`
- `skills/databricks/databricks-ai-functions/`
- `skills/databricks/databricks-agent-bricks/`
- `skills/databricks/databricks-vector-search/`
- `skills/databricks/databricks-model-serving/`
- `skills/databricks/databricks-mlflow-evaluation/`
- `skills/databricks/databricks-app-python/`
  - value: deeper Databricks operating knowledge for Unity Catalog, system tables, DABs, jobs, Lakeflow/SDP, AI Functions, Agent Bricks, Vector Search, Model Serving, MLflow Evaluation, and Databricks Apps
  - native result: enriched Databricks KB under `.agentcodex/kb/platforms/databricks/`

- `tools/fabric_health_check.py`
  - value: operational platform validation for Fabric auth and API reachability
  - native result: `agentcodex platform-health fabric`

- `kb/fabric/`
- `skills/fabric/`
  - value: Fabric-specific lakehouse, Direct Lake, RTI, Data Factory, deployment pipeline, Git integration, and cross-platform guidance
  - native result: `.agentcodex/kb/microsoft-fabric/fabric-data-agents-enrichment.md`

- `kb/data-quality/`
- `skills/patterns/data-quality/`
  - value: operational quality dimensions, profiling minimums, expectation placement, and SLA contract fields
  - native result: `.agentcodex/kb/data-quality/data-agents-quality-operations.md`

- `kb/governance/`
  - value: group-based access, PII classification, audit sources, compliance and lineage controls
  - native result: `.agentcodex/kb/controls/governance/data-agents-governance-controls.md` and `.agentcodex/kb/metadata/lineage/data-agents-lineage-patterns.md`

- `kb/semantic-modeling/`
- `skills/databricks/databricks-metric-views/`
  - value: semantic model rules, Direct Lake modeling concerns, DAX-style metric discipline, and Databricks Metric Views
  - native result: `.agentcodex/kb/data-modeling/concepts/semantic-modeling.md`

- `kb/migration/`
- `skills/migration/SKILL.md`
  - value: SQL Server/PostgreSQL migration phases, target selection, type-mapping concerns, and reconciliation checklist
  - native result: `.agentcodex/kb/lakehouse/patterns/relational-migration.md`

- `kb/spark-patterns/`
- `skills/patterns/spark-patterns/`
  - value: Spark operations, performance review, streaming review, and Delta review concerns
  - native result: `.agentcodex/kb/spark/patterns/data-agents-spark-operations.md`

- `kb/sql-patterns/`
- `skills/patterns/sql-generation/`
  - value: SQL generation guardrails, dialect checks, query grain, and production query discipline
  - native result: `.agentcodex/kb/sql-patterns/patterns/data-agents-sql-generation.md`

- `skills/databricks/databricks-vector-search/`
- `skills/databricks/databricks-model-serving/`
- `skills/databricks/databricks-mlflow-evaluation/`
  - value: Databricks RAG and serving building blocks across Vector Search, Model Serving, and MLflow evaluation
  - native result: `.agentcodex/kb/ai-data-engineering/patterns/databricks-rag-and-serving.md`

- `kb/task_routing.md`
  - value: KB-first task routing by task shape before specialist selection
  - native result: `.agentcodex/kb/orchestration/patterns/data-agents-kb-first-routing.md`

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

- split Databricks AI pages into narrower KB pages
  - value: richer implementation guidance for Vector Search, Model Serving, MLflow Evaluation, Agent Bricks, Lakebase, Zerobus, and Databricks Apps
  - native target: `.agentcodex/kb/platforms/databricks/concepts/` and `.agentcodex/kb/platforms/databricks/patterns/`

- split Fabric pages into narrower KB pages
  - value: detailed Fabric RTI, Direct Lake, Data Factory, deployment pipelines, Git integration, and monitoring guidance
  - native target: `.agentcodex/kb/microsoft-fabric/`

- split semantic modeling into platform-specific pages
  - value: separate Fabric/Power BI semantic model guidance from Databricks Metric Views and Genie/AI-BI surfaces
  - native target: `.agentcodex/kb/data-modeling/` plus platform KBs

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
