from __future__ import annotations

from pathlib import Path

from v1700.stage96.orchestrator import run_stage96_pipeline


def run_stage96_smoke(root: Path | None = None) -> dict:
    return run_stage96_pipeline(root)
