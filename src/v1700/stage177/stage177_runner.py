from __future__ import annotations

from pathlib import Path

from v1700.operational_safety_rollback_governance import run_stage177_operational_safety_rollback_governance

def run(root: Path | None = None) -> dict:
    return run_stage177_operational_safety_rollback_governance(root)
