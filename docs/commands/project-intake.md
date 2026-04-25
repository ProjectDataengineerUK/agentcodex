# Project Intake Procedure

## Purpose

Start a project from zero-state intake when AgentCodex is already installed in the current directory.

## Primary Role

- `planner`

## Escalation Roles

- `workflow-brainstormer`
- `workflow-definer`
- `explorer`

## KB Domains

- `governance`
- `ai-data-engineering`
- `data-modeling`

## Inputs

- interactive operator choice
- current repository context
- idea context for new projects or refactor goal for existing codebases

## Procedure

1. Run `python3 scripts/agentcodex.py project-intake`.
2. Abort if `.agentcodex/features/` already contains phase artifacts such as `BRAINSTORM_*`, `DEFINE_*`, or `DESIGN_*`.
3. Ask in English:
   - `1. New project from scratch`
   - `2. Information gathering for refactoring`
4. If the operator chooses `1`, present a single structured brainstorm intake block and collect all answers before writing anything.
5. Scan the current directory for lightweight context before writing the artifact.
6. Create `.agentcodex/features/BRAINSTORM_{FEATURE}.md` and follow the repo-defined brainstorm steps using both intake answers and directory evidence.
7. If the operator chooses `2`, present a single structured refactoring intake block, then scan the current directory and write a refactor intake report under `.agentcodex/reports/`.
8. Ask whether a refactoring approach is desired.
9. If approved, create `DEFINE` and `DESIGN` artifacts for the refactor path.
10. Stop before `build`; require explicit approval before any build-phase work starts.

## Outputs

- `.agentcodex/features/BRAINSTORM_{FEATURE}.md` for new-project intake
- `.agentcodex/reports/refactor-intake-report.md` for refactor analysis
- optional `.agentcodex/features/DEFINE_{FEATURE}.md`
- optional `.agentcodex/features/DESIGN_{FEATURE}.md`
