# Agent Router

AgentCodex does not load AgentSpec's `agent-router` skill as Claude runtime state.

The Codex-native routing source is:

- `.agentcodex/routing/routing.json`
- `.agentcodex/model-routing.json`

AgentSpec reference source:

- `.agentcodex/imports/agentspec/skills/agent-router/SKILL.md`
- `.agentcodex/imports/agentspec/skills/agent-router/routing.json`

## Parity Model

AgentSpec routes by agent frontmatter, KB domains, intent keywords, file patterns, and escalation hints.

AgentCodex preserves that model through explicit repo-local routing sections:

- `workflow_phase_routing`: brainstorm, define, design, build, ship, and iterate role selection
- `data_engineering_routing`: task-shape to role mapping for domain and implementation work
- `file_pattern_hints`: file evidence that should bias role choice
- `escalations`: deterministic follow-on role choices when a task needs deeper review or domain coverage

Model routing is a second deterministic step:

1. resolve task activity
2. resolve specialist role
3. resolve model tier from activity, role, budget, context pressure, and risk
4. record the automatic selection under `.agentcodex/reports/model-routing/`

## Operating Rule

Use `.agentcodex/routing/routing.json` before choosing specialist behavior for non-trivial work.

Use `agentcodex model-route [task]` before expensive or ambiguous work to record the selected model tier and reasoning effort.

Prefer these built-in Codex roles when the task maps cleanly:

- `explorer`: evidence gathering and impact tracing
- `reviewer`: bug, regression, and test-risk review
- `domain-researcher`: data-engineering validation against local KB-derived standards

Use AgentCodex role docs under `docs/roles/` for domain-specific behavior when no built-in role is enough.

## Maintenance

Regenerate routing after role changes:

```bash
python3 scripts/agentcodex.py generate-routing
python3 scripts/agentcodex.py validate
```

Do not copy `${CLAUDE_PLUGIN_ROOT}` paths into active AgentCodex routing. Imported AgentSpec files remain raw evidence only.
