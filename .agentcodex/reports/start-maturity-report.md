# DataOps MLOps LLMOps Maturity Report

- generated_at: `2026-04-29T22:56:37.087854+00:00`
- root: `/home/user/Projetos/agentcodex`
- maturity_model: `DataOps + MLOps + LLMOps`
- status: `warn`
- maturity_score: 80.0

## Track Summary

- DATAOPS: pass (100.0) - baseline: `data-platform`
- MLOPS: warn (80.0) - baseline: `start-mlops-track`
- LLMOPS: warn (60.0) - baseline: `agentic-llm`

## Tracks

### DataOps

- id: `DATAOPS`
- status: `pass`
- score: 100.0
- baseline: `data-platform`
- scope: Pipeline, data quality, lineage, contracts, deployment, and governed operations.

#### Checks

- project-standard scaffold: pass (100)
  - note: Feature work is anchored to the AgentCodex Project Standard.
  - present: `.agentcodex/features/example-project-standard/CHECKLIST.md`
- pipeline orchestration: pass (100)
  - note: Pipeline execution, ownership, and schedules are explicit.
  - present: `.agentcodex/features/example-project-standard/execution/orchestration.md`, `.agentcodex/features/example-project-standard/execution/pipelines/README.md`, `.agentcodex/features/example-project-standard/execution/schedules.md`
- data quality gates: pass (100)
  - note: Data quality checks can block release.
  - present: `.agentcodex/features/example-project-standard/validation/data-quality.md`, `.agentcodex/features/example-project-standard/validation/rules.md`, `.agentcodex/features/example-project-standard/validation/tests/README.md`
- lineage and contracts: pass (100)
  - note: Lineage and schema/data contract expectations are visible.
  - present: `.agentcodex/features/example-project-standard/metadata/lineage.md`, `.agentcodex/features/example-project-standard/contracts/schema-contracts/README.md`, `.agentcodex/features/example-project-standard/contracts/compatibility.md`
- deployment and rollback: pass (100)
  - note: Promotion, environment, and rollback paths are documented.
  - present: `.agentcodex/features/example-project-standard/deploy/ci-cd.md`, `.agentcodex/features/example-project-standard/deploy/environments.md`

### MLOps

- id: `MLOPS`
- status: `warn`
- score: 80.0
- baseline: `start-mlops-track`
- scope: Model lifecycle, validation, deployment, monitoring, governance, and cost controls.

#### Checks

- model registry and experiment tracking: fail (0)
  - note: Model versions, training runs, metrics, and approval history are traceable.
  - missing: `.agentcodex/ops/mlops/model-registry.md`, `.agentcodex/ops/mlops/experiments.md`
- model validation gates: pass (100)
  - note: Model validation has explicit checks before release.
  - present: `.agentcodex/features/example-project-standard/validation/rules.md`, `.agentcodex/features/example-project-standard/validation/tests/README.md`
- model deployment and rollback: pass (100)
  - note: Model promotion and rollback are treated as release operations.
  - present: `.agentcodex/features/example-project-standard/deploy/ci-cd.md`, `.agentcodex/features/example-project-standard/deploy/environments.md`
- model monitoring: pass (100)
  - note: Runtime quality, drift, and incident signals have monitoring surfaces.
  - present: `.agentcodex/features/example-project-standard/operations/observability/metrics.md`, `.agentcodex/features/example-project-standard/operations/observability/alerts.md`
- model governance and access: pass (100)
  - note: Ownership, access, and cost controls are part of the model operating surface.
  - present: `.agentcodex/features/example-project-standard/controls/governance.md`, `.agentcodex/features/example-project-standard/security/access-control.md`, `.agentcodex/features/example-project-standard/operations/cost/cost-model.md`

### LLMOps

- id: `LLMOPS`
- status: `warn`
- score: 60.0
- baseline: `agentic-llm`
- scope: LLM model policy, prompt/eval governance, token control, supervision, and quarantine.

#### Checks

- LLM model policy: fail (0)
  - note: Allowed models, routing, token budgets, and governance are explicit.
  - missing: `.agentcodex/ops/agentic-llm/model-policy.md`
- prompt and eval governance: fail (0)
  - note: Prompts, evals, and guardrails are versioned and auditable.
  - missing: `.agentcodex/ops/agentic-llm/prompt-registry.md`, `.agentcodex/ops/agentic-llm/evals.md`, `.agentcodex/ops/agentic-llm/guardrails.md`
- token and cost controls: pass (100)
  - note: Model routing and optimization evidence exist before autonomous expansion.
  - present: `.agentcodex/model-routing.json`, `.agentcodex/features/example-project-standard/operations/cost/optimization.md`
- supervision and quarantine: pass (100)
  - note: Human approval, blocked actions, and quarantine paths are documented.
  - present: `.agentcodex/features/example-project-standard/operations/sentinel/supervision.md`, `.agentcodex/features/example-project-standard/operations/sentinel/quarantine.md`
- API contracts and access: pass (100)
  - note: LLM-facing APIs and access boundaries are governed.
  - present: `.agentcodex/features/example-project-standard/contracts/api-contracts/README.md`, `.agentcodex/features/example-project-standard/security/access-control.md`

## Interpretation

- The repository has usable operating structure but should close the weaker maturity tracks before ship.
- Use `agentcodex maturity5-check <target-project-dir> --profile data-platform` for the executable DataOps gate.
- Use `agentcodex maturity5-check <target-project-dir> --profile agentic-llm` for the executable LLMOps gate.
- MLOps is reported here as a start-time operating track until a dedicated executable profile is added.
