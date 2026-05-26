from __future__ import annotations

from pathlib import Path
from typing import Any

from v1700.evaluation_body_contract import run_stage167_evaluation_contract


def run_stage167(root: Path | None = None) -> dict[str, Any]:
    return run_stage167_evaluation_contract(root)

