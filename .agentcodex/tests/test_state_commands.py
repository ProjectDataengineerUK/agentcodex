from __future__ import annotations

import contextlib
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPTS_DIR = ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import approval_gate_sync  # noqa: E402
import architecture_pivot  # noqa: E402
import databricks_readiness  # noqa: E402
import failure_pattern_promote  # noqa: E402
import preflight  # noqa: E402
import project_structure  # noqa: E402
import stack_detect  # noqa: E402
import status_reconcile  # noqa: E402


class StateCommandsTests(unittest.TestCase):
    def test_status_reconcile_script_entrypoint(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / ".agentcodex" / "history").mkdir(parents=True)
            (root / "AGENTS.md").write_text(
                "# AGENTS\n\n- primary_architecture: external frontend + databricks backend\n",
                encoding="utf-8",
            )
            (root / ".agentcodex" / "history" / "CONTEXT-HISTORY.md").write_text(
                "# Context\n\n- primary_architecture: databricks apps as primary surface\n",
                encoding="utf-8",
            )
            original_argv = sys.argv
            sys.argv = ["status_reconcile.py", str(root), "--json"]
            try:
                with contextlib.redirect_stdout(io.StringIO()) as buffer:
                    exit_code = status_reconcile.main()
            finally:
                sys.argv = original_argv
            payload = json.loads(buffer.getvalue())
            self.assertEqual(exit_code, 0)
            self.assertTrue(payload["needs_reconciliation"])
            self.assertTrue((root / ".agentcodex" / "state" / "project-state.json").exists())
            self.assertTrue((root / ".agentcodex" / "reports" / "status-reconcile.md").exists())

    def test_architecture_pivot_marks_pending_reconciliation(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / ".agentcodex").mkdir()
            (root / "AGENTS.md").write_text("# AGENTS\n", encoding="utf-8")
            original_argv = sys.argv
            sys.argv = [
                "architecture_pivot.py",
                str(root),
                "--to",
                "databricks apps primary surface",
                "--from",
                "external frontend + databricks backend",
                "--json",
            ]
            try:
                with contextlib.redirect_stdout(io.StringIO()) as buffer:
                    exit_code = architecture_pivot.main()
            finally:
                sys.argv = original_argv
            payload = json.loads(buffer.getvalue())
            state = json.loads((root / ".agentcodex" / "state" / "project-state.json").read_text(encoding="utf-8"))
            self.assertEqual(exit_code, 0)
            self.assertEqual(payload["new_architecture"], "databricks apps primary surface")
            self.assertTrue(state["architecture"]["pending_reconciliation"])

    def test_preflight_detects_python_and_github_actions(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / ".github" / "workflows").mkdir(parents=True)
            (root / ".github" / "workflows" / "ci.yml").write_text("name: ci\n", encoding="utf-8")
            (root / "pyproject.toml").write_text("[project]\nname='demo'\n", encoding="utf-8")
            original_argv = sys.argv
            sys.argv = ["preflight.py", str(root), "--json"]
            try:
                with contextlib.redirect_stdout(io.StringIO()) as buffer:
                    exit_code = preflight.main()
            finally:
                sys.argv = original_argv
            payload = json.loads(buffer.getvalue())
            self.assertEqual(exit_code, 0)
            self.assertIn("python", payload["stacks"])
            self.assertIn("github-actions", payload["stacks"])

    def test_approval_gate_sync_persists_gate_state(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            original_argv = sys.argv
            sys.argv = [
                "approval_gate_sync.py",
                str(root),
                "deploy-prod",
                "approved",
                "--commit",
                "abc123",
                "--run",
                "gh-42",
                "--note",
                "manual approval granted",
                "--json",
            ]
            try:
                with contextlib.redirect_stdout(io.StringIO()) as buffer:
                    exit_code = approval_gate_sync.main()
            finally:
                sys.argv = original_argv
            payload = json.loads(buffer.getvalue())
            state = json.loads((root / ".agentcodex" / "state" / "approval-gates.json").read_text(encoding="utf-8"))
            self.assertEqual(exit_code, 0)
            self.assertEqual(payload["status"], "approved")
            self.assertEqual(state["gates"]["deploy-prod"]["commit"], "abc123")

    def test_stack_detect_groups_layers(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / ".github" / "workflows").mkdir(parents=True)
            (root / "package.json").write_text("{\"name\":\"demo\"}\n", encoding="utf-8")
            (root / "main.tf").write_text("terraform {}\n", encoding="utf-8")
            (root / ".agentcodex" / "observability").mkdir(parents=True)
            original_argv = sys.argv
            sys.argv = ["stack_detect.py", str(root), "--json"]
            try:
                with contextlib.redirect_stdout(io.StringIO()) as buffer:
                    exit_code = stack_detect.main()
            finally:
                sys.argv = original_argv
            payload = json.loads(buffer.getvalue())
            self.assertEqual(exit_code, 0)
            self.assertIn("ci_cd", payload["layers"])
            self.assertIn("iac", payload["layers"])
            self.assertIn("observability", payload["layers"])

    def test_failure_pattern_promote_generates_candidates_for_repeated_failures(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            logs_root = root / ".agentcodex" / "observability" / "logs"
            logs_root.mkdir(parents=True)
            (logs_root / "sync.jsonl").write_text(
                "\n".join(
                    [
                        json.dumps({"script": "sync-sources", "level": "error", "stage": "network", "error": "<urlopen error [Errno -3] Temporary failure in name resolution>"}),
                        json.dumps({"script": "sync-sources", "level": "error", "stage": "network", "error": "<urlopen error [Errno -3] Temporary failure in name resolution>"}),
                    ]
                )
                + "\n",
                encoding="utf-8",
            )
            original_argv = sys.argv
            sys.argv = ["failure_pattern_promote.py", str(root), "--json"]
            try:
                with contextlib.redirect_stdout(io.StringIO()) as buffer:
                    exit_code = failure_pattern_promote.main()
            finally:
                sys.argv = original_argv
            payload = json.loads(buffer.getvalue())
            self.assertEqual(exit_code, 0)
            self.assertTrue(payload["patterns"])
            self.assertTrue((root / ".agentcodex" / "reports" / "failure-pattern-promotion.md").exists())
            self.assertTrue((root / ".agentcodex" / "memory" / "candidates").exists())

    def test_databricks_readiness_detects_bundle_app_and_boundary_gaps(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "resources").mkdir(parents=True)
            (root / "databricks.yml").write_text(
                "bundle:\n  name: demo\ninclude:\n  - resources/*.yml\ntargets:\n  dev:\n    default: true\n",
                encoding="utf-8",
            )
            (root / "resources" / "jobs.yml").write_text(
                "resources:\n  jobs:\n    demo:\n      tasks:\n        - task_key: t1\n          notebook_task:\n            notebook_path: ./src/jobs/notebook.py\n      permissions:\n        - level: CAN_MANAGE\n",
                encoding="utf-8",
            )
            (root / "app.yaml").write_text("command: python app.py\n", encoding="utf-8")
            original_argv = sys.argv
            sys.argv = ["databricks_readiness.py", str(root), "--json"]
            try:
                with contextlib.redirect_stdout(io.StringIO()) as buffer:
                    exit_code = databricks_readiness.main()
            finally:
                sys.argv = original_argv
            payload = json.loads(buffer.getvalue())
            self.assertEqual(exit_code, 0)
            self.assertEqual(payload["sections"]["bundles"]["status"], "warn")
            self.assertTrue((root / ".agentcodex" / "reports" / "databricks-readiness.md").exists())

    def test_project_structure_writes_report(self) -> None:
        original_argv = sys.argv
        sys.argv = ["project_structure.py"]
        try:
            with contextlib.redirect_stdout(io.StringIO()) as buffer:
                exit_code = project_structure.main()
        finally:
            sys.argv = original_argv
        self.assertEqual(exit_code, 0)
        self.assertIn("project-structure.md", buffer.getvalue())
