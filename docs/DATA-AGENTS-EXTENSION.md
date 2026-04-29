# Data Agents Extension Registry

This document exposes the imported Data Agents surface as a native AgentCodex extension layer without duplicating active AgentCodex roles, commands, or KB pages.

## Counts

- agents: 12
- commands: 6
- skills: 44
- KB files: 92
- MCP servers: 13
- hooks: 12
- tests: 42
- templates: 5
- mapped agents: 12
- mapped commands: 4

## Agent Mapping

| Data Agents agent | AgentCodex role | Activation |
|---|---|---|
| `business-analyst` | `planner` | `mapped-to-native-role` |
| `business-monitor` | `business-monitor` | `mapped-to-native-role` |
| `data-quality-steward` | `data-quality-analyst` | `mapped-to-native-role` |
| `dbt-expert` | `dbt-specialist` | `mapped-to-native-role` |
| `geral` | `codebase-explorer` | `mapped-to-native-role` |
| `governance-auditor` | `data-governance-architect` | `mapped-to-native-role` |
| `migration-expert` | `lakehouse-architect` | `mapped-to-native-role` |
| `pipeline-architect` | `pipeline-architect` | `mapped-to-native-role` |
| `python-expert` | `python-developer` | `mapped-to-native-role` |
| `semantic-modeler` | `semantic-modeler` | `mapped-to-native-role` |
| `spark-expert` | `spark-specialist` | `mapped-to-native-role` |
| `sql-expert` | `sql-optimizer` | `mapped-to-native-role` |

## Command Mapping

| Data Agents command module | AgentCodex command | Activation |
|---|---|---|
| `geral` | `status` | `mapped-to-native-command` |
| `monitor` | `platform-health` | `mapped-to-native-command` |
| `parser` | `` | `reference-only` |
| `party` | `` | `reference-only` |
| `sessions` | `session-controls` | `mapped-to-native-command` |
| `workflow` | `orchestrate-workflow` | `mapped-to-native-command` |

## MCP Servers

- `context7`
- `databricks`
- `databricks_genie`
- `fabric`
- `fabric_rti`
- `fabric_semantic`
- `fabric_sql`
- `firecrawl`
- `github`
- `memory_mcp`
- `migration_source`
- `postgres`
- `tavily`

## Activation Policy

- default: `reference-only`
- no duplicate rule: Do not create a new AgentCodex role, command, or KB page when an equivalent native surface already exists. Record the mapping instead.
- native Codex rule: Claude hooks, MCP tool names, and runtime-specific scripts remain raw source unless translated into file-based AgentCodex procedures, roles, reports, or validators.
- porting rule: Promote only missing behavior that adds distinct operational value, with validation coverage when code changes are involved.
