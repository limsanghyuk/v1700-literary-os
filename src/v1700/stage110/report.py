from __future__ import annotations
import json
from pathlib import Path
from .orchestrator import run_stage110

def write_stage110_report(root: Path | None = None) -> dict:
    root = root or Path(__file__).resolve().parents[3]
    return run_stage110(root)
