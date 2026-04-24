# Porting Roadmap

## Phase 0: Baseline

Status: done in scaffold

Deliver:

- project structure
- Codex config
- AGENTS instructions
- integration plan

## Phase 1: Workflow Port

Objective:
Port AgentSpec's SDD lifecycle into Codex-native docs and conventions.

Deliverables:

- `docs/workflow/brainstorm.md`
- `docs/workflow/define.md`
- `docs/workflow/design.md`
- `docs/workflow/build.md`
- `docs/workflow/ship.md`
- `docs/workflow/iterate.md`
- local feature/report/archive directory conventions

Priority:
highest

## Phase 2: Core Role Port

Objective:
Port the highest-value workflow and engineering agents first.

Suggested first roles:

- planner
- define
- design
- build
- reviewer
- pipeline architect
- schema designer
- dbt specialist
- spark engineer
- data quality analyst

Priority:
highest

## Phase 3: Routing Port

Objective:
Transform AgentSpec's router into Codex-readable routing rules.

Deliverables:

- routing guide
- escalation matrix
- intent-to-role mapping

Priority:
high

## Phase 4: KB Port

Objective:
Bring over the KB taxonomy and local lookup rules.

Suggested first KB domains:

- dbt
- spark
- airflow
- sql-patterns
- data-quality
- data-modeling
- lakehouse
- medallion
- genai
- python
- testing

Priority:
high

## Phase 5: Verification and Governance

Objective:
Replace Claude hook guarantees with Codex-native review and validation loops.

Deliverables:

- migration checklist
- phase exit criteria
- validation recipes
- review templates

Priority:
high

## Phase 6: Long Tail Port

Objective:
Port lower-frequency specialist agents and platform-specific domains.

Examples:

- Microsoft Fabric specialists
- cloud deployment specialists
- visual explainer workflows
- meeting analyst and utility roles

Priority:
medium

## Phase 7: Long-Term Memory Subsystem

Objective:
Add a Codex-first, file-auditable long-term memory subsystem that complements KB retrieval without replacing it.

Current status:

- retrieval and ranking: implemented
- local ingest and writeback: implemented
- compaction and deduplication: implemented
- local observability: implemented
- memory-specific roles: implemented
- memory routing: implemented
- tests: implemented
- JSON schemas and local contract validation: implemented

Remaining backlog for the memory subsystem:

- Mem0 adapter behind the implemented backend boundary
- Qdrant live-environment validation
- LangMem implementation behind the prepared boundary
- OpenAI Agents SDK integration adapter
- retrieval-time access enforcement
- retention execution and archival workflow
- CI checks for memory contracts
