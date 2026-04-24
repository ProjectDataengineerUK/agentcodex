# Memory Risk Report

- generated_at: 2026-04-23T11:45:16Z
- status: `active-risks-reviewed`

## High Risks

- access policy is documented but not enforced during retrieval
  - impact: sensitive memory could be returned if snapshots contain broader data than intended
  - mitigation: add retrieval-time policy filter before any packet is emitted

- retention policy is structural only
  - impact: stale or sensitive memory can remain longer than intended
  - mitigation: implement retention evaluator and archival workflow before scaling usage

- no JSON Schema enforcement yet
  - impact: manifests and payloads rely on ad hoc validation and can drift
  - mitigation: add schemas plus validation in CLI and CI

## Medium Risks

- YAML parsing is intentionally simplistic
  - impact: nested manifest structure is not robustly machine-readable yet
  - mitigation: either harden the parser or constrain manifests to a simpler validated shape

- local mock backend is still the only default active backend
  - impact: Qdrant is now implemented as an optional adapter, but external integration behavior is not yet validated end-to-end in a live environment
  - mitigation: exercise the Qdrant adapter behind env-configured runs before promoting any remote backend to active default

- retrieval ranking is lexical-first
  - impact: relevant memory recall may degrade as volume grows
  - mitigation: add backend-aware retrieval and richer ranking once schemas and adapters exist

## Low Risks

- observability is local-only
  - impact: acceptable for current phase, but cross-run analysis is limited
  - mitigation: keep local-first files as source of truth and add optional export later

- tests cover the current slice but not external integrations
  - impact: acceptable because no external backend is active yet
  - mitigation: extend the suite when adapters are introduced

## Architectural Boundaries Preserved

- KB is still the primary domain reference layer
- memory is not treated as chat history
- memory is not treated as equivalent to generic RAG
- all implemented state remains repo-local and file-auditable
