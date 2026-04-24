# AgentCodex KB

This directory is the Codex-native local knowledge base layer for AgentCodex.

Its purpose is to preserve the most valuable domain guidance from AgentSpec without depending on Claude plugin mechanics.

## Principles

1. Local-first: prefer these docs before external browsing when the topic is covered here.
2. Focused: port only the domains that materially improve Codex workflows.
3. Auditable: keep the structure simple and inspectable.
4. Workflow-aware: domains should support the SDD lifecycle, not float independently.

## Initial Domains

- `dbt`
- `spark`
- `data-quality`
- `data-modeling`
- `orchestration`
- `genai`

## Structure

Each domain should converge toward:

```text
domain/
├── index.md
├── quick-reference.md
├── concepts/
└── patterns/
```
