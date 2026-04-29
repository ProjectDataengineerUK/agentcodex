# Everything-Claude-Code Adherence Report - 2026-04-29

## Scope

This report compares the current AgentCodex surface against the raw
Everything-Claude-Code import preserved under `.agentcodex/imports/ecc/`.

Primary source:

- upstream local source: `/home/user/Projetos/everything-claude-code`
- imported source root: `.agentcodex/imports/ecc/`
- generated catalog: `docs/UPSTREAM-CATALOG.md`
- import manifest: `.agentcodex/imports/manifest.json`

AgentCodex surfaces checked:

- `AGENTS.md`
- `.codex/config.toml`
- `.codex/agents/*.toml`
- `docs/commands/`
- `.agentcodex/commands/`
- `docs/roles/`
- `scripts/`
- `.agentcodex/scripts/`
- `docs/STATUS.md`

## Raw ECC Import Numbers

From `.agentcodex/imports/manifest.json`, the current ECC import contains:

- total files: `1340`
- `AGENTS.md`: `1`
- agents: `48`
- commands: `79`
- skills tree files: `288`
- current skill entrypoints: `183` `SKILL.md` files
- rules files: `89`
- current rule markdown files excluding README files: `87`
- contexts: `3`
- Codex config/agent files: `5`
- docs: `755`
- docs/pt-BR: `47`
- CI validators: `10`
- schemas: `10`
- manifests: `3`
- README: `1`
- commands quick reference: `1`

## AgentCodex Current Numbers

Current AgentCodex runtime/documented surface:

- active command procedures in `docs/commands/`: `37`
- project-local command procedures in `.agentcodex/commands/`: `36`
- active role docs in `docs/roles/`: `66`
- Codex agent configs in `.codex/agents/`: `3`
- Project Standard blocks: `16`
- Maturity 5 profiles: `3`
- workflow fidelity phases: `6`

Relevant AgentCodex validation and operation scripts already present:

- `scripts/validate_agentcodex.py`
- `scripts/check_bootstrapped_project.py`
- `scripts/validate_plugin_manifest.py`
- `scripts/package_plugin.py`
- `scripts/control_plane_check.py`
- `scripts/project_readiness_report.py`
- `scripts/project_ship_gate.py`
- `scripts/platform_health.py`
- `scripts/maturity5_check.py`
- `.agentcodex/scripts/validate_kb_contracts.py`

## Direct Coverage

### Codex Runtime Surface

ECC imports a Codex-native reference surface:

- `.agentcodex/imports/ecc/codex/config.toml`
- `.agentcodex/imports/ecc/codex/AGENTS.md`
- `.agentcodex/imports/ecc/codex/agents/explorer.toml`
- `.agentcodex/imports/ecc/codex/agents/reviewer.toml`
- `.agentcodex/imports/ecc/codex/agents/docs-researcher.toml`

AgentCodex implements the same core runtime pattern through:

- `.codex/config.toml`
- `.codex/agents/explorer.toml`
- `.codex/agents/reviewer.toml`
- `.codex/agents/domain-researcher.toml`

Assessment:

- Runtime-surface adherence is strong for the Codex-first model.
- AgentCodex intentionally replaces ECC `docs-researcher` with a domain-specific
  `domain-researcher` focused on AgentSpec-derived data-engineering workflows.
- AgentCodex omits ECC's broad MCP defaults from project config. This is a
  conservative product decision because AgentCodex currently favors local
  evidence and repo-local KB before network-backed MCP dependencies.

### Role Coverage

ECC imported agents: `48`

AgentCodex active role docs: `66`

Direct filename matches between ECC agents and AgentCodex roles: `13`

Matched roles:

- `architect.md`
- `build-error-resolver.md`
- `code-architect.md`
- `code-reviewer.md`
- `doc-updater.md`
- `docs-lookup.md`
- `performance-optimizer.md`
- `planner.md`
- `pr-test-analyzer.md`
- `refactor-cleaner.md`
- `security-reviewer.md`
- `silent-failure-hunter.md`
- `tdd-guide.md`

Assessment:

- AgentCodex has broader active role count by number.
- AgentCodex is not a direct role-name mirror of ECC.
- The strongest direct ECC alignment is in generic engineering roles:
  planning, architecture, review, security, tests, docs, refactor, performance,
  and build-error resolution.
- Missing direct ECC role mirrors are mostly language/framework specialists,
  autonomous loop roles, open-source workflow roles, and frontend/product
  specialists.

### Command Coverage

ECC imported command procedures: `79`

AgentCodex active command procedures: `37`

Direct filename matches between ECC commands and AgentCodex commands: `0`

Assessment:

- Command-name adherence to ECC is currently weak by direct count.
- This is not the same kind of gap as AgentSpec workflow adherence. ECC itself
  says `skills/` is the canonical workflow surface and `commands/` is a legacy
  slash-entry compatibility surface.
- AgentCodex has so far translated ECC as an operating model and raw reference
  layer, not as a command-by-command port.

High-value ECC command families not yet represented as first-class AgentCodex
procedures include:

- planning and PRP flow: `plan`, `prp-plan`, `prp-prd`, `prp-implement`,
  `prp-commit`, `prp-pr`
- quality gates: `quality-gate`, `verify`, `test-coverage`, `review-pr`,
  `code-review`
- context/session control: `save-session`, `resume-session`, `sessions`,
  `checkpoint`, `context-budget`
- multi-agent execution: `multi-plan`, `multi-execute`, `multi-workflow`,
  `orchestrate`
- learning/evolution: `learn`, `learn-eval`, `evolve`, `rules-distill`
- skill lifecycle: `skill-create`, `skill-health`
- language-specific review/build/test: Go, Rust, Kotlin, C++, Flutter, Python,
  Gradle

### Rules And Guardrails

ECC imported rules:

- manifest count: `89`
- markdown rules excluding README files: `87`
- rulesets in catalog: `15`

Rulesets:

- `common`
- `cpp`
- `csharp`
- `dart`
- `golang`
- `java`
- `kotlin`
- `perl`
- `php`
- `python`
- `rust`
- `swift`
- `typescript`
- `web`
- `zh`

AgentCodex currently carries a strong but narrower rule surface:

- repo-level `AGENTS.md`
- project standard manifest
- workflow fidelity contract
- maturity baseline
- control-plane/readiness/ship-gate scripts
- local KB and routing manifests

Assessment:

- AgentCodex is aligned with ECC's rule-driven operating idea.
- AgentCodex does not yet expose ECC's language-specific rules as active
  AgentCodex rules, role docs, or project gates.
- This matters most if AgentCodex is expected to serve as a general coding
  platform, not only a Codex-native AgentSpec/data-engineering workflow system.

### Skills Coverage

ECC imported skill tree:

- manifest files copied: `288`
- `SKILL.md` entrypoints currently present: `183`

AgentCodex currently keeps ECC skills as raw reference material under:

- `.agentcodex/imports/ecc/skills/`

Assessment:

- Skill preservation is strong.
- Active skill adaptation is limited.
- AgentCodex does not currently have a first-class AgentCodex skill registry
  that ports ECC skills into the runtime surface.

### CI, Schemas, And Manifests

ECC imported CI validators:

- `validate-install-manifests.js`
- `check-unicode-safety.js`
- `validate-rules.js`
- `validate-hooks.js`
- `validate-skills.js`
- `validate-commands.js`
- `validate-agents.js`
- `validate-no-personal-paths.js`
- `validate-workflow-security.js`
- `catalog.js`

ECC imported schemas:

- `ecc-install-config.schema.json`
- `hooks.schema.json`
- `install-components.schema.json`
- `install-modules.schema.json`
- `install-profiles.schema.json`
- `install-state.schema.json`
- `package-manager.schema.json`
- `plugin.schema.json`
- `provenance.schema.json`
- `state-store.schema.json`

ECC imported manifests:

- `install-components.json`
- `install-modules.json`
- `install-profiles.json`

Assessment:

- AgentCodex has its own Python validation stack and plugin validation.
- AgentCodex has not yet ported ECC's install-manifest, rules, skills, hooks,
  command, agent, no-personal-paths, workflow-security, or catalog validators
  as active checks.
- This is the clearest actionable adherence gap after command-family triage.

## Executive Assessment

AgentCodex is adherent to ECC in these areas:

- raw ECC source is preserved locally
- Codex-first runtime configuration pattern exists
- multi-agent explorer/reviewer pattern exists
- project-level `AGENTS.md` is authoritative
- validation is command-driven and reproducible
- repo-local artifacts and manifests are preferred over hidden runtime state
- security, review, planning, docs, TDD, refactor, performance, and build-error
  roles are represented

AgentCodex is not yet fully adherent to ECC in these areas:

- ECC command surface: `0/79` direct command-name coverage
- ECC language-specialist agents: only `13/48` direct role-name coverage
- ECC skills: preserved but not actively registered as AgentCodex runtime skills
- ECC rulesets: preserved but not surfaced as active language/profile gates
- ECC validators: imported but not ported into AgentCodex validation flow
- ECC MCP-heavy docs-researcher config: intentionally not copied into the active
  AgentCodex config

Best current description:

- ECC raw import preservation: strong
- ECC Codex operating-model adherence: strong
- ECC command parity: weak
- ECC skills/rules active parity: partial
- ECC validation parity: partial

## Recommended Next Passes

### Priority 1: Port ECC Validation Contracts

Bring the highest-value ECC validators into the AgentCodex Python validation
stack or wrap them as explicit checks:

- command catalog validation
- role/agent validation
- skill registry validation
- ruleset validation
- no-personal-paths validation
- workflow-security validation
- install-manifest validation

This gives AgentCodex durable ECC-style guardrails without turning the product
into a generic clone.

Status after implementation pass:

- `no-personal-paths`: ported into `scripts/validate_agentcodex.py`
- `workflow-security`: ported into `scripts/validate_agentcodex.py`
- `validate-rules`: ported into `scripts/validate_agentcodex.py`
- `validate-skills`: ported into `scripts/validate_agentcodex.py`
- `validate-commands`: ported into `scripts/validate_agentcodex.py`
- regression tests: `.agentcodex/tests/test_ecc_style_validators.py`
- contract declaration: `.agentcodex/ecc-fidelity.json`

### Priority 2: Add ECC Operating Contract

Create `.agentcodex/ecc-fidelity.json` to declare which ECC surfaces AgentCodex
must preserve, adapt, or intentionally omit.

The contract should distinguish:

- raw preserved source
- active Codex-native runtime surface
- intentional exclusions
- optional extension packs
- validation gates

### Priority 3: Port High-Value Command Families

Do not port all `79` ECC commands blindly. Start with command families that
strengthen AgentCodex's existing product:

- `quality-gate`
- `verify`
- `test-coverage`
- `context-budget`
- `checkpoint`
- `save-session`
- `resume-session`
- `multi-plan`
- `multi-execute`
- `skill-health`
- `rules-distill`

### Priority 4: Surface Rules As Profiles

Map ECC language rulesets into AgentCodex profile overlays:

- Python/data platform profile first
- TypeScript/web profile second
- Rust/Go/Kotlin optional profiles later

This fits AgentCodex's current profile and maturity-gate model better than
copying every ECC rule into the default runtime.

### Priority 5: Decide Skill Runtime Strategy

AgentCodex should either:

- keep ECC skills as imported reference only, or
- create a lightweight AgentCodex skill registry with explicit activation rules.

Until that decision is made, ECC skill adherence should be considered preserved
but not operational.
