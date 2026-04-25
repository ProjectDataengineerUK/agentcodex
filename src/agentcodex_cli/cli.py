from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def installed_runtime_roots() -> list[Path]:
    module_path = Path(__file__).resolve()
    prefixes = {
        Path(sys.prefix),
        Path(sys.base_prefix),
        module_path.parents[3] if len(module_path.parents) > 3 else module_path.parent,
    }
    candidates: list[Path] = []
    for prefix in prefixes:
        candidates.append(prefix / "share" / "agentcodex")
    return candidates


def resolve_repo_root() -> Path:
    current = Path(__file__).resolve()
    for candidate in [current, *current.parents]:
        if (candidate / "pyproject.toml").exists() and (candidate / ".agentcodex").exists() and (candidate / "scripts").exists():
            return candidate
    for candidate in installed_runtime_roots():
        if (candidate / ".agentcodex").exists() and (candidate / "scripts").exists():
            return candidate
    raise RuntimeError("Could not resolve AgentCodex runtime root")


def run(script_name: str, args: list[str]) -> int:
    root = resolve_repo_root()
    script_path = root / "scripts" / script_name
    if not script_path.exists():
        print(f"Missing script: {script_path}", file=sys.stderr)
        return 1
    current_dir = Path.cwd()
    run_cwd = current_dir if (current_dir / ".agentcodex").exists() else root
    result = subprocess.run(
        [sys.executable, str(script_path), *args],
        cwd=str(run_cwd),
    )
    return int(result.returncode)


def print_help() -> int:
    print(
        """AgentCodex CLI

Usage:
  agentcodex install <target-project-dir> [--profile <profile-id>]
  agentcodex init <target-project-dir> [--with-codex]
  agentcodex sync-project <target-project-dir> [--with-codex]
  agentcodex sync-kb-upstreams [--refresh-imports] [--apply] [--domain <domain>]
  agentcodex sync-sources [--source <source-id>] [--apply] [--use-git] [--limit <n>]
  agentcodex sync-context <feature> [--owner <owner>]
  agentcodex project-intake
  agentcodex new-context <feature-or-topic> [--kind feature|session] [--owner <owner>]
  agentcodex resume-context <feature-or-topic> [--kind feature|session]
  agentcodex status [section]
  agentcodex session-controls [--json]
  agentcodex audit-summary [--json]
  agentcodex orchestrate-workflow <prompt> [--json]
  agentcodex list-workflows [--json]
  agentcodex workflow-status <workflow-run-id> [--json]
  agentcodex resume-workflow <workflow-run-id> [--json]
  agentcodex workflow-note <workflow-run-id> <stage-id> --note <text> [--json]
  agentcodex workflow-handoff <workflow-run-id> <from-stage-id> <to-stage-id> --note <text> [--json]
  agentcodex start-stage <workflow-run-id> <stage-id> [--note <text>] [--json]
  agentcodex complete-stage <workflow-run-id> <stage-id> [--note <text>] [--json]
  agentcodex advance-stage <workflow-run-id> <stage-id> [--note <text>] [--json]
  agentcodex workflow-next <workflow-run-id> [--note <text>] [--json]
  agentcodex workflow-close <workflow-run-id> [--note <text>] [--json]
  agentcodex workflow-archive <workflow-run-id> [--note <text>] [--json]
  agentcodex validate
  agentcodex validate-plugin
  agentcodex generate-roles
  agentcodex generate-routing
  agentcodex import-upstreams [all|agentspec|ecc]
  agentcodex generate-import-catalog
  agentcodex check-project <target-project-dir>
  agentcodex control-plane-check <target-project-dir> [all|multi-agent|token|cost|security] [--json]
  agentcodex enterprise-readiness <target-project-dir> [all|multi-agent|token|cost|security] [--json]
  agentcodex memory-health [backend-id] [--json]
  agentcodex memory-lint [--json]
  agentcodex memory-extract [--json]
  agentcodex extract-log-knowledge [--json]
  agentcodex memory-review-candidates [candidate-file] [--json]
  agentcodex memory-approve-candidates [review-file] [--json]
  agentcodex review-kb-updates [--json]
  agentcodex promote-kb-update <candidate-file> [--json]
  agentcodex platform-health <databricks|fabric> [--json]
  agentcodex help

Commands:
  install          Codex-first install flow; bootstrap a target project with local .codex support
  init             Bootstrap a target project with AgentCodex
  sync-project     Refresh AgentCodex-managed files in an existing project
  sync-kb-upstreams Refresh imported KB sources and sync mapped KB domains into .agentcodex/kb
  sync-sources     Collect lightweight metadata from trusted upstream source repositories
  sync-context     Create or refresh a feature context history entry from workflow artifacts
  project-intake   Run the interactive zero-state project intake flow
  new-context      Create a standardized context history entry in .agentcodex/history
  resume-context   Show the latest context history entry summary for a scope
  status           Show the current repo status snapshot or a specific section
  session-controls Show local context-budget and cost-summary controls
  audit-summary    Summarize repo-local run and failure audit signals
  orchestrate-workflow Create repo-local workflow state, stages, and handoffs for a multi-agent task
  list-workflows   List repo-local workflow runs and their progress
  workflow-status  Show the current state and next step of a workflow run
  resume-workflow  Show the current state and next step of a workflow run
  workflow-note    Add a repo-local note to a workflow stage
  workflow-handoff Record a handoff note between two workflow stages
  start-stage      Mark a workflow stage as in progress
  complete-stage   Mark a workflow stage as completed
  advance-stage    Complete a stage and automatically hand off to the next stage
  workflow-next    Start only the next valid pending stage
  workflow-close   Close a fully completed workflow run
  workflow-archive Archive a closed workflow run under .agentcodex/archive
  validate         Validate routing, KB, and roles manifests
  validate-plugin  Validate plugin manifest publication readiness
  generate-roles   Regenerate .agentcodex/roles/roles.yaml from docs/roles
  generate-routing Regenerate .agentcodex/routing/routing.json
  import-upstreams Import as much as possible from AgentSpec and ECC into .agentcodex/imports
  generate-import-catalog Regenerate import indexes from .agentcodex/imports
  check-project    Validate a bootstrapped target project
  control-plane-check Run multi-agent, token, cost, and security/compliance control checks for a target project
  enterprise-readiness Alias for control-plane-check
  memory-health    Show health and storage paths for the active or requested memory backend
  memory-lint      Run local memory lint checks over the current snapshots
  memory-extract   Produce repo-local seed memory candidates without external LLM calls
  extract-log-knowledge Produce memory/knowledge candidates from local observability logs
  memory-review-candidates Create a review file for the latest or requested memory candidates
  memory-approve-candidates Approve and ingest reviewed memory candidates
  review-kb-updates List KB update proposal files generated from reviewed operational evidence
  promote-kb-update Promote a KB update proposal into draft KB pages without overwriting existing content
  platform-health  Run repo-local Databricks or Fabric platform health checks
  help             Show this help

Note:
  `install` is the preferred Codex-first bootstrap path and maps to `init --with-codex`.
  The CLI can run from an editable checkout or from an installed runtime bundle.
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
            print("Usage: agentcodex install <target-project-dir> [--profile <profile-id>]", file=sys.stderr)
            return 1
        return run("bootstrap_project.py", [*rest, "--with-codex"])

    if command == "init":
        if not rest:
            print("Usage: agentcodex init <target-project-dir> [--with-codex]", file=sys.stderr)
            return 1
        return run("bootstrap_project.py", rest)

    if command == "sync-project":
        if not rest:
            print("Usage: agentcodex sync-project <target-project-dir> [--with-codex]", file=sys.stderr)
            return 1
        return run("sync_project.py", rest)

    if command == "sync-kb-upstreams":
        return run("sync_upstream_kb.py", rest)

    if command == "sync-sources":
        return run("sync_sources.py", rest)

    if command == "validate":
        return run("validate_agentcodex.py", [])

    if command == "validate-plugin":
        return run("validate_plugin_manifest.py", [])

    if command == "new-context":
        if not rest:
            print(
                "Usage: agentcodex new-context <feature-or-topic> "
                "[--kind feature|session] [--owner <owner>]",
                file=sys.stderr,
            )
            return 1
        return run("new_context_history.py", rest)

    if command == "sync-context":
        if not rest:
            print(
                "Usage: agentcodex sync-context <feature> [--owner <owner>]",
                file=sys.stderr,
            )
            return 1
        return run("sync_context_history.py", rest)

    if command == "project-intake":
        return run("project_intake.py", rest)

    if command == "resume-context":
        if not rest:
            print(
                "Usage: agentcodex resume-context <feature-or-topic> "
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
            print("Usage: agentcodex orchestrate-workflow <prompt> [--json]", file=sys.stderr)
            return 1
        return run("workflow_orchestrator.py", rest)

    if command == "list-workflows":
        return run("workflow_orchestrator.py", ["list-workflows", *rest])

    if command == "workflow-status":
        if not rest:
            print("Usage: agentcodex workflow-status <workflow-run-id> [--json]", file=sys.stderr)
            return 1
        return run("workflow_orchestrator.py", ["workflow-status", *rest])

    if command == "resume-workflow":
        if not rest:
            print("Usage: agentcodex resume-workflow <workflow-run-id> [--json]", file=sys.stderr)
            return 1
        return run("workflow_orchestrator.py", ["resume-workflow", *rest])

    if command == "workflow-note":
        if len(rest) < 2:
            print("Usage: agentcodex workflow-note <workflow-run-id> <stage-id> --note <text> [--json]", file=sys.stderr)
            return 1
        return run("workflow_orchestrator.py", ["workflow-note", *rest])

    if command == "workflow-handoff":
        if len(rest) < 3:
            print(
                "Usage: agentcodex workflow-handoff <workflow-run-id> <from-stage-id> <to-stage-id> --note <text> [--json]",
                file=sys.stderr,
            )
            return 1
        return run("workflow_orchestrator.py", ["workflow-handoff", *rest])

    if command == "start-stage":
        if len(rest) < 2:
            print("Usage: agentcodex start-stage <workflow-run-id> <stage-id> [--note <text>] [--json]", file=sys.stderr)
            return 1
        return run("workflow_orchestrator.py", ["start-stage", *rest])

    if command == "complete-stage":
        if len(rest) < 2:
            print("Usage: agentcodex complete-stage <workflow-run-id> <stage-id> [--note <text>] [--json]", file=sys.stderr)
            return 1
        return run("workflow_orchestrator.py", ["complete-stage", *rest])

    if command == "advance-stage":
        if len(rest) < 2:
            print("Usage: agentcodex advance-stage <workflow-run-id> <stage-id> [--note <text>] [--json]", file=sys.stderr)
            return 1
        return run("workflow_orchestrator.py", ["advance-stage", *rest])

    if command == "workflow-next":
        if not rest:
            print("Usage: agentcodex workflow-next <workflow-run-id> [--note <text>] [--json]", file=sys.stderr)
            return 1
        return run("workflow_orchestrator.py", ["workflow-next", *rest])

    if command == "workflow-close":
        if not rest:
            print("Usage: agentcodex workflow-close <workflow-run-id> [--note <text>] [--json]", file=sys.stderr)
            return 1
        return run("workflow_orchestrator.py", ["workflow-close", *rest])

    if command == "workflow-archive":
        if not rest:
            print("Usage: agentcodex workflow-archive <workflow-run-id> [--note <text>] [--json]", file=sys.stderr)
            return 1
        return run("workflow_orchestrator.py", ["workflow-archive", *rest])

    if command == "generate-roles":
        return run("generate_roles_manifest.py", [])

    if command == "generate-routing":
        return run("generate_routing_manifest.py", [])

    if command == "import-upstreams":
        if not rest:
            print("Usage: agentcodex import-upstreams [all|agentspec|ecc]", file=sys.stderr)
            return 1
        return run("import_upstreams.py", rest)

    if command == "generate-import-catalog":
        return run("generate_import_catalog.py", [])

    if command == "check-project":
        if not rest:
            print("Usage: agentcodex check-project <target-project-dir>", file=sys.stderr)
            return 1
        return run("check_bootstrapped_project.py", rest)

    if command == "control-plane-check":
        if not rest:
            print(
                "Usage: agentcodex control-plane-check <target-project-dir> "
                "[all|multi-agent|token|cost|security] [--json]",
                file=sys.stderr,
            )
            return 1
        return run("control_plane_check.py", rest)

    if command == "enterprise-readiness":
        if not rest:
            print(
                "Usage: agentcodex enterprise-readiness <target-project-dir> "
                "[all|multi-agent|token|cost|security] [--json]",
                file=sys.stderr,
            )
            return 1
        return run("control_plane_check.py", rest)

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
            print("Usage: agentcodex promote-kb-update <candidate-file> [--json]", file=sys.stderr)
            return 1
        return run("promote_kb_update.py", rest)

    if command == "platform-health":
        return run("platform_health.py", rest)

    print(f"Unknown command: {command}", file=sys.stderr)
    return print_help()
