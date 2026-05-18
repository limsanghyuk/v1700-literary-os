from __future__ import annotations

from v1700.narrative_optimization.objective import calculate_narrative_fitness
from v1700.provider_ensemble.contracts import ProviderCandidate


def score_candidate(candidate: ProviderCandidate, stage95_report: dict, optimization: dict) -> dict:
    narrative_fitness = calculate_narrative_fitness(
        stage95_report,
        _coefficient_proxy(optimization.get("learned_coefficients", {})),
    )
    provider_reliability = float(candidate.metadata.get("provider_average_score", 8.0))
    reader_surface_score = 9.2 if "surface" in candidate.normalized_response else 8.5
    agent_benchmark_score = 8.8
    cost_efficiency_score = max(0.0, 10.0 - candidate.estimated_cost)
    leakage_risk = 10.0 if candidate.safety_flags else 0.0
    branchpoint_regression_risk = 0.0 if not candidate.safety_flags else 3.0
    repetition_penalty = 0.0
    style_drift_penalty = 0.2 if candidate.provider_kind == "gemini" else 0.0
    total = (
        narrative_fitness * 0.28
        + reader_surface_score * 0.16
        + agent_benchmark_score * 0.12
        + provider_reliability * 0.18
        + cost_efficiency_score * 0.08
        - leakage_risk
        - branchpoint_regression_risk
        - repetition_penalty
        - style_drift_penalty
    )
    return {
        "candidate_id": candidate.candidate_id,
        "provider_id": candidate.provider_id,
        "narrative_fitness": narrative_fitness,
        "reader_surface_score": reader_surface_score,
        "agent_benchmark_score": agent_benchmark_score,
        "provider_reliability_score": provider_reliability,
        "cost_efficiency_score": round(cost_efficiency_score, 3),
        "leakage_risk": leakage_risk,
        "branchpoint_regression_risk": branchpoint_regression_risk,
        "style_drift_penalty": style_drift_penalty,
        "arbitration_score": round(total, 3),
    }


def _coefficient_proxy(values: dict):
    from v1700.narrative_optimization.coefficients import NarrativePhysicsCoefficientSet

    return NarrativePhysicsCoefficientSet.from_mapping(values) if values else NarrativePhysicsCoefficientSet()
