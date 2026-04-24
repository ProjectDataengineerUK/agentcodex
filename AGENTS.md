# AgentCodex Instructions

## Purpose

AgentCodex is a Codex-native adaptation of AgentSpec built on ECC patterns.

This repository exists to make AgentSpec usable in Codex without relying on:

- Claude plugin manifests
- Claude-only slash command behavior
- Claude hook runtime
- `CLAUDE.md` as the primary instruction surface

## Operating Model

Use these rules by default:

1. Treat `AGENTS.md` as the authoritative project instruction file.
2. Use `.codex/config.toml` and `.codex/agents/*.toml` as the runtime surface.
3. Prefer Codex multi-agent roles for exploration, review, and domain validation.
4. Preserve AgentSpec's KB-first mindset before proposing implementation details.
5. Treat ECC as the baseline operating system for Codex and AgentSpec as the domain/workflow layer.
6. Use `.agentcodex/imports/` as the raw upstream reference layer when you need original AgentSpec or ECC material.

## Core Principles

1. Codex-first, not Claude-compatible-by-accident.
2. Domain-specific knowledge should remain local and explicit.
3. Workflow state should be represented by files, not hidden plugin state.
4. Validation should be reproducible through commands, not implicit hook magic.
5. Routing should be deterministic and documented.

## AgentCodex Project Standard

Every generated or bootstrapped project must satisfy the AgentCodex Project Standard.

Do not treat a project as complete until all of these blocks are implemented or explicitly justified as not applicable:

- contexto
- arquitetura
- dados
- governanca
- lineage
- execucao
- validacao
- observabilidade
- access control
- data contracts
- operacao
- deploy
- custo
- compliance

The canonical scaffold lives under `.agentcodex/features/example-project-standard/` in the bootstrap and must be used as the default project structure reference.

The authoritative manifest for these blocks lives in `.agentcodex/project-standard.json`.

Projects that should start at mature DataOps + LLMOps level must also satisfy one of the executable `Maturity 5 Project Baseline` profiles in `.agentcodex/maturity/maturity5-baseline.json`.
Use `agentcodex maturity5-check <target-project-dir> --profile <profile-id>` as the explicit gate for that higher operating bar.
When a project is bootstrapped with `--profile <profile-id>`, the corresponding profile overlay under `.agentcodex/ops/` becomes part of the expected operating scaffold.

If a block is not applicable, justify it explicitly in the corresponding artifact instead of silently skipping it.

## AgentCodex Workflow

The target workflow remains:

1. `brainstorm`
2. `define`
3. `design`
4. `build`
5. `ship`

But in Codex this must be implemented through:

- documented procedures
- role prompts
- file conventions
- verification loops

not through Claude plugin command wiring.

Reference docs:

- `docs/workflow/brainstorm.md`
- `docs/workflow/define.md`
- `docs/workflow/design.md`
- `docs/workflow/build.md`
- `docs/workflow/ship.md`
- `docs/workflow/iterate.md`
- `docs/COMMANDS.md`
- `docs/CONTEXT-HISTORY.md`

## Role Usage

- `explorer`: collect evidence, execution paths, file references, and dependency impact
- `reviewer`: inspect correctness, regressions, tests, and risks
- `domain-researcher`: validate data-engineering choices against the local AgentSpec-derived KB

Ported role docs:

- `docs/roles/workflow-brainstormer.md`
- `docs/roles/workflow-definer.md`
- `docs/roles/workflow-designer.md`
- `docs/roles/workflow-builder.md`
- `docs/roles/ai-data-engineer.md`
- `docs/roles/pipeline-architect.md`
- `docs/roles/data-contracts-engineer.md`
- `docs/roles/schema-designer.md`
- `docs/roles/dbt-specialist.md`
- `docs/roles/spark-engineer.md`
- `docs/roles/data-quality-analyst.md`

Routing reference:

- `docs/ROUTING-GUIDE.md`
- `.agentcodex/routing/routing.json`

## Guardrails

1. Do not assume Claude hooks exist.
2. Do not assume slash commands exist.
3. Do not reference `${CLAUDE_PLUGIN_ROOT}` in new Codex-native artifacts.
4. Do not encode workflow state in global user directories when project-local files are sufficient.
5. When porting AgentSpec material, normalize paths and terminology to Codex surfaces.

## Working Directories

AgentCodex expects workflow artifacts to converge toward these project-local locations:

- `.agentcodex/features/`
- `.agentcodex/reports/`
- `.agentcodex/archive/`
- `.agentcodex/history/`
- `.agentcodex/templates/`
- `.agentcodex/kb/`
- `.agentcodex/routing/`

These are preferred over hidden Claude plugin state or user-global directories.

Imported upstream source material is preserved separately in:

- `.agentcodex/imports/agentspec/`
- `.agentcodex/imports/ecc/`

## Local Knowledge Base

Use `.agentcodex/kb/` as the first local domain reference layer.

Current domains:

- `governance`
- `lineage`
- `observability`
- `access-control`
- `data-contracts`
- `azure`
- `databricks`
- `snowflake`
- `mcp`
- `rag`
- `dbt`
- `spark`
- `data-quality`
- `data-modeling`
- `orchestration`
- `genai`
- `ai-data-engineering`
- `airflow`
- `aws`
- `gcp`
- `microsoft-fabric`
- `lakehouse`
- `lakeflow`
- `medallion`
- `sql-patterns`
- `streaming`
- `terraform`

Additional repo-local KB surfaces also exist under the taxonomy in:

- `.agentcodex/kb/platforms/`
- `.agentcodex/kb/patterns/`
- `.agentcodex/kb/controls/`
- `.agentcodex/kb/metadata/`
- `.agentcodex/kb/operations/`
- `.agentcodex/kb/integrations/`

## Porting Rules

When converting content from AgentSpec:

1. Replace `CLAUDE.md` references with `AGENTS.md`.
2. Replace plugin-relative paths with repo-local paths.
3. Convert command-centric flows into procedural instruction docs.
4. Convert agent frontmatter into role or prompt metadata that Codex can use directly.
5. Keep domain terminology intact where it adds value.

When converting content from ECC:

1. Preserve Codex-specific operating patterns where they are already valid.
2. Avoid copying Claude-only hooks or harness assumptions into Codex-native flows.
3. Use imported ECC skills, rules, and `.codex` content as reference material before writing new variants.

## Success Criteria

AgentCodex is successful when:

- a Codex user can run the workflow without Claude plugin infrastructure
- role prompts are sufficient to reproduce the intended specialist behavior
- data-engineering guidance remains strong
- the system is easier to audit than the original Claude plugin setup
