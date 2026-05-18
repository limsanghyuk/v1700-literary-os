from __future__ import annotations

from pathlib import Path

from v1700.stage98.orchestrator import run_stage98


def run_stage98_smoke(root: Path | None = None) -> dict:
    report = run_stage98(root)
    return {"status": report.get("status", "blocked"), "report": report}
