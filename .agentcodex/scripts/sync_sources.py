#!/usr/bin/env python3
from __future__ import annotations

import runpy
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPT_PATH = ROOT / "scripts" / "sync_sources.py"


if __name__ == "__main__":
    sys.path.insert(0, str(SCRIPT_PATH.parent))
    runpy.run_path(str(SCRIPT_PATH), run_name="__main__")
