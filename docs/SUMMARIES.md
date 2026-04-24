# Summary Refresh

## Purpose

Document how AgentCodex converts cached repository metadata into short, local summaries optimized for low-context Codex use.

## Inputs

- source metadata: `.agentcodex/cache/repo-metadata/*.json`

## Outputs

Per source, under:

`.agentcodex/cache/summaries/<domain>/<source-id>/`

Generated files:

- `overview.md`
- `latest-notes.md`
- `integration-notes.md`
- `anti-patterns.md`

Reports and manifests:

- report: `.agentcodex/reports/summary-refresh-report.md`
- manifest: `.agentcodex/cache/manifests/summary-refresh-manifest.json`

## Usage

```bash
python3 .agentcodex/scripts/refresh_summaries.py
python3 .agentcodex/scripts/refresh_summaries.py --apply
python3 .agentcodex/scripts/refresh_summaries.py --domain rag --apply
python3 .agentcodex/scripts/refresh_summaries.py --source openai-agents-python --apply
```

## Rules

- summaries are intentionally short and synthesis-oriented
- they should reduce prompt context, not mirror upstream docs
- organization is by domain and source
- current implementation uses `category` from cached metadata as the domain folder key

