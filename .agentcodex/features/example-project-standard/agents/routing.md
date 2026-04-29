# Agent Routing

## Model Selection

- route first by activity, then specialist role, then risk, budget, and context pressure
- use `agentcodex model-route` to persist selected model, tier, effort, and reasons
- use smaller tiers for exploration, status, summaries, and deterministic low-risk updates
- escalate high-risk security, compliance, production, migration, or architecture arbitration to frontier tiers

## Handoff Rules

- watcher outputs hand off to analyzers when repeated signals, threshold breaches, or correlated failures appear
- analyzer outputs hand off to interpreters when a human-readable incident narrative or remediation suggestion is needed
- interpreter outputs hand off to supervisor flow when approval, quarantine, or customer-visible action is involved

## Fallback Rules

- when no project-local specialist exists, fall back to repo-standard roles defined in `AGENTS.md`
- when confidence is low, prefer escalation over autonomous continuation
- when evidence is incomplete, produce a reviewable report instead of an action request

## Escalation Rules

- security incidents escalate to security and Sentinel supervision
- cost spikes escalate to platform and finance owner review
- customer-visible regressions escalate to product and runtime owners
- quarantine candidates require explicit operator review
