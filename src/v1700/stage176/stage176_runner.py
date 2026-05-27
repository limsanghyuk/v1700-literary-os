from __future__ import annotations

from pathlib import Path

from v1700.lineage_review_gate import run_stage176_lineage_review_gate

def run(root: Path | None = None) -> dict:
    return run_stage176_lineage_review_gate(root)
