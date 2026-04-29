# Semantic Modeling

## Purpose

Bring `data-agents` semantic-modeling guidance into the AgentCodex modeling KB.

## Core Rules

1. Define business metrics as measures, not hidden ad hoc report formulas.
2. Use a dedicated calendar/date dimension for fact tables.
3. Prefer many-to-one fact-to-dimension relationships.
4. Hide technical foreign keys from report consumers.
5. Use safe division semantics for ratios.
6. Document metric owner, grain, filters, and unit of measure.

## Fabric / Power BI Notes

- Direct Lake works best when Gold tables have clean grain and report-friendly column types.
- Date keys and date columns should be modeled deliberately for time intelligence.
- Avoid many-to-many relationships unless there is a documented bridge design.
- Keep semantic model changes tied to upstream data contracts.

## Databricks Metric Views

Use Databricks Metric Views when metrics should live close to governed data and
be reusable by BI or conversational analytics.

Metric view review points:

- measure has a business description
- measure has owner and unit
- dimensions are constrained and documented
- source table grain is clear
- comments are present for discoverability

## Source Notes

- Enriched from `data-agents/kb/semantic-modeling/`
- Enriched from `data-agents/skills/databricks/databricks-metric-views/`
