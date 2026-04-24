# Memory Observability Report

## Purpose

This report tracks the local observability surface prepared for the memory subsystem.

## Current Metrics

- retrieval count
- memory hit rate
- write count
- dedup count
- compaction events
- retention actions
- access denials
- latency per operation
- backend failures

## Current Files

- `.agentcodex/observability/logs/memory-retrieve.jsonl`
- `.agentcodex/observability/logs/memory-ingest.jsonl`
- `.agentcodex/observability/logs/memory-compact.jsonl`
- `.agentcodex/observability/runs/*memory*.json`
- `.agentcodex/observability/metrics/memory-health.json`
- `.agentcodex/observability/failures/memory-failures.json`

## External Integration Posture

Prepared structurally only:

- OpenTelemetry
- Phoenix
- Langfuse

No external integration is required in this phase.
