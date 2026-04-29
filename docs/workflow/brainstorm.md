# Brainstorm

## Purpose

Phase 0 of AgentCodex.

Use this phase when the problem is still fuzzy, multiple approaches are possible, the user is unsure about scope, or LLM/data work needs grounding material before formal requirements are captured.

Skip this phase only when requirements are clear enough to move directly to `define`.

## Inputs

- a short feature request
- notes from a meeting
- a problem statement
- a business objective
- an existing rough architecture idea
- a file containing raw notes, samples, or expected outputs

## Outputs

Write:

- `.agentcodex/features/BRAINSTORM_{FEATURE}.md`

Use:

- `.agentcodex/templates/BRAINSTORM_TEMPLATE.md`

## Procedure

1. Gather context from `AGENTS.md`, `.agentcodex/kb/`, current feature/history artifacts, and relevant code/docs.
2. Identify likely KB domains and project patterns that should feed `define`.
3. Ask one discovery question at a time. Ask at least 3 questions before finalizing a direction.
4. Ask for grounding material: sample inputs, expected outputs, ground truth, schemas, requirements, or reference docs.
5. Compare 2-3 candidate approaches with pros, cons, operational cost, evidence, and confidence.
6. Lead with a recommendation, but document rejected alternatives.
7. Apply YAGNI and record removed or deferred features.
8. Validate at least 2 sections with the user before completion.
9. Save the brainstorm artifact with draft requirements ready for `define`.

## Required Sections

The brainstorm artifact must include:

- initial idea and context gathered
- technical context observed for `define`
- discovery questions and answers
- sample data inventory or explicit note that samples are unavailable
- candidate approaches
- data engineering context when applicable
- selected approach
- recommendation
- key decisions made
- features removed by YAGNI
- incremental validations
- suggested requirements for `define`
- session summary
- exit check

## Minimum Quality Gate

- minimum 3 discovery questions asked
- sample collection question asked
- at least 2 approaches explored
- relevant KB domains identified for `define`
- YAGNI applied and removed/deferred features documented
- minimum 2 validation checkpoints completed
- selected approach confirmed by user
- draft requirements included for `define`

## Recommended Role Usage

- `workflow-brainstormer` as the primary role
- `explorer` for repo/context discovery
- `domain-researcher` when the problem touches data architecture or platform choices

## Handoff to Next Phase

Move to `define` when:

- the recommended direction is accepted
- the user goal is understandable
- major ambiguity is reduced enough to write measurable requirements
- samples or the lack of samples are documented
- relevant KB domains and constraints are listed

