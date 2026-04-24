from __future__ import annotations

import sys
import unittest
from datetime import UTC, datetime, timedelta
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
SCRIPTS_DIR = ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import memory_lifecycle as lifecycle  # noqa: E402


class MemoryLifecycleTests(unittest.TestCase):
    def test_semantic_memories_do_not_decay(self) -> None:
        item = {
            "memory_type": "semantic",
            "confidence": 0.91,
            "created_at": "2026-04-01T00:00:00Z",
        }
        self.assertEqual(lifecycle.compute_decayed_confidence(item), 0.91)

    def test_episodic_memories_decay_over_time(self) -> None:
        now = datetime(2026, 4, 23, tzinfo=UTC)
        item = {
            "memory_type": "episodic",
            "confidence": 1.0,
            "timestamp": (now - timedelta(days=20)).isoformat().replace("+00:00", "Z"),
        }
        self.assertLess(lifecycle.compute_decayed_confidence(item, now), 0.3)

    def test_extract_seed_memories_returns_repo_local_candidates(self) -> None:
        seeds = lifecycle.extract_seed_memories()
        self.assertGreaterEqual(len(seeds), 1)
        self.assertTrue(all("memory_type" in item for item in seeds))
