# Memory Architecture

## Design Goal

AgentCodex memory must stay:

- Codex-first
- repo-local
- file-auditable
- explicit in scope, source, ownership, and sensitivity

## Target Architecture

The target subsystem is divided into:

1. memory manager
2. memory schemas
3. memory storage adapters
4. retrieval and ranking
5. write and update policies
6. governance and access rules
7. observability
8. validation and tests

## Current Implemented Slice

The current slice implements:

- `retrieval and ranking`
- `writeback and compaction`
- `observability`
- `schema contracts and validation`
- `roles and routing`
- `tests and reporting`

That slice uses:

- local snapshot files under `.agentcodex/cache/memory/snapshots/`
- local manifests under `.agentcodex/memory/manifests/`
- a backend adapter boundary in `scripts/memory_backend.py`
- deterministic scripts in:
  - `scripts/memory_retrieve.py`
  - `scripts/memory_ingest.py`
  - `scripts/memory_compact.py`
  - `scripts/memory_observability.py`

## Memory Layers

### KB

The KB remains the first domain reference layer.

Use the KB for:

- stable domain knowledge
- platform guidance
- pattern lookup
- implementation reference

### Memory

Use memory for:

- stable facts about user, project, or team
- significant past events and outcomes
- reusable procedural learnings

### Short-Term Context

Use short-term context for:

- current task state
- transient reasoning
- in-flight execution details

## Retrieval Flow

1. task arrives
2. retrieval policy checks if memory is justified
3. local summaries are consulted first
4. semantic memories are ranked
5. episodic memories are ranked
6. procedural memory is consulted only when the task type justifies it
7. a compact context packet is produced

## Current Backend Posture

Currently active:

- automatic backend selection that prefers Qdrant when configured and falls back to local file snapshots
- local mock backend using file snapshots behind a formal adapter boundary
- local observability for retrieval, ingest, and compaction operations
- deterministic routing through memory-specific roles

Prepared but not yet implemented:

- Mem0 adapter
- LangMem adapter
- OpenAI Agents SDK integration adapter

## Adapter Boundary

The memory runtime now separates command behavior from backend storage through a small backend interface.

Current interface:

- `snapshot_paths()`
- `summary_path()`
- `load(memory_type)`
- `upsert(memory_type, items)`
- `compact(compacted, summary_text, index_payload)`
- `health()`

Current implementation:

- `local-mock` adapter in `scripts/memory_backend.py`
- `mem0` adapter in `scripts/memory_backend.py`
- `qdrant` adapter in `scripts/memory_backend.py`

This keeps retrieval, ingest, and compaction backend-aware without forcing backend-specific logic into each command script.

Current backend notes:

- `auto` resolves to `qdrant` when `AGENTCODEX_MEMORY_QDRANT_URL` is set, otherwise `local-mock`
- `local-mock` remains the fallback active backend
- `mem0` is implemented as an optional REST adapter driven by environment variables
- `qdrant` is implemented as an optional REST adapter driven by environment variables
- `langmem` remains prepared as an explicit stub behind the same boundary

## Backlog Dependency Notes

The following prerequisites are still pending and remain backlog items:

- schemas for machine validation
- access enforcement beyond local filtering
- retention execution and archival workflow
- LangMem adapter implementation
- agent-runtime integration
