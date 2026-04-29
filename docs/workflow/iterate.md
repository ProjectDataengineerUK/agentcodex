# Iterate

## Purpose

Cross-phase update procedure for AgentCodex.

Use when requirements, design assumptions, or implementation details change after one or more workflow artifacts already exist.

`iterate` is the change-control phase. It exists to keep `BRAINSTORM`, `DEFINE`, `DESIGN`, build evidence, and ship readiness consistent instead of letting implementation drift away from the documented workflow.

## Primary Role

- `workflow-iterator`

## Inputs

Accepted inputs:

- changed user requirement
- changed constraints
- changed architecture assumption
- changed implementation outcome
- target artifact path
- change description
- downstream artifacts that may now be stale

## Outputs

Update one or more of:

- `.agentcodex/features/BRAINSTORM_{FEATURE}.md`
- `.agentcodex/features/DEFINE_{FEATURE}.md`
- `.agentcodex/features/DESIGN_{FEATURE}.md`
- `.agentcodex/reports/BUILD_REPORT_{FEATURE}.md`
- `.agentcodex/archive/{FEATURE}/SHIPPED_{DATE}.md` follow-up notes when shipped work requires revision

## Change Classification

Classify every requested change before editing:

| Change Type | Impact | Handling |
|---|---|---|
| additive | low | apply when no downstream conflict exists |
| modifying | medium | check downstream requirements and design |
| removing | medium | simplify downstream docs and acceptance scope |
| architectural | high | require explicit cascade decision and design review |

## Cascade Rules

Changes must be propagated downstream:

- if `BRAINSTORM` changes, review `DEFINE`
- if `DEFINE` changes, review `DESIGN`
- if `DESIGN` changes, review `BUILD_REPORT`
- if design changes affect code, update `DESIGN` first and rerun `build`
- if scope changes after build, review `ship` readiness

## Version Tracking

Every updated artifact must include or update:

- `## Revision History`
- version bump
- date
- author, normally `workflow-iterator`
- concise change note
- cascade impact note

## Procedure

1. Load the target document.
2. Identify the phase from the artifact name.
3. Classify the change as additive, modifying, removing, or architectural.
4. Determine which downstream artifacts exist.
5. Assess whether each downstream artifact is stale.
6. Ask for cascade handling when the impact is material.
7. Update the earliest affected artifact first.
8. Bump revision history.
9. Cascade updates through downstream artifacts when selected.
10. Record unresolved downstream impact as follow-up.

## User Decision Rule

When a change affects downstream artifacts, present the decision clearly:

```text
This change to {DOCUMENT} affects {DOWNSTREAM}. Choose one:
(a) update the downstream artifact now
(b) update only the target artifact and record the downstream follow-up
(c) show the downstream changes first
```

## Minimum Quality Gate

- stale artifacts identified
- change classification recorded
- cascade impact assessed
- material cascade decision recorded
- downstream docs updated
- revision history bumped
- reason for the change documented
- unresolved downstream impact called out explicitly
- design updated before any rebuild when code impact exists
