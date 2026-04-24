# Index Strategy

## Purpose

Document how AgentCodex builds a simple, auditable retrieval index over local knowledge and imported reference material.

## Script

- `.agentcodex/scripts/build_index.py`

## Retrieval Priority

AgentCodex indexes local material with this fixed priority:

1. summaries
2. manifests
3. kb pages
4. docs complementares
5. material bruto upstream

This order is encoded directly in the generated index so retrieval can prefer compressed, local context before broader reference material.

## Indexed Layers

- `summaries`
  - source: `.agentcodex/cache/summaries/`
  - purpose: shortest source-specific context for Codex use
- `manifests`
  - source: `.agentcodex/cache/manifests/`
  - purpose: audit state, generation state, and retrieval control artifacts
- `kb-pages`
  - source: `.agentcodex/kb/`
  - purpose: local domain and platform knowledge
- `docs-complementary`
  - source: `docs/`
  - purpose: supporting workflow, routing, and process context
- `upstream-raw`
  - source: `.agentcodex/imports/`
  - purpose: fallback reference when local layers are insufficient

## Retrieval Views

The index produces auditable views for:

- `by_domain`
- `by_platform`
- `by_control`
- `by_integration`

These are derived from:

- `.agentcodex/registry/domains.yaml`
- KB taxonomy paths such as `platforms/`, `controls/`, and `integrations/`
- summary domain folders under `.agentcodex/cache/summaries/`

## Outputs

- `.agentcodex/cache/manifests/retrieval-index.json`
- `.agentcodex/cache/manifests/retrieval-index.md`
- `.agentcodex/reports/index-build-report.md`

## Usage

```bash
python3 .agentcodex/scripts/build_index.py
python3 .agentcodex/scripts/build_index.py --apply
python3 .agentcodex/scripts/build_index.py --domain databricks --apply
```

## Design Notes

- the index is file-based and deterministic
- it avoids hidden vector state
- it stores path, layer, priority, domain, kind, and short snippet
- it is meant for routing and retrieval narrowing, not semantic search replacement

