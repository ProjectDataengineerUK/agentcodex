# Command Procedures

AgentCodex does not assume Claude-style slash commands.

Instead, command intent is represented as explicit procedure documents that Codex can follow directly.

For repository installation and bootstrap, the preferred Codex-first command is:

- `agentcodex install <target-project-dir> [--mode light|full] [--profile <profile-id>]`
- `agentcodex start`
- `agentcodex daily-tasks`
- `agentcodex model-route`
- `agentcodex generate-ecc-extension`
- `agentcodex generate-data-agents-extension`

This command maps to the lightweight bootstrap flow by default, matching AgentSpec's plugin model.

Default lightweight install writes only:

- `AGENTS.md`
- `.agentcodex/features/`
- `.agentcodex/reports/`
- `.agentcodex/archive/`
- `.agentcodex/history/`

Runtime assets such as KB, command procedures, templates, routing, maturity baselines, and role docs remain in the installed plugin/package unless full mode is requested:

```bash
agentcodex install <target-project-dir> --mode full --with-codex
```

Current procedures:

- `docs/commands/brainstorm.md`
- `docs/commands/start.md`
- `docs/commands/daily-tasks.md`
- `docs/commands/model-route.md`
- `docs/commands/define.md`
- `docs/commands/design.md`
- `docs/commands/build.md`
- `docs/commands/ship.md`
- `docs/commands/iterate.md`
- `docs/commands/create-pr.md`
- `docs/commands/diff-review.md`
- `docs/commands/fact-check.md`
- `docs/commands/generate-slides.md`
- `docs/commands/generate-visual-plan.md`
- `docs/commands/generate-web-diagram.md`
- `docs/commands/plan-review.md`
- `docs/commands/project-recap.md`
- `docs/commands/share.md`
- `docs/commands/project-intake.md`
- `docs/commands/pipeline.md`
- `docs/commands/schema.md`
- `docs/commands/sql-review.md`
- `docs/commands/lakehouse.md`
- `docs/commands/migrate.md`
- `docs/commands/data-contract.md`
- `docs/commands/data-quality.md`
- `docs/commands/ai-pipeline.md`
- `docs/commands/review.md`
- `docs/commands/judge.md`
- `docs/commands/readme-maker.md`
- `docs/commands/memory.md`
- `docs/commands/meeting.md`
- `docs/commands/status.md`
- `docs/commands/sync-context.md`
- `docs/commands/create-kb.md`
- `docs/commands/platform-health.md`
- `docs/commands/session-controls.md`
- `docs/commands/memory-candidates.md`
- `docs/commands/audit-summary.md`
- `docs/commands/orchestrate-workflow.md`

These procedures are ports of high-value AgentSpec command flows into Codex-native project documentation.

Related governance:

- `docs/CONTEXT-HISTORY.md`
- `agentcodex project-intake`
- `agentcodex new-context <feature-or-topic>`
- `agentcodex install <target-project-dir> [--mode light|full] [--profile <profile-id>]`
- `agentcodex generate-ecc-extension`
- `agentcodex generate-data-agents-extension`

When a project is bootstrapped or synchronized in full mode, these procedures are copied into:

- `.agentcodex/commands/`

That full project-local bundle is checked by `agentcodex check-project` for:

- expected procedure presence
- minimum required sections
- consistency with the managed scaffold

Project completeness is now governed separately by the `AgentCodex Project Standard` manifest in:

- `.agentcodex/project-standard.json`

and its default feature scaffold:

- `.agentcodex/features/example-project-standard/`
