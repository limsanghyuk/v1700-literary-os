from __future__ import annotations


def build_coefficient_memory(optimization: dict, features: tuple, privacy_report: dict) -> dict:
    return {
        "version": "stage96",
        "source_policy": "local_feature_only",
        "baseline_coefficients": optimization["baseline_coefficients"],
        "learned_coefficients": optimization["learned_coefficients"],
        "update_log": optimization["update_log"],
        "drift_guard": optimization["drift_guard"],
        "privacy_report": privacy_report,
        "feature_summary": {
            "scene_count": len(features),
            "reveal_event_count": sum(item.reveal_event_count for item in features),
            "curiosity_hook_count": sum(item.curiosity_hook_count for item in features),
            "branchpoint_touchpoint_count": sum(len(item.branchpoint_touchpoints) for item in features),
        },
    }
