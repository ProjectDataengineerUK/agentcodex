# Define

## Purpose

Phase 1 of AgentCodex.

Turn rough intent into a structured requirement set with enough clarity to design and implement safely. This phase combines intake, PRD shaping, and refinement into one validated requirements artifact.

## Inputs

- `.agentcodex/features/BRAINSTORM_{FEATURE}.md`
- raw notes
- direct user request
- stakeholder email or conversation notes
- existing project docs
- multiple source files that must be consolidated

## Outputs

Write:

- `.agentcodex/features/DEFINE_{FEATURE}.md`

Use:

- `.agentcodex/templates/DEFINE_TEMPLATE.md`

## Procedure

1. Load `AGENTS.md`, `.agentcodex/templates/DEFINE_TEMPLATE.md`, `.agentcodex/kb/`, and the provided input.
2. Classify the input as brainstorm document, meeting notes, email thread, conversation, direct requirement, or mixed sources.
3. Extract problem, users, goals, success criteria, acceptance tests, constraints, out of scope, assumptions, and technical context.
4. Preserve chosen approach, YAGNI removals, sample inventory, and KB domains when the input is a brainstorm artifact.
5. Add a data contract section when the feature involves data pipelines, ETL, analytics, schemas, contracts, freshness, lineage, or data quality.
6. Score clarity across problem, users, goals, success, and scope.
7. Ask targeted clarification questions when score is below `12/15`.
8. Save the define artifact only when the quality gate is satisfied or remaining gaps are explicitly marked as blocking.

## Required Sections

- input classification
- problem statement
- target users with pain points
- goals with MoSCoW priority
- measurable success criteria
- acceptance tests
- out of scope
- constraints
- technical context
- data contract when applicable
- assumptions
- clarity score breakdown
- open questions
- revision history
- exit check

## Clarity Gate

Score each area from 0 to 3:

- problem
- users
- goals
- success criteria
- scope boundaries

Minimum passing score:

- `12/15`

If the score is below threshold, do not advance to `design`. Ask focused clarification questions with concrete options where possible and update the document.

## Recommended Role Usage

- `workflow-definer` as the primary role
- `explorer` for current system evidence
- `domain-researcher` for validating platform/domain assumptions

## Handoff to Next Phase

Move to `design` when:

- clarity score is at least `12/15`
- acceptance tests are testable
- scope boundaries are explicit
- assumptions and their impact are documented
- KB domains and technical context are ready for design

