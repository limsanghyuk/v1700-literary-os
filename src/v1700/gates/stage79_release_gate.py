from __future__ import annotations
from pathlib import Path
from v1700.gates.stage78_release_gate import run_stage78_release_gate
from v1700.integration import run_full_literary_os_smoke


def run_stage79_release_gate(root: Path | None = None) -> dict:
    root = root or Path(__file__).resolve().parents[3]
    stage78 = run_stage78_release_gate(root)
    integration = run_full_literary_os_smoke()
    issues: list[str] = []
    if stage78.get("status") != "pass":
        issues.append("stage78_release_gate_blocked")
    if integration.get("status") != "pass":
        issues.append("full_literary_os_integration_blocked")
    final = integration.get("final_output", {})
    if final.get("scene_count_total", 0) < 532:
        issues.append("stage79_scene_scale_incomplete")
    return {"stage": "79", "status": "pass" if not issues else "blocked", "issues": issues, "stage78_release_gate": stage78, "full_literary_os_integration": integration, "provider_default_calls": 0, "node2_raw_reveal_access_count": 0}
