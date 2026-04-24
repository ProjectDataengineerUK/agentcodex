# KB Contracts

## Purpose

Define the contracts for the AgentCodex KB control layer and how they are validated in CI.

## Schemas

Registry schemas:

- `.agentcodex/registry/schemas/sources.schema.json`
- `.agentcodex/registry/schemas/repos-lock.schema.json`

Manifest schemas:

- `.agentcodex/registry/schemas/summary-refresh-manifest.schema.json`
- `.agentcodex/registry/schemas/retrieval-index.schema.json`

Summary contract:

- `.agentcodex/registry/schemas/summaries.schema.yaml`

## Scope

Validated artifacts:

- `.agentcodex/registry/sources.yaml`
- `.agentcodex/registry/repos-lock.yaml`
- `.agentcodex/cache/manifests/summary-refresh-manifest.json`
- `.agentcodex/cache/manifests/retrieval-index.json`
- `.agentcodex/cache/summaries/**`

## Validation

Local validator:

```bash
python3 .agentcodex/scripts/validate_kb_contracts.py
```

CI workflow:

- `.github/workflows/validate-kb-contracts.yml`

## Notes

- JSON Schema is used where the artifact is naturally JSON-shaped or easily represented as JSON
- markdown summaries use a lighter local contract because the output is file-based prose, not structured JSON
- the validator is repo-local and dependency-free

