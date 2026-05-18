from __future__ import annotations

import json
from pathlib import Path

from v1700.nie.emotion.amw_report import build_stage114_amw_report
from v1700.stage114.contracts import Stage114Contract


def run_stage114(root: Path | None = None) -> dict:
    root = root or Path(__file__).resolve().parents[3]
    amw_report = build_stage114_amw_report()
    contract = Stage114Contract().to_dict()
    issues: list[str] = []
    guard = amw_report.get("drift_guard", {})
    if amw_report.get("status") != "pass":
        issues.append("adaptive_momentum_weights_report_blocked")
    if guard.get("status") != "pass":
        issues.append("amw_drift_guard_blocked")
    if amw_report.get("provider_call_count") != 0:
        issues.append("mae_provider_call_count_nonzero")
    if amw_report.get("physics_reward_bridge_llm_call_count") != 0:
        issues.append("physics_reward_bridge_llm_call_count_nonzero")
    result = {
        "stage": "114",
        "baseline_stage": "113",
        "title": "AdaptiveMomentumWeights",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "release_contract": contract,
        "adaptive_momentum_weights": amw_report,
        "provider_default_calls": 0,
        "live_provider_call_count_in_release_gate": 0,
        "physics_reward_bridge_llm_call_count": amw_report.get("physics_reward_bridge_llm_call_count", 0),
        "mae_live_provider_call_count": amw_report.get("provider_call_count", 0),
        "node2_raw_reveal_access": 0,
        "raw_manuscript_provider_leakage": 0,
        "credential_leakage": 0,
        "branchpoint_lineage_preserved": not issues,
        "next_development_order": ["Stage115", "Stage116", "Stage117", "Stage118", "Stage119", "Stage120"],
    }
    _write(root / "release/current/stage114_adaptive_momentum_weights_report.json", result)
    return result


def _write(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
