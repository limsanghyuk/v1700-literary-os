from __future__ import annotations

from v1700.narrative_optimization.coefficients import NarrativePhysicsCoefficientSet


def calculate_narrative_fitness(metrics: dict, coefficients: NarrativePhysicsCoefficientSet | None = None) -> float:
    coefficients = coefficients or NarrativePhysicsCoefficientSet()
    values = _normalized_metrics(metrics)
    weights = coefficients.to_dict()
    reward = (
        weights["state_continuity_weight"] * values["state_continuity"]
        + weights["belief_consistency_weight"] * values["belief_consistency"]
        + weights["reveal_entropy_weight"] * values["reveal_entropy_health"]
        + weights["emotional_momentum_weight"] * values["emotional_momentum_health"]
        + weights["conflict_collision_weight"] * values["collision_productivity"]
        + weights["scene_energy_weight"] * values["scene_energy_transfer"]
        + weights["motif_residue_weight"] * values["motif_residue_payoff"]
        + weights["curiosity_gradient_weight"] * values["curiosity_gradient"]
        + weights["surface_safety_weight"] * values["node2_surface_safety"]
        + weights["branchpoint_survival_weight"] * values["branchpoint_survival"]
    )
    penalty = (
        weights["leakage_penalty_weight"] * values["leakage_penalty"]
        + weights["fatigue_penalty_weight"] * values["fatigue_penalty"]
        + weights["confusion_penalty_weight"] * values["confusion_penalty"]
        + weights["repetition_penalty_weight"] * values["repetition_penalty"]
    )
    return round(max(0.0, min(10.0, (reward / 11.6) * 10.0 - penalty)), 3)


def _normalized_metrics(metrics: dict) -> dict[str, float]:
    return {
        "state_continuity": _status(metrics.get("tensor", {}).get("status", "pass")),
        "belief_consistency": 1.0 if not metrics.get("belief_vectors", []) else 0.98,
        "reveal_entropy_health": _status(metrics.get("reveal_entropy", {}).get("status", "pass")),
        "emotional_momentum_health": _status(metrics.get("emotional_momentum", {}).get("status", "pass")),
        "collision_productivity": _status(metrics.get("conflict_collision", {}).get("status", "pass")),
        "scene_energy_transfer": _status(metrics.get("scene_energy", {}).get("status", "pass")),
        "motif_residue_payoff": _status(metrics.get("motif_residue", {}).get("status", "pass")),
        "curiosity_gradient": _status(metrics.get("curiosity_gradient", {}).get("status", "pass")),
        "node2_surface_safety": _status(metrics.get("surface_guard", {}).get("status", "pass")),
        "branchpoint_survival": _status(metrics.get("branchpoint_survival", {}).get("status", "pass")),
        "leakage_penalty": float(metrics.get("node2_raw_reveal_access_count", 0)),
        "fatigue_penalty": 0.0,
        "confusion_penalty": 0.0,
        "repetition_penalty": 0.0,
    }


def _status(status: str) -> float:
    return 1.0 if status == "pass" else 0.0
