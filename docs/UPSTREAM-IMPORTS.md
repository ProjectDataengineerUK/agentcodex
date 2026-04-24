# Upstream Imports

This document tracks the raw import layer copied into AgentCodex from the two upstream frameworks on April 22, 2026.

The goal of this layer is simple:

- preserve as much source material as possible
- make it available locally inside the Codex project
- keep upstream content separated from Codex-native rewrites
- support gradual porting instead of one risky bulk rewrite

## Import Location

All imported upstream content lives under:

- `.agentcodex/imports/agentspec/`
- `.agentcodex/imports/ecc/`

The machine-readable catalog is:

- `.agentcodex/imports/manifest.json`

## Imported From AgentSpec

Source repository:

- `/home/user/Projetos/agentspec`

Imported surfaces:

- `agents`: 60 files
- `commands`: 33 files
- `skills`: 22 files
- `kb`: 333 files
- `sdd`: 9 files
- `.claude`: 460 files
- `plugin-extras/skills`: 2 files
- `plugin/hooks`: 1 file
- `docs`: 5 files
- `README.md`: imported as `.agentcodex/imports/agentspec/readme`
- `CLAUDE.md`: imported as `.agentcodex/imports/agentspec/claude_md`

Practical meaning:

- AgentSpec remains the stronger source for data-engineering domain knowledge
- the `kb/`, `agents/`, and `sdd/` trees are the highest-value porting inputs
- the mirrored `.claude/` tree preserves the original Claude-native surface for reference during Codex rewrites
- `plugin-extras/skills` and `plugin/hooks` preserve extra workflow material that can be translated into explicit Codex checks
- imported files are preserved raw, not yet normalized to Codex conventions

## Imported From Everything-Claude-Code

Source repository:

- `/home/user/Projetos/everything-claude-code`

Imported surfaces:

- `AGENTS.md`: imported as `.agentcodex/imports/ecc/agents_md`
- `agents`: 48 files
- `commands`: 79 files
- `skills`: 288 files
- `rules`: 89 files
- `contexts`: 3 files
- `.codex`: 5 files
- `docs`: 755 files
- `docs/pt-BR`: 47 files
- `scripts/ci`: 10 files
- `schemas`: 10 files
- `manifests`: 3 files
- `README.md`: imported as `.agentcodex/imports/ecc/readme`
- `COMMANDS-QUICK-REF.md`: imported as `.agentcodex/imports/ecc/commands_quick_ref`

Practical meaning:

- ECC remains the stronger source for Codex operating patterns
- `AGENTS.md`, `.codex`, `skills`, `rules`, and `commands` form the main runtime reference layer
- the mirrored `docs`, `scripts/ci`, `schemas`, and `manifests` provide direct input for validation, installation, and governance work
- imported files are preserved raw, then selectively adapted into AgentCodex-native docs and tooling

## Current Totals

Current raw imports copied into AgentCodex:

- `agentspec`: 927 files
- `everything-claude-code`: 1340 files
- total: 2267 files

## How To Use The Imports

Use the raw import layer as source material, not as the primary runtime contract.

Prefer this order:

1. `AGENTS.md`
2. `docs/`
3. `.agentcodex/kb/`
4. `.agentcodex/routing/`
5. `.agentcodex/imports/*` for upstream reference and porting

That keeps Codex-facing behavior stable while still exposing the original frameworks in full where practical.

## Re-Import

To refresh the raw import layer:

```bash
agentcodex import-upstreams all
```

To refresh only one upstream:

```bash
agentcodex import-upstreams agentspec
agentcodex import-upstreams ecc
```

## KB Sync Automation

AgentCodex can also sync selected local KB domains from the imported upstream KB layer.

Configuration lives in:

- `.agentcodex/kb/upstream-sync.json`

Dry run:

```bash
agentcodex sync-kb-upstreams
```

Refresh upstream imports first, then apply KB changes:

```bash
agentcodex sync-kb-upstreams --refresh-imports --apply
```

Sync only one domain:

```bash
agentcodex sync-kb-upstreams --domain lakeflow --apply
```

Current automation syncs mapped domains from imported AgentSpec KB sources into `.agentcodex/kb/` for:

- `index.md`
- `quick-reference.md`
- `concepts/`
- `patterns/`
- `reference/`
- `specs/`
