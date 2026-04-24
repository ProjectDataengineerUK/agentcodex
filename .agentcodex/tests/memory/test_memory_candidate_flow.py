from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
SCRIPTS_DIR = ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import memory_candidate_flow as flow  # noqa: E402


class MemoryCandidateFlowTests(unittest.TestCase):
    def test_build_review_marks_all_candidates_pending(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            candidate_path = Path(tmp) / "memory-extract-2026-04-23.json"
            candidate_path.write_text(json.dumps([{"memory_type": "semantic", "canonical_fact": "x"}]), encoding="utf-8")
            review_path, payload = flow.build_review(candidate_path, json.loads(candidate_path.read_text()))
            self.assertTrue(review_path.name.startswith("memory-review-"))
            self.assertEqual(payload["items"][0]["decision"], "pending")

    def test_normalize_candidate_builds_valid_semantic_shape(self) -> None:
        normalized = flow.normalize_candidate(
            {
                "memory_type": "semantic",
                "canonical_fact": "AgentCodex keeps repo-local status.",
            },
            "memory-extract-2026-04-23:1",
        )
        self.assertEqual(normalized["memory_type"], "semantic")
        self.assertIn("memory_id", normalized)
        self.assertIn("subject", normalized)
        self.assertIn("owner", normalized)


if __name__ == "__main__":
    unittest.main()
