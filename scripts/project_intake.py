#!/usr/bin/env python3
from __future__ import annotations

from collections import Counter
from datetime import UTC, datetime
from pathlib import Path
import re
import sys


ROOT = Path.cwd()
FEATURES_ROOT = ROOT / ".agentcodex" / "features"
REPORTS_ROOT = ROOT / ".agentcodex" / "reports"
MAX_SCAN_FILES = 400
CODE_SUFFIXES = {
    ".py": "Python",
    ".js": "JavaScript",
    ".ts": "TypeScript",
    ".tsx": "TSX",
    ".jsx": "JSX",
    ".java": "Java",
    ".go": "Go",
    ".rs": "Rust",
    ".rb": "Ruby",
    ".php": "PHP",
    ".cs": "C#",
    ".scala": "Scala",
    ".sql": "SQL",
    ".sh": "Shell",
}
IGNORE_DIRS = {".git", ".agentcodex", ".codex", "dist", "build", "node_modules", "__pycache__", ".venv", "venv"}


def now_iso() -> str:
    return datetime.now(UTC).isoformat()


def slugify(value: str) -> str:
    value = re.sub(r"[^a-zA-Z0-9]+", "_", value.strip().upper())
    return value.strip("_") or "PROJECT"


def phase_files_exist() -> list[Path]:
    if not FEATURES_ROOT.exists():
        return []
    return sorted(
        path for path in FEATURES_ROOT.glob("*.md")
        if path.name.startswith(("BRAINSTORM_", "DEFINE_", "DESIGN_", "BUILD_REPORT_", "SHIPPED_"))
        and path.name != "DEFINE_EXAMPLE_PROJECT_FEATURE.md"
    )


def prompt_choice() -> str:
    print("Select the starting workflow:")
    print("1. New project from scratch")
    print("2. Information gathering for refactoring")
    while True:
        answer = input("Enter 1 or 2: ").strip()
        if answer in {"1", "2"}:
            return answer
        print("Invalid choice. Enter 1 or 2.")


def prompt_nonempty(label: str) -> str:
    while True:
        value = input(label).strip()
        if value:
            return value
        print("This field is required.")


def prompt_yes_no(label: str) -> bool:
    while True:
        value = input(label).strip().lower()
        if value in {"y", "yes"}:
            return True
        if value in {"n", "no"}:
            return False
        print("Enter yes or no.")


def project_scan() -> dict:
    scanned = 0
    top_level_entries: list[str] = []
    code_files: list[Path] = []
    language_counter: Counter[str] = Counter()
    key_files: list[str] = []

    for entry in sorted(ROOT.iterdir()):
        if entry.name in IGNORE_DIRS:
            continue
        top_level_entries.append(entry.name + ("/" if entry.is_dir() else ""))

    for path in ROOT.rglob("*"):
        if scanned >= MAX_SCAN_FILES:
            break
        parts = set(path.parts)
        if parts & IGNORE_DIRS:
            continue
        if not path.is_file():
            continue
        scanned += 1
        suffix = path.suffix.lower()
        if suffix in CODE_SUFFIXES:
            code_files.append(path)
            language_counter[CODE_SUFFIXES[suffix]] += 1
        rel = str(path.relative_to(ROOT))
        if path.name in {"package.json", "pyproject.toml", "setup.py", "go.mod", "Cargo.toml", "pom.xml", "build.gradle"}:
            key_files.append(rel)

    return {
        "top_level_entries": top_level_entries[:20],
        "code_file_count": len(code_files),
        "languages": language_counter.most_common(8),
        "key_files": key_files[:12],
        "is_mostly_empty": len(code_files) == 0,
    }


def ensure_dirs() -> None:
    FEATURES_ROOT.mkdir(parents=True, exist_ok=True)
    REPORTS_ROOT.mkdir(parents=True, exist_ok=True)


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def brainstorm_content(feature: str, owner: str, idea: str, scan: dict) -> str:
    repo_state = "The repository looks mostly empty or scaffold-only." if scan["is_mostly_empty"] else "The repository already contains code or supporting assets that may shape the first increment."
    top_level = ", ".join(scan["top_level_entries"]) if scan["top_level_entries"] else "No relevant top-level entries detected."
    return f"""# BRAINSTORM_{feature}

## Metadata

- feature: `{feature}`
- phase: `brainstorm`
- status: `draft`
- owner: `{owner}`
- updated_at: `{now_iso()}`

## Problem

{idea}

## Users or Stakeholders

- primary: project sponsor or product owner still defining the first deliverable
- secondary: implementation team that needs enough clarity to move safely into define

## Candidate Approaches

### Approach A

- summary: start with a narrow vertical slice that proves the main user value quickly
- advantages: fast feedback, lower initial cost, easier to adjust after first review
- disadvantages: architecture depth may stay shallow until later
- operational cost: low to medium

### Approach B

- summary: define a stronger project foundation first, including structure, controls, and reusable patterns before feature depth
- advantages: better long-term consistency, easier governance, clearer operating model
- disadvantages: slower visible progress, higher upfront design effort
- operational cost: medium

## Tradeoffs

- speed of first delivery versus upfront architecture rigor
- low-cost experimentation versus stronger initial governance and controls
- immediate feature depth versus reusable foundations for later work

## Questions

- What is the first concrete outcome the project must deliver?
- Who will approve the recommended direction and success criteria?
- What constraints already exist for platform, compliance, budget, or timeline?

## YAGNI Filter

### Needed Now

- define the initial problem clearly
- compare at least two viable directions
- select one direction that is good enough to move into define

### Defer

- implementation details at file level
- full rollout planning
- optimization work before the first value path is clear

## Recommendation

Recommended direction: start with Approach A unless there is already a hard governance or platform constraint that requires a foundation-first sequence.

Rationale: the current context is still early-stage, so reducing ambiguity before investing in broad architecture is the safest path. {repo_state} Top-level context observed: {top_level}

## Exit Check

- [x] at least 2 approaches considered
- [x] main tradeoffs documented
- [x] open questions captured
- [x] recommendation made
"""


def refactor_report_content(owner: str, goal: str, scan: dict) -> str:
    languages = ", ".join(f"{name} ({count})" for name, count in scan["languages"]) or "No code files detected in the scan."
    key_files = ", ".join(scan["key_files"]) or "No common entrypoint/build files detected."
    top_level = ", ".join(scan["top_level_entries"]) or "No relevant top-level entries detected."
    risk = "low evidence" if scan["is_mostly_empty"] else "live-code refactor"
    return f"""# Refactor Intake Report

- owner: `{owner}`
- generated_at: `{now_iso()}`
- mode: `information-gathering-for-refactoring`
- risk_profile: `{risk}`

## Refactor Goal

{goal}

## Directory Context

- top_level_entries: {top_level}
- code_file_count: {scan['code_file_count']}
- languages: {languages}
- key_files: {key_files}

## Findings

- The current directory was scanned for existing implementation context before any refactor recommendation.
- Existing languages and key files should shape the refactor plan instead of replacing the system blindly.
- If the stated goal is structural and not cosmetic, the next safe step is `define`, followed by `design`, before any build or rewrite work.

## Risks

- hidden coupling may exist outside the shallow scan
- missing tests may reduce refactor safety
- architecture changes may be larger than the initial request suggests

## Recommendation

- confirm whether you want a refactor approach
- if yes, create `DEFINE` and `DESIGN` artifacts first
- do not proceed to build without explicit approval
"""


def define_content(feature: str, owner: str, goal: str, scan: dict) -> str:
    languages = ", ".join(name for name, _ in scan["languages"]) or "unknown"
    return f"""# DEFINE_{feature}

## Metadata

- feature: `{feature}`
- phase: `define`
- status: `draft`
- owner: `{owner}`
- updated_at: `{now_iso()}`

## Problem Statement

The current codebase needs a refactoring-oriented definition before implementation work starts. Refactor goal: {goal}

## Users

- primary user: maintainers of the current codebase
- secondary user: reviewers and operators who need a safer change boundary

## Goals

- reduce ambiguity around the refactor scope
- preserve behavior where intended while improving structure
- define a safe path from analysis to design without premature code changes

## Success Criteria

- a bounded refactor scope is documented
- affected modules or areas are identified from the existing directory context
- build work is not started before design is explicit and approved

## Acceptance Criteria

- [ ] affected areas are named clearly
- [ ] refactor boundaries are explicit
- [ ] risks and dependencies are captured

## Constraints

- technical: existing stack includes {languages}
- operational: work must start from current repository evidence, not assumptions
- security/compliance: no uncontrolled broad rewrite without review

## Out of Scope

- direct implementation changes before design approval

## Clarity Score

- problem: 3
- users: 2
- goals: 3
- success criteria: 2
- scope: 2
- total: 12/15

## Open Questions

- Which module or file group should be the first refactor target?

## Exit Check

- [x] clarity score >= 12/15
- [x] acceptance criteria are testable
- [x] constraints are explicit
- [x] out of scope is defined
"""


def design_content(feature: str, owner: str, scan: dict) -> str:
    candidate_paths = scan["key_files"][:5] or ["[identify target module]"]
    file_manifest = "\n".join(
        f"- path: {path}\n  purpose: assess or refactor this existing surface safely\n  depends_on: repository evidence\n  role: planner"
        for path in candidate_paths
    )
    return f"""# DESIGN_{feature}

## Metadata

- feature: `{feature}`
- phase: `design`
- status: `draft`
- owner: `{owner}`
- updated_at: `{now_iso()}`

## Architecture Overview

This design exists to shape a refactor approach before any build activity begins. It uses current repository evidence as the starting point.

## System Flow

- inspect current modules and boundaries
- choose the smallest viable refactor slice
- define verification before changing code

## File Manifest

{file_manifest}

## Implementation Strategy

- start with the smallest high-value refactor slice
- preserve behavior unless a change is explicitly approved
- require a review checkpoint before build execution

## Dependencies and Interfaces

- current repository structure
- existing configuration and build files
- existing tests, if any

## Test Strategy

- identify current tests first
- add or strengthen a safety harness before structural edits
- require explicit approval before build starts

## Risks and Open Decisions

- missing regression coverage
- hidden cross-module coupling
- uncertain rollout impact until target slice is confirmed

## Exit Check

- [x] complete manifest exists
- [x] each major file has a purpose
- [x] testing approach is explicit
- [x] major dependencies are named
- [x] risks are identified
"""


def main() -> int:
    if not (ROOT / ".agentcodex").exists():
        print("AgentCodex is not installed in this directory. Install it before running project-intake.", file=sys.stderr)
        return 1

    existing = phase_files_exist()
    if existing:
        print("A workflow phase is already defined in this directory.")
        print("Existing phase artifacts:")
        for path in existing:
            print(f"- {path.relative_to(ROOT)}")
        print("This intake flow is intended only for directories starting from zero.")
        return 1

    ensure_dirs()
    owner = "operator"
    scan = project_scan()
    choice = prompt_choice()

    if choice == "1":
        idea = prompt_nonempty("What is the idea context for this new project? ")
        feature_label = prompt_nonempty("Choose a short feature name for the brainstorm artifact: ")
        feature = slugify(feature_label)
        target = FEATURES_ROOT / f"BRAINSTORM_{feature}.md"
        write_text(target, brainstorm_content(feature, owner, idea, scan))
        print(f"Created brainstorm artifact: {target.relative_to(ROOT)}")
        print("Next phase gate: review the recommendation and only then move to define.")
        return 0

    goal = prompt_nonempty("What refactoring or investigation goal do you want to assess? ")
    report_path = REPORTS_ROOT / "refactor-intake-report.md"
    write_text(report_path, refactor_report_content(owner, goal, scan))
    print(f"Created refactor analysis report: {report_path.relative_to(ROOT)}")

    if not prompt_yes_no("Do you want a refactoring approach proposal now? [yes/no] "):
        print("Stopped after directory analysis. No define/design artifacts were created.")
        return 0

    feature_label = prompt_nonempty("Choose a short feature name for the refactor artifacts: ")
    feature = slugify(feature_label)
    define_path = FEATURES_ROOT / f"DEFINE_{feature}.md"
    design_path = FEATURES_ROOT / f"DESIGN_{feature}.md"
    write_text(define_path, define_content(feature, owner, goal, scan))
    write_text(design_path, design_content(feature, owner, scan))
    print(f"Created define artifact: {define_path.relative_to(ROOT)}")
    print(f"Created design artifact: {design_path.relative_to(ROOT)}")

    if prompt_yes_no("Do you have explicit approval to proceed to build? [yes/no] "):
        print("Approval recorded, but this intake flow stops before build by design.")
        print("Next step: run the normal build-phase workflow explicitly.")
        return 0

    print("Stopped at design. Build must not start without explicit approval.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
