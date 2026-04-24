from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[2]
SCRIPTS_DIR = ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import workflow_orchestrator as orchestrator  # noqa: E402


class WorkflowOrchestratorTests(unittest.TestCase):
    def test_validate_workflow_run_id_rejects_path_traversal(self) -> None:
        with self.assertRaises(ValueError):
            orchestrator.validate_workflow_run_id("../escape")

        with self.assertRaises(ValueError):
            orchestrator.validate_workflow_run_id("wf/escape")

    def test_list_workflows_includes_archived_runs_without_active_root(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            archived_root = root / ".agentcodex" / "archive" / "workflows" / "wf-test"
            archived_root.mkdir(parents=True, exist_ok=True)
            payload = {
                "generated_at": "2026-04-23T00:00:00+00:00",
                "updated_at": "2026-04-23T00:00:00+00:00",
                "workflow_id": "wf-pipeline",
                "workflow_name": "WF-PIPELINE",
                "workflow_run_id": "wf-test",
                "workflow_status": "archived",
                "stages": [
                    {"id": "stage-01", "status": "completed"},
                ],
            }
            (archived_root / "state.json").write_text(json.dumps(payload), encoding="utf-8")

            with patch.object(orchestrator, "ROOT", root), patch.object(
                orchestrator, "WORKFLOWS_ROOT", root / ".agentcodex" / "workflows"
            ), patch.object(orchestrator, "ARCHIVE_ROOT", root / ".agentcodex" / "archive" / "workflows"):
                with patch("builtins.print") as mock_print:
                    exit_code = orchestrator.list_workflows(as_json=False)

            self.assertEqual(exit_code, 0)
            printed = "\n".join(" ".join(str(arg) for arg in call.args) for call in mock_print.call_args_list)
            self.assertIn("wf-test", printed)
            self.assertIn("archived", printed)

    def test_next_workflow_run_id_adds_incremental_suffix_on_collision(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            active_root = root / ".agentcodex" / "workflows"
            archive_root = root / ".agentcodex" / "archive" / "workflows"
            active_root.mkdir(parents=True, exist_ok=True)
            archive_root.mkdir(parents=True, exist_ok=True)
            (active_root / "wf-pipeline-same-prompt").mkdir()
            (archive_root / "wf-pipeline-same-prompt-2").mkdir()

            with patch.object(orchestrator, "WORKFLOWS_ROOT", active_root), patch.object(
                orchestrator, "ARCHIVE_ROOT", archive_root
            ):
                run_id = orchestrator.next_workflow_run_id("wf-pipeline", "same prompt")

            self.assertEqual(run_id, "wf-pipeline-same-prompt-3")


if __name__ == "__main__":
    unittest.main()
