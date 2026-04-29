from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PLUGIN_SCRIPTS_DIR = ROOT / "plugins" / "agentcodex" / "scripts"
if str(PLUGIN_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(PLUGIN_SCRIPTS_DIR))

import install_runtime  # noqa: E402


class InstallRuntimeSafetyTests(unittest.TestCase):
    def test_sync_tree_preserves_extra_files_on_sync(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            src = root / "src"
            dest = root / "dest"
            (src / "nested").mkdir(parents=True, exist_ok=True)
            (dest / "nested").mkdir(parents=True, exist_ok=True)
            (src / "nested" / "managed.txt").write_text("new", encoding="utf-8")
            (dest / "nested" / "managed.txt").write_text("old", encoding="utf-8")
            (dest / "local.txt").write_text("keep", encoding="utf-8")

            install_runtime.sync_tree(src, dest, "sync")

            self.assertEqual((dest / "nested" / "managed.txt").read_text(encoding="utf-8"), "new")
            self.assertEqual((dest / "local.txt").read_text(encoding="utf-8"), "keep")


if __name__ == "__main__":
    unittest.main()
