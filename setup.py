from __future__ import annotations

from pathlib import Path

from setuptools import find_packages, setup


ROOT = Path(__file__).resolve().parent
INSTALL_ROOT = Path("share") / "agentcodex"


EXCLUDED_PREFIXES = {
    ".agentcodex/workflows",
    ".agentcodex/archive/workflows",
    ".agentcodex/reports/workflows",
    ".agentcodex/cache",
    ".agentcodex/imports",
    ".agentcodex/observability/logs",
    ".agentcodex/observability/runs",
    ".agentcodex/observability/failures",
    ".agentcodex/observability/metrics",
    ".agentcodex/memory/candidates",
    ".agentcodex/memory/reviews",
    "plugins",
    ".agents",
}


def should_include(path: Path) -> bool:
    relative = path.relative_to(ROOT).as_posix()
    if "__pycache__" in path.parts or path.suffix == ".pyc":
        return False
    return not any(relative == prefix or relative.startswith(f"{prefix}/") for prefix in EXCLUDED_PREFIXES)


def collect_data_files() -> list[tuple[str, list[str]]]:
    groups: dict[str, list[str]] = {}
    for base in [ROOT / "scripts", ROOT / ".agentcodex", ROOT / "docs"]:
        for path in sorted(base.rglob("*")):
            if not path.is_file() or not should_include(path):
                continue
            relative_parent = path.relative_to(ROOT).parent
            target = (INSTALL_ROOT / relative_parent).as_posix()
            groups.setdefault(target, []).append(path.relative_to(ROOT).as_posix())
    return sorted(groups.items())


setup(
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    data_files=collect_data_files(),
)
