from __future__ import annotations
from pathlib import Path
from .orchestrator import run_stage110

def run_smoke(root: Path | None = None) -> dict:
    result = run_stage110(root)
    return {"status": result.get("status"), "stage": "110"}
