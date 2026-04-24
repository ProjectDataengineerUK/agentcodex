from __future__ import annotations

import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
SCRIPTS_DIR = ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import memory_compact as compact  # noqa: E402


class MemoryCompactionTests(unittest.TestCase):
    def test_deduplicate_merges_by_memory_id(self) -> None:
        items = [
            {"memory_id": "sem-1", "canonical_fact": "first fact"},
            {"memory_id": "sem-1", "canonical_fact": "updated fact", "owner": "agentcodex"},
        ]

        deduped, dedup_count = compact.deduplicate(items, "semantic")

        self.assertEqual(len(deduped), 1)
        self.assertEqual(dedup_count, 1)
        self.assertEqual(deduped[0]["canonical_fact"], "updated fact")
        self.assertEqual(deduped[0]["owner"], "agentcodex")

    def test_deduplicate_merges_near_duplicates(self) -> None:
        items = [
            {
                "memory_id": "proc-1",
                "procedure_title": "Compact memory snapshots",
                "trigger": "run compaction after repeated ingests",
                "steps": ["load snapshots", "merge duplicates", "write summary"],
                "constraints": ["preserve file state"],
                "success_signals": ["dedup count > 0"],
                "failure_signals": ["write fails"],
                "tags": ["compaction"],
            },
            {
                "memory_id": "proc-2",
                "procedure_title": "Compact memory snapshots",
                "trigger": "run compaction after repeated ingests",
                "steps": ["load snapshots", "merge duplicates", "write summary"],
                "constraints": ["preserve file state"],
                "success_signals": ["dedup count > 0"],
                "failure_signals": ["write fails"],
                "tags": ["compaction"],
            },
        ]

        deduped, dedup_count = compact.deduplicate(items, "procedural")

        self.assertEqual(len(deduped), 1)
        self.assertEqual(dedup_count, 1)


if __name__ == "__main__":
    unittest.main()
