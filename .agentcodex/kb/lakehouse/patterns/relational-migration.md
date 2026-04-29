# Relational Migration

## Purpose

Capture the `data-agents` migration playbook for SQL Server/PostgreSQL to
Databricks or Microsoft Fabric targets.

## Migration Flow

```text
ASSESS -> ANALYZE -> DESIGN -> TRANSPILE -> RECONCILE
```

| Phase | Goal |
|---|---|
| Assess | inventory schemas, tables, procedures, volumes, dependencies |
| Analyze | classify complexity, identify unsupported types and SQL patterns |
| Design | choose Databricks, Fabric, or cross-platform target architecture |
| Transpile | generate target DDL, pipeline code, and orchestration |
| Reconcile | compare counts, keys, checksums, freshness, and critical aggregates |

## Target Decision

Never assume the target. Determine:

- Databricks Delta/Spark SQL
- Fabric Lakehouse/Warehouse
- cross-platform Databricks plus Fabric
- open table format or warehouse-native target

## Type Mapping Defaults

| Source | Target Concern |
|---|---|
| SQL Server `MONEY` | map to fixed precision decimal, not floating point |
| SQL Server `TEXT` / `NTEXT` | map to modern string type |
| SQL Server `DATETIMEOFFSET` | document timezone/offset handling |
| SQL Server `IDENTITY` | document surrogate key generation strategy |
| PostgreSQL arrays/json/geospatial | decide string, struct, variant, or target-specific representation |
| PostgreSQL serial/identity | document sequence or generated key behavior |

## Reconciliation Minimum

- row counts by table
- primary/natural key uniqueness
- null counts on required columns
- critical aggregate totals
- sample record comparison
- freshness timestamp comparison
- rejected/incompatible row report

## Anti-Patterns

- migrating stored procedures one-to-one without redesigning orchestration
- using float for money
- ignoring timezone conversion
- skipping source profiling before DDL generation
- creating Gold/reporting tables before reconciling Silver
- treating Fabric and Databricks SQL dialects as interchangeable

## Source Notes

- Enriched from `data-agents/kb/migration/index.md`
- Enriched from `data-agents/skills/migration/SKILL.md`
