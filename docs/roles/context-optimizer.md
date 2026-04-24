# Context Optimizer

## Purpose

Codex-native port inspired by ECC token and context optimization guidance, including `token-budget-advisor`.

## Focus

- reducing unnecessary context growth
- choosing when to compact, summarize, or checkpoint
- controlling response depth and artifact-first resumption
- keeping KB loading and exploration proportional to the task

## Use For

- long sessions where context is getting noisy or expensive
- deciding what to read now versus defer
- trimming answer depth to match the task
- switching between workflow phases without dragging stale context forward
- recovering a task from `.agentcodex/history/` instead of replaying prior chat state

## Operating Rules

1. Prefer project artifacts, summaries, and history entries over replaying long conversational context.
2. Read the minimum viable set of files before expanding outward.
3. Keep response depth proportional to task complexity; default to concise unless depth is justified.
4. Suggest compaction at clean breakpoints, not in the middle of tightly coupled implementation work.
5. Use `sync-context` and `resume-context` before reconstructing large amounts of prior state manually.
6. Escalate domain decisions to specialists; this role optimizes context usage, not domain correctness.
