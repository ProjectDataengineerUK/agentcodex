# Session Context History

## Session

- date: `2026-04-24`
- topic: `plugin distribution and Codex-native installation`
- owner: `codex`
- scope: `agentcodex repository`

## Objective

Shift AgentCodex installation away from a clone-dependent local bootstrap model and toward a Codex-native plugin plus bundled runtime model.

## What Was Implemented

- added a Codex plugin manifest at `plugins/agentcodex/.codex-plugin/plugin.json`
- added a plugin skill at `plugins/agentcodex/skills/install-agentcodex/SKILL.md`
- added a plugin installer at `plugins/agentcodex/scripts/install_runtime.py`
- added a runtime bundle builder at `scripts/build_plugin_runtime.py`
- added a plugin packager at `scripts/package_plugin.py`
- added a local plugin marketplace file at `.agents/plugins/marketplace.json`
- added distribution documentation at `docs/PLUGIN-DISTRIBUTION.md`
- updated `README.md` to describe the intended plugin plus local scaffold installation model
- updated `setup.py` so packaged artifacts include `plugins/` and `.agents/`

## Runtime Model

Current intended install model:

1. install the `AgentCodex` plugin in Codex
2. ask Codex to install AgentCodex in a target repository
3. plugin applies:
   - `AGENTS.md`
   - `.codex/`
   - `.agentcodex/`

The bundled runtime is built into:

- `plugins/agentcodex/runtime/agentcodex-runtime/`

The packaged plugin archive is:

- `dist/plugins/agentcodex-plugin-0.1.0.tar.gz`

## Verification Completed

- `python3 scripts/build_plugin_runtime.py`
- `python3 plugins/agentcodex/scripts/install_runtime.py <tmpdir>`
- `python3 scripts/package_plugin.py`
- verified plugin tarball contains `.codex-plugin/`, `runtime/agentcodex-runtime/`, and installer files

## Constraints And Open Gaps

- public Codex docs confirm plugins, a plugins library, and plugin creation, but do not clearly document a canonical third-party publish CLI or upload flow
- `plugin.json` still contains unresolved publication metadata placeholders because this repository has no reliable public URLs configured locally
- unresolved manifest fields:
  - `author.email`
  - `author.url`
  - `homepage`
  - `repository`
  - `interface.websiteURL`
  - `interface.privacyPolicyURL`
  - `interface.termsOfServiceURL`

## Recommended Next Step

Provide the real publication metadata and target Codex workspace/library path, then finalize `plugin.json` and run the release checklist in `docs/PLUGIN-DISTRIBUTION.md`.

## Update 2026-04-24 Credits And Attribution

### Scope

Record the repository-level attribution status for upstream bases and imported raw material.

### Current State

- implementation state: attribution and credit surfaces were added
- current phase: documentation and compliance hardening
- known stable artifacts:
  - `docs/CREDITS.md`
  - `NOTICE`
  - `README.md`
  - `.agentcodex/imports/`

### Decisions

- decision: document explicit credits for AgentSpec and everything-claude-code (ECC)
- rationale: preserve provenance, make upstream basis auditable, and keep imports clearly separated from normalized AgentCodex artifacts
- decision: state MIT verification locally for both upstream bases
- rationale: make current attribution posture explicit in repo-local documentation

### Changed Artifacts

- path: `docs/CREDITS.md`
- path: `NOTICE`
- path: `README.md`

### Open Gaps

- gap: `README.md` still lacks public links for the upstream repositories alongside the local import paths
- assumption: the current local license verification remains accurate until upstream references are added

### Next Recommended Step

- next owner: `codex`
- next phase: documentation refinement
- next concrete action: add the public repository links for AgentSpec and ECC to `README.md` near the credits and attribution section

### Resume Prompt

Continue from `.agentcodex/history/SESSION_2026-04-24_PLUGIN_DISTRIBUTION_AGENTCODEX.md` and reconcile it with the latest attribution artifacts in `docs/CREDITS.md`, `NOTICE`, and `README.md`.
