# model-route

## Purpose

Select the Codex model tier for an AgentCodex activity and record the automatic decision in repo-local files.

## Primary Role

- workflow-designer

Use this command before expensive or ambiguous work, or when a workflow needs to prove which model class was selected for token, cost, and risk reasons.

## Inputs

- Optional task description.
- Optional `--activity <id>` for explicit workflow activity.
- Optional `--role <role-id>` for specialist-aware routing.
- Optional `--budget low|standard|high`.
- Optional `--risk low|medium|high`.
- Optional `--json`.

## Procedure

1. Load `.agentcodex/model-routing.json`.
2. Resolve the activity from `--activity`, specialist role rules, or task keywords.
3. Resolve risk from `--risk` or risk keywords.
4. Read the current context status from `scripts/session_controls.py`.
5. Select the model tier and reasoning effort.
6. Record the selection under `.agentcodex/reports/model-routing/`.

## Outputs

- `.agentcodex/reports/model-routing/latest-selection.json`
- `.agentcodex/reports/model-routing/model-routing.md`
- Console output with selected model, tier, reasoning effort, activity, and risk.

## Examples

```bash
python3 scripts/agentcodex.py model-route --role reviewer --risk high "security review before ship"
python3 scripts/agentcodex.py model-route --activity implementation --budget low "add focused unit test"
python3 scripts/agentcodex.py model-route --json "brainstorm data contracts for a lakehouse pipeline"
```
