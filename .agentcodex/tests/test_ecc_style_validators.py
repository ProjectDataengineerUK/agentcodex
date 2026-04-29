from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPTS_DIR = ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import validate_agentcodex  # noqa: E402


class EccStyleValidatorTests(unittest.TestCase):
    def _write_file(self, root: Path, rel_path: str, text: str = "content\n") -> Path:
        path = root / rel_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        return path

    def test_workflow_security_rejects_privileged_untrusted_checkout(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self._write_file(
                root,
                ".github/workflows/unsafe.yml",
                """
on:
  pull_request_target:

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          ref: ${{ github.event.pull_request.head.sha }}
""",
            )
            old_dir = validate_agentcodex.GITHUB_WORKFLOWS_DIR
            try:
                validate_agentcodex.GITHUB_WORKFLOWS_DIR = root / ".github" / "workflows"
                errors: list[str] = []

                validate_agentcodex.validate_ecc_style_workflow_security(errors)

                self.assertTrue(any("workflow-security violation" in error for error in errors), errors)
            finally:
                validate_agentcodex.GITHUB_WORKFLOWS_DIR = old_dir

    def test_imported_skill_validator_requires_skill_entrypoint(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / ".agentcodex/imports/ecc/skills/example").mkdir(parents=True)
            old_root = validate_agentcodex.ECC_IMPORT_ROOT
            try:
                validate_agentcodex.ECC_IMPORT_ROOT = root / ".agentcodex" / "imports" / "ecc"
                errors: list[str] = []

                validate_agentcodex.validate_ecc_style_skills(errors)

                self.assertTrue(any("missing SKILL.md" in error for error in errors), errors)
            finally:
                validate_agentcodex.ECC_IMPORT_ROOT = old_root

    def test_imported_command_validator_rejects_unknown_command_reference(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self._write_file(root, ".agentcodex/imports/ecc/commands/build.md", "Use `/missing`.\n")
            self._write_file(root, ".agentcodex/imports/ecc/agents/planner.md")
            self._write_file(root, ".agentcodex/imports/ecc/skills/tdd/SKILL.md")
            old_root = validate_agentcodex.ECC_IMPORT_ROOT
            try:
                validate_agentcodex.ECC_IMPORT_ROOT = root / ".agentcodex" / "imports" / "ecc"
                errors: list[str] = []

                validate_agentcodex.validate_ecc_style_commands(errors)

                self.assertTrue(any("non-existent command /missing" in error for error in errors), errors)
            finally:
                validate_agentcodex.ECC_IMPORT_ROOT = old_root

    def test_no_personal_paths_rejects_user_home_path(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            bad_path = "/" + "Users" + "/alice/project"
            self._write_file(root, "docs/example.md", f"Bad path: {bad_path}\n")
            old_roots = validate_agentcodex.ECC_STYLE_TEXT_ROOTS
            try:
                validate_agentcodex.ECC_STYLE_TEXT_ROOTS = [root / "docs"]
                errors: list[str] = []

                validate_agentcodex.validate_ecc_style_no_personal_paths(errors)

                self.assertTrue(any("no-personal-paths violation" in error for error in errors), errors)
            finally:
                validate_agentcodex.ECC_STYLE_TEXT_ROOTS = old_roots


if __name__ == "__main__":
    unittest.main()
