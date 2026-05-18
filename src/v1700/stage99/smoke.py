from __future__ import annotations

from pathlib import Path

from v1700.stage99.impact_baseline import run_stage99_0_gitnexus_impact_baseline
from v1700.security_hardening.report import run_stage99_1_security_privacy_hardening
from v1700.stage99.gate_replay import run_stage99_2_gate_replay_freeze


def run_stage99_smoke(root: Path | None = None) -> dict:
    root = root or Path.cwd()
    impact = run_stage99_0_gitnexus_impact_baseline(root)
    security = run_stage99_1_security_privacy_hardening(root)
    replay = run_stage99_2_gate_replay_freeze(root)
    return {
        "stage": "99",
        "status": "pass" if all(report.get("status") == "pass" for report in (impact, security, replay)) else "blocked",
        "stage99_0_status": impact.get("status"),
        "stage99_1_status": security.get("status"),
        "stage99_2_status": replay.get("status"),
    }
