# AgentSpec Installation Comparison - 2026-04-25

## Question

Verify how AgentSpec installation works and whether it copies framework files into each new project.

## Evidence Checked

- `.agentcodex/imports/agentspec/readme`
- `.agentcodex/imports/agentspec/docs/getting-started/README.md`
- `.agentcodex/imports/agentspec/plugin_hooks/hooks.json`
- `/home/user/Projetos/agentspec/plugin/scripts/init-workspace.sh`
- `/home/user/Projetos/agentspec/plugin/.claude-plugin/plugin.json`

## Finding

AgentSpec has two installation modes:

1. Recommended plugin mode.
2. Legacy copy mode.

The recommended mode is plugin-based:

```bash
claude plugin marketplace add luanmorenommaciel/agentspec
claude plugin install agentspec
```

In this mode, the agents, commands, skills, KB, and SDD templates live in the installed plugin payload, not as a full copied scaffold in every project.

The legacy mode still exists:

```bash
git clone https://github.com/luanmorenommaciel/agentspec.git
cp -r agentspec/.claude your-project/.claude
```

That legacy mode copies the full `.claude` framework into the target project, but it is not the recommended installation path.

## What AgentSpec Writes Into a Project

AgentSpec's plugin hook runs on `SessionStart`:

```json
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/scripts/init-workspace.sh"
          }
        ]
      }
    ]
  }
}
```

The initializer is intentionally small and idempotent.

If the current directory looks like a project, it creates only:

- `.claude/sdd/features`
- `.claude/sdd/reports`
- `.claude/sdd/archive`

It also may generate:

- `.claude/sdd/.detected-stack.md`

That file is generated only when project stack detection finds relevant technologies such as dbt, Airflow, Spark, Terraform, Databricks, Fabric, Kafka, etc.

The plugin runtime itself contains:

- agents
- commands
- skills
- KB
- SDD architecture/templates
- hooks
- scripts

But the project receives only workflow state/output, not a full copy of the framework.

## Implication for AgentCodex

AgentCodex currently behaves more like a bootstrap/scaffold system:

- it copies `AGENTS.md`
- it copies `.codex/`
- it copies `.agentcodex/`
- it includes KB, commands, templates, routing, project standard, maturity baseline, and reports/state locations

That is heavier than AgentSpec's recommended plugin mode.

If the goal is to match AgentSpec's product ergonomics, AgentCodex should move toward:

- plugin-owned runtime assets
- target-project minimal state
- explicit project initialization only when requested
- no full KB/command/template copy by default

## Recommended AgentCodex Model

Use two modes:

### Lightweight Plugin Mode

Default for end users.

Writes only:

- `AGENTS.md` or a short AgentCodex project marker
- `.agentcodex/features/`
- `.agentcodex/reports/`
- `.agentcodex/archive/`
- `.agentcodex/history/`
- `.agentcodex/context.md` or `.agentcodex/status.md` if needed

Keeps these in the plugin/runtime package:

- KB
- commands/procedures
- templates
- routing
- role docs
- project-standard defaults
- maturity profile defaults

### Full Scaffold Mode

Explicit opt-in.

Command shape:

```bash
agentcodex install <target-project-dir> --mode full
```

or:

```bash
agentcodex sync-project <target-project-dir> --full-runtime
```

Copies the full `.agentcodex/` managed surface only for teams that want all assets vendored into the repo.

## Recommendation

Do not remove the current full scaffold capability.

Instead, add a lightweight install mode and make it the default plugin behavior.

This gives AgentCodex the same low-friction behavior as AgentSpec while preserving the stronger file-based/auditable mode when needed.

