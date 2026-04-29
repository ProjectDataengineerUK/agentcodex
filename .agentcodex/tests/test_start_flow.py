from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPTS_DIR = ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import start  # noqa: E402


class StartFlowTests(unittest.TestCase):
    def setUp(self) -> None:
        self.original_root = start.ROOT
        self.original_reports_root = start.REPORTS_ROOT

    def tearDown(self) -> None:
        start.ROOT = self.original_root
        start.REPORTS_ROOT = self.original_reports_root

    def test_detects_base_project_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / ".agentcodex").mkdir()
            (root / "README.md").write_text("hello\n", encoding="utf-8")
            (root / "docs").mkdir()
            (root / "docs" / "notes.md").write_text("# Notes\ncontent\n", encoding="utf-8")

            evidence = start.collect_project_evidence(root)

            self.assertTrue(start.has_base_project(evidence))
            self.assertIn("README.md", evidence.base_files)
            self.assertIn("docs/notes.md", evidence.markdown_files)
            self.assertIn("README.md", evidence.all_files)

    def test_light_install_agents_file_alone_is_not_existing_project(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / ".agentcodex").mkdir()
            (root / "AGENTS.md").write_text("# Project AGENTS\n", encoding="utf-8")
            (root / "Requisitos.pdf").write_text("pdf placeholder\n", encoding="utf-8")

            evidence = start.collect_project_evidence(root)

            self.assertIn("AGENTS.md", evidence.base_files)
            self.assertFalse(start.has_base_project(evidence))

    def test_collect_project_evidence_ignores_generated_context(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / ".agentcodex").mkdir()
            (root / "context.md").write_text(
                "# Context\n\n- generated_at: `2026-04-29T00:00:00+00:00`\n\n## Directory Scan\n",
                encoding="utf-8",
            )
            (root / "notes.md").write_text("# Notes\nOperator input\n", encoding="utf-8")

            evidence = start.collect_project_evidence(root)

            self.assertNotIn("context.md", evidence.markdown_files)
            self.assertNotIn("context.md", evidence.all_files)
            self.assertIn("notes.md", evidence.markdown_files)

    def test_context_includes_markdown_pdf_and_video_inventory(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / ".agentcodex").mkdir()
            (root / "notes.md").write_text("# Title\nFirst line\n", encoding="utf-8")
            (root / "report.pdf").write_text("binary placeholder", encoding="utf-8")
            (root / "report.txt").write_text("pdf transcript sidecar\n", encoding="utf-8")
            (root / "clip.mp4").write_text("video placeholder", encoding="utf-8")
            (root / "clip.srt").write_text("video transcript sidecar\n", encoding="utf-8")

            start.ROOT = root
            evidence = start.collect_project_evidence(root)
            context = start.build_context_markdown(evidence)

            self.assertIn("notes.md", context)
            self.assertIn("First line", context)
            self.assertIn("report.pdf", context)
            self.assertIn("pdf transcript sidecar", context)
            self.assertIn("multimodal review rule", context)
            self.assertIn("visual inspection", context)
            self.assertIn("clip.mp4", context)
            self.assertIn("video transcript sidecar", context)

    def test_brainstorm_prompt_mentions_context_and_brainstorm(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / ".agentcodex").mkdir()
            (root / "notes.md").write_text("# Notes\nCustomer churn model\n", encoding="utf-8")
            (root / "requirements.pdf").write_text("pdf placeholder", encoding="utf-8")
            (root / "requirements.txt").write_text("Build a governed Databricks pipeline\n", encoding="utf-8")

            start.ROOT = root
            evidence = start.collect_project_evidence(root)
            prompt = start.build_brainstorm_prompt(evidence)

            self.assertIn("Read context.md", prompt)
            self.assertIn("brainstorm flow", prompt)
            self.assertIn(str(root), prompt)
            self.assertIn("## Evidence Brief", prompt)
            self.assertIn("## Sequential Brainstorm Flow", prompt)
            self.assertIn("Build a governed Databricks pipeline", prompt)
            self.assertIn("Do not treat extracted PDF text as complete", prompt)
            self.assertIn("Start now with only Question 1", prompt)

    def test_deliver_selected_reports_writes_detailed_report_for_option_one(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / ".agentcodex" / "reports").mkdir(parents=True)
            (root / "README.md").write_text("# Project\nUseful context\n", encoding="utf-8")

            start.ROOT = root
            start.REPORTS_ROOT = root / ".agentcodex" / "reports"
            evidence = start.collect_project_evidence(root)

            answers, written = start.deliver_selected_reports(evidence, "1")

            self.assertEqual(answers["detailed_report"], "yes")
            self.assertEqual(answers["maturity_report"], "no")
            self.assertEqual(len(written), 1)
            self.assertTrue((root / ".agentcodex" / "reports" / "start-detailed-project-report.md").exists())
            self.assertIn("start-detailed-project-report.md", answers["delivered_report"])

    def test_maturity_report_includes_dataops_mlops_llmops_tracks(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / ".agentcodex" / "reports").mkdir(parents=True)
            (root / "README.md").write_text("# Project\nUseful context\n", encoding="utf-8")
            (root / ".agentcodex" / "features" / "example-project-standard").mkdir(parents=True)
            (root / ".agentcodex" / "model-routing.json").write_text("{}", encoding="utf-8")

            start.ROOT = root
            start.REPORTS_ROOT = root / ".agentcodex" / "reports"
            evidence = start.collect_project_evidence(root)

            answers, written = start.deliver_selected_reports(evidence, "2")
            report = (root / ".agentcodex" / "reports" / "start-maturity-report.md").read_text(encoding="utf-8")

            self.assertEqual(answers["maturity_report"], "yes")
            self.assertEqual(len(written), 1)
            self.assertIn("DataOps MLOps LLMOps Maturity Report", report)
            self.assertIn("- DATAOPS:", report)
            self.assertIn("- MLOPS:", report)
            self.assertIn("- LLMOPS:", report)


if __name__ == "__main__":
    unittest.main()
