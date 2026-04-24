# Retrieval

## Purpose

Define how AgentCodex retrieves long-term memory without flooding the model context.

## Current Retrieval Order

1. local summaries
2. semantic memory
3. episodic memory
4. procedural memory when task type justifies it

## Procedural Memory Gate

Procedural memory should be consulted only for task types such as:

- `implement`
- `operate`
- `debug`
- `troubleshoot`
- `review`
- `ship`

## Context Limits

Never send the full memory store.

Current retrieval cap:

- semantic: up to `3`
- episodic: up to `2`
- procedural: up to `1`

## Current Script

- `python3 scripts/agentcodex.py memory-retrieve "<query>" [--task-type <type>]`

Optional filters:

- `--scope <scope>`
- `--scope-value <value>`
- `--json`

Related writeback commands:

- `python3 scripts/agentcodex.py memory-ingest <semantic|episodic|procedural> <json-file>`
- `python3 scripts/agentcodex.py memory-compact`

## Output

The current script returns a compact context packet with:

- summaries considered
- ranked semantic memories
- ranked episodic memories
- ranked procedural memories
- issues or filters applied

## Current Limitations

- retrieval is file-based only
- access policy is advisory, not yet fully enforced
- summaries are local files, not generated from memory compaction yet
- there is no writeback path in this phase
