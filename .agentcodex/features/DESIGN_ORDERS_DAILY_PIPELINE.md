# DESIGN_ORDERS_DAILY_PIPELINE

## Metadata

- feature: `ORDERS_DAILY_PIPELINE`
- phase: `design`
- status: `example`
- owner: `agentcodex`
- updated_at: `2026-04-22`

## Architecture Overview

Use an Airflow DAG to orchestrate ingestion and dbt transformations. Raw orders are landed into the warehouse staging area and transformed into marts through dbt.

## System or Data Flow

Source database -> ingestion task -> raw landing table -> dbt staging model -> dbt mart models -> quality checks -> publish

## File Manifest

```text
- path: dags/orders_daily.py
  purpose: orchestrate the daily orders pipeline
  depends_on: jobs/load_orders.py, dbt project assets
  role: pipeline-architect

- path: jobs/load_orders.py
  purpose: extract orders from source and land raw data
  depends_on: config/settings.py
  role: spark-engineer

- path: models/staging/stg_orders.sql
  purpose: normalize raw orders into staging semantics
  depends_on: raw.orders
  role: dbt-specialist

- path: models/marts/fct_orders.sql
  purpose: publish analytics-ready orders fact model
  depends_on: models/staging/stg_orders.sql
  role: dbt-specialist

- path: tests/data/orders_quality.yml
  purpose: define quality checks for freshness and key integrity
  depends_on: models/marts/fct_orders.sql
  role: data-quality-analyst
```

## Interfaces and Dependencies

- interface: source orders extract contract
- dependency: Airflow runtime
- dependency: warehouse and dbt runtime

## Implementation Strategy

- step 1: define orchestration boundary and scheduling
- step 2: implement ingestion path
- step 3: implement dbt transformations
- step 4: add quality checks

## Test Strategy

- lint: Python lint and SQL lint where applicable
- typecheck: Python type checks if codebase uses them
- unit/integration: DAG load validation and dbt model validation
- domain-specific checks: freshness and key integrity checks

## Risks

- late-arriving-order policy may force redesign of incremental logic
- source extract reliability is not yet validated

## Open Decisions

- exact incremental watermark strategy

## Exit Check

- [x] manifest is complete
- [x] test strategy is explicit
- [x] risks are called out
- [x] role assignments exist where specialization matters
