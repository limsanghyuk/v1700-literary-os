from __future__ import annotations


def build_stage96_narrative_optimization_manifest() -> dict:
    return {
        "stage": "96A",
        "title": "Narrative Physics Optimization",
        "status": "pass_pending_export",
        "drift_guard": {
            "max_single_update_delta": 0.05,
            "max_total_drift_from_baseline": 0.20,
            "protected_non_decreasing_weights": [
                "branchpoint_survival_weight",
                "surface_safety_weight",
                "leakage_penalty_weight",
            ],
        },
    }
