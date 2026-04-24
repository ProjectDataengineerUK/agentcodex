# Mapping AgentSpec to Codex

## Concept Mapping

| AgentSpec | Codex / AgentCodex Equivalent |
|---|---|
| `CLAUDE.md` | `AGENTS.md` |
| `.claude/agents/*.md` | role instructions or project docs plus `.codex/agents/*.toml` |
| `.claude/commands/*.md` | workflow procedure docs and prompt recipes |
| `.claude/skills/*` | repo-local capability docs, templates, and role guidance |
| `.claude/kb/*` | local domain docs and lookup conventions |
| `.claude/sdd/*` | project-local workflow files and templates |
| plugin manifest | not needed for Codex-native operation |
| hooks | explicit checks, review roles, and verification commands |

## Priority Component Mapping

### Workflow Commands

| AgentSpec Source | AgentCodex Target |
|---|---|
| `plugin/commands/workflow/brainstorm.md` | `docs/workflow/brainstorm.md` |
| `plugin/commands/workflow/define.md` | `docs/workflow/define.md` |
| `plugin/commands/workflow/design.md` | `docs/workflow/design.md` |
| `plugin/commands/workflow/build.md` | `docs/workflow/build.md` |
| `plugin/commands/workflow/ship.md` | `docs/workflow/ship.md` |
| `plugin/commands/workflow/iterate.md` | `docs/workflow/iterate.md` |

### Workflow Agents

| AgentSpec Source | AgentCodex Target |
|---|---|
| `brainstorm-agent` | workflow role prompt |
| `define-agent` | workflow role prompt |
| `design-agent` | workflow role prompt |
| `build-agent` | workflow role prompt |
| `ship-agent` | workflow role prompt |
| `iterate-agent` | workflow role prompt |

### Specialist Agents

| AgentSpec Source | AgentCodex Target |
|---|---|
| `pipeline-architect` | specialist instruction doc + optional Codex role |
| `schema-designer` | specialist instruction doc + optional Codex role |
| `dbt-specialist` | specialist instruction doc + optional Codex role |
| `spark-engineer` | specialist instruction doc + optional Codex role |
| `sql-optimizer` | specialist instruction doc + optional Codex role |
| `data-quality-analyst` | specialist instruction doc + optional Codex role |

## Incompatibilities to Resolve

### Claude Plugin Root Paths

Pattern:

- `${CLAUDE_PLUGIN_ROOT}/...`

Codex replacement:

- project-local relative paths

### Slash Commands

Pattern:

- `/agentspec:define`
- `/agentspec:build`

Codex replacement:

- documented procedures
- role invocations
- prompt conventions

### Hooks

Pattern:

- automatic `SessionStart`
- hidden lifecycle behavior

Codex replacement:

- explicit initialization checklist
- reproducible verification steps

## Recommended Port Order

1. workflow command docs
2. workflow agent prompts
3. top-value DE specialist prompts
4. routing guide
5. KB-loading rules
6. long-tail platform agents
