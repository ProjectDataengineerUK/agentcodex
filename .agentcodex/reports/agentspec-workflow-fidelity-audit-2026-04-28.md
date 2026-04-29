# AgentSpec Workflow Fidelity Audit - 2026-04-28

## Scope

This audit compares the current AgentCodex workflow surface against the imported AgentSpec source for the core SDD lifecycle:

- brainstorm
- define
- design
- ship

Primary AgentSpec references:

- `.agentcodex/imports/agentspec/commands/workflow/brainstorm.md`
- `.agentcodex/imports/agentspec/commands/workflow/define.md`
- `.agentcodex/imports/agentspec/commands/workflow/design.md`
- `.agentcodex/imports/agentspec/commands/workflow/ship.md`
- `.agentcodex/imports/agentspec/agents/workflow/*-agent.md`
- `.agentcodex/imports/agentspec/sdd/templates/*_TEMPLATE.md`
- `.agentcodex/imports/agentspec/sdd/architecture/WORKFLOW_CONTRACTS.yaml`

Current AgentCodex surfaces checked:

- `docs/workflow/brainstorm.md`
- `docs/workflow/define.md`
- `docs/workflow/design.md`
- `docs/workflow/ship.md`
- `docs/roles/workflow-brainstormer.md`
- `docs/roles/workflow-definer.md`
- `docs/roles/workflow-designer.md`
- `docs/roles/workflow-shipper.md`
- `.agentcodex/templates/BRAINSTORM_TEMPLATE.md`
- `.agentcodex/templates/DEFINE_TEMPLATE.md`
- `.agentcodex/templates/DESIGN_TEMPLATE.md`
- `.agentcodex/templates/SHIPPED_TEMPLATE.md`
- `.agentcodex/commands/`
- `scripts/project_intake.py`
- `scripts/workflow_orchestrator.py`
- `src/agentcodex_cli/dispatcher.py`

## Executive Finding

AgentCodex has not lost the imported AgentSpec source: the raw AgentSpec command, role, template, and workflow-contract material is present under `.agentcodex/imports/agentspec/`.

However, the active AgentCodex workflow surface is a shortened adaptation. It preserves the phase names and some minimum gates, but it does not carry the full AgentSpec behavior into the Codex-native docs, role prompts, templates, command procedures, or CLI surface. This does make the current AgentCodex weaker than AgentSpec for the core brainstorm -> define -> design -> ship flow.

## Evidence

### Workflow Procedure Size

| Phase | AgentSpec command | AgentCodex workflow doc |
|---|---:|---:|
| brainstorm | 240 lines | 57 lines |
| define | 180 lines | 74 lines |
| design | 174 lines | 80 lines |
| ship | 180 lines | 56 lines |

### Workflow Role Size

| Role | AgentSpec agent | AgentCodex role doc |
|---|---:|---:|
| brainstorm | 199 lines | 32 lines |
| define | 266 lines | 31 lines |
| design | 258 lines | 31 lines |
| ship | 247 lines | 31 lines |

### Workflow Template Size

| Template | AgentSpec | AgentCodex |
|---|---:|---:|
| BRAINSTORM | 215 lines | 67 lines |
| DEFINE | 189 lines | 66 lines |
| DESIGN | 257 lines | 60 lines |
| SHIPPED | 133 lines | 50 lines |

## Functional Gaps

### 1. Workflow commands are not first-class project-local commands

`.agentcodex/commands/` does not include:

- `brainstorm.md`
- `define.md`
- `design.md`
- `build.md`
- `ship.md`
- `iterate.md`

The workflow exists in `docs/workflow/`, but the project-local command directory only exposes adjacent commands such as `pipeline`, `review`, `schema`, `project-intake`, and `orchestrate-workflow`.

Impact: the AgentSpec lifecycle is documented, but not represented as first-class command procedures in the same local command surface used by the rest of AgentCodex.

### 2. Brainstorm is materially simplified

AgentSpec includes:

- one-question-at-a-time discovery
- minimum 3 questions
- sample data collection for LLM grounding
- explicit approach comparison
- YAGNI removal table
- incremental validation by section
- selected approach and rejected alternatives
- data engineering context
- suggested requirements for define

The current AgentCodex brainstorm doc/template keeps the general outline, but omits or weakens sample inventory, incremental validation, session summary, decision log depth, data-engineering context, and suggested define-ready requirements.

Impact: brainstorm can become a lightweight idea summary instead of the AgentSpec dialogue and grounding phase.

### 3. Define is materially simplified

AgentSpec includes:

- input classification
- entity extraction
- clarity score thresholds
- targeted clarification with options when score is below 12/15
- technical-context questions
- data engineering context extraction
- data contract section with source inventory, schema, freshness, completeness, and lineage
- assumptions with impact if false
- score breakdown
- revision history

The current AgentCodex define template retains problem, users, goals, success criteria, constraints, out of scope, and clarity score, but it does not preserve the full score breakdown, data contract depth, assumptions table, technical-context prompts, or detailed clarification behavior.

Impact: define can pass with a shallow requirements artifact, especially for data engineering projects.

### 4. Design is materially simplified

AgentSpec includes:

- architecture diagram conventions
- components table
- inline ADRs
- agent assignment rationale
- KB-derived code patterns
- detailed data flow
- integration points
- testing strategy with coverage goals
- error handling
- configuration
- security considerations
- observability
- pipeline architecture with DAG, partitions, incremental strategy, schema evolution, and data quality gates

The current AgentCodex design template keeps architecture, flow, manifest, dependencies, implementation strategy, tests, risks, and open decisions, but omits the stronger AgentSpec sections for components, ADR detail, code patterns, error handling, configuration, security, observability, and pipeline-specific design.

Impact: design can become a short implementation plan instead of an executable architecture contract.

### 5. Ship is materially simplified

AgentSpec includes:

- completion verification
- archive folder creation
- artifact copying
- status updates to prior documents
- working-file cleanup
- timeline
- metrics
- built components and files
- success-criteria verification
- lessons by process, technical, communication, tools
- archived artifacts
- explicit when-not-to-ship rules

The current AgentCodex ship template keeps delivered outcome, acceptance review, deviations, lessons, follow-up, risks, and project-standard gate, but omits the richer timeline, metrics, artifact inventory, built-file inventory, success-criteria verification table, and status update/cleanup procedure.

Impact: ship can become a closeout note instead of a reproducible release/archive record.

### 6. Validation passes despite fidelity loss

`python3 scripts/validate_agentcodex.py` passes, but its checks only require minimum markers such as:

- `## Candidate Approaches`
- `## Recommendation`
- `## Exit Check`
- `## Success Criteria`
- `## Acceptance Criteria`
- `## Clarity Score`
- `## File Manifest`
- `## Test Strategy`
- `## Lessons Learned`

The validator does not compare AgentCodex templates, roles, or workflow docs against the imported AgentSpec workflow contract.

Impact: the repo can report healthy while the AgentSpec workflow has been compressed.

## Assessment

The current AgentCodex implementation is a Codex-native adaptation, but it is not a full-content port of AgentSpec. It is best described as:

- AgentSpec source preserved: yes
- AgentSpec workflow names preserved: yes
- AgentSpec intent partially preserved: yes
- AgentSpec workflow content fully preserved in active AgentCodex surfaces: no
- AgentCodex weakened versus AgentSpec for brainstorm/define/design/ship: yes

## Recommended Remediation

### Priority 1: Restore full workflow procedures

Create Codex-native command procedure files:

- `.agentcodex/commands/brainstorm.md`
- `.agentcodex/commands/define.md`
- `.agentcodex/commands/design.md`
- `.agentcodex/commands/build.md`
- `.agentcodex/commands/ship.md`
- `.agentcodex/commands/iterate.md`

Use the imported AgentSpec command docs as the content baseline and normalize only:

- `.claude/sdd/` -> `.agentcodex/`
- `${CLAUDE_PLUGIN_ROOT}` -> repo-local paths
- slash-command assumptions -> documented Codex procedure and CLI invocation
- `AskUserQuestion` -> Codex interaction rule: ask one question at a time, use multiple-choice when possible

Do not summarize away the AgentSpec gates.

### Priority 2: Restore full templates

Replace or expand the active templates under `.agentcodex/templates/` using the AgentSpec templates as the baseline, while adding AgentCodex project-standard gates where needed.

The active templates should keep the full AgentSpec sections and add AgentCodex-specific sections, not substitute shorter versions.

### Priority 3: Restore full workflow roles

Expand:

- `docs/roles/workflow-brainstormer.md`
- `docs/roles/workflow-definer.md`
- `docs/roles/workflow-designer.md`
- `docs/roles/workflow-builder.md`
- `docs/roles/workflow-shipper.md`
- `docs/roles/workflow-iterator.md`

The role docs should preserve AgentSpec capabilities, confidence thresholds, anti-patterns, quality gates, and response formats.

### Priority 4: Add fidelity validation

Add validation that fails when active AgentCodex workflow docs/templates drop required AgentSpec sections. The source of truth can be:

- `.agentcodex/imports/agentspec/sdd/architecture/WORKFLOW_CONTRACTS.yaml`
- a new `.agentcodex/workflow-fidelity.json`

Minimum check categories:

- phase command docs exist under `.agentcodex/commands/`
- active templates include all required AgentSpec sections
- role docs include core capabilities, gates, anti-patterns, and handoff rules
- docs/COMMANDS.md lists the workflow commands
- project-intake writes artifacts that satisfy the fuller templates

### Priority 5: Update CLI/routing surface

Add command entries for the core workflow phases to `src/agentcodex_cli/dispatcher.py` and `scripts/agentcodex.py` if the intended user path is CLI-first.

At minimum, document exact invocations in `docs/COMMANDS.md`.

## Suggested Next Work Item

Start with `brainstorm`, because it is the most important behavioral gap and the one the user already corrected in prior work.

Concrete first patch:

1. Create `.agentcodex/commands/brainstorm.md` from `.agentcodex/imports/agentspec/commands/workflow/brainstorm.md`.
2. Normalize paths and remove Claude-only runtime assumptions.
3. Expand `.agentcodex/templates/BRAINSTORM_TEMPLATE.md` from the AgentSpec template.
4. Expand `docs/roles/workflow-brainstormer.md` from `brainstorm-agent.md`.
5. Update validation to require sample inventory, minimum 3 questions, incremental validation, selected/rejected approaches, YAGNI, and suggested define requirements.

## Remediation Status

### 2026-04-28 - Brainstorm restored

Completed:

- added first-class command procedure: `.agentcodex/commands/brainstorm.md`
- added distributable command procedure: `docs/commands/brainstorm.md`
- expanded active template: `.agentcodex/templates/BRAINSTORM_TEMPLATE.md`
- expanded role prompt: `docs/roles/workflow-brainstormer.md`
- expanded workflow doc: `docs/workflow/brainstorm.md`
- listed `docs/commands/brainstorm.md` in `docs/COMMANDS.md`
- updated `scripts/check_bootstrapped_project.py` to require `brainstorm.md` and stronger brainstorm template markers
- updated `scripts/validate_agentcodex.py` to enforce core brainstorm template markers

Verified:

- `python3 scripts/validate_agentcodex.py`
- `python3 scripts/agentcodex.py check-project .`

Remaining high-priority remediation:

1. Restore `define` from the AgentSpec command, role, and template baselines.
2. Restore `design` from the AgentSpec command, role, and template baselines.
3. Restore `ship` from the AgentSpec command, role, and template baselines.
4. Add first-class project-local command procedures for `build` and `iterate`.
5. Expand fidelity validation for all workflow phases, not only brainstorm.

### 2026-04-28 - Define restored

Completed:

- added first-class command procedure: `.agentcodex/commands/define.md`
- added distributable command procedure: `docs/commands/define.md`
- expanded active template: `.agentcodex/templates/DEFINE_TEMPLATE.md`
- expanded role prompt: `docs/roles/workflow-definer.md`
- expanded workflow doc: `docs/workflow/define.md`
- listed `docs/commands/define.md` in `docs/COMMANDS.md`
- updated `scripts/check_bootstrapped_project.py` to require `define.md` and stronger define template markers
- updated `scripts/validate_agentcodex.py` to enforce core define template markers

Restored AgentSpec behaviors:

- input classification
- entity extraction
- MoSCoW goals
- measurable success criteria
- acceptance tests
- technical context gathering
- data contract section when applicable
- assumptions with impact if wrong
- clarity score breakdown with `12/15` gate
- targeted clarification before design

Verified:

- `python3 scripts/validate_agentcodex.py`
- `python3 scripts/agentcodex.py check-project .`

Remaining high-priority remediation:

1. Restore `design` from the AgentSpec command, role, and template baselines.
2. Restore `ship` from the AgentSpec command, role, and template baselines.
3. Add first-class project-local command procedures for `build` and `iterate`.
4. Expand fidelity validation for all workflow phases.

### 2026-04-28 - Design restored

Completed:

- added first-class command procedure: `.agentcodex/commands/design.md`
- added distributable command procedure: `docs/commands/design.md`
- expanded active template: `.agentcodex/templates/DESIGN_TEMPLATE.md`
- expanded role prompt: `docs/roles/workflow-designer.md`
- expanded workflow doc: `docs/workflow/design.md`
- listed `docs/commands/design.md` in `docs/COMMANDS.md`
- updated `scripts/check_bootstrapped_project.py` to require `design.md` and stronger design template markers
- updated `scripts/validate_agentcodex.py` to enforce core design template markers

Restored AgentSpec behaviors:

- KB pattern loading from define's domains
- ASCII architecture overview
- component mapping
- inline ADR-style key decisions
- complete file manifest
- role/agent assignment rationale
- code/config pattern sections
- testing strategy
- error handling
- configuration
- security considerations
- observability
- pipeline architecture with DAG, partition, incremental, schema evolution, and data quality gates when applicable

Verified:

- `python3 scripts/validate_agentcodex.py`
- `python3 scripts/agentcodex.py check-project .`

Remaining high-priority remediation:

1. Restore `ship` from the AgentSpec command, role, and template baselines.
2. Add first-class project-local command procedures for `build` and `iterate`.
3. Expand fidelity validation for all workflow phases.

### 2026-04-28 - Ship restored

Completed:

- added first-class command procedure: `.agentcodex/commands/ship.md`
- added distributable command procedure: `docs/commands/ship.md`
- expanded active template: `.agentcodex/templates/SHIPPED_TEMPLATE.md`
- expanded role prompt: `docs/roles/workflow-shipper.md`
- expanded workflow doc: `docs/workflow/ship.md`
- listed `docs/commands/ship.md` in `docs/COMMANDS.md`
- updated `scripts/check_bootstrapped_project.py` to require `ship.md` and stronger shipped template markers
- updated `scripts/validate_agentcodex.py` to enforce core shipped template markers

Restored AgentSpec behaviors:

- completion verification
- ship readiness matrix
- archive structure
- artifact copying expectations
- timeline
- metrics
- what-was-built inventory
- success criteria verification
- acceptance review
- deviations from design
- lessons learned by category
- recommendations for future work
- archived artifact inventory
- explicit when-not-to-ship behavior through the role doc

AgentCodex-specific behavior retained:

- project-standard readiness and ship-gate recording
- working-file retention policy instead of unconditional deletion
- project-local archive paths under `.agentcodex/archive/`

Verified:

- `python3 scripts/validate_agentcodex.py`
- `python3 scripts/agentcodex.py check-project .`

Current fidelity status:

- `brainstorm`: restored
- `define`: restored
- `design`: restored
- `ship`: restored

Remaining remediation outside the user's named core flow:

1. Restore `build` from the AgentSpec command, role, and template baselines.
2. Add or restore first-class project-local command procedure for `iterate`.
3. Continue expanding fidelity validation beyond marker checks.

### 2026-04-29 - Build restored

Completed:

- added first-class command procedure: `.agentcodex/commands/build.md`
- added distributable command procedure: `docs/commands/build.md`
- expanded active template: `.agentcodex/templates/BUILD_REPORT_TEMPLATE.md`
- expanded role prompt: `docs/roles/workflow-builder.md`
- expanded workflow doc: `docs/workflow/build.md`
- listed `docs/commands/build.md` in `docs/COMMANDS.md`
- updated `scripts/check_bootstrapped_project.py` to require `build.md` and stronger build-report template markers
- updated `scripts/validate_agentcodex.py` to enforce core build-report template markers

Restored AgentSpec behaviors:

- design-first execution
- file-manifest task extraction
- dependency ordering
- role/agent attribution
- incremental verification
- build report generation
- deviations from design
- blocker recording
- acceptance test verification
- data-engineering verification section

AgentCodex-specific strengthening added:

- security review section
- explicit files-created and files-modified sections
- residual risk table
- exact verification commands section

Verified:

- `python3 scripts/validate_agentcodex.py`
- `python3 scripts/agentcodex.py check-project .`

Current fidelity status:

- `brainstorm`: restored
- `define`: restored
- `design`: restored
- `build`: restored
- `ship`: restored

Remaining remediation:

1. Restore `iterate` from the AgentSpec command and role baselines.
2. Continue expanding fidelity validation beyond marker checks.

### 2026-04-29 - Iterate restored

Completed:

- added first-class command procedure: `.agentcodex/commands/iterate.md`
- added distributable command procedure: `docs/commands/iterate.md`
- expanded role prompt: `docs/roles/workflow-iterator.md`
- expanded workflow doc: `docs/workflow/iterate.md`
- listed `docs/commands/iterate.md` in `docs/COMMANDS.md`
- updated `scripts/check_bootstrapped_project.py` to require `iterate.md`

Restored AgentSpec behaviors:

- target document phase detection
- change classification as additive, modifying, removing, or architectural
- downstream cascade analysis
- explicit user decision for material cascades
- revision-history bumping
- update earliest affected artifact first
- design-first rule before rebuilding code
- escalation to define/design/build roles when changes cross those boundaries

Current fidelity status:

- `brainstorm`: restored
- `define`: restored
- `design`: restored
- `build`: restored
- `ship`: restored
- `iterate`: restored

Remaining remediation:

1. Continue expanding fidelity validation beyond marker checks.

### 2026-04-29 - Fidelity validation contract added

Completed:

- added `.agentcodex/workflow-fidelity.json` as the repo-local executable fidelity contract
- linked the contract to the imported AgentSpec source contract at `.agentcodex/imports/agentspec/sdd/architecture/WORKFLOW_CONTRACTS.yaml`
- added validation for active command procedures, role prompts, workflow docs, and templates
- updated `scripts/validate_agentcodex.py` so validation fails when required AgentSpec-derived behaviors disappear from active AgentCodex surfaces
- tightened `define` command wording to make `Input Classification` and `Data Contract` explicit
- tightened `build` command wording to require explicit `Verification Commands`
- updated `scripts/generate_status_doc.py` so `docs/STATUS.md` reports the fidelity contract

Verified:

- `python3 scripts/validate_agentcodex.py`
- `python3 scripts/agentcodex.py check-project .`

Current fidelity status:

- `brainstorm`: restored and covered by fidelity validation
- `define`: restored and covered by fidelity validation
- `design`: restored and covered by fidelity validation
- `build`: restored and covered by fidelity validation
- `ship`: restored and covered by fidelity validation
- `iterate`: restored and covered by fidelity validation

Remaining remediation:

1. Expand the fidelity contract from marker checks into structural checks, such as minimum required sections in order and template/table expectations.
2. Add regression tests that intentionally remove a critical workflow behavior and assert validation fails.

### 2026-04-29 - Fidelity regression tests added

Completed:

- added `.agentcodex/tests/test_workflow_fidelity_validation.py`
- covered the success path for a complete workflow fidelity contract
- covered the failure path when a required phase behavior marker is missing
- verified the test mutates only a temporary contract and temporary surfaces

Verified:

- `python3 -m unittest discover -s .agentcodex/tests -p 'test_workflow_fidelity_validation.py'`
- `python3 -m unittest discover -s .agentcodex/tests -p 'test_*.py'`
- `python3 scripts/validate_agentcodex.py`

Remaining remediation:

1. Expand the fidelity contract from marker checks into structural checks, such as minimum required sections in order and template/table expectations.
2. Add full-command integration tests that run `scripts/validate_agentcodex.py` against a temporary copied repo surface with a deliberately weakened workflow file.
