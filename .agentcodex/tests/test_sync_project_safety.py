from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPTS_DIR = ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import sync_project  # noqa: E402


class SyncProjectSafetyTests(unittest.TestCase):
    def test_sync_tree_preserves_extra_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            src_root = root / "src"
            dest_root = root / "dest"
            (src_root / "managed").mkdir(parents=True, exist_ok=True)
            (dest_root / "managed").mkdir(parents=True, exist_ok=True)
            (src_root / "managed" / "template.md").write_text("fresh", encoding="utf-8")
            (dest_root / "managed" / "template.md").write_text("stale", encoding="utf-8")
            (dest_root / "managed" / "notes.local.md").write_text("keep", encoding="utf-8")
            drift: dict[str, list[str]] = {}

            sync_project.sync_tree(src_root, dest_root, ["managed"], drift, "templates")

            self.assertEqual((dest_root / "managed" / "template.md").read_text(encoding="utf-8"), "fresh")
            self.assertEqual((dest_root / "managed" / "notes.local.md").read_text(encoding="utf-8"), "keep")
            self.assertIn("templates", drift)


if __name__ == "__main__":
    unittest.main()
