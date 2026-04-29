# Fabric Data Agents Enrichment

## Purpose

Normalize the Microsoft Fabric guidance from the local `data-agents` repository
into AgentCodex's Fabric KB without copying Claude/MCP runtime assumptions.

## Capability Map

| Capability | Use |
|---|---|
| Lakehouse and OneLake | Delta tables, medallion layout, shortcut-based zero-copy access |
| Direct Lake | Power BI semantic consumption over lakehouse tables |
| Real-Time Intelligence | Eventhouse, KQL database, Eventstreams, Activator rules |
| Data Factory | Dataflows Gen2, pipelines, copy/orchestration patterns |
| Deployment pipelines | promotion across dev/test/prod Fabric workspaces |
| Git integration | workspace item versioning and reviewable change flow |
| Monitoring DMV | semantic model and capacity diagnostics |

## Fabric Rules From Data Agents

1. Use Delta Lake as the default Lakehouse storage format.
2. Organize lakehouse data by medallion zones: `Bronze/`, `Silver/`, `Gold/`.
3. Optimize Gold tables for Direct Lake consumption.
4. Prefer shortcuts when the goal is cross-platform access without duplicating data.
5. Use Real-Time Intelligence for streaming/event analytics rather than forcing every stream into batch lakehouse flows.
6. Configure Activator-style alerts for operational and quality thresholds.
7. Treat Fabric workspace roles and item permissions as part of the architecture, not a deployment afterthought.

## Direct Lake Review Points

- Gold tables should have BI-friendly grain and stable schema.
- Date columns should be `DATE` for calendar integration where possible.
- Avoid unnecessary high-cardinality columns in report-facing tables.
- Keep fact-to-dimension relationships explicit.
- Document whether a model is Direct Lake, Import, DirectQuery, or composite.

## Cross-Platform Review Points

When Fabric and Databricks interact:

- define the system of record
- define whether data is copied, shortcut-backed, mirrored, or shared by open table format
- document identity and access boundaries in both platforms
- document lineage at the platform handoff
- validate freshness and schema compatibility at the boundary

## Source Notes

- Enriched from `data-agents/kb/fabric/`
- Enriched from `data-agents/skills/fabric/`
