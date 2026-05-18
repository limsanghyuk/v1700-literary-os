from __future__ import annotations
from pathlib import Path
from .orchestrator import run_stage108

def run_stage108_smoke(root: Path | None = None) -> dict:
    return run_stage108(root)
