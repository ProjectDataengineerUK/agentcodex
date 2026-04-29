# Data Agents SQL Generation

## Purpose

Capture SQL generation guardrails from `data-agents` without duplicating the
existing AgentCodex SQL pattern pages.

## Generation Rules

1. Determine SQL dialect before writing syntax.
2. State table grain before joins and aggregations.
3. Use explicit column lists in production queries.
4. Use window functions for deterministic deduplication.
5. Avoid many-to-many joins unless a bridge or allocation rule is explicit.
6. Preserve decimal precision for monetary values.
7. Add filters to audit, lineage, and high-volume operational tables.

## Cross-Dialect Checks

| Concern | Check |
|---|---|
| date functions | dialect-specific syntax |
| `QUALIFY` | supported in some engines, not universal |
| identity/autoincrement | target-specific |
| geospatial | target-specific type support |
| JSON/variant | target-specific representation |
| materialized views | syntax and refresh semantics vary |

## Source Notes

- Enriched from `data-agents/kb/sql-patterns/`
- Enriched from `data-agents/skills/patterns/sql-generation/`
