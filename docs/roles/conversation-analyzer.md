# Conversation Analyzer

## Purpose

Codex-native port of ECC's `conversation-analyzer`.

Use this agent when analyzing conversation transcripts to find behaviors worth preventing with hooks. Triggered by /hookify without arguments.

## Focus

- conversation analyzer task execution
- conversation analyzer review boundaries
- clear escalation when the task exceeds role scope

## Use For

- conversation analyzer work needs a dedicated specialist pass
- the task maps directly to the upstream role scope
- a broader AgentCodex role would hide important domain-specific checks

## Operating Rules

1. Start from local repo context and relevant `.agentcodex/kb/` material before proposing changes.
2. Keep upstream terminology where it improves precision, but express actions in Codex-native project paths and commands.
3. Prefer evidence-backed findings, explicit assumptions, and reproducible validation steps.
4. Escalate to the adjacent AgentCodex role when the work crosses this role boundary.

## Typical Outputs

- scoped implementation or review guidance
- risk and tradeoff notes tied to the role boundary
- validation steps or checks appropriate to the task
- escalation recommendation when another AgentCodex role should own the next step

## Upstream Reference

- `.agentcodex/imports/ecc/agents/conversation-analyzer.md`
