# ECC Extension Registry

This document exposes the complete imported Everything-Claude-Code surface as an AgentCodex extension layer.

The registry does not duplicate ECC files into active AgentCodex command or role directories. It references the raw import under `.agentcodex/imports/ecc/` and records what is already active, what is extension-only, and what can be ported later.

## Counts

- commands: 79
- agents: 48
- skills: 183
- rules: 87
- docs: 750
- docs pt-BR: 47
- schemas: 10
- CI validators: 10
- install components: 53
- install modules: 20
- install profiles: 5
- Codex runtime reference files: 5
- active command name matches: 1
- active role name matches: 47

## Codex And OpenCode Coverage

ECC modules that explicitly target Codex or OpenCode:

- `agentic-patterns` (skills): claude, cursor, antigravity, codex, opencode, codebuddy
- `agents-core` (agents): claude, cursor, antigravity, codex, codebuddy
- `business-content` (skills): claude, cursor, antigravity, codex, opencode, codebuddy
- `commands-core` (commands): claude, cursor, antigravity, opencode, codebuddy
- `database` (skills): claude, cursor, antigravity, codex, opencode, codebuddy
- `devops-infra` (skills): claude, cursor, antigravity, codex, opencode, codebuddy
- `document-processing` (skills): claude, cursor, antigravity, codex, opencode, codebuddy
- `framework-language` (skills): claude, cursor, antigravity, codex, opencode, codebuddy
- `hooks-runtime` (hooks): claude, cursor, opencode, codebuddy
- `media-generation` (skills): claude, cursor, codex, opencode, codebuddy
- `operator-workflows` (skills): claude, cursor, antigravity, codex, opencode, codebuddy
- `orchestration` (orchestration): claude, codex, opencode
- `platform-configs` (platform): claude, cursor, antigravity, codex, gemini, opencode, codebuddy
- `research-apis` (skills): claude, cursor, antigravity, codex, opencode, codebuddy
- `security` (skills): claude, cursor, antigravity, codex, opencode, codebuddy
- `social-distribution` (skills): claude, cursor, antigravity, codex, opencode, codebuddy
- `supply-chain-domain` (skills): claude, cursor, antigravity, codex, opencode, codebuddy
- `swift-apple` (skills): claude, cursor, antigravity, codex, opencode, codebuddy
- `workflow-quality` (skills): claude, cursor, antigravity, codex, opencode, codebuddy

## Activation Policy

- default: `reference-only`
- no duplicate rule: Do not duplicate active surfaces: if AgentCodex already has an active command or role with the same filename, keep the ECC source as upstream reference and do not copy it into docs/commands or docs/roles.
- porting rule: Port only through an explicit AgentCodex procedure, role, profile, or validator change with tests.
- runtime rule: Keep Claude/OpenCode hook or slash-command assumptions in the imported layer unless they are normalized to Codex file-based behavior.

## Registry

Machine-readable registry:

- `.agentcodex/ecc-extension.json`

Use that file when selecting ECC material to port into AgentCodex profiles, commands, roles, validators, or runtime docs.
