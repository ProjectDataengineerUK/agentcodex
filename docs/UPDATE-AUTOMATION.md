# Update Automation

## Purpose

Document the non-destructive automation flow for checking upstream source changes and refreshing the local KB control layer.

## Components

- checker: `.agentcodex/scripts/check_updates.py`
- source sync: `.agentcodex/scripts/sync_sources.py`
- summaries refresh: `.agentcodex/scripts/refresh_summaries.py`
- retrieval index build: `.agentcodex/scripts/build_index.py`

Workflows:

- `.github/workflows/check-source-updates.yml`
- `.github/workflows/refresh-kb.yml`

## Flow

1. read `.agentcodex/registry/sources.yaml`
2. compare current upstream refs against `.agentcodex/registry/repos-lock.yaml`
3. write `.agentcodex/reports/update-report.md`
4. when running with `--apply`:
   - update `.agentcodex/registry/repos-lock.yaml`
   - refresh changed source metadata with `.agentcodex/scripts/sync_sources.py --apply`
   - regenerate summaries
   - rebuild the retrieval index

## Safety

- the checker is dry-run by default
- no repository cleanup or destructive file removal is performed
- only repository-local lock, cache, manifests, and reports are updated
- pull requests are created only when the repository actually changes

## Usage

```bash
python3 .agentcodex/scripts/check_updates.py
python3 .agentcodex/scripts/check_updates.py --apply
python3 .agentcodex/scripts/check_updates.py --source openai-agents-python --apply
```

## GitHub Actions

`check-source-updates.yml`

- scheduled dry-run
- uploads the update report as an artifact

`refresh-kb.yml`

- scheduled or manual apply run
- updates lock, metadata, summaries, and index
- uploads artifacts
- opens a PR automatically when relevant repository changes were produced

## Notes

- current implementation supports GitHub-hosted repositories
- the PR flow uses `peter-evans/create-pull-request@v8`
- `actions/checkout@v6` and `actions/setup-python@v6` are used in workflows
- if `sources.yaml` is empty, the workflows complete safely with no content changes
