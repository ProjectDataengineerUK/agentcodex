# Data Agents Quality Operations

## Purpose

Add operational quality rules from `data-agents` to the AgentCodex data-quality
domain.

## Quality Dimensions

| Dimension | Default Expectation |
|---|---|
| Completeness | required fields should meet an explicit non-null threshold |
| Uniqueness | primary and natural keys should have zero duplicates |
| Validity | values must conform to declared domains and formats |
| Consistency | foreign keys and cross-table totals should reconcile |
| Freshness | data should arrive within the table SLA |
| Accuracy | critical facts should reconcile to the source of truth |

## Placement Rules

- Bronze: capture raw data plus ingestion metadata; avoid business transformation.
- Silver: validate schema, nullability, deduplication, business keys, and conformed types.
- Gold: validate report grain, metrics, joins, aggregates, and semantic readiness.
- Streaming: treat schema drift and late data as first-class quality scenarios.

## Expectation Strategy

| Severity | Action |
|---|---|
| Informational | record metric and continue |
| Warning | alert owner and continue |
| Recoverable invalid row | drop or quarantine row |
| Critical contract failure | fail the pipeline before downstream propagation |

For Spark Declarative Pipelines:

- use `expect` for alerting
- use `expect_or_drop` for invalid rows that should not block the whole flow
- use `expect_or_fail` for contract-breaking failures

## Profiling Minimum

Run profiling when a new source is onboarded, schema changes, or volume changes
materially.

Minimum profile:

- row count
- null percentage by column
- distinct count for keys and dimensions
- min/max for numeric and timestamp columns
- format validity for emails, identifiers, dates, and codes
- top values for categorical fields

## SLA Contract Fields

- dataset owner
- expected freshness
- minimum volume
- required keys
- duplicate tolerance
- null tolerance by required column
- accepted value domains
- alert target
- remediation runbook

## Source Notes

- Enriched from `data-agents/kb/data-quality/`
- Enriched from `data-agents/skills/patterns/data-quality/`
