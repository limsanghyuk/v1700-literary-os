from __future__ import annotations


def build_stage96_manifest() -> dict:
    return {
        "stage": "96",
        "title": "Narrative Physics Optimization, Manuscript Learning, and Provider Ensemble Arbitration",
        "status": "pass_pending_export",
        "baseline_stage": "95",
        "phases": ["96A_narrative_physics_optimization", "96B_manuscript_learning", "96C_provider_ensemble_arbitration"],
        "provider_default_calls": 0,
        "live_provider_call_count": 0,
        "node2_raw_reveal_access_count": 0,
    }


def build_stage96_branchpoint_trace_manifest() -> dict:
    return {
        "stage": "96",
        "branchpoint_authority": "Stage95 Native Narrative Physics + Stage96 release gate",
        "survival_required": True,
        "tracepoints": [
            "surface_only_node2",
            "branchpoint_survival_weight_non_decreasing",
            "provider_candidate_veto_on_leakage",
            "directive_level_merge_only",
        ],
    }
