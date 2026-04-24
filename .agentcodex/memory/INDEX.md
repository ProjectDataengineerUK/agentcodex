# Memory

## Purpose

This directory defines the Codex-first, local-first memory subsystem for AgentCodex.

Memory is a complement to:

- short-term context
- KB retrieval
- explicit reasoning and planning

Memory is not:

- raw chat history
- a replacement for `.agentcodex/kb/`
- equivalent to generic RAG

## Current Status

Current implementation status:

- phases `1` to `7`: not yet implemented as code; tracked as backlog
- phase `8` `retrieval/ranking`: implemented as a local file-based slice
- phase `9` `writeback/compaction`: implemented for the local mock backend and adapter-aware for optional remote backends
- phase `10` `observability`: implemented as local file-based telemetry
- phase `11` `roles`: implemented
- phase `12` `routing`: implemented
- phase `13` `tests`: implemented
- phase `14` `reports`: implemented

Implemented now:

- memory architecture and policy docs
- JSON Schemas for semantic, episodic, procedural, query, and write-event contracts
- local manifests for backends, access, retention, and sources
- file-based example and snapshot data for semantic, episodic, and procedural memory
- local retrieval and ranking script:
  - `python3 scripts/agentcodex.py memory-retrieve "<query>"`
- local ingest script:
  - `python3 scripts/agentcodex.py memory-ingest <semantic|episodic|procedural> <json-file>`
- local compaction script:
  - `python3 scripts/agentcodex.py memory-compact`
- local schema validation script:
  - `python3 scripts/agentcodex.py memory-validate`
- optional remote backend configuration:
  - `AGENTCODEX_MEMORY_QDRANT_URL`
  - `AGENTCODEX_MEMORY_QDRANT_API_KEY`
  - `AGENTCODEX_MEMORY_QDRANT_COLLECTION_PREFIX`
- local observability files for memory operations:
  - `.agentcodex/observability/logs/memory-*.jsonl`
  - `.agentcodex/observability/metrics/memory-health.json`
  - `.agentcodex/observability/failures/memory-failures.json`
- memory-specific roles:
  - `memory-architect`
  - `memory-governance-engineer`
  - `memory-observability-engineer`
- explicit routing for memory design, governance, and observability
- unit tests under `.agentcodex/tests/memory/`
- final reports under `.agentcodex/reports/memory/`

## Backlog

Backlog items that are viable and explicitly pending:

1. memory manager orchestration
2. live validation of the current backend boundary
3. Mem0 adapter
4. Qdrant adapter integration validation
5. LangMem adapter preparation
6. OpenAI Agents SDK adapter
7. CI checks for memory contracts
8. retrieval-time access enforcement
9. retention execution and archival workflow
10. backend integration with Mem0 and Qdrant

## Retrieval Entry Point

The current retrieval slice is designed to be:

- explicit
- file-based
- auditable
- low-context

Entry point:

- `python3 scripts/agentcodex.py memory-retrieve "<query>" [--task-type <type>]`

## Directories

- `manifests/`: current local control layer for backends, access, retention, and sources
- `examples/`: reference payload examples by memory type
- `.agentcodex/cache/memory/`: local snapshots, summaries, and retrieval indexes
