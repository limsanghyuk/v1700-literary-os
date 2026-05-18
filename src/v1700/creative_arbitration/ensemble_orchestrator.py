from __future__ import annotations

from .arbitration_policy import arbitrate_candidates
from .candidate_lanes import build_candidate_lanes
from .literary_scorer import score_candidates
from .normalization import build_response_normalization_matrix
from .role_matrix import build_provider_role_matrix
from .sandbox_policy import build_release_provider_policy


def run_creative_arbitration() -> dict:
    roles = build_provider_role_matrix()
    candidates = build_candidate_lanes()
    normalization = build_response_normalization_matrix(candidates.get("candidates", []))
    scoring = score_candidates(normalization.get("normalized_candidates", []))
    arbitration = arbitrate_candidates(scoring.get("weighted_candidates", []))
    release_policy = build_release_provider_policy()
    reports = {
        "role_matrix": roles,
        "candidate_lanes": candidates,
        "response_normalization": normalization,
        "literary_scoring": scoring,
        "arbitration": arbitration,
        "release_provider_policy": release_policy,
    }
    issues = [name for name, report in reports.items() if report.get("status") != "pass"]
    return {
        "stage": "105",
        "baseline_stage": "104",
        "title": "Multi-Provider Creative Arbitration 2.0",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        **reports,
        "provider_default_calls": 0,
        "live_provider_call_count_in_release_gate": 0,
        "raw_manuscript_provider_leakage": 0,
        "node2_raw_reveal_access": 0,
        "credential_leakage": 0,
        "writer_approval_required": True,
        "python_fallback_required": True,
        "gitnexus_runtime_dependency_required": False,
    }
