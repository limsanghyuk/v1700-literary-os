from __future__ import annotations

from pathlib import Path

from v1700.gates.drse_quality_gate import run_drse_quality_gate
from v1700.gates.literary_formula_survival_gate import run_literary_formula_survival_gate


def run_stage73_1_release_gate(root: Path | None = None) -> dict:
    root = root or Path(__file__).resolve().parents[3]
    formula = run_literary_formula_survival_gate(root)
    drse = run_drse_quality_gate(root)
    issues: list[str] = []
    if formula.get("status") != "pass":
        issues.append("literary_formula_survival_gate_blocked")
    if drse.get("status") != "pass":
        issues.append("drse_quality_gate_blocked")
    return {
        "stage": "73.1",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "literary_formula_survival_gate": formula,
        "drse_quality_gate": drse,
        "provider_default_calls": 0,
        "node2_raw_reveal_access_count": 0,
    }
