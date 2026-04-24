from __future__ import annotations

import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
SCRIPTS_DIR = ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import memory_ingest as ingest  # noqa: E402


class MemoryIngestTests(unittest.TestCase):
    def test_validate_item_requires_scope_owner_source_and_policy_fields(self) -> None:
        item = {
            "memory_id": "sem-1",
            "memory_type": "semantic",
            "subject": "project standard",
            "canonical_fact": "Ship gate requires readiness.",
            "supporting_context": "project standard",
            "confidence": 0.9,
            "created_at": "2026-04-23T10:00:00Z",
            "updated_at": "2026-04-23T10:00:00Z",
            "tags": ["ship"],
        }

        errors = ingest.validate_item(item, "semantic")

        self.assertIn("missing field: scope", errors)
        self.assertIn("missing field: source", errors)
        self.assertIn("missing field: sensitivity", errors)
        self.assertIn("missing field: retention_policy", errors)
        self.assertIn("missing field: owner", errors)
        self.assertIn("scope must be an object with type and value", errors)

    def test_similarity_detects_near_duplicates(self) -> None:
        left = {
            "subject": "project standard ship gate",
            "canonical_fact": "Ship gate blocks incomplete project standard readiness.",
            "supporting_context": "readiness score and required blocks",
            "tags": ["ship", "readiness"],
        }
        right = {
            "subject": "project standard ship gate",
            "canonical_fact": "Ship gate blocks incomplete readiness for project standard.",
            "supporting_context": "required blocks and readiness score",
            "tags": ["ship", "readiness"],
        }

        score = ingest.similarity(left, right, "semantic")
        self.assertGreaterEqual(score, 0.82)


if __name__ == "__main__":
    unittest.main()
