# ADR-0003: Deterministic routing through repo-local manifests

**Status**: accepted
**Date**: 2026-04-22

## Context

AgentCodex aims to be KB-first and audit-friendly. Routing decisions cannot depend on hidden plugin hooks or implicit runtime heuristics.

## Decision

Keep routing deterministic and file-backed through:

- `docs/roles/*.md`
- `.agentcodex/roles/roles.yaml`
- `.agentcodex/routing/routing.json`
- `.agentcodex/kb/**`

Platform, domain, and control routing must map to named roles with explicit escalation paths.

## Consequences

- role selection is reviewable and reproducible
- scaffold validation can verify routing consistency
- adding a new platform domain requires explicit role and routing updates

## Related

- [docs/ROUTING-GUIDE.md](/home/user/Projetos/agentcodex/docs/ROUTING-GUIDE.md:1)
- [.agentcodex/routing/routing.json](/home/user/Projetos/agentcodex/.agentcodex/routing/routing.json:1)
