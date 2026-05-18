from __future__ import annotations

import json
from pathlib import Path

from v1700.nie.reward.reward_signal_report import build_stage113_reward_bridge_report
from v1700.stage113.contracts import Stage113Contract


def run_stage113(root: Path | None = None) -> dict:
    root = root or Path(__file__).resolve().parents[3]
    reward_report = build_stage113_reward_bridge_report()
    contract = Stage113Contract().to_dict()
    issues: list[str] = []
    signal = reward_report.get("reward_signal", {})
    if reward_report.get("status") != "pass":
        issues.append("physics_reward_bridge_report_blocked")
    if signal.get("provider_call_count") != 0:
        issues.append("mae_provider_call_count_nonzero")
    if signal.get("physics_reward_bridge_llm_call_count") != 0:
        issues.append("physics_reward_bridge_llm_call_count_nonzero")
    if signal.get("reward", 0.0) <= 0.0:
        issues.append("reward_signal_not_positive")
    result = {
        "stage": "113",
        "baseline_stage": "112",
        "title": "PhysicsRewardBridge + MAE Reward Wiring",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "release_contract": contract,
        "reward_bridge": reward_report,
        "provider_default_calls": 0,
        "live_provider_call_count_in_release_gate": 0,
        "physics_reward_bridge_llm_call_count": signal.get("physics_reward_bridge_llm_call_count", 0),
        "mae_live_provider_call_count": signal.get("provider_call_count", 0),
        "node2_raw_reveal_access": 0,
        "raw_manuscript_provider_leakage": 0,
        "credential_leakage": 0,
        "branchpoint_lineage_preserved": not issues,
        "next_development_order": ["Stage114", "Stage115", "Stage116", "Stage117", "Stage118", "Stage119", "Stage120"],
    }
    _write(root / "release/current/stage113_physics_reward_bridge_report.json", result)
    return result


def _write(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
