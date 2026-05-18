from __future__ import annotations

REQUIRED_KEYS = {
    "stage",
    "baseline_stage",
    "status",
    "issues",
    "repo_id",
    "index_fresh",
    "stale_index_detected",
    "queried_symbols",
    "impact_depth_1",
    "impact_depth_2",
    "impact_depth_3",
    "detect_changes",
    "concept_impact",
    "survival_matrix",
    "branchpoint_trace",
    "shape_check_pass",
    "release_gate_integration",
}


def shape_check_preflight(result: dict) -> dict:
    missing = sorted(REQUIRED_KEYS - set(result))
    bad_types = []
    if "issues" in result and not isinstance(result["issues"], list):
        bad_types.append("issues_not_list")
    if "queried_symbols" in result and not isinstance(result["queried_symbols"], list):
        bad_types.append("queried_symbols_not_list")
    if "survival_matrix" in result and not isinstance(result["survival_matrix"], dict):
        bad_types.append("survival_matrix_not_dict")
    return {"status": "pass" if not missing and not bad_types else "blocked", "missing_keys": missing, "bad_types": bad_types}

