# Source Sync

## Purpose

Document how AgentCodex captures lightweight metadata from trusted upstream repositories without cloning full repositories by default.

## Files

- registry: `.agentcodex/registry/sources.yaml`
- lock file: `.agentcodex/registry/repos-lock.yaml`
- sync entrypoint: `.agentcodex/scripts/sync_sources.py`
- metadata cache: `.agentcodex/cache/repo-metadata/`
- summaries cache: `.agentcodex/cache/summaries/`
- manifests cache: `.agentcodex/cache/manifests/`
- report: `.agentcodex/reports/source-sync-report.md`

## Behavior

- reads trusted sources from `.agentcodex/registry/sources.yaml`
- prefers GitHub API for repository metadata, README, top-level docs/examples detection, and latest release lookup
- does not download the full repository by default
- optionally uses shallow sparse clone with `--use-git`
- writes per-source metadata JSON and summary JSON when `--apply` is used
- updates `.agentcodex/registry/repos-lock.yaml` with the observed reference and sync status

## Usage

```bash
python3 scripts/agentcodex.py sync-sources
python3 scripts/agentcodex.py sync-sources --source openai-agents-python
python3 scripts/agentcodex.py sync-sources --apply
python3 scripts/agentcodex.py sync-sources --apply --use-git
python3 scripts/agentcodex.py sync-sources --limit 5
```

Packaged CLI:

```bash
agentcodex sync-sources --apply
```

## sources.yaml Format

Expected shape:

```yaml
version: 0.1.0
sources:
  - id: openai-agents-python
    name: OpenAI Agents Python
    repo: https://github.com/openai/openai-agents-python
    category: agents
    trust: official
    ingest_mode: metadata-first
    update_strategy: periodic
```

Required fields per source:

- `id`
- `name`
- `repo`
- `category`
- `trust`
- `ingest_mode`
- `update_strategy`

## Notes

- this script is intentionally metadata-first and audit-friendly
- README and release content are summarized, not mirrored wholesale
- repositories outside GitHub are not supported by the current implementation
- network access is required for real sync execution
