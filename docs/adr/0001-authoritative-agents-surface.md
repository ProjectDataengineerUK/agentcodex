# ADR-0001: AGENTS.md is the authoritative instruction surface

**Status**: accepted
**Date**: 2026-04-22

## Context

AgentCodex is a Codex-first adaptation and must not depend on Claude-specific runtime behavior or instruction files.

## Decision

Use `AGENTS.md` as the single authoritative instruction surface for project operation. Do not rely on `CLAUDE.md` for runtime behavior, routing, or workflow execution.

## Consequences

- project instructions remain repo-local and audit-friendly
- Codex runtime behavior stays aligned with documented files
- imported Claude-native material can exist only as reference under `.agentcodex/imports/`

## Related

- [AGENTS.md](/home/user/Projetos/agentcodex/AGENTS.md:1)
- [docs/MAPPING-AGENTSPEC-TO-CODEX.md](/home/user/Projetos/agentcodex/docs/MAPPING-AGENTSPEC-TO-CODEX.md:1)
