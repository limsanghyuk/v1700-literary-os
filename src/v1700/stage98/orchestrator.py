from __future__ import annotations

from pathlib import Path

from v1700.studio_workflow.studio_orchestrator import run_stage98_studio_workflow


def run_stage98(root: Path | None = None) -> dict:
    return run_stage98_studio_workflow(root)
