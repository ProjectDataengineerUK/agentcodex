# Local Observability

## Purpose

Document the file-based observability layer for AgentCodex scripts.

## Scope

Current local observability covers:

- structured logs
- execution run records
- per-source failure registry
- basic KB health metrics
- future integration markers for OpenTelemetry, Phoenix, and Langfuse

## Files

- logs: `.agentcodex/observability/logs/*.jsonl`
- runs: `.agentcodex/observability/runs/*.json`
- failures: `.agentcodex/observability/failures/source-failures.json`
- metrics: `.agentcodex/observability/metrics/kb-health.json`
- future integration markers: `.agentcodex/observability/integrations/targets.json`

## Metrics

Current basic metrics include:

- `freshness`
- `coverage`
- `update_success_rate`
- script-specific counters such as checked sources, changed sources, indexed entries, and generated summaries

## Notes

- everything is local and auditable by files
- no external telemetry service is required
- current scripts integrated with this layer:
  - `.agentcodex/scripts/sync_sources.py`
  - `.agentcodex/scripts/check_updates.py`
  - `.agentcodex/scripts/refresh_summaries.py`
  - `.agentcodex/scripts/build_index.py`
