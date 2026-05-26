from __future__ import annotations

from pathlib import Path
from typing import Any

from v1700.evaluation_boundary_preflight.report import run_stage171_evaluation_boundary_leakage_preflight


def run_stage171(root: Path | None = None) -> dict[str, Any]:
    return run_stage171_evaluation_boundary_leakage_preflight(root)
