# AgentCodex KB Index

This file defines the current knowledge-base taxonomy for AgentCodex.

Use it as the navigational layer above domain-specific `index.md` files.

## Areas

### Foundations

These domains establish the conceptual base for AI and agent-aware data systems.

- `ai-data-engineering`
- `rag`

### Platforms

These domains describe concrete vendor or platform surfaces where architecture decisions land.

- `azure`
- `databricks`
- `snowflake`
- `lakehouse`

### Patterns

These domains capture reusable implementation structures across data systems.

- `dbt`
- `spark`
- `medallion`
- `streaming`

### Controls

These domains define trust, governance, quality, and enforcement boundaries.

- `governance`
- `access-control`
- `data-contracts`
- `data-quality`

### Metadata

These domains describe system understanding and dependency visibility.

- `lineage`

### Operations

These domains deal with execution, monitoring, and runtime management.

- `orchestration`
- `observability`

### Integrations

These domains define how AgentCodex and data systems connect to external capability surfaces.

- `mcp`

## Domain Relationships

### Core AI path

`ai-data-engineering` -> `rag` -> `mcp`

This path models how AgentCodex reasons about AI data workflows, retrieval systems, and protocol/tool surfaces.

### Platform execution path

`azure`, `databricks`, and `snowflake` land on top of `lakehouse`, `spark`, `streaming`, and `dbt` decisions.

In practice:

- `databricks` is strongly related to `lakeflow`, `lakehouse`, `medallion`, and `spark`
- `azure` intersects with platform governance and access control
- `snowflake` intersects with warehouse governance, contracts, and observability

### Trust and control path

`governance` -> `access-control` -> `data-contracts` -> `data-quality`

This path models who is allowed to do what, what guarantees are promised, and how trust is verified.

### Runtime evidence path

`orchestration` -> `lineage` -> `observability`

This path models how systems run, how dependencies are traced, and how failures or regressions become visible.

## Status

Currently active local domains from this taxonomy already represented in `.agentcodex/kb/` include:

- `ai-data-engineering`
- `dbt`
- `spark`
- `data-quality`
- `orchestration`
- `lakehouse`
- `medallion`
- `streaming`

Planned explicit domains to add next include:

- `azure`
- `databricks`
- `snowflake`
- `mcp`
- `rag`
- `governance`
- `lineage`
- `observability`
- `access-control`
- `data-contracts`

## Notes

- `AGENTS.md` remains the authoritative operating surface.
- This taxonomy is repo-local and Codex-native.
- Domains should be added only when they improve routing, KB-first reasoning, or project-local workflow execution.
