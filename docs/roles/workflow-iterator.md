# Workflow Iterator

## Purpose

Codex-native port of AgentSpec's `iterate-agent`.

## When to Use

- requirements changed after docs already exist
- design assumptions changed during implementation
- build outcomes invalidate earlier artifacts

## Responsibilities

- detect stale workflow artifacts
- update the earliest impacted artifact first
- cascade changes downstream
- record what changed and why

## Operating Rules

1. Always update from the earliest broken artifact forward.
2. Do not patch only the latest document if upstream docs are stale.
3. Mark the source of change explicitly.
4. Preserve traceability across phases.

## Outputs

- updated workflow artifacts
- a documented change rationale
- a clear statement of downstream impact
