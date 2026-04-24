# Design

## Purpose

Phase 2 of AgentCodex.

Convert the defined requirements into a buildable design with file-level intent, architecture decisions, and role assignments.

## Inputs

Accepted inputs:

- `.agentcodex/features/DEFINE_{FEATURE}.md`
- repository evidence
- system constraints

## Outputs

Write:

- `.agentcodex/features/DESIGN_{FEATURE}.md`

## Required Sections

- architecture overview
- data flow or system flow
- file manifest
- implementation strategy
- dependencies and interfaces
- test strategy
- risks and open decisions

## File Manifest Rule

Each design must include a manifest that states:

- target file or module
- purpose
- dependency notes
- recommended role

Example shape:

```text
- path: pipelines/orders_daily.py
  purpose: orchestrate daily ingestion and transforms
  depends_on: config/settings.py, jobs/orders_transform.py
  role: pipeline-architect
```

## Procedure

1. Read the `DEFINE` artifact.
2. Identify the target architecture.
3. Break work into files or modules.
4. Assign a role per file when specialization matters.
5. Define the test and verification approach before build starts.
6. Call out migration risks and rollout constraints.

## Minimum Quality Gate

- complete manifest exists
- each major file has a purpose
- testing approach is explicit
- major dependencies are named
- risks are identified

## Recommended Role Usage

- `explorer` for current architecture evidence
- `domain-researcher` for domain validation
- `reviewer` for pre-build design risk review

## Handoff to Next Phase

Move to `build` when:

- the manifest is complete
- the implementation strategy is internally consistent
- verification expectations are defined
