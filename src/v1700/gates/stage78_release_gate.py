from __future__ import annotations
from pathlib import Path
from v1700.gates.stage77_release_gate import run_stage77_release_gate
from v1700.drama_execution import run_drama_execution_smoke


def run_stage78_release_gate(root: Path | None = None) -> dict:
    root = root or Path(__file__).resolve().parents[3]
    stage77 = run_stage77_release_gate(root)
    drama = run_drama_execution_smoke()
    issues: list[str] = []
    if stage77.get("status") != "pass":
        issues.append("stage77_release_gate_blocked")
    if drama.get("status") != "pass":
        issues.append("drama_execution_engine_blocked")
    return {"stage": "78", "status": "pass" if not issues else "blocked", "issues": issues, "stage77_release_gate": stage77, "drama_execution_engine": drama, "provider_default_calls": 0, "node2_raw_reveal_access_count": 0}
