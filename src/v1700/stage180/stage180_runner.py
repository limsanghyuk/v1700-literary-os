from __future__ import annotations
from pathlib import Path
from v1700.architecture_drift_self_audit import run_stage180_architecture_drift_self_audit
def run(root: Path | None = None) -> dict: return run_stage180_architecture_drift_self_audit(root)
