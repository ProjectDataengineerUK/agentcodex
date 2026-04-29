from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPTS_DIR = ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import model_route  # noqa: E402


class ModelRouteTests(unittest.TestCase):
    def test_security_review_escalates_to_frontier(self) -> None:
        policy = model_route.load_policy()
        args = model_route.parse_args(
            ["--role", "reviewer", "revisar vulnerabilidade antes do ship"]
        )

        selection = model_route.build_selection(args, policy)

        self.assertEqual(selection["activity"], "review")
        self.assertEqual(selection["risk"], "high")
        self.assertEqual(selection["tier"], "frontier")
        self.assertEqual(selection["model"], "gpt-5.5")

    def test_low_budget_status_uses_economy(self) -> None:
        policy = model_route.load_policy()
        args = model_route.parse_args(["--budget", "low", "qual o numero atual"])

        selection = model_route.build_selection(args, policy)

        self.assertEqual(selection["activity"], "status")
        self.assertEqual(selection["tier"], "economy")
        self.assertEqual(selection["model"], "gpt-5.4-mini")

    def test_every_declared_role_is_covered_by_policy(self) -> None:
        policy = model_route.load_policy()
        coverage = model_route.role_coverage(policy)

        self.assertGreater(coverage["roles_total"], 0)
        self.assertEqual(coverage["unresolved_roles"], [])

    def test_write_reports_records_latest_selection(self) -> None:
        policy = model_route.load_policy()
        args = model_route.parse_args(["--activity", "implementation", "crie teste focado"])
        selection = model_route.build_selection(args, policy)

        model_route.write_reports(selection)

        latest = json.loads(model_route.LATEST_JSON.read_text(encoding="utf-8"))
        self.assertEqual(latest["activity"], "implementation")
        self.assertEqual(latest["model"], selection["model"])
        self.assertTrue(model_route.LATEST_MD.exists())


if __name__ == "__main__":
    unittest.main()
