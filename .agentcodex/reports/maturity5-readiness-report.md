# Maturity 5 Readiness Report

- generated_at: 2026-04-24T00:07:35.833548+00:00
- target: /home/user/Projetos/agentcodex
- baseline: Maturity 5 Project Baseline
- baseline_version: 0.2.0
- profile: data-platform
- profile_name: Maturity 5 Data Platform
- status: pass
- average_score: 100.0

## dataops-foundation

- status: pass
- score: 100

### Evidence

- block contexto: complete
-   complete: /home/user/Projetos/agentcodex/.agentcodex/features/example-project-standard/definition/problem.md
-   complete: /home/user/Projetos/agentcodex/.agentcodex/features/example-project-standard/definition/scope.md
-   complete: /home/user/Projetos/agentcodex/.agentcodex/features/example-project-standard/definition/stakeholders.md
-   complete: /home/user/Projetos/agentcodex/.agentcodex/features/example-project-standard/definition/domain.md
- block arquitetura: complete
-   complete: /home/user/Projetos/agentcodex/.agentcodex/features/example-project-standard/design/architecture.md
-   complete: /home/user/Projetos/agentcodex/.agentcodex/features/example-project-standard/design/data-flow.md
-   complete: /home/user/Projetos/agentcodex/.agentcodex/features/example-project-standard/design/system-diagram.md
-   complete: /home/user/Projetos/agentcodex/.agentcodex/features/example-project-standard/design/decisions/README.md
- block dados: complete
-   complete: /home/user/Projetos/agentcodex/.agentcodex/features/example-project-standard/data/sources.md
-   complete: /home/user/Projetos/agentcodex/.agentcodex/features/example-project-standard/data/storage.md
-   complete: /home/user/Projetos/agentcodex/.agentcodex/features/example-project-standard/data/schemas/README.md
-   complete: /home/user/Projetos/agentcodex/.agentcodex/features/example-project-standard/data/models/README.md
- block execucao: complete
-   complete: /home/user/Projetos/agentcodex/.agentcodex/features/example-project-standard/execution/orchestration.md
-   complete: /home/user/Projetos/agentcodex/.agentcodex/features/example-project-standard/execution/schedules.md
-   complete: /home/user/Projetos/agentcodex/.agentcodex/features/example-project-standard/execution/pipelines/README.md
- block deploy: complete
-   complete: /home/user/Projetos/agentcodex/.agentcodex/features/example-project-standard/deploy/environments.md
-   complete: /home/user/Projetos/agentcodex/.agentcodex/features/example-project-standard/deploy/ci-cd.md
-   complete: /home/user/Projetos/agentcodex/.agentcodex/features/example-project-standard/deploy/infra/README.md
- feature path present: definition/problem.md
- feature path present: design/architecture.md
- feature path present: data/storage.md
- feature path present: execution/orchestration.md
- feature path present: deploy/ci-cd.md
- repo path present: AGENTS.md

### Issues

- none

## governance-and-risk

- status: pass
- score: 100

### Evidence

- block governanca: complete
-   complete: /home/user/Projetos/agentcodex/.agentcodex/features/example-project-standard/controls/governance.md
-   complete: /home/user/Projetos/agentcodex/.agentcodex/features/example-project-standard/controls/ownership.md
-   complete: /home/user/Projetos/agentcodex/.agentcodex/features/example-project-standard/controls/classification.md
-   complete: /home/user/Projetos/agentcodex/.agentcodex/features/example-project-standard/controls/policies.md
- block lineage: complete
-   complete: /home/user/Projetos/agentcodex/.agentcodex/features/example-project-standard/metadata/lineage.md
-   complete: /home/user/Projetos/agentcodex/.agentcodex/features/example-project-standard/metadata/impact-analysis.md
- block access control: complete
-   complete: /home/user/Projetos/agentcodex/.agentcodex/features/example-project-standard/security/access-control.md
-   complete: /home/user/Projetos/agentcodex/.agentcodex/features/example-project-standard/security/roles.md
-   complete: /home/user/Projetos/agentcodex/.agentcodex/features/example-project-standard/security/permissions.md
-   complete: /home/user/Projetos/agentcodex/.agentcodex/features/example-project-standard/security/secrets.md
- block data contracts: complete
-   complete: /home/user/Projetos/agentcodex/.agentcodex/features/example-project-standard/contracts/compatibility.md
-   complete: /home/user/Projetos/agentcodex/.agentcodex/features/example-project-standard/contracts/versioning.md
-   complete: /home/user/Projetos/agentcodex/.agentcodex/features/example-project-standard/contracts/schema-contracts/README.md
-   complete: /home/user/Projetos/agentcodex/.agentcodex/features/example-project-standard/contracts/api-contracts/README.md
- block compliance: complete
-   not_applicable: /home/user/Projetos/agentcodex/.agentcodex/features/example-project-standard/compliance/regulations.md
-   complete: /home/user/Projetos/agentcodex/.agentcodex/features/example-project-standard/compliance/audit.md
- control security: pass (100)
- feature path present: controls/governance.md
- feature path present: metadata/lineage.md
- feature path present: security/access-control.md
- feature path present: contracts/compatibility.md
- feature path present: compliance/audit.md

### Issues

- none

## reliability-and-operations

- status: pass
- score: 100

### Evidence

- block validacao: complete
-   complete: /home/user/Projetos/agentcodex/.agentcodex/features/example-project-standard/validation/data-quality.md
-   complete: /home/user/Projetos/agentcodex/.agentcodex/features/example-project-standard/validation/rules.md
-   complete: /home/user/Projetos/agentcodex/.agentcodex/features/example-project-standard/validation/tests/README.md
- block observabilidade: complete
-   complete: /home/user/Projetos/agentcodex/.agentcodex/features/example-project-standard/operations/observability/metrics.md
-   complete: /home/user/Projetos/agentcodex/.agentcodex/features/example-project-standard/operations/observability/alerts.md
-   complete: /home/user/Projetos/agentcodex/.agentcodex/features/example-project-standard/operations/observability/dashboards.md
-   complete: /home/user/Projetos/agentcodex/.agentcodex/features/example-project-standard/operations/observability/logs.md
- block monitoramento sentinela: complete
-   complete: /home/user/Projetos/agentcodex/.agentcodex/features/example-project-standard/operations/sentinel/architecture.md
-   complete: /home/user/Projetos/agentcodex/.agentcodex/features/example-project-standard/operations/sentinel/watchers.md
-   complete: /home/user/Projetos/agentcodex/.agentcodex/features/example-project-standard/operations/sentinel/analyzers.md
-   complete: /home/user/Projetos/agentcodex/.agentcodex/features/example-project-standard/operations/sentinel/interpreters.md
- block operacao: complete
-   complete: /home/user/Projetos/agentcodex/.agentcodex/features/example-project-standard/integrations/README.md
-   complete: /home/user/Projetos/agentcodex/.agentcodex/features/example-project-standard/kb/domain/README.md
-   complete: /home/user/Projetos/agentcodex/.agentcodex/features/example-project-standard/kb/patterns/README.md
-   complete: /home/user/Projetos/agentcodex/.agentcodex/features/example-project-standard/kb/decisions/README.md
- block custo: complete
-   complete: /home/user/Projetos/agentcodex/.agentcodex/features/example-project-standard/operations/cost/cost-model.md
-   complete: /home/user/Projetos/agentcodex/.agentcodex/features/example-project-standard/operations/cost/optimization.md
- control cost: pass (100)
- control token: pass (100)
- feature path present: validation/data-quality.md
- feature path present: operations/observability/metrics.md
- feature path present: operations/sentinel/architecture.md
- feature path present: operations/cost/cost-model.md
- feature path present: kb/decisions/README.md

### Issues

- none

## automation-and-gates

- status: pass
- score: 100

### Evidence

- block contexto: complete
-   complete: /home/user/Projetos/agentcodex/.agentcodex/features/example-project-standard/definition/problem.md
-   complete: /home/user/Projetos/agentcodex/.agentcodex/features/example-project-standard/definition/scope.md
-   complete: /home/user/Projetos/agentcodex/.agentcodex/features/example-project-standard/definition/stakeholders.md
-   complete: /home/user/Projetos/agentcodex/.agentcodex/features/example-project-standard/definition/domain.md
- block validacao: complete
-   complete: /home/user/Projetos/agentcodex/.agentcodex/features/example-project-standard/validation/data-quality.md
-   complete: /home/user/Projetos/agentcodex/.agentcodex/features/example-project-standard/validation/rules.md
-   complete: /home/user/Projetos/agentcodex/.agentcodex/features/example-project-standard/validation/tests/README.md
- block deploy: complete
-   complete: /home/user/Projetos/agentcodex/.agentcodex/features/example-project-standard/deploy/environments.md
-   complete: /home/user/Projetos/agentcodex/.agentcodex/features/example-project-standard/deploy/ci-cd.md
-   complete: /home/user/Projetos/agentcodex/.agentcodex/features/example-project-standard/deploy/infra/README.md
- control multi-agent: pass (100)
- control token: pass (100)
- control cost: pass (100)
- control security: pass (100)
- feature path present: CHECKLIST.md
- repo path present: .agentcodex/project-standard.json
- repo path present: .agentcodex/routing/routing.json

### Issues

- none
