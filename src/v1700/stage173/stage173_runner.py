from __future__ import annotations

from pathlib import Path

from v1700.governance_contract import run_stage173_governance_contract


def run(root: Path | None = None) -> dict:
    return run_stage173_governance_contract(root)
