# Session Handoff

## Purpose

This file preserves the working context for resuming AgentCodex after a Codex account switch or session reset.

## Current State

AgentCodex is functioning as a Codex-first framework that combines:

- ECC as the Codex operating baseline
- AgentSpec as the domain and workflow source

The project already contains:

- Codex runtime scaffolding under `.codex/`
- workflow docs for `brainstorm`, `define`, `design`, `build`, `ship`, and `iterate`
- imported upstream material under `.agentcodex/imports/`
- generated upstream catalog docs
- local KB domains under `.agentcodex/kb/`
- expanded local KB subtrees for `dbt`, `data-quality`, `orchestration`, `spark`, `airflow`, `sql-patterns`, `lakehouse`, `streaming`, `terraform`, and `ai-data-engineering`
- ported specialist roles under `docs/roles/`
- Codex-native command procedures under `docs/commands/`
- CLI support for bootstrap, sync, validation, manifest generation, upstream import, and context-history operations
- stronger scaffold verification via `check-project`
- drift reporting in `sync-project`
- project-local context history rules under `docs/CONTEXT-HISTORY.md`
- project-local context automation via `new-context`, `resume-context`, and `sync-context`
- a repo-local workflow orchestrator that writes workflow specs, stage state, and handoff reports under `.agentcodex/workflows/`
- imported-agent triage inventory under `docs/IMPORTED-AGENT-INVENTORY.md`
- KB taxonomy registry under `.agentcodex/registry/domains.yaml`
- KB source inventory and control layer under `.agentcodex/registry/`
- KB source sync, summary refresh, retrieval indexing, and update automation
- populated public source inventory under `.agentcodex/registry/sources.yaml`
- safer source update pipeline that delays `repos-lock.yaml` promotion until downstream refresh completes
- local observability for KB automation under `.agentcodex/observability/`
- KB contract validation under `.agentcodex/registry/schemas/` and `.agentcodex/scripts/validate_kb_contracts.py`
- repo-local ADRs under `docs/adr/`
- an explicit `AgentCodex Project Standard` under `.agentcodex/project-standard.json`
- an explicit `Maturity 5 Project Baseline` under `.agentcodex/maturity/maturity5-baseline.json`
- a default project-standard feature scaffold under `.agentcodex/bootstrap/PROJECT_STANDARD_FEATURE/`
- bootstrap, sync, and check support for `.agentcodex/features/example-project-standard/`
- semantic project-standard validation that distinguishes placeholder scaffold content from materially filled artifacts
- promoted enterprise KB domains into the managed and validated KB set
- taxonomic KB path support in scaffold, sync, and validation
- more deterministic KB/implementation templates with owner, artifact, and validation sections

## Ported Roles

Current Codex-native role set includes:

- workflow roles
- `planner`
- `code-reviewer`
- `security-reviewer`
- `pr-test-analyzer`
- `doc-updater`
- `code-documenter`
- `codebase-explorer`
- `code-architect`
- `meeting-analyst`
- `kb-architect`
- `context-optimizer`
- `build-error-resolver`
- `refactor-cleaner`
- `performance-optimizer`
- `pipeline-architect`
- `schema-designer`
- `dbt-specialist`
- `spark-engineer`
- `data-quality-analyst`
- `airflow-specialist`
- `sql-optimizer`
- `lakehouse-architect`
- `medallion-architect`
- `streaming-engineer`
- `aws-data-architect`
- `gcp-data-architect`
- `fabric-architect`
- `lakeflow-architect`
- `terraform-specialist`
- `ai-data-engineer`
- `genai-architect`
- `llm-specialist`
- `prompt-crafter`
- `data-platform-engineer`
- `data-contracts-engineer`
- `test-generator`
- `tdd-guide`
- `data-governance-architect`
- `metadata-platform-engineer`
- `lineage-analyst`
- `data-observability-engineer`
- `data-security-architect`
- `platform-access-engineer`
- `schema-governance-engineer`
- `azure-ai-architect`
- `databricks-architect`
- `mosaic-ai-engineer`
- `memory-architect`
- `memory-governance-engineer`
- `memory-observability-engineer`

## Memory Status

Long-term memory implementation is now completed through:

- phase `8`: retrieval and ranking
- phase `9`: writeback and compaction
- phase `10`: observability
- phase `11`: roles
- phase `12`: routing
- phase `13`: tests
- phase `14`: final reports

Current memory routing now includes:

- memory design and semantic/episodic/procedural architecture -> `memory-architect`
- memory retention, ownership, sensitivity, and access policy -> `memory-governance-engineer`
- memory metrics, tracing, hit rate, failures, and access denials -> `memory-observability-engineer`

Current memory-oriented file hints now include:

- `.agentcodex/memory/**/*`
- `.agentcodex/cache/memory/**/*`
- `.agentcodex/reports/memory/**/*`
- `.agentcodex/memory/candidates/**/*`
- `.agentcodex/memory/reviews/**/*`

Current memory schema surface now includes:

- `.agentcodex/memory/schemas/semantic-memory.schema.json`
- `.agentcodex/memory/schemas/episodic-memory.schema.json`
- `.agentcodex/memory/schemas/procedural-memory.schema.json`
- `.agentcodex/memory/schemas/memory-query.schema.json`
- `.agentcodex/memory/schemas/memory-write-event.schema.json`
- `python3 scripts/agentcodex.py memory-validate`
- `python3 scripts/agentcodex.py memory-health [backend-id] [--json]`

Current memory access state:

- retrieval now enforces `memory-access.yaml`
- requester role defaults to `explorer` unless overridden
- retrieval packets now record `access_denials`
- restricted memories are filtered by template role rules
- cross-scope retrieval is blocked when owner match is required and does not match

Current memory retention state:

- retrieval now enforces `memory-retention.yaml`
- retrieval packets now record `retention_filtered`
- unknown retention policies, scope mismatches, and stale episodic memories are filtered out during retrieval

Current memory tests now exist under:

- `.agentcodex/tests/memory/test_memory_retrieval.py`
- `.agentcodex/tests/memory/test_memory_ingest.py`
- `.agentcodex/tests/memory/test_memory_compaction.py`
- `.agentcodex/tests/memory/test_memory_policies.py`

Current memory test report:

- `.agentcodex/reports/memory/test-report.md`

Current final memory reports:

- `.agentcodex/reports/memory/implementation-report.md`
- `.agentcodex/reports/memory/risk-report.md`
- `.agentcodex/reports/memory/lint-report.md`
- `.agentcodex/reports/memory/extract-report.md`
- `.agentcodex/reports/memory/review-candidates-report.md`
- `.agentcodex/reports/memory/approve-candidates-report.md`

Current recommended next memory step:

- validate the implemented `qdrant` adapter in a live environment
- or configure and validate the implemented `mem0` adapter behind the same boundary while keeping `local-mock` as the active default

## Maturity 5 Baseline

AgentCodex now has an executable baseline for projects that should be born with high DataOps + LLMOps maturity.

Current baseline surface:

- `.agentcodex/maturity/maturity5-baseline.json`
- `python3 scripts/agentcodex.py maturity5-check <target-project-dir> [--profile <profile-id>] [--json]`
- report output in `.agentcodex/reports/maturity5-readiness-report.md`

Current implementation model:

- the baseline builds on the existing `Project Standard`
- it reuses `control-plane-check` instead of defining a parallel enterprise gate
- profiles and dimensions are declarative and auditable by file
- current profiles: `data-platform`, `agentic-llm`, `regulated-enterprise`
- `init` and `sync-project` now accept `--profile <profile-id>` and materialize profile-specific overlays under `.agentcodex/ops/`

## Data Agents Reuse Status

Current high-value reuse from `/home/user/Projetos/data-agents`:

- `tools/databricks_health_check.py` -> `agentcodex platform-health databricks`
- `tools/fabric_health_check.py` -> `agentcodex platform-health fabric`
- `hooks/context_budget_hook.py` + `hooks/cost_guard_hook.py` -> `agentcodex session-controls`
- `memory/decay.py` + `memory/lint.py` + parts of `memory/types.py` -> native memory lifecycle commands
- `templates/*.md` -> Codex-first templates under `.agentcodex/templates/`
- `kb/constitution.md` + `kb/collaboration-workflows.md` -> native policy/workflow docs under `docs/policies/`
- `hooks/audit_hook.py` + parts of `hooks/workflow_tracker.py` -> `agentcodex audit-summary` and repo-local workflow guidance

Current deferred reuse:

- deeper memory compiler/store integration
- Claude SDK runtime wiring
- UI surfaces

## Ported Command Procedures

Current Codex-native command replacements:

- `docs/commands/pipeline.md`
- `docs/commands/schema.md`
- `docs/commands/data-contract.md`
- `docs/commands/data-quality.md`
- `docs/commands/ai-pipeline.md`
- `docs/commands/review.md`
- `docs/commands/meeting.md`
- `docs/commands/sync-context.md`
- `docs/commands/create-kb.md`
- `docs/commands/orchestrate-workflow.md`

## Multi-Agent Orchestration Status

AgentCodex now has an explicit file-based workflow orchestrator.

Current orchestrator surface:

- `python3 scripts/agentcodex.py orchestrate-workflow "<prompt>"`
- `python3 scripts/agentcodex.py list-workflows`
- `python3 scripts/agentcodex.py workflow-status <workflow-run-id>`
- `docs/commands/orchestrate-workflow.md`
- `scripts/workflow_orchestrator.py`
- `python3 scripts/agentcodex.py resume-workflow <workflow-run-id>`
- `python3 scripts/agentcodex.py start-stage <workflow-run-id> <stage-id>`
- `python3 scripts/agentcodex.py complete-stage <workflow-run-id> <stage-id>`
- `python3 scripts/agentcodex.py workflow-note <workflow-run-id> <stage-id> --note "<text>"`
- `python3 scripts/agentcodex.py workflow-handoff <workflow-run-id> <from-stage-id> <to-stage-id> --note "<text>"`

Current orchestrator workflows:

- `wf-pipeline`
- `wf-star-schema`
- `wf-cross-platform`
- `wf-backlog-to-define`

Current orchestrator artifacts:

- `.agentcodex/workflows/<workflow-run-id>/state.json`
- `.agentcodex/workflows/<workflow-run-id>/<spec-template>.md`
- `.agentcodex/archive/workflows/<workflow-run-id>/state.json` after archive
- `.agentcodex/archive/workflows/<workflow-run-id>/<spec-template>.md` after archive
- `.agentcodex/reports/workflows/<workflow-run-id>.md`
- `events[]` inside `state.json`
- `handoff_log[]` inside `state.json`

Current practical role:

- choose a workflow from an input prompt
- materialize the matching repo-local spec template
- declare stage sequencing and handoffs between specialized roles
- preserve workflow progress as auditable files instead of hidden runtime state
- support stage start/completion, stage notes, and explicit inter-stage handoff records
- reject invalid `workflow_run_id` values containing traversal or separators
- preserve repeated prompts by generating unique run ids with incremental suffixes

Current validated example:

- workflow run: `wf-pipeline-crie-um-pipeline-bronze-silver-gold-no-databrick`
- `stage-01` completed
- `stage-02` in progress
- `stage-03` next
- one explicit handoff already recorded from `stage-02` to `stage-03`

## Context History Surface

Current context-history and resume surface includes:

- `docs/CONTEXT-HISTORY.md`
- `.agentcodex/templates/CONTEXT_HISTORY_TEMPLATE.md`
- `python3 scripts/agentcodex.py new-context <feature-or-topic>`
- `python3 scripts/agentcodex.py resume-context <feature-or-topic>`
- `python3 scripts/agentcodex.py sync-context <feature>`

Project checks now also enforce that real in-progress features have matching `.agentcodex/history/CONTEXT_<FEATURE>_<DATE>.md` entries.

## KB Taxonomy Status

The authoritative managed KB set now includes both the original data-engineering domains and the newer enterprise domains.

Enterprise domains now managed by scaffold and validation:

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

Resolution is now taxonomic-path based through `scripts/kb_domains.py`, so managed domains may map to nested paths inside `.agentcodex/kb/`.

## Source Control Plane Status

The source-control plane is now structurally in place and locally validated:

- `.agentcodex/registry/sources.yaml` is populated with the priority public source inventory
- `scripts/sync_sources.py` reads source definitions and writes repo metadata cache
- `.agentcodex/scripts/refresh_summaries.py` produces short local summaries from cached metadata
- `.agentcodex/scripts/build_index.py` produces auditable retrieval indexes
- `.agentcodex/scripts/check_updates.py` checks upstream drift and only promotes `repos-lock.yaml` after downstream refresh succeeds
- local observability captures runs, failures, and metrics under `.agentcodex/observability/`

Current practical limitation:

- live upstream collection still depends on external network availability; the latest local test against `openai-agents-python` recorded DNS failure in cache metadata, so the control plane is implemented and validated structurally, but real refresh behavior still needs more end-to-end exercise with stable connectivity

## Project Standard

AgentCodex now has an explicit project-completeness contract.

Authoritative source:

- `.agentcodex/project-standard.json`

This manifest defines:

- the canonical project-standard blocks
- workflow phase association for each block
- preferred role ownership
- required artifact paths
- required markers for key artifacts

Current required blocks:

- `contexto`
- `arquitetura`
- `dados`
- `governanca`
- `lineage`
- `execucao`
- `validacao`
- `observabilidade`
- `access control`
- `data contracts`
- `operacao`
- `deploy`
- `custo`
- `compliance`

Current conditional block:

- `agentes definidos (se houver)`

Bootstrap now creates the reference scaffold at:

- `.agentcodex/features/example-project-standard/`

including:

- `CHECKLIST.md`

## Current Recommended Next Step

The main structural reconciliation work is done. The next iteration should focus on operational hardening:

- exercise `sources.yaml` against live upstreams
- tighten downstream refresh consistency and failure semantics
- refine observability metrics for `freshness`, `coverage`, and `no_data` vs `failure`
- clean and normalize cache/summaries artifacts produced by the source pipeline
- `definition/`
- `design/`
- `data/`
- `controls/`
- `metadata/`
- `execution/`
- `validation/`
- `operations/observability/`
- `operations/cost/`
- `security/`
- `contracts/`
- `integrations/`
- `agents/`
- `kb/`
- `deploy/`
- `compliance/`

Checker behavior now distinguishes:

- the reference scaffold example, which may remain placeholder-heavy and is reported through notes
- real feature-local project-standard folders with `CHECKLIST.md`, which are validated strictly for required artifacts and minimum semantic content

If a block is not applicable, the expected path must justify that explicitly instead of being silently skipped.

## KB Domains

Current local KB domains:

- `dbt`
- `spark`
- `data-quality`
- `data-modeling`
- `orchestration`
- `aws`
- `ai-data-engineering`
- `gcp`
- `airflow`
- `microsoft-fabric`
- `lakehouse`
- `lakeflow`
- `medallion`
- `sql-patterns`
- `streaming`
- `terraform`
- `genai`

Expanded with local `concepts/` and `patterns/`:

- `dbt`
- `data-quality`
- `orchestration`
- `spark`
- `airflow`
- `sql-patterns`
- `lakehouse`
- `streaming`
- `terraform`
- `ai-data-engineering`

Taxonomy and physical KB structure now also include explicit enterprise surfaces under:

- `.agentcodex/kb/platforms/azure/`
- `.agentcodex/kb/platforms/databricks/`
- `.agentcodex/kb/platforms/snowflake/`
- `.agentcodex/kb/patterns/rag/`
- `.agentcodex/kb/patterns/mcp/`
- `.agentcodex/kb/controls/governance/`
- `.agentcodex/kb/controls/access-control/`
- `.agentcodex/kb/controls/data-contracts/`
- `.agentcodex/kb/metadata/lineage/`
- `.agentcodex/kb/operations/observability/`

Important caveat:

- the new enterprise taxonomy is now promoted into the authoritative managed KB set used by scaffold and validation
- KB domains are no longer flat-only; several domains now resolve through taxonomic paths such as `platforms/`, `patterns/`, `controls/`, `metadata/`, and `operations/`
- the main remaining structural gap is no longer taxonomy alignment, but real upstream source execution and operational hardening of the KB control plane

## KB Control Layer

The KB now has a local control plane:

- source registry: `.agentcodex/registry/sources.yaml`
- repo lock: `.agentcodex/registry/repos-lock.yaml`
- schemas: `.agentcodex/registry/schemas/`
- metadata cache: `.agentcodex/cache/repo-metadata/`
- summaries cache: `.agentcodex/cache/summaries/`
- manifests cache: `.agentcodex/cache/manifests/`
- reports: `.agentcodex/reports/`

Implemented scripts:

- `.agentcodex/scripts/sync_sources.py`
- `.agentcodex/scripts/refresh_summaries.py`
- `.agentcodex/scripts/build_index.py`
- `.agentcodex/scripts/check_updates.py`
- `.agentcodex/scripts/validate_kb_contracts.py`

Current remote-source state:

- `python3 scripts/agentcodex.py sync-sources --apply` completed successfully for the trusted public source registry
- `25` sources were refreshed from upstream
- `.agentcodex/registry/repos-lock.yaml` now reflects real observed upstream state
- `.agentcodex/reports/source-sync-report.md` is the current remote sync report
- `.agentcodex/reports/summary-refresh-report.md` was regenerated for all refreshed sources
- `.agentcodex/reports/index-build-report.md` was rebuilt after the remote refresh

Current limitation:

- `sources.yaml` is now populated with the prioritized public inventory
- source sync, summaries, contracts, routing, and update automation are structurally live
- real upstream refresh still depends on working network access at execution time; the latest local test recorded a DNS/network failure while attempting to sync `openai-agents-python`

## Templates And Seeds

Reusable templates added in `.agentcodex/templates/`:

- `kb-page.md`
- `platform-overview.md`
- `integration-pattern.md`
- `decision-record.md`
- `role-spec.md`
- `control-pattern.md`
- `lineage-pattern.md`
- `data-contract-spec.md`

Initial seed pages now exist for:

- governance
- lineage
- observability
- access-control
- data-contracts
- azure
- databricks
- snowflake
- mcp
- rag

## Routing And Contracts

Routing now includes:

- `domain_routing`
- `platform_routing`
- `control_routing`

Explicit routing exists for:

- `governance`
- `lineage`
- `observability`
- `access-control`
- `data-contracts`
- `azure`
- `databricks`
- `snowflake`
- `mcp`

KB contracts now exist for:

- `.agentcodex/registry/sources.yaml`
- `.agentcodex/registry/repos-lock.yaml`
- `.agentcodex/cache/manifests/*.json`
- `.agentcodex/cache/summaries/**`

CI workflow added:

- `.github/workflows/validate-kb-contracts.yml`

## Local Observability

KB automation now emits local observability artifacts:

- logs: `.agentcodex/observability/logs/*.jsonl`
- runs: `.agentcodex/observability/runs/*.json`
- source failures: `.agentcodex/observability/failures/source-failures.json`
- metrics: `.agentcodex/observability/metrics/kb-health.json`
- future integration markers: `.agentcodex/observability/integrations/targets.json`

## Validation State

Current validation and scaffold behavior now includes:

- stronger `validate` checks for roles, routing, commands, workflow docs, imports, and KB integrity
- `check-project` checks for scaffold presence, command and template integrity, managed KB structure, and context-history requirements
- project-standard validation driven by `.agentcodex/project-standard.json`
- project-standard semantic checks for placeholder-vs-filled content on real feature folders
- project-standard readiness reporting via `python3 scripts/agentcodex.py readiness-report <target-project-dir>`
- project-standard ship gating via `python3 scripts/agentcodex.py ship-gate <target-project-dir>`
- repo-level post-change refresh automation via `python3 scripts/agentcodex.py refresh-all`
- repo-local git hook automation prepared under `.githooks/` and installable via `python3 scripts/agentcodex.py install-local-automation`
- generated status snapshot via `docs/STATUS.md`
- bulk feature context synchronization via `python3 scripts/sync_all_context_histories.py`
- `sync-project` drift classification for `missing`, `outdated`, and `extra`

Current recommended next step after this handoff:

1. continue imported-agent classification work when role-surface rationalization resumes

## Memory Subsystem Status

Long-term memory is now explicitly tracked as a separate workstream.

Current status:

- no full memory subsystem existed before this slice
- a phase-8 retrieval/ranking slice now exists under `.agentcodex/memory/`
- a phase-9 local writeback/compaction slice now exists for the file-based backend
- a phase-10 local observability slice now exists for retrieval, ingest, and compaction operations
- phase-11 memory-specific roles now exist, but routing is still pending
- earlier phases 1-7 remain backlog items

Implemented in the current slice:

- `.agentcodex/memory/INDEX.md`
- `.agentcodex/memory/architecture.md`
- `.agentcodex/memory/policies.md`
- `.agentcodex/memory/retrieval.md`
- `.agentcodex/memory/manifests/*.yaml`
- `.agentcodex/memory/examples/*.json`
- `.agentcodex/cache/memory/`
- `scripts/memory_retrieve.py`
- `scripts/memory_ingest.py`
- `scripts/memory_compact.py`
- `scripts/memory_observability.py`
- `docs/roles/memory-architect.md`
- `docs/roles/memory-governance-engineer.md`
- `docs/roles/memory-observability-engineer.md`
- `python3 scripts/agentcodex.py memory-retrieve "<query>"`
- `python3 scripts/agentcodex.py memory-ingest <semantic|episodic|procedural> <json-file>`
- `python3 scripts/agentcodex.py memory-compact`
- `.agentcodex/observability/metrics/memory-health.json`
- `.agentcodex/observability/failures/memory-failures.json`
- `.agentcodex/reports/memory/observability-report.md`

Still pending and intentionally left for later phases:

- schemas
- tests
- routing
- final reports

Prepared-for markers exist for future integration with:

- OpenTelemetry
- Phoenix
- Langfuse

## Validation Status

Last known validation command:

```bash
python3 scripts/agentcodex.py validate
```

Last known result:

- validation passed
- roles manifest generation passed
- routing manifest generation passed
- KB contract validation passed
- local observability-enabled runs for update check, summary refresh, and index build passed
- the managed KB set now validates with the enterprise domains included

Related project-scaffold checks now also pass:

```bash
python3 scripts/agentcodex.py check-project /tmp/agentcodex-project-check-XXXXXX
python3 scripts/agentcodex.py sync-project /tmp/agentcodex-project-check-XXXXXX
```

Recent context-history checks also pass:

```bash
python3 scripts/agentcodex.py sync-context orders daily pipeline
python3 scripts/agentcodex.py resume-context orders daily pipeline
```

Recent KB control-plane checks also pass:

```bash
python3 .agentcodex/scripts/validate_kb_contracts.py
python3 .agentcodex/scripts/check_updates.py
python3 .agentcodex/scripts/refresh_summaries.py --apply
python3 .agentcodex/scripts/build_index.py --apply
```

Recent source inventory and sync checks:

```bash
python3 .agentcodex/scripts/sync_sources.py --source openai-agents-python
python3 .agentcodex/scripts/sync_sources.py --source openai-agents-python --apply
```

Latest observed behavior:

- the pipeline executed correctly
- the metadata cache and reports were updated
- the upstream request path recorded a network/DNS failure in the cached metadata, so summary generation proceeded from the local failure record rather than successful upstream content capture
- control-plane metrics now distinguish `freshness_state` and treat zero-input cases more explicitly
- summaries and retrieval indexing now normalize source categories toward managed KB domains instead of leaving important source groups stranded under ad hoc buckets
- legacy summary directories from older category names are now cleaned up automatically when the normalized replacement path is written

## Recommended Resume Point

The project-standard scaffold is now operationally hardened end-to-end for the current baseline.

Validated current state:

1. fresh bootstrap passes `enterprise-readiness` with `average_score: 100.0`
2. fresh bootstrap also passes `check-project`
3. remaining `check-project` notes are now expected extras, not placeholder debt in the standard scaffold

Suggested continuation order:

1. validate the populated `sources.yaml` inventory against real networked sync runs
2. harden `check_updates.py` further around rollback/reporting when downstream refresh fails after source drift is detected
3. improve observability semantics for freshness age reporting in human-facing reports, especially when network failures dominate
4. extend the workflow orchestrator with higher-level commands such as close/archive or next-stage helpers
5. revisit whether `mcp` should route through a dedicated specialist instead of `docs-lookup`

## Resume Prompt

After switching accounts, reopen this repository and start with a prompt like:

```text
Continue from docs/SESSION-HANDOFF.md and move on from scaffold completion to either KB control-plane operational hardening or workflow orchestrator lifecycle completion, using the now-stable project standard as the baseline.
```
