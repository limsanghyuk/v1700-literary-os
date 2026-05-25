from __future__ import annotations

from pathlib import Path
from typing import Any

from v1700.render_plan_builder import run_stage163_deterministic_render_plan_builder


def run_stage163(root: Path | None = None) -> dict[str, Any]:
    return run_stage163_deterministic_render_plan_builder(root)
