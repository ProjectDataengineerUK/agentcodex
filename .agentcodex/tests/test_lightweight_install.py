from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


class LightweightInstallTests(unittest.TestCase):
    def test_bootstrap_default_is_lightweight(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "project"

            result = subprocess.run(
                [sys.executable, str(ROOT / "scripts" / "bootstrap_project.py"), str(target)],
                cwd=str(ROOT),
                text=True,
                capture_output=True,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue((target / "AGENTS.md").exists())
            self.assertTrue((target / ".agentcodex" / "features").is_dir())
            self.assertTrue((target / ".agentcodex" / "reports").is_dir())
            self.assertTrue((target / ".agentcodex" / "archive").is_dir())
            self.assertTrue((target / ".agentcodex" / "history").is_dir())
            self.assertFalse((target / ".agentcodex" / "kb").exists())
            self.assertFalse((target / ".agentcodex" / "commands").exists())
            self.assertFalse((target / ".agentcodex" / "templates").exists())
            self.assertFalse((target / ".codex").exists())

    def test_bootstrap_full_vendors_runtime_assets(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "project"

            result = subprocess.run(
                [sys.executable, str(ROOT / "scripts" / "bootstrap_project.py"), str(target), "--full", "--with-codex"],
                cwd=str(ROOT),
                text=True,
                capture_output=True,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue((target / ".agentcodex" / "kb" / "index.yaml").exists())
            self.assertTrue((target / ".agentcodex" / "commands").is_dir())
            self.assertTrue((target / ".agentcodex" / "templates").is_dir())
            self.assertTrue((target / ".codex" / "config.toml").exists())

    def test_bootstrap_help_does_not_create_help_directory(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            result = subprocess.run(
                [sys.executable, str(ROOT / "scripts" / "bootstrap_project.py"), "--help"],
                cwd=tmp,
                text=True,
                capture_output=True,
            )

            self.assertEqual(result.returncode, 0)
            self.assertIn("Usage:", result.stdout)
            self.assertFalse((Path(tmp) / "--help").exists())

    def test_sync_project_default_is_lightweight(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "project"
            target.mkdir()

            result = subprocess.run(
                [sys.executable, str(ROOT / "scripts" / "sync_project.py"), str(target)],
                cwd=str(ROOT),
                text=True,
                capture_output=True,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue((target / ".agentcodex" / "PROJECT_AGENTSCODEX.md").exists())
            self.assertTrue((target / ".agentcodex" / "features").is_dir())
            self.assertFalse((target / ".agentcodex" / "kb").exists())
            self.assertFalse((target / ".agentcodex" / "commands").exists())


if __name__ == "__main__":
    unittest.main()
