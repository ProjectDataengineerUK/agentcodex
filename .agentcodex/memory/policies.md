# Memory Policies

## Retrieval Policy

Current implemented policy:

1. consult local memory summaries first when available
2. rank semantic memory before episodic memory
3. retrieve procedural memory only when the task type justifies it
4. keep context small
5. prefer compact summaries over raw memory payloads

Current limits:

- semantic: `3`
- episodic: `2`
- procedural: `1`

## Ranking Policy

Current ranking combines:

- lexical relevance
- recency
- confidence for semantic memory
- importance for episodic memory
- approval and success/failure signals for procedural memory

## Write Policy

Current implemented policy:

- ingest is file-based through `memory-ingest`
- require explicit scope object with `type` and `value`
- require `source`, `owner`, `sensitivity`, and `retention_policy`
- update in place on matching `memory_id`
- merge near-duplicates when similarity crosses the local threshold
- reject incomplete memory payloads instead of storing partial noise

## Compaction Policy

Current implemented policy:

- compact local snapshots through `memory-compact`
- deduplicate by exact `memory_id` or near-duplicate similarity
- refresh local summary and index after compaction
- never delete all content implicitly; compaction only merges duplicate/overlapping entries

Still backlog:

- mark obsolete memories explicitly
- retention execution
- archival actions

## Retention Policy

Current implemented policy:

- retrieval now enforces `memory-retention.yaml`
- unknown `retention_policy` values are filtered out
- policy `memory_type` and `scope` must match the memory item
- episodic memories are filtered out when decay pushes them below the stale threshold
- retrieval packets now record `retention_filtered`

Current limitations:

- retention is enforced at retrieval time, not yet as archival/deletion workflow
- semantic and procedural retention are still structural rules, not full lifecycle transitions
- compaction does not yet mark obsolete memories explicitly

## Access Policy

Current implemented policy:

- retrieval now enforces access templates from `memory-access.yaml`
- requester role defaults to `explorer` unless explicitly overridden
- restricted memories are only returned to roles permitted by the `restricted-memory` template
- missing `owner` or missing `sensitivity` now block retrieval when required by policy
- cross-scope retrieval is denied when owner match is required and does not match

Current limitations:

- access templates are still simple and manifest-driven, not a full RBAC/ABAC engine
- ingest does not yet stamp `permitted_roles`; access is inferred from sensitivity/template rules
- policy denials are enforced at retrieval time only

## Observability Policy

Current implemented policy:

- every memory operation should emit local run and log data
- metrics must remain file-based and repo-local
- failures should be written to a local failure file
- no external telemetry backend is required in this phase
