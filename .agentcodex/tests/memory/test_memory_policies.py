from __future__ import annotations

import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
SCRIPTS_DIR = ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import memory_retrieve as memory  # noqa: E402


MEMORY_ROOT = ROOT / ".agentcodex" / "memory"


class MemoryPolicyTests(unittest.TestCase):
    def test_retention_manifest_covers_required_memory_types(self) -> None:
        manifest = memory.parse_simple_yaml(MEMORY_ROOT / "manifests" / "memory-retention.yaml")
        policies = manifest.get("policies", [])
        ids_by_type = {item.get("memory_type"): item.get("id") for item in policies if isinstance(item, dict)}

        self.assertEqual(ids_by_type["semantic"], "semantic-default")
        self.assertEqual(ids_by_type["episodic"], "episodic-default")
        self.assertEqual(ids_by_type["procedural"], "procedural-default")

    def test_access_manifest_has_owner_and_scope_guards(self) -> None:
        text = (MEMORY_ROOT / "manifests" / "memory-access.yaml").read_text(encoding="utf-8")

        self.assertIn("deny_cross_scope_without_owner_match: true", text)
        self.assertIn("require_owner: true", text)
        self.assertIn("require_sensitivity: true", text)
        self.assertIn("template_id: project-default", text)
        self.assertIn("template_id: restricted-memory", text)


if __name__ == "__main__":
    unittest.main()
