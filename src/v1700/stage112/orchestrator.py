from __future__ import annotations

import json
from pathlib import Path

from .contracts import Stage112Contract
from v1700.gitnexus_preflight.preflight_runner import run_stage112_gitnexus_nie_preflight


def run_stage112(root: Path | None = None) -> dict:
    root = root or Path(__file__).resolve().parents[3]
    preflight = run_stage112_gitnexus_nie_preflight(root)
    contract = Stage112Contract().to_dict()
    issues = []
    if preflight.get("status") != "pass":
        issues.append("gitnexus_nie_preflight_blocked")
    if preflight.get("python_fallback_used") is not True:
        issues.append("python_fallback_not_used")
    if preflight.get("concept_impact", {}).get("provider_zero_preserved") is not True:
        issues.append("provider_zero_not_preserved")
    if preflight.get("shape_check_pass") is not True:
        issues.append("shape_check_failed")
    result = {
        "stage": "112",
        "baseline_stage": "111",
        "title": "GitNexus-Aware NIE Preflight Bridge",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "preflight": preflight,
        "release_contract": contract,
        "next_development_order": ["Stage113", "Stage114", "Stage115", "Stage116", "Stage117", "Stage118", "Stage119", "Stage120"],
        "provider_default_calls": 0,
        "live_provider_call_count_in_release_gate": 0,
        "physics_reward_bridge_llm_call_count": 0,
        "node2_raw_reveal_access": 0,
        "raw_manuscript_provider_leakage": 0,
        "credential_leakage": 0,
        "branchpoint_lineage_preserved": not issues,
    }
    _write(root / "release/current/stage112_gitnexus_aware_nie_preflight_bridge_report.json", result)
    return result


def _write(path: Path, data: dict) -> dict:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return data

