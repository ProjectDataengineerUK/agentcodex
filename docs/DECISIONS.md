# Decisions

## D-001: ECC is the Codex runtime baseline

AgentCodex uses ECC patterns for:

- `.codex/config.toml`
- multi-agent role definitions
- Codex-oriented operating guidance

Reason:
ECC already models Codex as a first-class target.

## D-002: AgentSpec is the domain and workflow source

AgentSpec remains the source for:

- SDD workflow design
- data-engineering specialist taxonomy
- KB-first operating model
- routing and escalation ideas

Reason:
AgentSpec is stronger than ECC in domain specificity for data engineering.

## D-003: No direct Claude plugin dependency

AgentCodex must not depend on:

- `.claude-plugin`
- Claude slash-command dispatch
- Claude hook runtime
- `${CLAUDE_PLUGIN_ROOT}`

Reason:
Those assumptions break portability to Codex.

## D-004: Files over hidden state

Workflow state should live in repository files rather than opaque plugin state.

Reason:
Codex workflows should be inspectable, versionable, and project-local.

## D-005: Progressive porting

AgentCodex will not attempt a full one-shot migration.

Porting order:

1. runtime baseline
2. workflow semantics
3. specialist roles
4. KB conventions
5. verification layer

Reason:
This reduces migration risk and keeps the port auditable.

## D-006: Port broad strategy agents only when AgentCodex has a native surface for them

Current additions:

- `genai-architect`
- `data-platform-engineer`
- `kb-architect`
- `meeting-analyst`
- `codebase-explorer`
- `planner`
- `code-reviewer`
- `doc-updater`
- `context-optimizer`
- `security-reviewer`
- `refactor-cleaner`
- `tdd-guide`
- `prompt-crafter`
- `llm-specialist`
- `test-generator`
- `build-error-resolver`
- `performance-optimizer`
- `code-documenter`
- `pr-test-analyzer`
- `code-architect`
- `architect`
- `python-developer`
- `docs-lookup`
- `silent-failure-hunter`

Reason:
These two imported agents cover real routing gaps that are broader than a single cloud or implementation detail, and they can be expressed cleanly with the current KB and routing surfaces.

Constraint:
Do not port every imported ECC or AgentSpec agent one-to-one. Port only agents that improve Codex-native routing, local KB use, or project-local workflow execution.
