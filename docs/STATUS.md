# Status

Generated status snapshot for AgentCodex.

## Current Surface

- documented roles: 125
- command procedures: 40
- codex agents: 3
- ADRs: 3
- history entries: 7

## Upstream Role Coverage

- coverage report: `docs/ROLE-COVERAGE.md`
- imported AgentSpec files under `.agentcodex/imports/agentspec/agents/`: 60
- imported ECC agents under `.agentcodex/imports/ecc/agents/`: 48
- gross imported AgentSpec + ECC files: 108
- unique imported filename stems: 107
- exact upstream stems already active as AgentCodex roles: 96
- exact upstream stems not active as AgentCodex roles: 11
- AgentCodex-native role stems beyond exact upstream matches: 29

## Project Standard

- manifest: `.agentcodex/project-standard.json`
- version: 0.1.0
- scaffold root: `example-project-standard`
- total blocks: 16

Blocks:
- `contexto`
- `arquitetura`
- `dados`
- `governanca`
- `lineage`
- `execucao`
- `validacao`
- `observabilidade`
- `monitoramento sentinela`
- `access control`
- `data contracts`
- `operacao`
- `deploy`
- `custo`
- `compliance`
- `agentes definidos (se houver)`

## Maturity 5 Baseline

- manifest: `.agentcodex/maturity/maturity5-baseline.json`
- version: 0.2.0
- default profile: `data-platform`
- profiles: 3

Profiles:
- `data-platform`: Maturity 5 Data Platform
- `agentic-llm`: Maturity 5 Agentic LLMOps
- `regulated-enterprise`: Maturity 5 Regulated Enterprise

## Workflow Fidelity

- manifest: `.agentcodex/workflow-fidelity.json`
- version: 0.1.0
- source contract: `.agentcodex/imports/agentspec/sdd/architecture/WORKFLOW_CONTRACTS.yaml`
- phases: 6

Phases:
- `brainstorm`
- `build`
- `define`
- `design`
- `iterate`
- `ship`

## ECC Fidelity

- manifest: `.agentcodex/ecc-fidelity.json`
- version: 0.1.0
- source root: `.agentcodex/imports/ecc`
- preserved surfaces: 10
- codex runtime adaptations: 4
- direct ECC role matches: 13
- validation stack files: 10
- ported ECC validator checks: 5

## ECC Extension Registry

- manifest: `.agentcodex/ecc-extension.json`
- commands: 79
- agents: 48
- skills: 183
- rules: 87
- install modules: 20
- Codex/OpenCode modules: 19
- active command name matches: 1
- active role name matches: 47

## Data Agents Extension Registry

- manifest: `.agentcodex/data-agents-extension.json`
- agents: 12
- commands: 6
- skills: 44
- KB files: 92
- MCP servers: 13
- hooks: 12
- tests: 42
- templates: 5
- mapped agents: 12
- mapped commands: 4

## Model Routing

- manifest: `.agentcodex/model-routing.json`
- version: 0.1.0
- model tiers: 4
- activities: 10
- role overrides: 14
- latest selected model: `gpt-5.3-codex`
- latest activity: `implementation`
- latest tier: `coding`

## Automation

- `agentcodex refresh-all` refreshes generated artifacts and validates the repo
- `agentcodex model-route [task]` records automatic model selection for token and risk control
- `agentcodex readiness-report <target-project-dir>` writes a project readiness report
- `agentcodex ship-gate <target-project-dir>` enforces readiness before ship
- `agentcodex control-plane-check <target-project-dir>` scores multi-agent, token, cost, and security/compliance readiness
- `agentcodex maturity5-check <target-project-dir> [--profile <profile-id>]` evaluates the executable DataOps + LLMOps maturity baseline
- `agentcodex install-local-automation` prepares repo-local git hooks when a `.git` root exists

## Control Plane

- `agentcodex control-plane-check <target-project-dir>` is the authoritative enterprise gate for `multi-agent`, `token`, `cost`, and `security`
- `agentcodex enterprise-readiness <target-project-dir>` is a concise alias for the same control-plane evaluation
- `fail` means a structural gap that blocks enterprise readiness
- `warn` means the surface exists but still contains placeholder or incomplete operational content
- `pass` means the evaluated control surface has no detected gaps in the current file-based checks

