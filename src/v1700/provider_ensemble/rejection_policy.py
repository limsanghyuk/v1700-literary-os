from __future__ import annotations

from v1700.provider_ensemble.contracts import ProviderCandidate

BLOCKING_FLAGS = {
    "Node2_raw_reveal_leakage",
    "READER_ONLY_leakage",
    "internal_marker_leakage",
    "credential_leakage",
    "branchpoint_survival_regression",
    "surface_safety_fail",
}


def rejection_reasons(candidate: ProviderCandidate, score: dict) -> tuple[str, ...]:
    reasons = [flag for flag in candidate.safety_flags if flag in BLOCKING_FLAGS]
    if score.get("arbitration_score", 0.0) < 4.0:
        reasons.append("arbitration_score_below_floor")
    if score.get("branchpoint_regression_risk", 0.0) > 0.0:
        reasons.append("branchpoint_regression_risk")
    return tuple(sorted(set(reasons)))
