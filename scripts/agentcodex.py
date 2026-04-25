#!/usr/bin/env python3
from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"


def run(script_name: str, args: list[str]) -> int:
    script_path = SCRIPTS / script_name
    if not script_path.exists():
        print(f"Missing script: {script_path}", file=sys.stderr)
        return 1
    current_dir = Path.cwd()
    run_cwd = current_dir if (current_dir / ".agentcodex").exists() else ROOT
    result = subprocess.run(
        [sys.executable, str(script_path), *args],
        cwd=str(run_cwd),
    )
    return int(result.returncode)


def print_help() -> int:
    print(
        """AgentCodex CLI

Usage:
  python3 scripts/agentcodex.py install <target-project-dir> [--profile <profile-id>]
  python3 scripts/agentcodex.py init <target-project-dir> [--with-codex] [--profile <profile-id>]
  python3 scripts/agentcodex.py sync-project <target-project-dir> [--with-codex] [--profile <profile-id>]
  python3 scripts/agentcodex.py sync-kb-upstreams [--refresh-imports] [--apply] [--domain <domain>]
  python3 scripts/agentcodex.py sync-sources [--source <source-id>] [--apply] [--use-git] [--limit <n>]
  python3 scripts/agentcodex.py sync-context <feature> [--owner <owner>]
  python3 scripts/agentcodex.py project-intake
  python3 scripts/agentcodex.py new-context <feature-or-topic> [--kind feature|session] [--owner <owner>]
  python3 scripts/agentcodex.py resume-context <feature-or-topic> [--kind feature|session]
  python3 scripts/agentcodex.py status [section]
  python3 scripts/agentcodex.py session-controls [--json]
  python3 scripts/agentcodex.py audit-summary [--json]
  python3 scripts/agentcodex.py orchestrate-workflow <prompt> [--json]
  python3 scripts/agentcodex.py list-workflows [--json]
  python3 scripts/agentcodex.py workflow-status <workflow-run-id> [--json]
  python3 scripts/agentcodex.py resume-workflow <workflow-run-id> [--json]
  python3 scripts/agentcodex.py workflow-note <workflow-run-id> <stage-id> --note <text> [--json]
  python3 scripts/agentcodex.py workflow-handoff <workflow-run-id> <from-stage-id> <to-stage-id> --note <text> [--json]
  python3 scripts/agentcodex.py start-stage <workflow-run-id> <stage-id> [--note <text>] [--json]
  python3 scripts/agentcodex.py complete-stage <workflow-run-id> <stage-id> [--note <text>] [--json]
  python3 scripts/agentcodex.py advance-stage <workflow-run-id> <stage-id> [--note <text>] [--json]
  python3 scripts/agentcodex.py workflow-next <workflow-run-id> [--note <text>] [--json]
  python3 scripts/agentcodex.py workflow-close <workflow-run-id> [--note <text>] [--json]
  python3 scripts/agentcodex.py workflow-archive <workflow-run-id> [--note <text>] [--json]
  python3 scripts/agentcodex.py validate
  python3 scripts/agentcodex.py validate-plugin
  python3 scripts/agentcodex.py generate-roles
  python3 scripts/agentcodex.py generate-routing
  python3 scripts/agentcodex.py import-upstreams [all|agentspec|ecc]
  python3 scripts/agentcodex.py generate-import-catalog
  python3 scripts/agentcodex.py check-project <target-project-dir>
  python3 scripts/agentcodex.py readiness-report <target-project-dir>
  python3 scripts/agentcodex.py ship-gate <target-project-dir>
  python3 scripts/agentcodex.py control-plane-check <target-project-dir> [all|multi-agent|token|cost|security] [--json]
  python3 scripts/agentcodex.py enterprise-readiness <target-project-dir> [all|multi-agent|token|cost|security] [--json]
  python3 scripts/agentcodex.py maturity5-check <target-project-dir> [--profile <profile-id>] [--json]
  python3 scripts/agentcodex.py refresh-all [--target-project <path>] [--with-codex] [--skip-import-catalog]
  python3 scripts/agentcodex.py install-local-automation
  python3 scripts/agentcodex.py memory-retrieve <query> [--task-type <type>] [--scope <scope>] [--scope-value <value>] [--json]
  python3 scripts/agentcodex.py memory-ingest <semantic|episodic|procedural> <json-file>
  python3 scripts/agentcodex.py memory-compact
  python3 scripts/agentcodex.py memory-health [backend-id] [--json]
  python3 scripts/agentcodex.py memory-lint [--json]
  python3 scripts/agentcodex.py memory-extract [--json]
  python3 scripts/agentcodex.py extract-log-knowledge [--json]
  python3 scripts/agentcodex.py memory-review-candidates [candidate-file] [--json]
  python3 scripts/agentcodex.py memory-approve-candidates [review-file] [--json]
  python3 scripts/agentcodex.py review-kb-updates [--json]
  python3 scripts/agentcodex.py promote-kb-update <candidate-file> [--json]
  python3 scripts/agentcodex.py platform-health <databricks|fabric> [--json]
  python3 scripts/agentcodex.py memory-validate
  python3 scripts/agentcodex.py help

Commands:
  install         Codex-first install flow; bootstrap a target project with local .codex support
  init            Bootstrap a target project with AgentCodex
  sync-project    Refresh AgentCodex-managed files in an existing project
  sync-kb-upstreams Refresh imported KB sources and sync mapped KB domains into .agentcodex/kb
  sync-sources    Collect lightweight metadata from trusted upstream source repositories
  sync-context    Create or refresh a feature context history entry from workflow artifacts
  project-intake  Run the interactive zero-state project intake flow
  new-context     Create a standardized context history entry in .agentcodex/history
  resume-context  Show the latest context history entry summary for a scope
  status          Show the current repo status snapshot or a specific section
  session-controls Show local context-budget and cost-summary controls
  audit-summary   Summarize repo-local run and failure audit signals
  orchestrate-workflow Create repo-local workflow state, stages, and handoffs for a multi-agent task
  list-workflows  List repo-local workflow runs and their progress
  workflow-status Show the current state and next step of a workflow run
  resume-workflow Show the current state and next step of a workflow run
  workflow-note  Add a repo-local note to a workflow stage
  workflow-handoff Record a handoff note between two workflow stages
  start-stage     Mark a workflow stage as in progress
  complete-stage  Mark a workflow stage as completed
  advance-stage   Complete a stage and automatically hand off to the next stage
  workflow-next   Start only the next valid pending stage
  workflow-close  Close a fully completed workflow run
  workflow-archive Archive a closed workflow run under .agentcodex/archive
  validate        Validate routing, KB, and roles manifests
  validate-plugin Validate plugin manifest publication readiness
  generate-roles  Regenerate .agentcodex/roles/roles.yaml from docs/roles
  generate-routing Regenerate .agentcodex/routing/routing.json
  import-upstreams Import as much as possible from AgentSpec and ECC into .agentcodex/imports
  generate-import-catalog Regenerate import indexes from .agentcodex/imports
  check-project   Validate a bootstrapped target project
  readiness-report Generate a project-standard readiness report for a target project
  ship-gate      Enforce the project-standard ship gate for a target project
  control-plane-check Run multi-agent, token, cost, and security/compliance control checks for a target project
  enterprise-readiness Alias for control-plane-check
  maturity5-check Evaluate the executable Maturity 5 DataOps + LLMOps baseline for a target project
  refresh-all    Refresh generated artifacts and optionally sync/check a target project
  install-local-automation Install repo-local git hooks for refresh automation
  memory-retrieve Retrieve compact long-term memory context from local memory snapshots
  memory-ingest  Ingest a local memory payload into the file-based memory backend
  memory-compact Deduplicate and compact file-based memory snapshots
  memory-health  Show health and storage paths for the active or requested memory backend
  memory-lint    Run local memory lint checks over the current snapshots
  memory-extract Produce repo-local seed memory candidates without external LLM calls
  extract-log-knowledge Produce memory/knowledge candidates from local observability logs
  memory-review-candidates Create a review file for the latest or requested memory candidates
  memory-approve-candidates Approve and ingest reviewed memory candidates
  review-kb-updates List KB update proposal files generated from reviewed operational evidence
  promote-kb-update Promote a KB update proposal into draft KB pages without overwriting existing content
  platform-health Run repo-local Databricks or Fabric platform health checks
  memory-validate Validate memory schemas, examples, snapshots, and synthetic contracts
  help            Show this help

Note:
  `install` is the preferred Codex-first bootstrap path and maps to `init --with-codex`.
"""
    )
    return 0


def main() -> int:
    args = sys.argv[1:]
    if not args or args[0] in {"help", "--help", "-h"}:
        return print_help()

    command = args[0]
    rest = args[1:]

    if command == "install":
        if not rest:
            print(
                "Usage: python3 scripts/agentcodex.py install <target-project-dir> [--profile <profile-id>]",
                file=sys.stderr,
            )
            return 1
        return run("bootstrap_project.py", [*rest, "--with-codex"])

    if command == "init":
        if not rest:
            print(
                "Usage: python3 scripts/agentcodex.py init <target-project-dir> [--with-codex] [--profile <profile-id>]",
                file=sys.stderr,
            )
            return 1
        return run("bootstrap_project.py", rest)

    if command == "validate":
        return run("validate_agentcodex.py", [])

    if command == "validate-plugin":
        return run("validate_plugin_manifest.py", [])

    if command == "sync-project":
        if not rest:
            print(
                "Usage: python3 scripts/agentcodex.py sync-project <target-project-dir> [--with-codex] [--profile <profile-id>]",
                file=sys.stderr,
            )
            return 1
        return run("sync_project.py", rest)

    if command == "sync-kb-upstreams":
        return run("sync_upstream_kb.py", rest)

    if command == "sync-sources":
        return run("sync_sources.py", rest)

    if command == "sync-context":
        if not rest:
            print(
                "Usage: python3 scripts/agentcodex.py sync-context <feature> [--owner <owner>]",
                file=sys.stderr,
            )
            return 1
        return run("sync_context_history.py", rest)

    if command == "project-intake":
        return run("project_intake.py", rest)

    if command == "new-context":
        if not rest:
            print(
                "Usage: python3 scripts/agentcodex.py new-context <feature-or-topic> "
                "[--kind feature|session] [--owner <owner>]",
                file=sys.stderr,
            )
            return 1
        return run("new_context_history.py", rest)

    if command == "resume-context":
        if not rest:
            print(
                "Usage: python3 scripts/agentcodex.py resume-context <feature-or-topic> "
                "[--kind feature|session]",
                file=sys.stderr,
            )
            return 1
        return run("resume_context.py", rest)

    if command == "status":
        return run("current_status.py", rest)

    if command == "session-controls":
        return run("session_controls_status.py", rest)

    if command == "audit-summary":
        return run("audit_summary.py", rest)

    if command == "orchestrate-workflow":
        if not rest:
            print("Usage: python3 scripts/agentcodex.py orchestrate-workflow <prompt> [--json]", file=sys.stderr)
            return 1
        return run("workflow_orchestrator.py", rest)

    if command == "list-workflows":
        return run("workflow_orchestrator.py", ["list-workflows", *rest])

    if command == "workflow-status":
        if not rest:
            print("Usage: python3 scripts/agentcodex.py workflow-status <workflow-run-id> [--json]", file=sys.stderr)
            return 1
        return run("workflow_orchestrator.py", ["workflow-status", *rest])

    if command == "resume-workflow":
        if not rest:
            print("Usage: python3 scripts/agentcodex.py resume-workflow <workflow-run-id> [--json]", file=sys.stderr)
            return 1
        return run("workflow_orchestrator.py", ["resume-workflow", *rest])

    if command == "workflow-note":
        if len(rest) < 2:
            print(
                "Usage: python3 scripts/agentcodex.py workflow-note <workflow-run-id> <stage-id> --note <text> [--json]",
                file=sys.stderr,
            )
            return 1
        return run("workflow_orchestrator.py", ["workflow-note", *rest])

    if command == "workflow-handoff":
        if len(rest) < 3:
            print(
                "Usage: python3 scripts/agentcodex.py workflow-handoff <workflow-run-id> <from-stage-id> <to-stage-id> --note <text> [--json]",
                file=sys.stderr,
            )
            return 1
        return run("workflow_orchestrator.py", ["workflow-handoff", *rest])

    if command == "start-stage":
        if len(rest) < 2:
            print(
                "Usage: python3 scripts/agentcodex.py start-stage <workflow-run-id> <stage-id> [--note <text>] [--json]",
                file=sys.stderr,
            )
            return 1
        return run("workflow_orchestrator.py", ["start-stage", *rest])

    if command == "complete-stage":
        if len(rest) < 2:
            print(
                "Usage: python3 scripts/agentcodex.py complete-stage <workflow-run-id> <stage-id> [--note <text>] [--json]",
                file=sys.stderr,
            )
            return 1
        return run("workflow_orchestrator.py", ["complete-stage", *rest])

    if command == "advance-stage":
        if len(rest) < 2:
            print(
                "Usage: python3 scripts/agentcodex.py advance-stage <workflow-run-id> <stage-id> [--note <text>] [--json]",
                file=sys.stderr,
            )
            return 1
        return run("workflow_orchestrator.py", ["advance-stage", *rest])

    if command == "workflow-next":
        if not rest:
            print(
                "Usage: python3 scripts/agentcodex.py workflow-next <workflow-run-id> [--note <text>] [--json]",
                file=sys.stderr,
            )
            return 1
        return run("workflow_orchestrator.py", ["workflow-next", *rest])

    if command == "workflow-close":
        if not rest:
            print(
                "Usage: python3 scripts/agentcodex.py workflow-close <workflow-run-id> [--note <text>] [--json]",
                file=sys.stderr,
            )
            return 1
        return run("workflow_orchestrator.py", ["workflow-close", *rest])

    if command == "workflow-archive":
        if not rest:
            print(
                "Usage: python3 scripts/agentcodex.py workflow-archive <workflow-run-id> [--note <text>] [--json]",
                file=sys.stderr,
            )
            return 1
        return run("workflow_orchestrator.py", ["workflow-archive", *rest])

    if command == "generate-roles":
        return run("generate_roles_manifest.py", [])

    if command == "generate-routing":
        return run("generate_routing_manifest.py", [])

    if command == "import-upstreams":
        if not rest:
            print("Usage: python3 scripts/agentcodex.py import-upstreams [all|agentspec|ecc]", file=sys.stderr)
            return 1
        return run("import_upstreams.py", rest)

    if command == "generate-import-catalog":
        return run("generate_import_catalog.py", [])

    if command == "check-project":
        if not rest:
            print("Usage: python3 scripts/agentcodex.py check-project <target-project-dir>", file=sys.stderr)
            return 1
        return run("check_bootstrapped_project.py", rest)

    if command == "readiness-report":
        if not rest:
            print("Usage: python3 scripts/agentcodex.py readiness-report <target-project-dir>", file=sys.stderr)
            return 1
        return run("project_readiness_report.py", rest)

    if command == "ship-gate":
        if not rest:
            print("Usage: python3 scripts/agentcodex.py ship-gate <target-project-dir>", file=sys.stderr)
            return 1
        return run("project_ship_gate.py", rest)

    if command == "control-plane-check":
        if not rest:
            print(
                "Usage: python3 scripts/agentcodex.py control-plane-check <target-project-dir> "
                "[all|multi-agent|token|cost|security] [--json]",
                file=sys.stderr,
            )
            return 1
        return run("control_plane_check.py", rest)

    if command == "enterprise-readiness":
        if not rest:
            print(
                "Usage: python3 scripts/agentcodex.py enterprise-readiness <target-project-dir> "
                "[all|multi-agent|token|cost|security] [--json]",
                file=sys.stderr,
            )
            return 1
        return run("control_plane_check.py", rest)

    if command in {"maturity5-check", "maturity-5-check"}:
        if not rest:
            print(
                "Usage: python3 scripts/agentcodex.py maturity5-check <target-project-dir> "
                "[--profile <profile-id>] [--json]",
                file=sys.stderr,
            )
            return 1
        return run("maturity5_check.py", rest)

    if command == "refresh-all":
        return run("refresh_all.py", rest)

    if command == "install-local-automation":
        return run("install_local_automation.py", rest)

    if command == "memory-retrieve":
        if not rest:
            print(
                "Usage: python3 scripts/agentcodex.py memory-retrieve <query> "
                "[--task-type <type>] [--scope <scope>] [--scope-value <value>] [--json]",
                file=sys.stderr,
            )
            return 1
        return run("memory_retrieve.py", rest)

    if command == "memory-ingest":
        if len(rest) != 2:
            print(
                "Usage: python3 scripts/agentcodex.py memory-ingest <semantic|episodic|procedural> <json-file>",
                file=sys.stderr,
            )
            return 1
        return run("memory_ingest.py", rest)

    if command == "memory-compact":
        return run("memory_compact.py", rest)

    if command == "memory-health":
        return run("memory_backend_health.py", rest)

    if command == "memory-lint":
        return run("memory_lint.py", rest)

    if command == "memory-extract":
        return run("memory_extract.py", rest)

    if command == "extract-log-knowledge":
        return run("extract_log_knowledge.py", rest)

    if command == "memory-review-candidates":
        return run("memory_review_candidates.py", rest)

    if command == "memory-approve-candidates":
        return run("memory_approve_candidates.py", rest)

    if command == "review-kb-updates":
        return run("review_kb_updates.py", rest)

    if command == "promote-kb-update":
        if not rest:
            print("Usage: python3 scripts/agentcodex.py promote-kb-update <candidate-file> [--json]", file=sys.stderr)
            return 1
        return run("promote_kb_update.py", rest)

    if command == "platform-health":
        return run("platform_health.py", rest)

    if command == "memory-validate":
        return run("memory_validate.py", rest)

    print(f"Unknown command: {command}", file=sys.stderr)
    return print_help()


if __name__ == "__main__":
    raise SystemExit(main())
