# Plugin Distribution

This document describes the current AgentCodex plugin distribution workflow for Codex and the intended end-user experience after publication.

## End-user experience

The target user flow is:

1. install the `AgentCodex` plugin in Codex
2. open a target repository in Codex
3. ask Codex:

```text
Install AgentCodex in this repository.
```

The plugin then applies:

- `AGENTS.md`
- `.codex/`
- `.agentcodex/`

No source-repo clone should be required for the end user.

## What exists today

The repository contains:

- plugin manifest: `plugins/agentcodex/.codex-plugin/plugin.json`
- plugin skill: `plugins/agentcodex/skills/install-agentcodex/SKILL.md`
- plugin installer: `plugins/agentcodex/scripts/install_runtime.py`
- local marketplace entry: `.agents/plugins/marketplace.json`
- runtime bundle builder: `scripts/build_plugin_runtime.py`
- plugin packager: `scripts/package_plugin.py`

The runtime bundle is the key piece that removes the need for end users to clone the AgentCodex source repository.

## Official Codex surfaces

OpenAI documents that Codex supports:

- plugins
- a plugins library
- creating a new plugin from within Codex

Sources:

- [Plugins and skills](https://openai.com/academy/codex-plugins-and-skills)
- [Working with Codex](https://openai.com/academy/working-with-codex)

What is not yet explicit in the public docs we checked:

- a step-by-step plugin publishing pipeline
- a canonical packaging/upload command for third-party plugins

Because of that, the packaging and release mechanics below are an implementation strategy for AgentCodex, not a verbatim OpenAI-published release procedure.

## Maintainer release preparation

Build the plugin runtime bundle:

```bash
python3 scripts/build_plugin_runtime.py
```

These commands are for plugin packaging and release validation. They are not the intended end-user installation flow.

## Package the plugin

After building the runtime bundle:

```bash
python3 scripts/package_plugin.py
```

This generates:

- `dist/plugins/agentcodex-plugin-0.1.0.tar.gz`

That archive contains the plugin plus the bundled runtime payload.

## Release checklist

1. Update the plugin version in `plugins/agentcodex/.codex-plugin/plugin.json`.
2. Replace `[TODO: ...]` metadata fields in the plugin manifest.
3. Confirm these manifest fields before publishing:
   - `author.email`
   - `author.url`
   - `homepage`
   - `repository`
   - `interface.websiteURL`
   - `interface.privacyPolicyURL`
   - `interface.termsOfServiceURL`
4. Ensure the plugin card text matches the intended release:
   - `description`
   - `interface.shortDescription`
   - `interface.longDescription`
   - `interface.defaultPrompt`
5. Run `python3 scripts/build_plugin_runtime.py`.
6. Run `python3 scripts/package_plugin.py`.
7. Verify the archive contents.
8. Validate the published plugin flow in Codex by asking:
   - `Install AgentCodex in this repository.`
9. Publish the plugin through the Codex plugin surface your team uses.

## Manifest fields to finalize

Current placeholders still require a real publication context:

- `plugins/agentcodex/.codex-plugin/plugin.json`

Fields still intentionally unresolved:

- `author.email`

Repository-local source documents now exist at:

- `docs/PRIVACY.md`
- `docs/TERMS.md`
- `docs/PRIVACY-SHORT.md`
- `docs/TERMS-SHORT.md`

The short versions are intended for marketplace-facing publication pages, while the full versions remain the canonical repo copies.

These should be published at real public URLs and then copied into the manifest fields above. Do not publish the plugin with placeholder values.

Recommended public paths:

- `https://<your-domain>/privacy`
- `https://<your-domain>/terms`

Acceptable alternative paths:

- `https://<your-domain>/legal/privacy`
- `https://<your-domain>/legal/terms`

Current GitHub-based publication paths for this repository:

- `https://github.com/ProjectDataengineerUK/agentcodex`
- `https://github.com/ProjectDataengineerUK/agentcodex/blob/main/docs/PRIVACY-SHORT.md`
- `https://github.com/ProjectDataengineerUK/agentcodex/blob/main/docs/TERMS-SHORT.md`

## Suggested publication model

Because the public Codex docs currently confirm plugin/library support but do not publish a detailed third-party release CLI, the safest release model is:

1. maintain the plugin in this source repository
2. package a self-contained plugin archive per release
3. register or upload that package through the Codex plugin workflow available in your workspace
4. have the plugin install the scaffold into user repositories from the bundled runtime

## Current gap to close

The remaining publication gap is not the installer logic. It is the public plugin metadata and the actual Codex publication step for your workspace or marketplace.
