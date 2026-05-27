from __future__ import annotations

from pathlib import Path

from v1700.project_boundary_governor import run_stage175_project_boundary_governor

def run(root: Path | None = None) -> dict:
    return run_stage175_project_boundary_governor(root)
