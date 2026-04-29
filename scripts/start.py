#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Iterable
import sys


ROOT = Path.cwd()
REPORTS_ROOT = ROOT / ".agentcodex" / "reports"
FEATURES_ROOT = ROOT / ".agentcodex" / "features"
CONTEXT_PATH = ROOT / "context.md"
IGNORED_DIRS = {".git", ".agentcodex", ".codex", "dist", "build", "node_modules", "__pycache__", ".venv", "venv"}
BASE_MARKERS = {
    "README.md",
    "AGENTS.md",
    "pyproject.toml",
    "package.json",
    "go.mod",
    "Cargo.toml",
    "pom.xml",
    "Makefile",
    "requirements.txt",
    "docker-compose.yml",
}
MARKDOWN_SUFFIX = ".md"
PDF_SUFFIX = ".pdf"
VIDEO_SUFFIXES = {".mp4", ".mov", ".mkv", ".avi", ".webm", ".m4v"}
TEXT_SIDEcars = {".txt", ".md", ".srt", ".vtt"}


@dataclass(frozen=True)
class ProjectEvidence:
    base_files: list[str]
    markdown_files: list[str]
    pdf_files: list[str]
    video_files: list[str]
    top_level_entries: list[str]


def now_iso() -> str:
    return datetime.now(UTC).isoformat()


def slugify(value: str) -> str:
    cleaned = "".join(ch if ch.isalnum() else "_" for ch in value.strip().lower())
    cleaned = "_".join(part for part in cleaned.split("_") if part)
    return cleaned or "start"


def prompt_yes_no(question: str, default: bool = False) -> bool:
    suffix = "[Y/n]" if default else "[y/N]"
    while True:
        answer = input(f"{question} {suffix} ").strip().lower()
        if not answer:
            return default
        if answer in {"y", "yes", "sim", "s"}:
            return True
        if answer in {"n", "no", "nao", "não"}:
            return False
        print("Enter yes or no.")


def prompt_choice(question: str, options: list[tuple[str, str]]) -> tuple[str, str]:
    print(question)
    for key, label in options:
        print(f"({key}) {label}")
    while True:
        answer = input("Choose one option: ").strip().lower()
        for key, label in options:
            if answer == key:
                return key, label
        print("Invalid choice.")


def prompt_nonempty(label: str) -> str:
    while True:
        value = input(f"{label}: ").strip()
        if value:
            return value
        print("This field is required.")


def ensure_dirs() -> None:
    REPORTS_ROOT.mkdir(parents=True, exist_ok=True)
    FEATURES_ROOT.mkdir(parents=True, exist_ok=True)


def collect_top_level_entries(root: Path) -> list[str]:
    items: list[str] = []
    for entry in sorted(root.iterdir()):
        if entry.name in IGNORED_DIRS:
            continue
        if entry.is_dir():
            items.append(f"{entry.name}/")
        else:
            items.append(entry.name)
    return items


def first_non_empty_line(path: Path, limit: int = 240) -> str:
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if line and not line.startswith("#"):
            return line[:limit]
    return ""


def sidecar_text(path: Path) -> str | None:
    for suffix in TEXT_SIDEcars:
        candidate = path.with_suffix(suffix)
        if candidate.exists() and candidate.is_file():
            try:
                text = candidate.read_text(encoding="utf-8", errors="replace").strip()
            except OSError:
                continue
            if text:
                return text[:800]
    return None


def collect_project_evidence(root: Path) -> ProjectEvidence:
    base_files: list[str] = []
    markdown_files: list[str] = []
    pdf_files: list[str] = []
    video_files: list[str] = []

    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if any(part in IGNORED_DIRS for part in path.parts):
            continue
        rel = str(path.relative_to(root))
        if path.name in BASE_MARKERS or path.suffix.lower() in {".toml", ".yaml", ".yml"} and path.name in {"pyproject.toml", "package.json"}:
            base_files.append(rel)
        if path.suffix.lower() == MARKDOWN_SUFFIX:
            markdown_files.append(rel)
        elif path.suffix.lower() == PDF_SUFFIX:
            pdf_files.append(rel)
        elif path.suffix.lower() in VIDEO_SUFFIXES:
            video_files.append(rel)

    return ProjectEvidence(
        base_files=sorted(base_files),
        markdown_files=sorted(markdown_files),
        pdf_files=sorted(pdf_files),
        video_files=sorted(video_files),
        top_level_entries=collect_top_level_entries(root),
    )


def has_base_project(evidence: ProjectEvidence) -> bool:
    return bool(evidence.base_files)


def build_base_project_report(evidence: ProjectEvidence, answers: dict[str, str]) -> str:
    lines = [
        "# Start Report",
        "",
        f"- generated_at: `{now_iso()}`",
        f"- root: `{ROOT}`",
        "",
        "## Scan",
        "",
        f"- base files detected: {len(evidence.base_files)}",
        f"- markdown files detected: {len(evidence.markdown_files)}",
        f"- pdf files detected: {len(evidence.pdf_files)}",
        f"- video files detected: {len(evidence.video_files)}",
        "",
        "## Selected Reports",
        "",
        f"- detailed project report: {answers['detailed_report']}",
        f"- maturity report: {answers['maturity_report']}",
        f"- vulnerability report: {answers['vulnerability_report']}",
        f"- improvement report: {answers['improvement_report']}",
        "",
        "## Base Files",
        "",
    ]
    lines.extend(f"- `{item}`" for item in evidence.base_files or ["[none]"])
    lines.extend(
        [
            "",
            "## Next Action",
            "",
            "- Review the selected outputs and continue with the most relevant report or workflow phase.",
        ]
    )
    return "\n".join(lines) + "\n"


def build_context_markdown(evidence: ProjectEvidence) -> str:
    lines = [
        "# Context",
        "",
        f"- generated_at: `{now_iso()}`",
        f"- root: `{ROOT}`",
        "",
        "## Directory Scan",
        "",
        f"- top_level_entries: {', '.join(evidence.top_level_entries) if evidence.top_level_entries else '[none]'}",
        f"- base_files: {len(evidence.base_files)}",
        f"- markdown_files: {len(evidence.markdown_files)}",
        f"- pdf_files: {len(evidence.pdf_files)}",
        f"- video_files: {len(evidence.video_files)}",
        "",
        "## Markdown Evidence",
        "",
    ]
    if evidence.markdown_files:
        for rel_path in evidence.markdown_files:
            path = ROOT / rel_path
            excerpt = first_non_empty_line(path)
            if not excerpt:
                excerpt = "[empty or unreadable]"
            lines.append(f"- `{rel_path}`")
            lines.append(f"  - excerpt: {excerpt}")
    else:
        lines.append("- [none]")

    lines.extend(["", "## PDF Evidence", ""])
    if evidence.pdf_files:
        for rel_path in evidence.pdf_files:
            path = ROOT / rel_path
            transcript = sidecar_text(path)
            lines.append(f"- `{rel_path}`")
            if transcript:
                lines.append(f"  - extracted text: {transcript}")
            else:
                lines.append("  - extracted text: unavailable in this environment")
    else:
        lines.append("- [none]")

    lines.extend(["", "## Video Evidence", ""])
    if evidence.video_files:
        for rel_path in evidence.video_files:
            path = ROOT / rel_path
            transcript = sidecar_text(path)
            lines.append(f"- `{rel_path}`")
            if transcript:
                lines.append(f"  - transcript: {transcript}")
            else:
                lines.append("  - transcript: unavailable in this environment")
    else:
        lines.append("- [none]")

    lines.extend(
        [
            "",
            "## Brainstorm Prompt",
            "",
            "You are the AgentCodex workflow-brainstormer.",
            "Use the context in this file to start a structured brainstorm in English.",
            "Ask one question at a time, prefer multiple-choice prompts when possible, and keep the first phase focused on problem framing, users, constraints, samples, and candidate approaches.",
        ]
    )
    return "\n".join(lines) + "\n"


def build_brainstorm_prompt(evidence: ProjectEvidence) -> str:
    return "\n".join(
        [
            "You are a specialist prompt engineer and AgentCodex workflow-brainstormer.",
            "Read context.md before asking anything else.",
            "Start with one question at a time and prefer multiple-choice prompts when the options are clear.",
            "If the repository already has base project files, ask the operator whether they want: a detailed project report, a maturity report, a vulnerability report, and an improvement report.",
            "If the repository does not yet have base project files, extract the raw context from markdown files and any available sidecar text for PDFs or videos, then begin the brainstorm flow.",
            "Create a BRAINSTORM artifact in English with the project context, candidate approaches, YAGNI cuts, and a clear next step into define.",
            f"Repository root: {ROOT}",
            f"Detected base files: {len(evidence.base_files)}",
            f"Detected markdown files: {len(evidence.markdown_files)}",
            f"Detected pdf files: {len(evidence.pdf_files)}",
            f"Detected video files: {len(evidence.video_files)}",
        ]
    ) + "\n"


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def main() -> int:
    if not (ROOT / ".agentcodex").exists():
        print("AgentCodex is not installed in this directory. Install it before running start.", file=sys.stderr)
        return 1

    ensure_dirs()
    evidence = collect_project_evidence(ROOT)

    if has_base_project(evidence):
        detailed = prompt_yes_no("Do you want a detailed project report?", default=True)
        maturity = prompt_yes_no("Do you want the project maturity level?", default=True)
        vulnerability = prompt_yes_no("Do you want a vulnerability report?", default=False)
        improvement = prompt_yes_no("Do you want a project improvement report?", default=True)
        answers = {
            "detailed_report": "yes" if detailed else "no",
            "maturity_report": "yes" if maturity else "no",
            "vulnerability_report": "yes" if vulnerability else "no",
            "improvement_report": "yes" if improvement else "no",
        }
        report_path = REPORTS_ROOT / "start-report.md"
        write_text(report_path, build_base_project_report(evidence, answers))
        print(f"Created start report: {report_path.relative_to(ROOT)}")
        return 0

    context_path = CONTEXT_PATH
    write_text(context_path, build_context_markdown(evidence))
    print(f"Created context file: {context_path.relative_to(ROOT)}")

    prompt_path = REPORTS_ROOT / "start-brainstorm-prompt.md"
    write_text(prompt_path, build_brainstorm_prompt(evidence))
    print(f"Created brainstorm prompt: {prompt_path.relative_to(ROOT)}")

    feature_slug = slugify(ROOT.name)
    brainstorm_path = FEATURES_ROOT / f"BRAINSTORM_{feature_slug}.md"
    write_text(
        brainstorm_path,
        "\n".join(
            [
                f"# BRAINSTORM_{feature_slug.upper()}",
                "",
                "## Metadata",
                "",
                f"- feature: `{feature_slug}`",
                "- phase: `brainstorm`",
                "- status: `draft`",
                "- owner: `operator`",
                f"- updated_at: `{now_iso()}`",
                "",
                "## Prompt",
                "",
                "Use `context.md` as the source of truth and follow the brainstorm prompt stored in `.agentcodex/reports/start-brainstorm-prompt.md`.",
                "",
                "## Exit Check",
                "",
                "- [x] context.md created",
                "- [x] brainstorm prompt created",
                "- [x] next step ready for workflow-brainstormer",
            ]
        )
        + "\n",
    )
    print(f"Created brainstorm artifact: {brainstorm_path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
