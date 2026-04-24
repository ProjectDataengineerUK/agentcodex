# Context History Rule

## Purpose

Define a Codex-native, file-based rule for preserving resumable project context without relying on hidden session memory.

## Rule

1. Treat context history as a project artifact, not a chat artifact.
2. Store resumable context in `.agentcodex/history/`.
3. Create a new history entry whenever one of these happens:
   - a working session ends with unfinished implementation
   - ownership changes between agents or humans
   - a feature changes phase between `define`, `design`, `build`, and `ship`
   - important assumptions, blockers, or next steps change
4. Keep the latest durable summary in a dedicated file instead of depending on previous chat turns.
5. Link history entries to concrete artifacts in `.agentcodex/features/`, `.agentcodex/reports/`, and relevant code paths.

## File Convention

Use this naming pattern:

- `.agentcodex/history/CONTEXT_{FEATURE}_{YYYY-MM-DD}.md`
- `.agentcodex/history/SESSION_{YYYY-MM-DD}_{TOPIC}.md`

Prefer feature-scoped history when work is attached to a named feature. Use session-scoped history only for cross-cutting work.

## Required Sections

Each history file should contain:

- `## Scope`
- `## Current State`
- `## Decisions`
- `## Changed Artifacts`
- `## Open Gaps`
- `## Next Recommended Step`
- `## Resume Prompt`

## Writing Rules

1. Record facts, not narrative filler.
2. Prefer exact file paths and commands.
3. State unresolved assumptions explicitly.
4. Separate completed work from inferred next steps.
5. Keep entries append-only for auditability; if context changes, add a new file or a dated update block.

## Operational Use

- Use `docs/commands/sync-context.md` when artifacts drift or a resume point must be reconstructed.
- Use `agentcodex sync-context <feature>` to generate or refresh feature history directly from workflow artifacts.
- Use `context-optimizer` when reducing session load depends on stronger history usage, narrower file reads, or tighter answer depth.
- Use `docs/SESSION-HANDOFF.md` only as the repository-level handoff for this framework itself.
- In bootstrapped projects, prefer `.agentcodex/history/` over ad hoc notes in personal directories.
- Use `agentcodex new-context <feature-or-topic>` to create a standardized history entry from the template.
- Use `agentcodex resume-context <feature-or-topic>` to retrieve the latest saved resume point for a scope.
