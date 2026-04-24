from __future__ import annotations

import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
SCRIPTS_DIR = ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import memory_backend as backend  # noqa: E402


class MemoryBackendTests(unittest.TestCase):
    def test_get_backend_returns_local_mock_by_default(self) -> None:
        resolved = backend.get_backend()
        self.assertEqual(resolved.backend_id, "local-mock")

    def test_local_mock_exposes_expected_sources(self) -> None:
        resolved = backend.get_backend("local-mock")
        paths = resolved.snapshot_paths()

        self.assertIn("semantic", paths)
        self.assertIn("episodic", paths)
        self.assertIn("procedural", paths)
        self.assertTrue(str(resolved.summary_path()).endswith("local-memory-summary.md"))

    def test_langmem_stub_backend_is_resolvable_but_not_active(self) -> None:
        for backend_id in ["langmem"]:
            resolved = backend.get_backend(backend_id)
            health = resolved.health()
            self.assertEqual(health.backend_id, backend_id)
            self.assertEqual(health.status, "planned")
            with self.assertRaises(NotImplementedError):
                resolved.load("semantic")

    def test_mem0_backend_is_resolvable(self) -> None:
        resolved = backend.get_backend("mem0")
        health = resolved.health()
        self.assertEqual(resolved.backend_id, "mem0")
        self.assertIn(health.status, {"configured-missing-url", "configured-missing-api-key", "unreachable", "active"})

    def test_qdrant_backend_is_resolvable(self) -> None:
        resolved = backend.get_backend("qdrant")
        health = resolved.health()
        self.assertEqual(resolved.backend_id, "qdrant")
        self.assertIn(health.status, {"configured-missing-url", "unreachable", "active"})

    def test_qdrant_vectorization_is_deterministic(self) -> None:
        resolved = backend.get_backend("qdrant")
        item = {
            "subject": "project standard",
            "canonical_fact": "Ship gate uses readiness.",
            "supporting_context": "readiness report",
        }
        left = resolved.vectorize_payload(item, "semantic")
        right = resolved.vectorize_payload(item, "semantic")
        self.assertEqual(left, right)
        self.assertEqual(len(left), resolved.vector_size)


if __name__ == "__main__":
    unittest.main()
