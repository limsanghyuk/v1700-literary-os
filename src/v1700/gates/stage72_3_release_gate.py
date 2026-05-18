from __future__ import annotations

from pathlib import Path

from v1700.gates.pre_stage40_survival_gate import run_pre_stage40_survival_gate
from v1700.gates.stage72_2_release_gate import run_stage72_2_release_gate
from v1700.graph_nexus.tools.survival_matrix import build_survival_matrix


def run_stage72_3_release_gate(root: Path) -> dict:
    stage72_2 = run_stage72_2_release_gate(root)
    survival = run_pre_stage40_survival_gate(root)
    matrix = build_survival_matrix(root)

    issues: list[str] = []
    if stage72_2.get("status") != "pass":
        issues.append("stage72_2_release_gate_blocked")
    if survival.get("status") != "pass":
        issues.append("pre_stage40_survival_gate_blocked")
    if matrix.get("status") != "pass":
        issues.append("survival_matrix_blocked")

    return {
        "stage": "72.3",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "stage72_2_release_gate": stage72_2,
        "pre_stage40_survival_gate": survival,
        "survival_matrix": matrix,
        "provider_default_calls": 0,
        "node2_raw_reveal_access_count": 0,
    }
