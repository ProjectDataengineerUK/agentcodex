# CONTEXT_ORDERS_DAILY_PIPELINE

## Metadata

- scope: `ORDERS_DAILY_PIPELINE`
- kind: `feature`
- owner: `agentcodex`
- updated_at: `2026-04-23`

## Scope

Synchronized context for feature `ORDERS_DAILY_PIPELINE` based on current AgentCodex workflow artifacts.

## Current State

- implementation state: current artifact phase is `build`
- current phase summary: Use an Airflow DAG to orchestrate ingestion and dbt transformations. Raw orders are landed into the warehouse staging area and transformed into marts through dbt.
- known stable artifacts: `.agentcodex/features/BRAINSTORM_ORDERS_DAILY_PIPELINE.md`, `.agentcodex/features/DEFINE_ORDERS_DAILY_PIPELINE.md`, `.agentcodex/features/DESIGN_ORDERS_DAILY_PIPELINE.md`, `.agentcodex/reports/BUILD_REPORT_ORDERS_DAILY_PIPELINE.md`

## Decisions

- decision: Use an Airflow DAG to orchestrate ingestion and dbt transformations. Raw orders are landed into the warehouse staging area and transformed into marts through dbt.
- rationale: unresolved design decision remains: exact incremental watermark strategy

## Changed Artifacts

- path: `.agentcodex/features/BRAINSTORM_ORDERS_DAILY_PIPELINE.md`
- path: `.agentcodex/features/DEFINE_ORDERS_DAILY_PIPELINE.md`
- path: `.agentcodex/features/DESIGN_ORDERS_DAILY_PIPELINE.md`
- path: `.agentcodex/reports/BUILD_REPORT_ORDERS_DAILY_PIPELINE.md`
- path: `dags/orders_daily.py`
- path: `jobs/load_orders.py`
- path: `models/staging/stg_orders.sql`
- path: `models/marts/fct_orders.sql`
- path: `tests/data/orders_quality.yml`
- command: see verification commands captured in build artifacts

## Open Gaps

- gap: confirm warehouse target and naming standards
- gap: define late-arriving-order policy
- blocker: exact incremental watermark strategy
- assumption: incremental watermark behavior still needs implementation detail

## Next Recommended Step

- next owner: workflow-shipper
- next phase: ship
- next concrete action: review acceptance, residual risks, and publish a shipped artifact when ready

## Resume Prompt

Continue from `.agentcodex/history/CONTEXT_ORDERS_DAILY_PIPELINE_2026-04-23.md` and reconcile it with the latest project artifacts.
