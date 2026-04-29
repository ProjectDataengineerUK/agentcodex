from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[2]
SCRIPTS_DIR = ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import daily_tasks  # noqa: E402


class DailyTasksTests(unittest.TestCase):
    def test_merge_tasks_moves_items_between_sections(self) -> None:
        existing = {
            "Done": ["ship start flow"],
            "In Progress": ["build daily-task command"],
            "Backlog": ["add dashboards"],
        }
        additions = {
            "Done": ["build daily-task command"],
            "In Progress": ["add dashboards"],
            "Backlog": ["new backlog item"],
        }

        merged = daily_tasks.merge_tasks(existing, additions)

        self.assertIn("build daily-task command", merged["Done"])
        self.assertNotIn("build daily-task command", merged["In Progress"])
        self.assertIn("add dashboards", merged["In Progress"])
        self.assertNotIn("add dashboards", merged["Backlog"])
        self.assertIn("new backlog item", merged["Backlog"])

    def test_render_daily_tasks_includes_all_sections(self) -> None:
        rendered = daily_tasks.render_daily_tasks(
            "2026-04-29",
            "agentcodex",
            {
                "Done": ["ship start flow"],
                "In Progress": ["implement daily tasks"],
                "Backlog": ["wire summary"],
            },
        )

        self.assertIn("## Done", rendered)
        self.assertIn("ship start flow", rendered)
        self.assertIn("## In Progress", rendered)
        self.assertIn("implement daily tasks", rendered)
        self.assertIn("## Backlog", rendered)
        self.assertIn("wire summary", rendered)

    def test_command_creates_daily_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / ".agentcodex").mkdir()
            (root / ".agentcodex" / "templates").mkdir(parents=True, exist_ok=True)
            (root / ".agentcodex" / "templates" / "DAILY_TASKS_TEMPLATE.md").write_text("template\n", encoding="utf-8")

            old_root = daily_tasks.ROOT
            old_resolve = daily_tasks.resolve_project_root
            try:
                daily_tasks.ROOT = root
                daily_tasks.resolve_project_root = lambda: root  # type: ignore[assignment]
                with mock.patch.object(sys, "argv", ["daily-tasks", "--date", "2026-04-29", "--done", "ship start flow"]):
                    exit_code = daily_tasks.main()
                self.assertEqual(exit_code, 0)
                output = root / ".agentcodex" / "history" / "DAILY_TASKS_2026-04-29.md"
                self.assertTrue(output.exists())
                text = output.read_text(encoding="utf-8")
                self.assertIn("ship start flow", text)
                self.assertIn("## In Progress", text)
            finally:
                daily_tasks.ROOT = old_root
                daily_tasks.resolve_project_root = old_resolve  # type: ignore[assignment]


if __name__ == "__main__":
    unittest.main()
