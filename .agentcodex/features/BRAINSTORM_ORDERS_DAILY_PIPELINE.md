# BRAINSTORM_ORDERS_DAILY_PIPELINE

## Metadata

- feature: `ORDERS_DAILY_PIPELINE`
- phase: `brainstorm`
- status: `example`
- owner: `agentcodex`
- updated_at: `2026-04-22`

## Problem

The analytics team needs a reliable daily pipeline that ingests orders from the operational database and publishes analytics-ready facts and dimensions.

## Users or Stakeholders

- primary: analytics engineers
- secondary: BI analysts, finance stakeholders

## Candidate Approaches

### Approach A

- summary: build an Airflow-orchestrated ELT flow with dbt transformations
- advantages: strong lineage, clear orchestration boundary, maintainable analytics layer
- disadvantages: requires orchestration and warehouse coordination
- operational cost: moderate

### Approach B

- summary: implement a Spark-first batch job that performs ingestion and transformation in one pipeline
- advantages: fewer moving parts for heavy transformations
- disadvantages: weaker semantic separation between ingestion and marts
- operational cost: moderate to high

## Tradeoffs

- Airflow + dbt improves semantic clarity but introduces orchestration overhead
- Spark-first centralizes logic but can blur ownership of analytics transformations
- ELT is easier for BI teams to evolve, while Spark-first may be better for large-scale reshaping

## Questions

- What is the authoritative warehouse target?
- Do we need incremental late-arriving-order handling on day one?
- Is the current source CDC-capable or snapshot-only?

## YAGNI Filter

### Needed Now

- one daily batch pipeline
- clear fact and dimension outputs
- basic quality checks

### Defer

- real-time streaming ingestion
- multi-region failover
- advanced cost optimization

## Recommendation

Start with Airflow orchestration plus dbt transformations. It gives clearer separation of concerns and better long-term maintainability for analytics.

## Exit Check

- [x] at least 2 approaches considered
- [x] main tradeoffs documented
- [x] open questions captured
- [x] recommendation made
