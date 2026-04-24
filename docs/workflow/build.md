# Build

## Purpose

Phase 3 of AgentCodex.

Execute the design in a controlled way using specialist roles where helpful, while keeping verification explicit and reproducible.

## Inputs

Accepted inputs:

- `.agentcodex/features/DESIGN_{FEATURE}.md`
- repository state
- local tooling available in the project

## Outputs

Write:

- code changes
- `.agentcodex/reports/BUILD_REPORT_{FEATURE}.md`

## Procedure

1. Read the manifest from `DESIGN`.
2. Order work by dependency.
3. Implement baseline modules first.
4. Use specialist roles when the manifest indicates domain complexity.
5. Verify incrementally:
   - lint
   - typecheck
   - tests
   - domain-specific validation where relevant
6. Record what was built and how it was verified.

## Verification Rule

Do not treat build as complete until verification is explicit.

The report must state:

- files changed
- commands run
- results
- unresolved risks or blockers

## Suggested Specialist Mapping

- pipeline orchestration: `pipeline-architect`
- data modeling and schema: `schema-designer`
- dbt assets: `dbt-specialist`
- Spark jobs: `spark-engineer`
- data tests and quality: `data-quality-analyst`

## Minimum Quality Gate

- manifest items implemented or explicitly deferred
- verification commands recorded
- failures resolved or clearly documented
- report written

## Handoff to Next Phase

Move to `ship` when:

- intended scope is implemented
- verification is complete
- residual risk is understood
