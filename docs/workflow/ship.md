# Ship

## Purpose

Phase 4 of AgentCodex.

Close the implementation loop, summarize outcomes, capture lessons, and mark the work as shippable or archived.

## Inputs

Accepted inputs:

- `.agentcodex/reports/BUILD_REPORT_{FEATURE}.md`
- diff summary
- acceptance criteria from `DEFINE`

## Outputs

Write:

- `.agentcodex/archive/{FEATURE}/SHIPPED_{DATE}.md`

## Procedure

1. Re-check the original acceptance criteria.
2. Confirm what was delivered.
3. Record what changed from the original design.
4. Capture lessons learned:
   - technical
   - workflow
   - domain
5. Record known follow-ups.
6. Run the project-standard readiness gate before closing the feature:
   - `python3 scripts/agentcodex.py readiness-report <target-project-dir>`
   - `python3 scripts/agentcodex.py ship-gate <target-project-dir>`
7. Do not mark the work as shipped while required project-standard blocks remain incomplete.

## Minimum Quality Gate

- acceptance criteria reviewed
- final delivered scope stated clearly
- deviations from plan documented
- follow-up items listed
- required project-standard blocks pass the ship gate

## Recommended Role Usage

- `reviewer` for final risk sweep

## Archive Rule

The archive should help a future agent understand:

- what was built
- why it was built that way
- what still needs work
