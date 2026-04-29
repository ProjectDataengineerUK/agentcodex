from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPTS_DIR = ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import import_upstreams  # noqa: E402


class ImportUpstreamsTests(unittest.TestCase):
    def test_agentspec_mapping_imports_scripts_and_plugin_metadata(self) -> None:
        self.assertEqual(import_upstreams.AGENTSPEC_IMPORTS["scripts"], "scripts")
        self.assertEqual(import_upstreams.AGENTSPEC_IMPORTS["plugin_metadata"], "plugin/.claude-plugin")

    def test_data_agents_mapping_imports_raw_operating_surfaces(self) -> None:
        required = {
            "agents": "agents",
            "commands": "commands",
            "hooks": "hooks",
            "kb": "kb",
            "mcp_servers": "mcp_servers",
            "memory": "memory",
            "skills": "skills",
            "workflow": "workflow",
            "readme": "README.md",
        }

        for name, rel_path in required.items():
            self.assertEqual(import_upstreams.DATA_AGENTS_IMPORTS[name], rel_path)

    def test_partial_manifest_upsert_preserves_other_sources(self) -> None:
        manifest = {
            "version": "0.1.0",
            "imports": [
                {"source": "agentspec", "total_files": 1},
                {"source": "ecc", "total_files": 42},
                {"source": "data-agents", "total_files": 7},
            ],
        }

        import_upstreams.upsert_import(manifest, {"source": "agentspec", "total_files": 3})

        self.assertEqual([item["source"] for item in manifest["imports"]], ["agentspec", "ecc", "data-agents"])
        self.assertEqual(manifest["imports"][0]["total_files"], 3)
        self.assertEqual(manifest["imports"][1]["total_files"], 42)
        self.assertEqual(manifest["imports"][2]["total_files"], 7)

    def test_load_existing_manifest_keeps_imports(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            manifest_path = Path(tmp) / "manifest.json"
            manifest_path.write_text(
                json.dumps({"version": "0.1.0", "imports": [{"source": "ecc"}]}),
                encoding="utf-8",
            )

            manifest = import_upstreams.load_existing_manifest(manifest_path)

        self.assertEqual(manifest["imports"], [{"source": "ecc"}])


if __name__ == "__main__":
    unittest.main()
