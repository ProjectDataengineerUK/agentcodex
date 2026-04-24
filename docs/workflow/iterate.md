# Iterate

## Purpose

Cross-phase update procedure for AgentCodex.

Use when requirements, design assumptions, or implementation details change after one or more workflow artifacts already exist.

## Inputs

Accepted inputs:

- changed user requirement
- changed constraints
- changed architecture assumption
- changed implementation outcome

## Outputs

Update one or more of:

- `.agentcodex/features/BRAINSTORM_{FEATURE}.md`
- `.agentcodex/features/DEFINE_{FEATURE}.md`
- `.agentcodex/features/DESIGN_{FEATURE}.md`
- `.agentcodex/reports/BUILD_REPORT_{FEATURE}.md`
- `.agentcodex/archive/{FEATURE}/SHIPPED_{DATE}.md`

## Cascade Rule

Changes must be propagated downstream:

- if `DEFINE` changes, review `DESIGN`
- if `DESIGN` changes, review `BUILD_REPORT`
- if scope changes after build, update `SHIP`

## Procedure

1. Identify the source of change.
2. Determine which artifacts are now stale.
3. Update the earliest affected artifact first.
4. Cascade updates through downstream artifacts.
5. Mark what changed and why.

## Minimum Quality Gate

- stale artifacts identified
- downstream docs updated
- reason for the change documented
- unresolved downstream impact called out explicitly
