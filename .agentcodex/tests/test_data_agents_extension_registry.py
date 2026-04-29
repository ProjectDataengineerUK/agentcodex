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


class DataAgentsExtensionRegistryTests(unittest.TestCase):
    def _write_file(self, root: Path, rel_path: str, text: str = "content\n") -> None:
        path = root / rel_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

    def test_registry_ignores_template_mcp_server(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self._write_file(root, ".agentcodex/imports/data-agents/agents/registry/business-monitor.md")
            self._write_file(root, ".agentcodex/imports/data-agents/commands/monitor.py")
            self._write_file(root, ".agentcodex/imports/data-agents/skills/patterns/data-quality/SKILL.md")
            self._write_file(root, ".agentcodex/imports/data-agents/kb/data-quality/index.md")
            self._write_file(root, ".agentcodex/imports/data-agents/mcp_servers/_template/README.md")
            self._write_file(root, ".agentcodex/imports/data-agents/mcp_servers/fabric/README.md")
            self._write_file(root, ".agentcodex/imports/data-agents/hooks/security_hook.py")
            self._write_file(root, ".agentcodex/imports/data-agents/tests/test_monitor.py")
            self._write_file(root, ".agentcodex/imports/data-agents/templates/pipeline-spec.md")
            self._write_file(root, "docs/roles/business-monitor.md")
            self._write_file(root, "docs/commands/platform-health.md")
            self._write_file(
                root,
                ".agentcodex/data-agents-extension.json",
                json.dumps(
                    {
                        "source": {"root": ".agentcodex/imports/data-agents"},
                        "counts": {
                            "agents": 1,
                            "commands": 1,
                            "skills": 1,
                            "kb_files": 1,
                            "mcp_servers": 1,
                            "hooks": 1,
                            "tests": 1,
                            "templates": 1,
                            "mapped_agents": 1,
                            "mapped_commands": 1,
                        },
                        "agents": [
                            {
                                "id": "business-monitor",
                                "source_path": ".agentcodex/imports/data-agents/agents/registry/business-monitor.md",
                                "target_agentcodex_role": "business-monitor",
                                "activation": "mapped-to-native-role",
                            }
                        ],
                        "commands": [
                            {
                                "id": "monitor",
                                "source_path": ".agentcodex/imports/data-agents/commands/monitor.py",
                                "target_agentcodex_command": "platform-health",
                                "activation": "mapped-to-native-command",
                            }
                        ],
                        "skills": [
                            {
                                "id": "patterns/data-quality",
                                "source_path": ".agentcodex/imports/data-agents/skills/patterns/data-quality/SKILL.md",
                            }
                        ],
                        "kb_files": [".agentcodex/imports/data-agents/kb/data-quality/index.md"],
                        "mcp_servers": ["fabric"],
                        "hooks": [".agentcodex/imports/data-agents/hooks/security_hook.py"],
                        "tests": [".agentcodex/imports/data-agents/tests/test_monitor.py"],
                        "templates": [".agentcodex/imports/data-agents/templates/pipeline-spec.md"],
                        "activation_policy": {
                            "no_duplicate_rule": "Do not create duplicate active surfaces",
                            "native_codex_rule": "Translate behavior to native Codex files before activation.",
                        },
                    },
                    indent=2,
                ),
            )
            old_root = validate_agentcodex.ROOT
            old_import = validate_agentcodex.DATA_AGENTS_IMPORT_ROOT
            old_registry = validate_agentcodex.DATA_AGENTS_EXTENSION_PATH
            old_commands = validate_agentcodex.COMMANDS_DIR
            try:
                validate_agentcodex.ROOT = root
                validate_agentcodex.DATA_AGENTS_IMPORT_ROOT = root / ".agentcodex" / "imports" / "data-agents"
                validate_agentcodex.DATA_AGENTS_EXTENSION_PATH = root / ".agentcodex" / "data-agents-extension.json"
                validate_agentcodex.COMMANDS_DIR = root / "docs" / "commands"
                errors: list[str] = []

                validate_agentcodex.validate_data_agents_extension_registry(errors)

                self.assertEqual(errors, [], errors)
            finally:
                validate_agentcodex.ROOT = old_root
                validate_agentcodex.DATA_AGENTS_IMPORT_ROOT = old_import
                validate_agentcodex.DATA_AGENTS_EXTENSION_PATH = old_registry
                validate_agentcodex.COMMANDS_DIR = old_commands

    def test_registry_rejects_missing_mapped_native_role(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self._write_file(root, ".agentcodex/imports/data-agents/agents/registry/business-monitor.md")
            self._write_file(root, ".agentcodex/imports/data-agents/commands/monitor.py")
            self._write_file(root, ".agentcodex/imports/data-agents/skills/patterns/data-quality/SKILL.md")
            self._write_file(root, ".agentcodex/imports/data-agents/kb/data-quality/index.md")
            self._write_file(root, ".agentcodex/imports/data-agents/mcp_servers/fabric/README.md")
            self._write_file(root, ".agentcodex/imports/data-agents/hooks/security_hook.py")
            self._write_file(root, ".agentcodex/imports/data-agents/tests/test_monitor.py")
            self._write_file(root, ".agentcodex/imports/data-agents/templates/pipeline-spec.md")
            self._write_file(root, "docs/commands/platform-health.md")
            self._write_file(
                root,
                ".agentcodex/data-agents-extension.json",
                json.dumps(
                    {
                        "source": {"root": ".agentcodex/imports/data-agents"},
                        "counts": {
                            "agents": 1,
                            "commands": 1,
                            "skills": 1,
                            "kb_files": 1,
                            "mcp_servers": 1,
                            "hooks": 1,
                            "tests": 1,
                            "templates": 1,
                            "mapped_agents": 1,
                            "mapped_commands": 1,
                        },
                        "agents": [
                            {
                                "id": "business-monitor",
                                "source_path": ".agentcodex/imports/data-agents/agents/registry/business-monitor.md",
                                "target_agentcodex_role": "business-monitor",
                                "activation": "mapped-to-native-role",
                            }
                        ],
                        "commands": [
                            {
                                "id": "monitor",
                                "source_path": ".agentcodex/imports/data-agents/commands/monitor.py",
                                "target_agentcodex_command": "platform-health",
                                "activation": "mapped-to-native-command",
                            }
                        ],
                        "skills": [
                            {
                                "id": "patterns/data-quality",
                                "source_path": ".agentcodex/imports/data-agents/skills/patterns/data-quality/SKILL.md",
                            }
                        ],
                        "kb_files": [".agentcodex/imports/data-agents/kb/data-quality/index.md"],
                        "mcp_servers": ["fabric"],
                        "hooks": [".agentcodex/imports/data-agents/hooks/security_hook.py"],
                        "tests": [".agentcodex/imports/data-agents/tests/test_monitor.py"],
                        "templates": [".agentcodex/imports/data-agents/templates/pipeline-spec.md"],
                        "activation_policy": {
                            "no_duplicate_rule": "Do not create duplicate active surfaces",
                            "native_codex_rule": "Translate behavior to native Codex files before activation.",
                        },
                    },
                    indent=2,
                ),
            )
            old_root = validate_agentcodex.ROOT
            old_import = validate_agentcodex.DATA_AGENTS_IMPORT_ROOT
            old_registry = validate_agentcodex.DATA_AGENTS_EXTENSION_PATH
            old_commands = validate_agentcodex.COMMANDS_DIR
            try:
                validate_agentcodex.ROOT = root
                validate_agentcodex.DATA_AGENTS_IMPORT_ROOT = root / ".agentcodex" / "imports" / "data-agents"
                validate_agentcodex.DATA_AGENTS_EXTENSION_PATH = root / ".agentcodex" / "data-agents-extension.json"
                validate_agentcodex.COMMANDS_DIR = root / "docs" / "commands"
                errors: list[str] = []

                validate_agentcodex.validate_data_agents_extension_registry(errors)

                self.assertTrue(any("mapped agent target missing" in error for error in errors), errors)
            finally:
                validate_agentcodex.ROOT = old_root
                validate_agentcodex.DATA_AGENTS_IMPORT_ROOT = old_import
                validate_agentcodex.DATA_AGENTS_EXTENSION_PATH = old_registry
                validate_agentcodex.COMMANDS_DIR = old_commands


if __name__ == "__main__":
    unittest.main()
