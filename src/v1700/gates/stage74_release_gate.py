from __future__ import annotations

from pathlib import Path

from v1700.gates.longform_execution_gate import run_longform_execution_gate
from v1700.gates.stage73_1_release_gate import run_stage73_1_release_gate


def run_stage74_release_gate(root: Path | None = None) -> dict:
    root = root or Path(__file__).resolve().parents[3]
    stage73_1 = run_stage73_1_release_gate(root)
    longform = run_longform_execution_gate(root)
    issues: list[str] = []
    if stage73_1.get("status") != "pass":
        issues.append("stage73_1_release_gate_blocked")
    if longform.get("status") != "pass":
        issues.append("longform_execution_gate_blocked")
    return {
        "stage": "74",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "stage73_1_release_gate": stage73_1,
        "longform_execution_gate": longform,
        "provider_default_calls": 0,
        "node2_raw_reveal_access_count": 0,
    }
