from __future__ import annotations
from pathlib import Path
from v1700.migration_plan_compiler import run_stage181_migration_plan_compiler
def run(root: Path | None = None) -> dict: return run_stage181_migration_plan_compiler(root)
