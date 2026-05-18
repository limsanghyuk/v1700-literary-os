from __future__ import annotations

from pathlib import Path

from .orchestrator import run_stage104


def run_stage104_smoke(root: Path | None = None) -> dict:
    return run_stage104(root or Path.cwd())
