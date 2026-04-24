# Status

Generated status snapshot for AgentCodex.

## Current Surface

- documented roles: 66
- command procedures: 14
- codex agents: 3
- ADRs: 3
- history entries: 4

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

## Automation

- `agentcodex refresh-all` refreshes generated artifacts and validates the repo
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

