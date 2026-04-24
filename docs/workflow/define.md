# Define

## Purpose

Phase 1 of AgentCodex.

Turn rough intent into a structured requirement set with enough clarity to design and implement safely.

## Inputs

Accepted inputs:

- `.agentcodex/features/BRAINSTORM_{FEATURE}.md`
- raw notes
- direct user request
- existing project docs

## Outputs

Write:

- `.agentcodex/features/DEFINE_{FEATURE}.md`

## Required Sections

- problem statement
- users or consumers
- goals
- measurable success criteria
- acceptance criteria
- constraints
- explicit out-of-scope

## Procedure

1. Extract the core problem.
2. Identify primary users or stakeholders.
3. Convert intent into concrete goals.
4. Define measurable success criteria.
5. Draft acceptance criteria that can be tested.
6. Capture constraints:
   - technical
   - operational
   - compliance or security
7. Define what is intentionally excluded.

## Clarity Gate

Score each area from 0 to 3:

- problem
- users
- goals
- success criteria
- scope boundaries

Minimum passing score:

- `12/15`

If the score is below threshold, do not advance to design. Ask focused clarification questions and update the document.

## Recommended Role Usage

- `explorer` for current system evidence
- `domain-researcher` for validating platform/domain assumptions

## Handoff to Next Phase

Move to `design` when:

- clarity score is at least `12/15`
- acceptance criteria are testable
- scope boundaries are explicit
