# Session Controls Report

- generated_at: 2026-04-29T18:08:31.535665+00:00

## Context Budget

- input_tokens: 29125
- output_tokens: 2330
- total_tokens: 31455
- limit: 180000
- usage_ratio: 0.1618
- remaining_tokens: 150875
- status: ok
- estimation_mode: repo-local-heuristic

## Cost Summary

- total_operations: 28
- classification_mode: repo-local-script-tiering

### By Tier

- LOW: 24
- MEDIUM: 4

### By Script

- build-index: 8
- check-updates: 3
- memory-compact: 2
- memory-ingest: 2
- memory-retrieve: 8
- refresh-summaries: 4
- sync-sources: 1

## Model Routing

- policy_present: True
- policy_version: 0.1.0
- record_every_automatic_selection: True
- latest_model: gpt-5.3-codex
- latest_activity: implementation
- latest_tier: coding
- latest_reasoning_effort: medium
- latest_generated_at: 2026-04-29T18:08:28.258059+00:00
- classification_mode: repo-local-model-routing-policy
