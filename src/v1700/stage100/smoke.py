from __future__ import annotations

from pathlib import Path

from v1700.stage100.rc_orchestrator import run_stage100_rc


def run_stage100_smoke(root: Path | None = None) -> dict:
    report = run_stage100_rc(root)
    return {"stage": "100", "status": report.get("status", "blocked"), "report": report}

