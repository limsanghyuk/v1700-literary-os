from __future__ import annotations
from pathlib import Path
from v1700.future_absorption_deprecation_planner import run_stage183_future_absorption_deprecation_planner
def run(root: Path | None = None) -> dict: return run_stage183_future_absorption_deprecation_planner(root)
