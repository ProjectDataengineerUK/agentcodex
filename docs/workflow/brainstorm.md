# Brainstorm

## Purpose

Phase 0 of AgentCodex.

Use this phase when the problem is still fuzzy, there are multiple possible approaches, or the user is unsure about scope and tradeoffs.

Skip this phase when requirements are already clear enough to move directly to `define`.

## Inputs

Accepted inputs:

- a short feature request
- notes from a meeting
- a problem statement
- a business objective
- an existing rough architecture idea

## Outputs

Write:

- `.agentcodex/features/BRAINSTORM_{FEATURE}.md`

## Procedure

1. Restate the problem in plain language.
2. Identify the user, team, or system affected.
3. Generate at least 2 viable approaches.
4. List the main tradeoffs for each approach.
5. Apply a YAGNI filter:
   - what is necessary now
   - what can be deferred
6. List the key open questions.
7. Recommend one direction, with reasons.

## Minimum Quality Gate

- at least 2 approaches compared
- at least 3 concrete questions raised or resolved
- one recommended direction
- explicit statement of what is out of scope for now

## Recommended Role Usage

- `explorer` for repo/context discovery
- `domain-researcher` when the problem touches data architecture or platform choices

## Handoff to Next Phase

Move to `define` when:

- the recommended direction is accepted
- the user goal is understandable
- major ambiguity is reduced enough to write measurable requirements
