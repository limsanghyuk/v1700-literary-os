from __future__ import annotations
from pathlib import Path
from .provider_sandbox_orchestrator import run_stage107_5

def run_smoke(root: Path | None = None) -> dict:
    return run_stage107_5(root)
