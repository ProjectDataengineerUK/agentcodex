# Judge Layer

AgentCodex includes an opt-in Judge Layer adapted from AgentSpec v3.2.

It sends a target file or stdin content to OpenRouter for a second-model review and writes usage to:

- `.agentcodex/storage/judge-ledger.jsonl`

The judge is advisory. Do not send secrets, customer data, payment data, health data, or confidential code.

## Setup

```bash
export OPENROUTER_API_KEY=sk-or-v1-...
```

Optional:

```bash
export JUDGE_MODEL=openai/gpt-4o
export JUDGE_BUDGET=25
```

## Usage

```bash
python3 scripts/agentcodex.py judge path/to/file.py --context "review before merge"
python3 scripts/agentcodex.py judge .agentcodex/features/DESIGN_FEATURE.md --phase design
python3 scripts/agentcodex.py judge --ledger
```

Exit codes:

| Code | Meaning |
|---|---|
| 0 | PASS |
| 1 | FAIL |
| 2 | config or input error |
| 3 | daily budget exhausted |
| 4 | network or OpenRouter API error |

## Phase Prompts

- `generic`: general code or content review
- `define`: requirements clarity, acceptance criteria, assumptions, scope
- `design`: architecture, edge cases, security, rollback, data/model risks
- `build`: concrete bugs, unsafe SQL, error handling, resource leaks, API misuse
