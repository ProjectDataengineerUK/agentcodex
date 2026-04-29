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


class WorkflowFidelityValidationTests(unittest.TestCase):
    def _write_contract(self, root: Path, missing_marker_phase: str | None = None) -> Path:
        source_contract = root / ".agentcodex" / "imports" / "agentspec" / "sdd" / "architecture" / "WORKFLOW_CONTRACTS.yaml"
        source_contract.parent.mkdir(parents=True, exist_ok=True)
        source_contract.write_text("version: test\n", encoding="utf-8")

        phases: dict[str, dict] = {}
        for phase in sorted(validate_agentcodex.WORKFLOW_PHASES):
            surface = root / "surfaces" / f"{phase}.md"
            surface.parent.mkdir(parents=True, exist_ok=True)
            surface.write_text("required-behavior\n", encoding="utf-8")
            marker = "missing-behavior" if phase == missing_marker_phase else "required-behavior"
            phases[phase] = {
                "source_refs": [],
                "surfaces": [
                    {
                        "path": str(surface.relative_to(root)),
                        "required_markers": [marker],
                    }
                ],
            }

        contract_path = root / ".agentcodex" / "workflow-fidelity.json"
        contract_path.write_text(
            json.dumps(
                {
                    "version": "test",
                    "source": {
                        "name": "test",
                        "contract": str(source_contract.relative_to(root)),
                    },
                    "phases": phases,
                },
                indent=2,
            ),
            encoding="utf-8",
        )
        return contract_path

    def test_workflow_fidelity_contract_passes_when_markers_exist(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            contract_path = self._write_contract(root)
            old_root = validate_agentcodex.ROOT
            old_contract = validate_agentcodex.WORKFLOW_FIDELITY_PATH
            try:
                validate_agentcodex.ROOT = root
                validate_agentcodex.WORKFLOW_FIDELITY_PATH = contract_path
                errors: list[str] = []

                validate_agentcodex.validate_workflow_fidelity(errors)

                self.assertEqual(errors, [])
            finally:
                validate_agentcodex.ROOT = old_root
                validate_agentcodex.WORKFLOW_FIDELITY_PATH = old_contract

    def test_workflow_fidelity_contract_fails_when_marker_is_removed(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            contract_path = self._write_contract(root, missing_marker_phase="define")
            old_root = validate_agentcodex.ROOT
            old_contract = validate_agentcodex.WORKFLOW_FIDELITY_PATH
            try:
                validate_agentcodex.ROOT = root
                validate_agentcodex.WORKFLOW_FIDELITY_PATH = contract_path
                errors: list[str] = []

                validate_agentcodex.validate_workflow_fidelity(errors)

                self.assertTrue(
                    any("Workflow fidelity marker missing for define" in error for error in errors),
                    errors,
                )
            finally:
                validate_agentcodex.ROOT = old_root
                validate_agentcodex.WORKFLOW_FIDELITY_PATH = old_contract


if __name__ == "__main__":
    unittest.main()
