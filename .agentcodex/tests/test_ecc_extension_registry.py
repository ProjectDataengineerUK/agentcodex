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

import validate_agentcodex  # noqa: E402


class EccExtensionRegistryTests(unittest.TestCase):
    def _write_file(self, root: Path, rel_path: str, text: str = "content\n") -> None:
        path = root / rel_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

    def test_registry_rejects_stale_command_active_flag(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self._write_file(root, ".agentcodex/imports/ecc/commands/plan.md")
            self._write_file(root, ".agentcodex/imports/ecc/agents/planner.md")
            self._write_file(root, ".agentcodex/imports/ecc/skills/tdd/SKILL.md")
            self._write_file(root, ".agentcodex/imports/ecc/rules/common/testing.md")
            self._write_file(root, ".agentcodex/imports/ecc/schemas/plugin.schema.json", "{}\n")
            self._write_file(root, ".agentcodex/imports/ecc/scripts_ci/validate-commands.js")
            self._write_file(root, "docs/commands/plan.md")
            self._write_file(root, "docs/roles/planner.md")
            self._write_file(
                root,
                ".agentcodex/ecc-extension.json",
                json.dumps(
                    {
                        "source": {"root": ".agentcodex/imports/ecc"},
                        "counts": {
                            "commands": 1,
                            "agents": 1,
                            "skills": 1,
                            "rules": 1,
                            "schemas": 1,
                            "ci_validators": 1,
                            "active_command_name_matches": 0,
                            "active_role_name_matches": 1,
                        },
                        "commands": [
                            {
                                "id": "plan",
                                "source_path": ".agentcodex/imports/ecc/commands/plan.md",
                                "active_agentcodex_command": False,
                                "activation": "reference-only",
                            }
                        ],
                        "agents": [
                            {
                                "id": "planner",
                                "source_path": ".agentcodex/imports/ecc/agents/planner.md",
                                "active_agentcodex_role": True,
                                "activation": "already-active",
                            }
                        ],
                        "skills": [{"id": "tdd", "path": ".agentcodex/imports/ecc/skills/tdd/SKILL.md"}],
                        "rules": [{"ruleset": "common", "name": "testing.md", "path": ".agentcodex/imports/ecc/rules/common/testing.md"}],
                        "activation_policy": {"no_duplicate_rule": "do not duplicate active surfaces"},
                    },
                    indent=2,
                ),
            )
            old_root = validate_agentcodex.ROOT
            old_import = validate_agentcodex.ECC_IMPORT_ROOT
            old_registry = validate_agentcodex.ECC_EXTENSION_PATH
            old_commands = validate_agentcodex.COMMANDS_DIR
            try:
                validate_agentcodex.ROOT = root
                validate_agentcodex.ECC_IMPORT_ROOT = root / ".agentcodex" / "imports" / "ecc"
                validate_agentcodex.ECC_EXTENSION_PATH = root / ".agentcodex" / "ecc-extension.json"
                validate_agentcodex.COMMANDS_DIR = root / "docs" / "commands"
                errors: list[str] = []

                validate_agentcodex.validate_ecc_extension_registry(errors)

                self.assertTrue(any("active command flag stale" in error for error in errors), errors)
            finally:
                validate_agentcodex.ROOT = old_root
                validate_agentcodex.ECC_IMPORT_ROOT = old_import
                validate_agentcodex.ECC_EXTENSION_PATH = old_registry
                validate_agentcodex.COMMANDS_DIR = old_commands


if __name__ == "__main__":
    unittest.main()
