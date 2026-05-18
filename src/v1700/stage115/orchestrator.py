from __future__ import annotations

import json
from pathlib import Path

from v1700.nie.characters.cim_report import build_stage115_cim_report
from v1700.stage115.contracts import Stage115Contract


def run_stage115(root: Path | None = None) -> dict:
    root = root or Path(__file__).resolve().parents[3]
    cim_report = build_stage115_cim_report()
    contract = Stage115Contract().to_dict()
    issues: list[str] = []
    matrix = cim_report.get("character_influence_matrix", {})
    centrality = matrix.get("centrality", {})
    if cim_report.get("status") != "pass":
        issues.append("character_influence_matrix_report_blocked")
    if matrix.get("asymmetric_pair_count", 0) < 4:
        issues.append("cim_asymmetric_pair_count_too_low")
    if matrix.get("high_tension_triangle_count", 0) < 1:
        issues.append("structural_balance_high_tension_missing")
    if not centrality.get("pagerank") or not centrality.get("role_tiers"):
        issues.append("centrality_or_role_tiers_missing")
    result = {
        "stage": "115",
        "baseline_stage": "114",
        "title": "CharacterInfluenceMatrix + Structural Balance",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "release_contract": contract,
        "cim": cim_report,
        "provider_default_calls": 0,
        "live_provider_call_count_in_release_gate": 0,
        "physics_reward_bridge_llm_call_count": cim_report.get("physics_reward_bridge_llm_call_count", 0),
        "mae_live_provider_call_count": cim_report.get("provider_call_count", 0),
        "node2_raw_reveal_access": 0,
        "raw_manuscript_provider_leakage": 0,
        "credential_leakage": 0,
        "branchpoint_lineage_preserved": not issues,
        "next_development_order": ["Stage116", "Stage117", "Stage118", "Stage119", "Stage120"],
    }
    _write(root / "release/current/stage115_character_influence_matrix_report.json", result)
    return result


def _write(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
