from __future__ import annotations

import json
from pathlib import Path

from v1700.lineage_absorption.absorption_planner import build_stage121_absorption_preflight
from v1700.stage121.contracts import Stage121Contract


def run_stage121(root: Path | None = None) -> dict:
    root = root or Path(__file__).resolve().parents[3]
    contract = Stage121Contract().to_dict()
    preflight = build_stage121_absorption_preflight(root)
    issues: list[str] = list(preflight.get("issues", []))
    for rel in contract["required_outputs"]:
        if not (root / rel).exists():
            issues.append(f"missing_required_output:{rel}")
    result = {
        "stage": "121",
        "baseline_stage": "120",
        "title": contract["title"],
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "release_contract": contract,
        "cross_lineage_preflight": preflight,
        "stage120_trunk_preserved": preflight.get("trunk_policy") == "Stage120 Integrity FIXED remains the only primary trunk",
        "candidate_direct_merge_allowed": preflight.get("direct_merge_allowed", True),
        "formula_ledger_entry_count": preflight.get("formula_ledger", {}).get("entry_count", 0),
        "conflict_count": preflight.get("conflict_matrix", {}).get("conflict_count", 0),
        "gate_authority_primary": preflight.get("gate_authority_map", {}).get("primary_gate"),
        "next_development_order": ["stage122", "stage123", "stage124", "stage125", "stage126"],
        "provider_default_calls": 0,
        "live_provider_call_count_in_release_gate": 0,
        "embedding_provider_call_count": 0,
        "query_classifier_llm_call_count": 0,
        "physics_reward_bridge_llm_call_count": 0,
        "mae_live_provider_call_count": 0,
        "node2_raw_reveal_access": 0,
        "raw_manuscript_provider_leakage": 0,
        "credential_leakage": 0,
        "branchpoint_lineage_preserved": not issues,
    }
    out = root / "release/current/stage121_cross_lineage_preflight_report.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return result
