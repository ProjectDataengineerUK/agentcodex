from __future__ import annotations

import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
SCRIPTS_DIR = ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import memory_retrieve as memory  # noqa: E402


class MemoryRetrievalTests(unittest.TestCase):
    def test_retention_filter_denies_unknown_policy(self) -> None:
        items = [
            {
                "memory_id": "sem-unknown-policy",
                "memory_type": "semantic",
                "scope": {"type": "project", "value": "agentcodex"},
                "retention_policy": "missing-policy",
                "subject": "x",
                "canonical_fact": "x",
                "supporting_context": "x",
                "confidence": 0.9,
            }
        ]

        filtered, denied = memory.retention_filter(items)
        self.assertEqual(filtered, [])
        self.assertEqual(denied, 1)

    def test_retention_filter_denies_scope_mismatch(self) -> None:
        items = [
            {
                "memory_id": "sem-scope-mismatch",
                "memory_type": "semantic",
                "scope": {"type": "session", "value": "agentcodex"},
                "retention_policy": "semantic-default",
                "subject": "x",
                "canonical_fact": "x",
                "supporting_context": "x",
                "confidence": 0.9,
            }
        ]

        filtered, denied = memory.retention_filter(items)
        self.assertEqual(filtered, [])
        self.assertEqual(denied, 1)

    def test_retention_filter_denies_stale_episodic_memory(self) -> None:
        items = [
            {
                "memory_id": "epi-stale",
                "memory_type": "episodic",
                "scope": {"type": "session", "value": "agentcodex"},
                "retention_policy": "episodic-default",
                "event_title": "old event",
                "event_summary": "old summary",
                "actors": ["agentcodex"],
                "timestamp": "2025-01-01T00:00:00Z",
                "outcome": "old outcome",
                "references": [],
                "importance": 0.5,
                "confidence": 1.0,
                "tags": [],
                "sensitivity": "internal",
                "owner": "agentcodex",
            }
        ]

        filtered, denied = memory.retention_filter(items)
        self.assertEqual(filtered, [])
        self.assertEqual(denied, 1)

    def test_retention_filter_allows_valid_semantic_memory(self) -> None:
        items = [
            {
                "memory_id": "sem-valid",
                "memory_type": "semantic",
                "scope": {"type": "project", "value": "agentcodex"},
                "retention_policy": "semantic-default",
                "subject": "project standard",
                "canonical_fact": "Ship gate exists.",
                "supporting_context": "project standard",
                "confidence": 0.9,
            }
        ]

        filtered, denied = memory.retention_filter(items)
        self.assertEqual(len(filtered), 1)
        self.assertEqual(denied, 0)

    def test_access_filter_denies_restricted_memory_for_explorer(self) -> None:
        items = [
            {
                "memory_id": "sem-restricted-1",
                "memory_type": "semantic",
                "scope": {"type": "project", "value": "agentcodex"},
                "owner": "agentcodex",
                "sensitivity": "restricted",
                "subject": "restricted-fact",
                "canonical_fact": "Highly restricted fact.",
                "supporting_context": "restricted support",
                "confidence": 0.9,
                "tags": ["restricted"],
            }
        ]

        filtered, denied = memory.access_filter(
            items,
            requester_role="explorer",
            requester_owner="agentcodex",
            requested_scope="project",
            requested_scope_value="agentcodex",
        )

        self.assertEqual(filtered, [])
        self.assertEqual(denied, 1)

    def test_access_filter_allows_restricted_memory_for_reviewer(self) -> None:
        items = [
            {
                "memory_id": "sem-restricted-1",
                "memory_type": "semantic",
                "scope": {"type": "project", "value": "agentcodex"},
                "owner": "agentcodex",
                "sensitivity": "restricted",
                "subject": "restricted-fact",
                "canonical_fact": "Highly restricted fact.",
                "supporting_context": "restricted support",
                "confidence": 0.9,
                "tags": ["restricted"],
            }
        ]

        filtered, denied = memory.access_filter(
            items,
            requester_role="reviewer",
            requester_owner="agentcodex",
            requested_scope="project",
            requested_scope_value="agentcodex",
        )

        self.assertEqual(len(filtered), 1)
        self.assertEqual(denied, 0)

    def test_access_filter_denies_cross_scope_without_owner_match(self) -> None:
        items = [
            {
                "memory_id": "sem-session-1",
                "memory_type": "semantic",
                "scope": {"type": "session", "value": "other-session"},
                "owner": "other-owner",
                "sensitivity": "internal",
                "subject": "session-fact",
                "canonical_fact": "Other session fact.",
                "supporting_context": "session support",
                "confidence": 0.8,
                "tags": ["session"],
            }
        ]

        filtered, denied = memory.access_filter(
            items,
            requester_role="explorer",
            requester_owner="agentcodex",
            requested_scope="project",
            requested_scope_value="agentcodex",
        )

        self.assertEqual(filtered, [])
        self.assertEqual(denied, 1)

    def test_rank_semantic_respects_limit_and_prefers_scope_match(self) -> None:
        query_tokens = memory.tokenize("project standard ship gate readiness")
        items = [
            {
                "memory_id": "sem-1",
                "memory_type": "semantic",
                "scope": {"type": "project", "value": "agentcodex"},
                "subject": "project standard",
                "canonical_fact": "Ship gate uses project standard readiness.",
                "supporting_context": "readiness score blocks incomplete ship",
                "confidence": 0.95,
                "created_at": "2026-04-22T10:00:00Z",
                "updated_at": "2026-04-23T10:00:00Z",
                "tags": ["ship", "readiness"],
                "sensitivity": "internal",
                "retention_policy": "semantic-default",
                "owner": "agentcodex",
            },
            {
                "memory_id": "sem-2",
                "memory_type": "semantic",
                "scope": {"type": "project", "value": "agentcodex"},
                "subject": "project standard",
                "canonical_fact": "Context blocks are required before ship.",
                "supporting_context": "context architecture data governance",
                "confidence": 0.85,
                "created_at": "2026-04-21T10:00:00Z",
                "updated_at": "2026-04-22T10:00:00Z",
                "tags": ["context", "ship"],
                "sensitivity": "internal",
                "retention_policy": "semantic-default",
                "owner": "agentcodex",
            },
            {
                "memory_id": "sem-3",
                "memory_type": "semantic",
                "scope": {"type": "session", "value": "other"},
                "subject": "review flow",
                "canonical_fact": "Reviews inspect regressions and weak tests.",
                "supporting_context": "risk review after implementation",
                "confidence": 0.8,
                "created_at": "2026-04-20T10:00:00Z",
                "updated_at": "2026-04-20T10:00:00Z",
                "tags": ["review"],
                "sensitivity": "internal",
                "retention_policy": "semantic-default",
                "owner": "agentcodex",
            },
            {
                "memory_id": "sem-4",
                "memory_type": "semantic",
                "scope": {"type": "project", "value": "agentcodex"},
                "subject": "readiness report",
                "canonical_fact": "Readiness report tracks complete partial missing states.",
                "supporting_context": "project standard report and ship gate",
                "confidence": 0.9,
                "created_at": "2026-04-19T10:00:00Z",
                "updated_at": "2026-04-23T09:00:00Z",
                "tags": ["readiness"],
                "sensitivity": "internal",
                "retention_policy": "semantic-default",
                "owner": "agentcodex",
            },
        ]

        ranked = memory.rank_semantic(items, query_tokens, "project", "agentcodex")

        self.assertEqual(len(ranked), 3)
        self.assertEqual(ranked[0]["memory_id"], "sem-1")
        self.assertNotIn("sem-3", [item["memory_id"] for item in ranked])

    def test_rank_procedural_only_returns_one_item(self) -> None:
        query_tokens = memory.tokenize("memory compaction deduplicate snapshots")
        items = [
            {
                "memory_id": "proc-1",
                "memory_type": "procedural",
                "scope": {"type": "agent", "value": "memory-architect"},
                "procedure_title": "Compact memory snapshots",
                "trigger": "run memory compact after repeated ingests",
                "steps": ["load snapshots", "merge duplicates", "write summary"],
                "constraints": ["preserve file-based state"],
                "success_signals": ["dedup count > 0"],
                "failure_signals": ["snapshot write fails"],
                "source": "local",
                "approval_state": "approved",
                "updated_at": "2026-04-23T10:00:00Z",
                "tags": ["compaction"],
                "owner": "agentcodex",
            },
            {
                "memory_id": "proc-2",
                "memory_type": "procedural",
                "scope": {"type": "agent", "value": "memory-architect"},
                "procedure_title": "Retrieve memory packet",
                "trigger": "query asks for memory context",
                "steps": ["tokenize query", "rank memories"],
                "constraints": ["keep context small"],
                "success_signals": ["result packet produced"],
                "failure_signals": ["no summary or memory selected"],
                "source": "local",
                "approval_state": "draft",
                "updated_at": "2026-04-22T10:00:00Z",
                "tags": ["retrieval"],
                "owner": "agentcodex",
            },
        ]

        ranked = memory.rank_procedural(items, query_tokens, "agent", "memory-architect")
        self.assertEqual(len(ranked), 1)
        self.assertEqual(ranked[0]["memory_id"], "proc-1")

    def test_scope_match_scores_expected_levels(self) -> None:
        item = {"scope": {"type": "project", "value": "agentcodex"}}
        self.assertEqual(memory.scope_match(item, None, None), 0.1)
        self.assertEqual(memory.scope_match(item, "project", None), 0.25)
        self.assertEqual(memory.scope_match(item, "project", "agentcodex"), 0.35)
        self.assertEqual(memory.scope_match(item, "session", "agentcodex"), 0.0)


if __name__ == "__main__":
    unittest.main()
