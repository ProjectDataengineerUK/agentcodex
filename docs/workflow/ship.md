# Ship

## Purpose

Phase 4 of AgentCodex.

Close the implementation loop, verify delivered work, archive artifacts, capture lessons, and mark the feature as shipped or explicitly not shippable.

## Inputs

- `.agentcodex/features/BRAINSTORM_{FEATURE}.md` when present
- `.agentcodex/features/DEFINE_{FEATURE}.md`
- `.agentcodex/features/DESIGN_{FEATURE}.md`
- `.agentcodex/reports/BUILD_REPORT_{FEATURE}.md`
- acceptance tests and success criteria from define
- final verification commands and results
- readiness/ship-gate outputs when applicable

## Outputs

Write:

- `.agentcodex/archive/{FEATURE}/SHIPPED_{DATE}.md`

Archive:

- brainstorm, define, design, and build-report artifacts when present

Use:

- `.agentcodex/templates/SHIPPED_TEMPLATE.md`

## Procedure

1. Verify all required artifacts exist.
2. Confirm the build report shows completion.
3. Confirm tests pass or exceptions are documented and accepted.
4. Re-check original acceptance tests and success criteria.
5. Run the project-standard readiness and ship gates when applicable:
   - `python3 scripts/agentcodex.py readiness-report <target-project-dir>`
   - `python3 scripts/agentcodex.py ship-gate <target-project-dir>`
6. Create `.agentcodex/archive/{FEATURE}/`.
7. Copy available workflow artifacts into the archive.
8. Generate `SHIPPED_{DATE}.md`.
9. Record timeline, metrics, what was built, deviations, lessons, follow-up work, and risks.
10. Update archived artifact status to shipped when possible.
11. Document whether working files are kept or removed.

## Required Sections

- ship readiness
- summary
- timeline
- metrics
- what was built
- success criteria verification
- acceptance review
- deviations from design
- lessons learned
- recommendations for future work
- follow-up work
- final risk notes
- project standard gate
- archived artifacts
- working file retention
- exit check

## Minimum Quality Gate

- all required artifacts verified
- build completion verified
- tests pass or accepted exceptions are documented
- acceptance criteria reviewed
- success criteria verified
- deviations from design documented
- at least 2 specific lessons captured
- follow-up work listed
- project-standard ship gate passed or exception documented
- archive locations recorded

## Recommended Role Usage

- `workflow-shipper` as the primary role
- `reviewer` for final risk sweep

## Archive Rule

The archive should help a future agent understand:

- what was built
- why it was built that way
- how it was verified
- what still needs work
- what should be reused or avoided next time

