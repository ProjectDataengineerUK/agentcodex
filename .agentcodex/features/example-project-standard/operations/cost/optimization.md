# Cost Optimization

## optimization levers

- reduce unnecessary agent depth for low-risk tasks
- compact logs, summaries, and memory candidates on a schedule
- align compute class with workload criticality
- prefer incremental processing over full recomputation
- route models by activity, role, budget, context pressure, and risk

## model routing policy

- use `.agentcodex/model-routing.json` as the canonical model selection policy when available
- use `agentcodex model-route` before expensive implementation, review, security, or ship work
- prefer smaller model tiers for status, exploration, and deterministic low-risk tasks
- escalate to frontier tiers only for high-risk security, compliance, production, or architecture arbitration

## tradeoffs

- lower latency often costs more
- more retention improves forensics but increases storage cost
- deeper multi-agent analysis improves quality but raises execution cost
- higher reasoning effort improves safety for ambiguous work but raises token and latency cost

## review cadence

- weekly review for production hot spots
- monthly review for baseline model and platform assumptions

## alert thresholds

- define daily spend threshold
- define abnormal cost spike threshold
- define per-workflow or per-crew anomaly threshold

## automatic selection evidence

- record latest selection in `.agentcodex/reports/model-routing/latest-selection.json`
- record human-readable selection in `.agentcodex/reports/model-routing/model-routing.md`
- retain selected model, activity, role, budget, risk, context status, and selection reasons
