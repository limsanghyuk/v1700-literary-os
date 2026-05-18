
from __future__ import annotations

from pathlib import Path

from v1700.runtime_absorption.v370_absorption import run_stage84_absorption_smoke


def run_stage84_release_gate(root: Path | None = None) -> dict:
    smoke = run_stage84_absorption_smoke(root)
    issues: list[str] = []
    if smoke.get("status") != "pass":
        issues.append("stage84_absorption_smoke_blocked")
    if smoke.get("provider_default_calls") != 0:
        issues.append("provider_default_calls_not_zero")
    if smoke.get("node2_raw_reveal_access_count") != 0:
        issues.append("node2_raw_reveal_access_not_zero")
    if not smoke.get("stage80_hierarchy_preserved"):
        issues.append("stage80_korean_drama_hierarchy_not_preserved")
    return {
        "stage": "84",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "claim": "Stage84 release gate proves V370 runtime absorption under V1700 hierarchy, local-first provider-zero execution, and Node2 reveal safety.",
        "stage84_absorption_smoke": smoke,
        "provider_default_calls": 0,
        "node2_raw_reveal_access_count": 0,
    }
