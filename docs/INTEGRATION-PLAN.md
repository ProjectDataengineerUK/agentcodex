# AgentSpec on Codex Using ECC

## Goal

Build a Codex-native framework that preserves the useful parts of AgentSpec while using ECC as the operational base layer.

## Strategy

Use a three-layer architecture:

1. **Runtime Layer**
   ECC-style Codex configuration, role definitions, and execution norms
2. **Workflow Layer**
   AgentSpec's SDD lifecycle adapted into Codex-native procedures
3. **Domain Layer**
   AgentSpec's data-engineering agents and knowledge-base structure, normalized for Codex

## Integration Model

### Layer 1: ECC Runtime

Adopt from ECC:

- `AGENTS.md` as the primary instruction surface
- `.codex/config.toml`
- `.codex/agents/*.toml`
- multi-agent usage patterns
- MCP and sandbox expectations where relevant

### Layer 2: AgentSpec Workflow

Port from AgentSpec:

- `brainstorm`
- `define`
- `design`
- `build`
- `ship`
- `iterate`

Adaptation:

- commands become procedures and templates
- hook-enforced transitions become documented gates
- plugin-managed state becomes repo-local files

### Layer 3: AgentSpec Domain System

Port from AgentSpec:

- workflow agents
- domain specialist agents
- KB domain taxonomy
- routing and escalation model

Adaptation:

- agent frontmatter becomes Codex role metadata or instruction blocks
- `agent-router` becomes a Codex-readable routing guide
- plugin path references become repo-local paths

## Workstreams

### W1: Runtime Baseline

Deliverables:

- `AGENTS.md`
- `.codex/config.toml`
- role configs

Success:

- Codex can run with no Claude-specific dependency

### W2: Workflow Port

Deliverables:

- workflow docs for each SDD phase
- project-local file conventions
- transition rules

Success:

- user can execute the 5-phase workflow from Codex prompts alone

### W3: Agent Port

Deliverables:

- ported workflow roles
- selected specialist roles
- escalation map

Success:

- Codex can route work between generic and specialist roles without Claude plugin semantics

### W4: KB Port

Deliverables:

- local KB index
- domain-loading rules
- references normalized for Codex

Success:

- domain reasoning is reproducible and local-first

### W5: Verification Layer

Deliverables:

- explicit review gates
- verification checklists
- repeatable build/test/review loops

Success:

- previous hook-dependent assurances are replaced by reproducible checks

## Risks

### Risk 1: Claude-only assumptions remain embedded

Examples:

- `${CLAUDE_PLUGIN_ROOT}`
- slash command semantics
- hook lifecycle expectations

Mitigation:

- reject these references during porting review

### Risk 2: Over-porting too early

Mitigation:

- start with workflow and top-value roles
- defer long-tail agents until the operating model is stable

### Risk 3: Domain quality drops during translation

Mitigation:

- preserve AgentSpec domain terminology
- validate each port against original KB intent

## Definition of Done

AgentCodex is ready when:

1. a Codex user can follow the SDD workflow using only repo-local artifacts
2. specialist roles can be invoked without Claude plugin infrastructure
3. data-engineering domain guidance is preserved
4. no critical path depends on Claude-only features
