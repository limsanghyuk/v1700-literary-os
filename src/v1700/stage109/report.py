from __future__ import annotations
from pathlib import Path
from .orchestrator import run_stage109

def build_report(root: Path | None = None) -> dict:
    return run_stage109(root)
