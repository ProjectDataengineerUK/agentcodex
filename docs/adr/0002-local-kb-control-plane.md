# ADR-0002: Local KB control plane for trusted public sources

**Status**: accepted
**Date**: 2026-04-22

## Context

AgentCodex needs a reliable local knowledge layer for Data + AI agents without depending on implicit online state or whole-repository mirrors.

## Decision

Maintain a repo-local KB control plane driven by:

- `.agentcodex/registry/sources.yaml`
- `.agentcodex/registry/repos-lock.yaml`
- `.agentcodex/cache/`
- `.agentcodex/reports/`
- `.agentcodex/scripts/`

Source sync stays metadata-first and prefers README, docs, examples, and releases over full clones.

## Consequences

- source provenance is explicit and auditable
- summaries and retrieval indexes can be regenerated locally
- network failures block refresh freshness, but not local operation

## Related

- [docs/SOURCE-SYNC.md](/home/user/Projetos/agentcodex/docs/SOURCE-SYNC.md:1)
- [docs/SUMMARIES.md](/home/user/Projetos/agentcodex/docs/SUMMARIES.md:1)
- [docs/INDEX-STRATEGY.md](/home/user/Projetos/agentcodex/docs/INDEX-STRATEGY.md:1)
