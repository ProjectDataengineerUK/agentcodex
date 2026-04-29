from __future__ import annotations

import contextlib
import io
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SRC_DIR = ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from agentcodex_cli import cli  # noqa: E402
from agentcodex_cli import dispatcher  # noqa: E402


class CliDispatcherTests(unittest.TestCase):
    def test_installed_cli_uses_shared_dispatcher_commands(self) -> None:
        required = {
            "readiness-report",
            "ship-gate",
            "maturity5-check",
            "refresh-all",
            "start",
            "daily-tasks",
            "model-route",
            "install-local-automation",
            "memory-retrieve",
            "memory-ingest",
            "memory-compact",
            "memory-validate",
        }

        self.assertTrue(required.issubset(set(dispatcher.command_names())))
        self.assertIs(cli.dispatch, dispatcher.dispatch)

    def test_dispatch_forwards_workflow_subcommands(self) -> None:
        calls: list[tuple[str, list[str]]] = []

        exit_code = dispatcher.dispatch(
            ["workflow-status", "wf-demo", "--json"],
            lambda script, args: calls.append((script, args)) or 0,
            "agentcodex",
        )

        self.assertEqual(exit_code, 0)
        self.assertEqual(calls, [("workflow_orchestrator.py", ["workflow-status", "wf-demo", "--json"])])

    def test_dispatch_supports_maturity5_alias(self) -> None:
        calls: list[tuple[str, list[str]]] = []

        exit_code = dispatcher.dispatch(
            ["maturity-5-check", "/tmp/project", "--json"],
            lambda script, args: calls.append((script, args)) or 0,
            "agentcodex",
        )

        self.assertEqual(exit_code, 0)
        self.assertEqual(calls, [("maturity5_check.py", ["/tmp/project", "--json"])])

    def test_dispatch_enforces_required_args(self) -> None:
        calls: list[tuple[str, list[str]]] = []

        with contextlib.redirect_stderr(io.StringIO()):
            exit_code = dispatcher.dispatch(
                ["ship-gate"],
                lambda script, args: calls.append((script, args)) or 0,
                "agentcodex",
            )

        self.assertEqual(exit_code, 1)
        self.assertEqual(calls, [])


if __name__ == "__main__":
    unittest.main()
