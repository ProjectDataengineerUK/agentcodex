# Build

## Purpose

Phase 3 of AgentCodex.

Execute the design in a controlled way using specialist roles where helpful, while keeping verification explicit and reproducible.

## Inputs

- `.agentcodex/features/DESIGN_{FEATURE}.md`
- `.agentcodex/features/DEFINE_{FEATURE}.md`
- repository state
- local tooling available in the project
- KB domains and code patterns from design

## Outputs

Write:

- code/config/test/doc changes
- `.agentcodex/reports/BUILD_REPORT_{FEATURE}.md`

Use:

- `.agentcodex/templates/BUILD_REPORT_TEMPLATE.md`

## Procedure

1. Read the design and define artifacts.
2. Extract the file manifest and role assignments.
3. Order work by dependency.
4. Implement manifest items following design patterns.
5. Use specialist roles when the manifest indicates domain complexity.
6. Verify incrementally with lint, typecheck, tests, imports, or domain-specific validation.
7. Run full project validation when available.
8. Record task attribution, commands, results, issues, deviations, and residual risks.
9. Write `BUILD_REPORT_{FEATURE}.md`.

## Required Sections

- metadata
- summary
- build order
- task execution with agent attribution
- agent contributions
- files created
- files modified
- verification results
- issues encountered
- deviations from design
- blockers
- acceptance test verification
- performance notes
- security review
- data quality results when applicable
- residual risks
- final status
- next step

## Verification Rule

Do not treat build as complete until verification is explicit.

The report must state:

- files changed
- commands run
- results
- skipped checks and why
- unresolved risks or blockers

## Suggested Specialist Mapping

- pipeline orchestration: `pipeline-architect`
- data modeling and schema: `schema-designer`
- dbt assets: `dbt-specialist`
- Spark jobs: `spark-engineer`
- data tests and quality: `data-quality-analyst`
- contracts: `data-contracts-engineer`

## Minimum Quality Gate

- manifest items implemented or explicitly deferred
- verification commands recorded
- failures resolved or clearly documented
- acceptance tests verified
- security review recorded
- data-quality checks included when applicable
- report written

## Handoff to Next Phase

Move to `ship` when:

- intended scope is implemented
- verification is complete
- residual risk is understood
- build report status is complete or accepted exceptions are documented

