# Design

## Purpose

Phase 2 of AgentCodex.

Convert validated requirements into a buildable technical design with architecture decisions, KB-grounded patterns, file-level intent, testing strategy, and role assignments.

## Inputs

- `.agentcodex/features/DEFINE_{FEATURE}.md`
- `.agentcodex/features/BRAINSTORM_{FEATURE}.md` when available
- repository evidence
- KB domains named in define
- system, platform, security, and operational constraints

## Outputs

Write:

- `.agentcodex/features/DESIGN_{FEATURE}.md`

Use:

- `.agentcodex/templates/DESIGN_TEMPLATE.md`

## Procedure

1. Read the `DEFINE` artifact and verify it passed the clarity gate.
2. Load relevant KB domains from `.agentcodex/kb/`.
3. Inspect existing code/docs/tests for local patterns.
4. Create an ASCII architecture diagram.
5. Document components, flow, integrations, configuration, error handling, security, and observability.
6. Record key decisions as inline ADRs with rejected alternatives.
7. Create a complete file manifest.
8. Assign a role or `(general)` to every file.
9. Define code/config/test patterns grounded in local KB and repo conventions.
10. Define the testing and verification strategy before build starts.
11. Add pipeline architecture when data engineering context exists.

## Required Sections

- KB patterns loaded
- architecture overview
- components
- key decisions
- file manifest
- agent assignment rationale
- code patterns
- data flow
- integration points
- testing strategy
- error handling
- configuration
- security considerations
- observability
- pipeline architecture when applicable
- risks
- revision history
- exit check

## File Manifest Rule

Each design must include a manifest that states:

- target file or module
- create/modify action
- purpose
- dependency notes
- recommended role

Build should not start until the manifest is complete.

## Minimum Quality Gate

- KB patterns loaded from define's domains
- architecture diagram exists
- each major component has a purpose
- at least one decision has full rationale
- complete file manifest exists
- each file has a role assignment or `(general)`
- testing strategy covers acceptance tests
- error handling, configuration, security, and observability are explicit
- pipeline architecture is present when data context exists
- major dependencies and risks are named

## Recommended Role Usage

- `workflow-designer` as the primary role
- `explorer` for current architecture evidence
- `domain-researcher` for domain validation
- `reviewer` for pre-build design risk review

## Handoff to Next Phase

Move to `build` when:

- the manifest is complete
- implementation strategy is internally consistent
- verification expectations are defined
- risks and assumptions are documented

