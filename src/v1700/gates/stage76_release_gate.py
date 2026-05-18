from __future__ import annotations
from pathlib import Path
from v1700.gates.stage75_release_gate import run_stage75_release_gate
from v1700.reabsorption import run_stage60_reabsorption_smoke


def run_stage76_release_gate(root: Path | None = None) -> dict:
    root = root or Path(__file__).resolve().parents[3]
    stage75 = run_stage75_release_gate(root)
    stage60 = run_stage60_reabsorption_smoke()
    issues: list[str] = []
    if stage75.get("status") != "pass":
        issues.append("stage75_release_gate_blocked")
    if stage60.get("status") != "pass":
        issues.append("stage60_literary_engine_reabsorption_blocked")
    return {"stage": "76", "status": "pass" if not issues else "blocked", "issues": issues, "stage75_release_gate": stage75, "stage60_reabsorption": stage60, "provider_default_calls": 0, "node2_raw_reveal_access_count": 0}
