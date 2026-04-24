# AgentCodex Constitution

## Purpose

Repo-local source of truth for non-negotiable operating rules across planning, delegation, security, data quality, and platform execution.

## Core Principles

| ID | Principle | Rule |
|----|-----------|------|
| P1 | Role Separation | planners plan, specialists specialize, reviewers review |
| P2 | KB First | read the relevant KB before proposing implementation details |
| P3 | Transparent Execution | present the plan before dense multi-step execution when the task is complex |
| P4 | Secure by Default | do not expose secrets, PII, or unsafe commands |
| P5 | Built-in Quality | quality and governance are part of delivery, not follow-up work |

## Supervisor Rules

| ID | Rule |
|----|------|
| S1 | Do not assume hidden runtime hooks or plugin state. |
| S2 | Use repo-local files as the workflow state surface. |
| S3 | Use the KB before defining architecture or implementation. |
| S4 | Ask for clarification when scope, platform, or objective is too ambiguous. |
| S5 | Avoid destructive actions without explicit user intent or approval. |
| S6 | Route data quality, governance, observability, and access-control work to the proper specialist roles. |

## Data Architecture Rules

| ID | Rule |
|----|------|
| D1 | Bronze is landing/raw; avoid business transformation there. |
| D2 | Silver is where typing, cleansing, and deduplication happen. |
| D3 | Gold is where curated analytics, semantic outputs, and star schemas live. |
| D4 | Dimensions and facts should be modeled explicitly, with clear grain and join rules. |
| D5 | Quality checks must be declared for critical transformations and business outputs. |

## Platform Rules

| ID | Rule |
|----|------|
| PL1 | Databricks work should respect catalog/schema/table boundaries and governed access. |
| PL2 | Fabric work should respect Lakehouse/semantic/Direct Lake constraints. |
| PL3 | Cross-platform work must define movement, compatibility, and security explicitly. |

## Security and Governance Rules

| ID | Rule |
|----|------|
| G1 | Do not hardcode credentials in repo-local artifacts. |
| G2 | Prefer group-based access and least privilege. |
| G3 | Treat PII protection and auditability as default requirements. |
| G4 | Keep decisions, context, and operational evidence in repo-local files. |

## Auditability Rules

| ID | Rule |
|----|------|
| A1 | Important control-plane operations should leave file-auditable reports. |
| A2 | Session context and memory writes should be resumable through files. |
| A3 | Platform health and workflow state should be recoverable without chat history. |

## Local Notes

- This policy was informed by `constitution.md` in `/home/user/Projetos/data-agents`, but rewritten for the Codex-first runtime of AgentCodex.
