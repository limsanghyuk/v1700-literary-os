from __future__ import annotations

from pathlib import Path
from typing import Any

from v1700.render_quality_boundary_preflight import run_stage165_render_quality_boundary_preflight


def run_stage165(root: Path | None = None) -> dict[str, Any]:
    return run_stage165_render_quality_boundary_preflight(root)
