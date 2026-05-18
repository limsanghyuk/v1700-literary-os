from __future__ import annotations

from pathlib import Path
from .preflight_runner import run_stage112_gitnexus_nie_preflight


def write_stage112_preflight_report(path: Path) -> dict:
    report = run_stage112_gitnexus_nie_preflight(path.parents[2] if len(path.parents) > 2 else None)
    path.parent.mkdir(parents=True, exist_ok=True)
    return report

