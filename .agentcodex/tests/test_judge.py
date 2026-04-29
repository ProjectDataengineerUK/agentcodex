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

import judge  # noqa: E402


class JudgeTests(unittest.TestCase):
    def test_ledger_entry_round_trip(self) -> None:
        raw = json.dumps(
            {
                "date": "2026-04-29",
                "ts": "2026-04-29T00:00:00+00:00",
                "model": "openai/gpt-4o",
                "target": "file.sql",
                "verdict": "PASS",
            }
        )

        entry = judge.LedgerEntry.from_json(raw)

        self.assertIsNotNone(entry)
        assert entry is not None
        self.assertEqual(entry.model, "openai/gpt-4o")
        self.assertEqual(entry.verdict, "PASS")
        self.assertIn("cost_usd", entry.to_dict())

    def test_malformed_ledger_row_is_skipped(self) -> None:
        self.assertIsNone(judge.LedgerEntry.from_json("not json"))

    def test_phase_defaults_have_prompts(self) -> None:
        self.assertEqual(set(judge.PHASE_MODEL_DEFAULTS), set(judge.PHASE_SYSTEM_PROMPTS))
        for model in judge.PHASE_MODEL_DEFAULTS.values():
            self.assertIn("/", model)

    def test_render_markdown_escapes_table_pipes(self) -> None:
        rendered = judge.render_markdown(
            {
                "verdict": "FAIL",
                "confidence": 0.8,
                "summary": "Issue found.",
                "concerns": [{"severity": "high", "issue": "bad | split", "evidence": "line | 1"}],
                "suggested_fixes": ["Fix it"],
            },
            "target.py",
            "openai/gpt-4o",
        )

        self.assertIn("bad \\| split", rendered)
        self.assertIn("line \\| 1", rendered)

    def test_today_count_reads_agentcodex_ledger(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            old_ledger = judge.LEDGER
            try:
                ledger = Path(tmp) / ".agentcodex" / "storage" / "judge-ledger.jsonl"
                ledger.parent.mkdir(parents=True)
                today = judge.today_utc()
                ledger.write_text(
                    "\n".join(
                        [
                            json.dumps({"date": today, "ts": "t", "model": "m", "target": "a", "verdict": "PASS"}),
                            json.dumps({"date": "1999-01-01", "ts": "t", "model": "m", "target": "b", "verdict": "FAIL"}),
                            "not json",
                        ]
                    ),
                    encoding="utf-8",
                )
                judge.LEDGER = ledger

                self.assertEqual(judge.load_today_count(), 1)
            finally:
                judge.LEDGER = old_ledger


if __name__ == "__main__":
    unittest.main()
