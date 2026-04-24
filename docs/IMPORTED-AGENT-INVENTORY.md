# Imported Agent Inventory

## Purpose

Track imported AgentSpec and ECC agents as an auditable backlog with explicit triage:

- `ported`: already represented by a native AgentCodex role or built-in Codex role
- `port-now`: strong candidate for near-term native port
- `defer`: potentially useful later, but not needed for the current runtime surface
- `reference-only`: keep as upstream reference, do not port unless strategy changes

## Triage Rule

Port an imported agent only if it materially improves one of these:

1. Codex-native routing
2. project-local workflow execution
3. KB-first domain reasoning
4. explicit validation or governance loops

Do not port imported agents one-to-one just because they exist upstream.

## Already Ported

### AgentSpec-aligned

- `brainstorm-agent` -> `workflow-brainstormer`
- `define-agent` -> `workflow-definer`
- `design-agent` -> `workflow-designer`
- `build-agent` -> `workflow-builder`
- `ship-agent` -> `workflow-shipper`
- `iterate-agent` -> `workflow-iterator`
- `pipeline-architect` -> `pipeline-architect`
- `schema-designer` -> `schema-designer`
- `dbt-specialist` -> `dbt-specialist`
- `spark-engineer` -> `spark-engineer`
- `sql-optimizer` -> `sql-optimizer`
- `streaming-engineer` -> `streaming-engineer`
- `data-quality-analyst` -> `data-quality-analyst`
- `data-contracts-engineer` -> `data-contracts-engineer`
- `airflow-specialist` -> `airflow-specialist`
- `lakehouse-architect` -> `lakehouse-architect`
- `medallion-architect` -> `medallion-architect`
- `lakeflow-architect` -> `lakeflow-architect`
- `fabric-architect` -> `fabric-architect`
- `ai-data-engineer` -> `ai-data-engineer`
- `aws-data-architect` -> `aws-data-architect`
- `gcp-data-architect` -> `gcp-data-architect`
- `genai-architect` -> `genai-architect`
- `data-platform-engineer` -> `data-platform-engineer`
- `kb-architect` -> `kb-architect`
- `meeting-analyst` -> `meeting-analyst`
- `prompt-crafter` -> `prompt-crafter`
- `llm-specialist` -> `llm-specialist`
- `test-generator` -> `test-generator`
- `code-documenter` -> `code-documenter`
- `codebase-explorer` -> `codebase-explorer`
- `python-developer` -> `python-developer`

### ECC-aligned

- `planner` -> `planner`
- `code-reviewer` -> `code-reviewer`
- `doc-updater` -> `doc-updater`
- `security-reviewer` -> `security-reviewer`
- `refactor-cleaner` -> `refactor-cleaner`
- `tdd-guide` -> `tdd-guide`
- `build-error-resolver` -> `build-error-resolver`
- `performance-optimizer` -> `performance-optimizer`
- `pr-test-analyzer` -> `pr-test-analyzer`
- `code-architect` -> `code-architect`
- `architect` -> `architect`
- `docs-lookup` -> `docs-lookup`
- token/context optimization guidance -> `context-optimizer`
- `silent-failure-hunter` -> `silent-failure-hunter`
- generic exploration/review behavior -> built-in `explorer` and `reviewer`

## Port-Now Candidates

These are the next imported agents that look strong enough to justify a native surface soon.

No strong `port-now` candidates remain. Future ports should be justified case by case.

## Defer

These may be useful later, but the current AgentCodex runtime does not need a dedicated native role yet.

### AgentSpec

- `ai-data-engineer-cloud`
- `ai-data-engineer-gcp`
- `ai-prompt-specialist-gcp`
- `aws-deployer`
- `aws-lambda-architect`
- `ci-cd-specialist`
- `lambda-builder`
- `supabase-specialist`
- `lakeflow-expert`
- `lakeflow-pipeline-builder`
- `lakeflow-specialist`
- `qdrant-specialist`
- `spark-performance-analyzer`
- `spark-specialist`
- `spark-streaming-architect`
- `spark-troubleshooter`
- `fabric-ai-specialist`
- `fabric-cicd-specialist`
- `fabric-logging-specialist`
- `fabric-pipeline-developer`
- `fabric-security-specialist`
- `ai-prompt-specialist`
- `code-cleaner`
- `python-developer`
- `shell-script-specialist`

Reason:
These are narrower implementation or platform-specific roles that can stay collapsed under broader native roles for now.

### ECC

- `architect`
- `code-simplifier`
- `docs-lookup`
- `e2e-runner`
- `silent-failure-hunter`
- `type-design-analyzer`
- `comment-analyzer`
- `conversation-analyzer`
- `chief-of-staff`

Reason:
Potentially useful, but not yet clearly necessary for the current Codex-first workflow surface.

## Reference-Only

These imports should remain upstream reference material unless AgentCodex changes scope significantly.

### AgentSpec

- `_template`
- `README`

### Highly specific or scope-expanding AgentSpec roles

- `supabase-specialist`
- `aws-lambda-architect`
- `lambda-builder`
- `qdrant-specialist`
- `fabric-ai-specialist`
- `fabric-security-specialist`

### ECC language- or ecosystem-specific reviewers/build resolvers

- `cpp-build-resolver`
- `cpp-reviewer`
- `csharp-reviewer`
- `dart-build-resolver`
- `database-reviewer`
- `flutter-reviewer`
- `go-build-resolver`
- `go-reviewer`
- `java-build-resolver`
- `java-reviewer`
- `kotlin-build-resolver`
- `kotlin-reviewer`
- `python-reviewer`
- `pytorch-build-resolver`
- `rust-build-resolver`
- `rust-reviewer`
- `typescript-reviewer`
- `healthcare-reviewer`
- `seo-specialist`
- `a11y-architect`
- `gan-evaluator`
- `gan-generator`
- `gan-planner`
- `harness-optimizer`
- `loop-operator`
- `opensource-forker`
- `opensource-packager`
- `opensource-sanitizer`

Reason:
These expand AgentCodex beyond its current Codex-first workflow and data-engineering focus, or they are too language-specific to justify a native role today.

## Next Action

If porting continues, the recommended order is:

1. Re-evaluate only when a new runtime gap appears
2. Prefer refining existing roles before adding more native surface
