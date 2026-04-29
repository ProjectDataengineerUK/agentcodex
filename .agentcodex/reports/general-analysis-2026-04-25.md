# AgentCodex General Analysis - 2026-04-25

## Scope

General repository review from `/home/user/Projetos/agentcodex`, using `AGENTS.md` as the project instruction surface.

Reviewed areas:

- CLI surface and command routing
- plugin packaging and distribution workflow
- validation and test coverage
- workflow lifecycle
- project-standard and control-plane artifacts
- repo hygiene and generated artifacts

## Current Strengths

- `python3 scripts/agentcodex.py validate` passes.
- `python3 scripts/agentcodex.py validate-plugin` passes.
- Local tests under `.agentcodex/tests` pass with `32` tests.
- The project has a strong Codex-native operating model: `AGENTS.md`, `.codex/`, `.agentcodex/`, command procedure docs, routing manifest, KB, project standard, maturity baseline, and file-based workflow state.
- Workflow lifecycle commands exist: `workflow-next`, `workflow-close`, and `workflow-archive`.
- Prior path traversal risks in workflow IDs are covered by tests.
- Plugin distribution has a concrete runtime bundle builder and packager.

## Main Findings

### 1. Two CLI Surfaces Are Diverging

`scripts/agentcodex.py` exposes the richer command surface, including:

- `readiness-report`
- `ship-gate`
- `maturity5-check`
- `refresh-all`
- `install-local-automation`
- `memory-retrieve`
- `memory-ingest`
- `memory-compact`
- `memory-validate`

The installed package CLI at `src/agentcodex_cli/cli.py` does not expose all of those commands.

Impact:

- Users running `python3 scripts/agentcodex.py ...` and users running installed `agentcodex ...` can get different behavior.
- Product distribution risk is high because the public entrypoint is `agentcodex`, not the source-tree script.

Recommended improvement:

- Collapse command routing into one shared command registry.
- Make both entrypoints call the same dispatcher.
- Add a test that compares help/command coverage between `scripts/agentcodex.py` and `src/agentcodex_cli/cli.py`.

### 2. Validation Does Not Run the Test Suite

`refresh-all` runs generated artifact refreshes, memory lint, import catalog generation, and `validate_agentcodex.py`, but it does not run:

- `.agentcodex/tests`
- plugin manifest validation
- package build validation
- plugin package archive validation

Impact:

- `validate` can pass even if runtime behavior regresses.
- Release checklist depends on human discipline rather than one reproducible gate.

Recommended improvement:

- Add `agentcodex verify` or extend `refresh-all --release` to run:
  - `python3 scripts/agentcodex.py validate`
  - `python3 scripts/agentcodex.py validate-plugin`
  - `python3 -m unittest discover -s .agentcodex/tests`
  - `python3 scripts/build_plugin_runtime.py`
  - `python3 scripts/package_plugin.py`
  - archive content inspection

### 3. Plugin Runtime Bundle Is Too Narrow for End-to-End Product Confidence

`scripts/build_plugin_runtime.py` copies bootstrap, templates, KB, maturity, commands, project standard, and routing.

It does not copy source CLI/package tests, release verification scripts, roles docs, status docs, or explicit runtime self-check instructions.

Impact:

- The plugin may install the scaffold correctly, but release confidence depends on source-repo checks outside the bundle.
- It is harder to validate a packaged plugin independently from the repository.

Recommended improvement:

- Add a plugin package self-check script or manifest.
- Include a minimal runtime verification command/procedure inside the plugin runtime.
- Add an archive inspection test that asserts required runtime files exist in `dist/plugins/agentcodex-plugin-*.tar.gz`.

### 4. Packaging Version Is Hardcoded

`scripts/package_plugin.py` writes `dist/plugins/agentcodex-plugin-0.1.0.tar.gz` directly.

Impact:

- Version drift can occur between `pyproject.toml`, plugin manifest, docs, and archive filename.

Recommended improvement:

- Read version from one authoritative source, preferably `plugins/agentcodex/.codex-plugin/plugin.json` or `pyproject.toml`.
- Validate version consistency across package metadata, plugin manifest, and archive.

### 5. Control Plane Can Overstate Readiness

The control-plane report shows `pass` with score `100` for multi-agent, token, cost, and security.

This is useful structurally, but most checks are file-presence and placeholder-oriented. They do not prove runtime behavior, integration behavior, or release installability.

Impact:

- The report can be interpreted as stronger than it actually is.

Recommended improvement:

- Split readiness into:
  - `structural_readiness`
  - `behavioral_readiness`
  - `release_readiness`
- Keep the current checks, but label them clearly as structural.
- Add behavioral checks for installed CLI parity, workflow lifecycle execution, plugin install dry-run, and archive integrity.

### 6. Generated Artifacts Are Noisy in the Working Tree

`git status --short` shows many modified/deleted files under `dist/plugins/...`, plus generated report/status changes and untracked tests.

Impact:

- It is hard to distinguish source changes from generated release output.
- Review and release discipline become weaker.

Recommended improvement:

- Decide whether `dist/plugins/` is tracked release output or ignored generated output.
- If generated, ignore it and release from CI/artifacts.
- If tracked, add a release command that fully rebuilds it and produces stable diffs.

## Prioritized Improvement Plan

1. Unify CLI dispatch.
2. Add command parity tests between source script and installed package CLI.
3. Add a single release verification gate.
4. Add plugin archive content validation.
5. Make versioning single-source.
6. Split readiness reports into structural, behavioral, and release readiness.
7. Reduce generated artifact noise in `git status`.

## Commands Executed

```bash
python3 scripts/agentcodex.py validate
python3 scripts/agentcodex.py validate-plugin
python3 -m unittest discover -s .agentcodex/tests
```

Results:

- AgentCodex validation passed.
- Plugin manifest validation passed.
- Unit tests passed: `32` tests.

## Recommended Next Implementation Slice

The highest-value next code change is CLI unification plus parity tests.

Why:

- It directly protects the product entrypoint.
- It reduces duplicated command logic.
- It makes future workflow additions safer.
- It is small enough to complete before deeper release automation.

