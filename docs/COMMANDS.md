# Command Procedures

AgentCodex does not assume Claude-style slash commands.

Instead, command intent is represented as explicit procedure documents that Codex can follow directly.

For repository installation and bootstrap, the preferred Codex-first command is:

- `agentcodex install <target-project-dir> [--profile <profile-id>]`

This command maps to the bootstrap flow with local `.codex/` support enabled by default.

Current procedures:

- `docs/commands/project-intake.md`
- `docs/commands/pipeline.md`
- `docs/commands/schema.md`
- `docs/commands/data-contract.md`
- `docs/commands/data-quality.md`
- `docs/commands/ai-pipeline.md`
- `docs/commands/review.md`
- `docs/commands/meeting.md`
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
- `agentcodex install <target-project-dir> [--profile <profile-id>]`

When a project is bootstrapped or synchronized, these procedures are copied into:

- `.agentcodex/commands/`

That project-local bundle is now checked by `agentcodex check-project` for:

- expected procedure presence
- minimum required sections
- consistency with the managed scaffold

Project completeness is now governed separately by the `AgentCodex Project Standard` manifest in:

- `.agentcodex/project-standard.json`

and its default feature scaffold:

- `.agentcodex/features/example-project-standard/`
