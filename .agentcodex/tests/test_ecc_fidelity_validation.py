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


class EccFidelityValidationTests(unittest.TestCase):
    def _write_file(self, root: Path, rel_path: str, text: str = "marker\n") -> None:
        path = root / rel_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

    def _write_contract(self, root: Path, missing_marker: bool = False) -> Path:
        self._write_file(root, ".agentcodex/imports/manifest.json", "{}\n")
        self._write_file(root, ".agentcodex/imports/ecc/agents_md", "required marker\n")
        self._write_file(root, ".agentcodex/imports/ecc/agents/planner.md")
        self._write_file(root, "docs/roles/planner.md")
        self._write_file(root, "scripts/validate_agentcodex.py")
        runtime_text = "wrong\n" if missing_marker else "runtime marker\n"
        self._write_file(root, ".codex/config.toml", runtime_text)

        contract_path = root / ".agentcodex" / "ecc-fidelity.json"
        contract_path.write_text(
            json.dumps(
                {
                    "version": "test",
                    "source": {
                        "name": "test",
                        "root": ".agentcodex/imports/ecc",
                        "manifest": ".agentcodex/imports/manifest.json",
                    },
                    "preserved_surfaces": {
                        "agents_md": {
                            "required_files": [".agentcodex/imports/ecc/agents_md"],
                            "required_markers": ["required marker"],
                        },
                        "agents": {
                            "path": ".agentcodex/imports/ecc/agents",
                            "pattern": "*.md",
                            "min_files": 1,
                        },
                    },
                    "active_adaptations": {
                        "codex_runtime": [
                            {
                                "path": ".codex/config.toml",
                                "required_markers": ["runtime marker"],
                            }
                        ],
                        "direct_role_matches": {
                            "min_matches": 1,
                            "roles": ["planner.md"],
                        },
                        "agentcodex_validation_stack": {
                            "required_files": ["scripts/validate_agentcodex.py"],
                        },
                    },
                    "intentional_differences": ["test difference"],
                },
                indent=2,
            ),
            encoding="utf-8",
        )
        return contract_path

    def test_ecc_fidelity_contract_passes_when_required_surfaces_exist(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            contract_path = self._write_contract(root)
            old_root = validate_agentcodex.ROOT
            old_contract = validate_agentcodex.ECC_FIDELITY_PATH
            try:
                validate_agentcodex.ROOT = root
                validate_agentcodex.ECC_FIDELITY_PATH = contract_path
                errors: list[str] = []

                validate_agentcodex.validate_ecc_fidelity(errors)

                self.assertEqual(errors, [])
            finally:
                validate_agentcodex.ROOT = old_root
                validate_agentcodex.ECC_FIDELITY_PATH = old_contract

    def test_ecc_fidelity_contract_fails_when_marker_is_removed(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            contract_path = self._write_contract(root, missing_marker=True)
            old_root = validate_agentcodex.ROOT
            old_contract = validate_agentcodex.ECC_FIDELITY_PATH
            try:
                validate_agentcodex.ROOT = root
                validate_agentcodex.ECC_FIDELITY_PATH = contract_path
                errors: list[str] = []

                validate_agentcodex.validate_ecc_fidelity(errors)

                self.assertTrue(
                    any("ECC fidelity marker missing" in error for error in errors),
                    errors,
                )
            finally:
                validate_agentcodex.ROOT = old_root
                validate_agentcodex.ECC_FIDELITY_PATH = old_contract


if __name__ == "__main__":
    unittest.main()
