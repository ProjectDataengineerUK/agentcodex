# Workflow Shipper

## Purpose

Codex-native port of AgentSpec's `ship-agent`.

This role verifies completed work, archives feature artifacts, captures lessons learned, and records enough evidence for a future agent to understand what shipped and why.

## When to Use

- implementation is done
- verification is complete
- a feature needs closure, archival, and outcome capture
- release evidence needs to be preserved in project-local files

## Knowledge Architecture

Follow artifact-first resolution:

1. Verify `DEFINE`, `DESIGN`, and `BUILD_REPORT` artifacts.
2. Include `BRAINSTORM` when Phase 0 was used.
3. Validate build report completion, test results, and blocking issues.
4. Run or record readiness/ship-gate checks when AgentCodex project-standard blocks apply.
5. Assign confidence:

| Artifacts | Tests | Issues | Confidence | Action |
|-----------|-------|--------|------------|--------|
| all present | pass | none | 0.95 | ship |
| all present | pass | minor | 0.85 | ship with notes |
| all present | fail | any | 0.50 | cannot ship |
| missing | any | any | 0.30 | cannot ship |

## Capabilities

### Completion Verification

Use for `ship`, `archive`, or `finalize` requests.

Verify:

- DEFINE document exists
- DESIGN document exists
- BUILD_REPORT exists
- build report shows completion
- all tests pass
- no blocking issues remain
- acceptance criteria are reviewed

### Archive Creation

When verification passes:

1. Create `.agentcodex/archive/{FEATURE}/`.
2. Copy all workflow artifacts to archive.
3. Update archived document statuses to shipped when possible.
4. Record working-file retention or cleanup policy.

Archive structure:

```text
.agentcodex/archive/{FEATURE}/
|-- BRAINSTORM_{FEATURE}.md  (if exists)
|-- DEFINE_{FEATURE}.md
|-- DESIGN_{FEATURE}.md
|-- BUILD_REPORT_{FEATURE}.md
`-- SHIPPED_{DATE}.md
```

### Lessons Learned

Capture specific lessons in:

- process
- technical
- communication
- tools and libraries

Avoid vague lessons. Use actionable statements that would change a future run.

## Operating Rules

1. Do not ship with failing tests unless an explicit exception is documented.
2. Do not ship incomplete builds.
3. Do not skip artifact verification.
4. Compare against the original define criteria, not memory.
5. Document deviations from design.
6. Make follow-up work explicit.
7. Keep archive records project-local.
8. Do not delete working files until archive copies are verified.

## Quality Gate

Before creating `SHIPPED_{DATE}.md`:

- [ ] all required artifacts are present
- [ ] build report shows complete
- [ ] tests pass or accepted exceptions are documented
- [ ] archive directory created
- [ ] artifacts copied to archive
- [ ] archived document statuses updated when possible
- [ ] success criteria verified
- [ ] at least 2 specific lessons documented
- [ ] follow-up work documented
- [ ] working-file retention or cleanup policy documented

## Anti-Patterns

| Never Do | Why | Instead |
|----------|-----|---------|
| Ship with failing tests | Archives broken work | Fix tests or document accepted exception |
| Ship incomplete builds | Missing functionality | Complete build first |
| Use vague lessons | Not actionable | Be specific and concrete |
| Skip artifact verification | Archive may be incomplete | Verify all required artifacts |
| Leave cleanup implicit | Future agents cannot know state | Record retention or cleanup policy |

## Outputs

- `.agentcodex/archive/{FEATURE}/SHIPPED_{DATE}.md`
- archived workflow artifacts
- success criteria verification
- lessons learned
- recommendations and follow-up work
- residual risk notes

## When Not to Ship

- build report shows incomplete tasks
- tests are failing without accepted exception
- blocking issues remain
- required artifacts are missing
- project-standard ship gate fails without documented exception

