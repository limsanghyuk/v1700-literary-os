from __future__ import annotations


def review_change_risk(preflight_parts: dict) -> dict:
    risks = []
    if preflight_parts.get("stale_index", {}).get("stale_index_detected"):
        risks.append("stale_index_based_impact_forbidden")
    if preflight_parts.get("concept_impact", {}).get("provider_zero_preserved") is not True:
        risks.append("provider_zero_risk")
    missing_branchpoints = [k for k, ok in preflight_parts.get("survival_matrix", {}).items() if not ok]
    if missing_branchpoints:
        risks.append("branchpoint_survival_gap")
    planned_missing = preflight_parts.get("symbol_trace", {}).get("planned_nie_symbols_missing_but_allowed", [])
    return {
        "status": "pass" if not risks else "blocked",
        "risk_level": "LOW" if not risks else "BLOCK",
        "risks": risks,
        "planned_gaps_for_stage113_plus": planned_missing,
        "decision": "proceed_to_stage112_release_gate" if not risks else "block_until_preflight_fixed",
    }

