from __future__ import annotations
from pathlib import Path
from v1700.upgrade_simulation_compatibility_sandbox import run_stage182_upgrade_simulation_compatibility_sandbox
def run(root: Path | None = None) -> dict: return run_stage182_upgrade_simulation_compatibility_sandbox(root)
