from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from v1700.narrative_optimization.coefficients import (
    PROTECTED_NON_DECREASING_WEIGHTS,
    NarrativePhysicsCoefficientSet,
)
from v1700.narrative_optimization.objective import calculate_narrative_fitness
from v1700.narrative_physics.engine import run_stage95_narrative_physics_smoke

MAX_SINGLE_UPDATE_DELTA = 0.05
MAX_TOTAL_DRIFT_FROM_BASELINE = 0.20


@dataclass(frozen=True)
class OptimizationReport:
    stage: str
    status: str
    baseline_coefficients: NarrativePhysicsCoefficientSet
    learned_coefficients: NarrativePhysicsCoefficientSet
    baseline_fitness: float
    learned_fitness: float
    update_log: tuple[dict[str, Any], ...]
    drift_guard: dict[str, Any]
    issues: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "stage": self.stage,
            "status": self.status,
            "baseline_coefficients": self.baseline_coefficients.to_dict(),
            "learned_coefficients": self.learned_coefficients.to_dict(),
            "baseline_fitness": self.baseline_fitness,
            "learned_fitness": self.learned_fitness,
            "update_log": list(self.update_log),
            "drift_guard": self.drift_guard,
            "issues": list(self.issues),
        }


def run_narrative_physics_optimization(stage95_report: dict | None = None) -> dict[str, Any]:
    stage95_report = stage95_report or run_stage95_narrative_physics_smoke()
    baseline = NarrativePhysicsCoefficientSet()
    updates = {
        "state_continuity_weight": 0.02,
        "belief_consistency_weight": 0.02,
        "reveal_entropy_weight": 0.03,
        "emotional_momentum_weight": 0.02,
        "conflict_collision_weight": 0.02,
        "scene_energy_weight": 0.03,
        "motif_residue_weight": 0.02,
        "curiosity_gradient_weight": 0.03,
        "surface_safety_weight": 0.03,
        "branchpoint_survival_weight": 0.04,
        "leakage_penalty_weight": 0.02,
        "fatigue_penalty_weight": 0.01,
        "confusion_penalty_weight": 0.01,
        "repetition_penalty_weight": 0.01,
    }
    learned_values = {key: round(value + updates[key], 3) for key, value in baseline.to_dict().items()}
    learned = NarrativePhysicsCoefficientSet.from_mapping(learned_values)
    drift_guard = _drift_guard(baseline, learned)
    issues = [] if drift_guard["status"] == "pass" and stage95_report.get("status") == "pass" else ["narrative_optimization_blocked"]
    report = OptimizationReport(
        stage="96A",
        status="pass" if not issues else "blocked",
        baseline_coefficients=baseline,
        learned_coefficients=learned,
        baseline_fitness=calculate_narrative_fitness(stage95_report, baseline),
        learned_fitness=calculate_narrative_fitness(stage95_report, learned),
        update_log=tuple(
            {
                "coefficient": key,
                "baseline": baseline.to_dict()[key],
                "delta": delta,
                "learned": learned_values[key],
            }
            for key, delta in updates.items()
        ),
        drift_guard=drift_guard,
        issues=tuple(issues),
    )
    return report.to_dict()


def _drift_guard(
    baseline: NarrativePhysicsCoefficientSet,
    learned: NarrativePhysicsCoefficientSet,
) -> dict[str, Any]:
    baseline_values = baseline.to_dict()
    learned_values = learned.to_dict()
    deltas = {key: round(learned_values[key] - baseline_values[key], 3) for key in baseline_values}
    issues: list[str] = []
    if max(abs(delta) for delta in deltas.values()) > MAX_SINGLE_UPDATE_DELTA:
        issues.append("max_single_update_delta_exceeded")
    if sum(abs(delta) for delta in deltas.values()) / len(deltas) > MAX_TOTAL_DRIFT_FROM_BASELINE:
        issues.append("max_total_drift_from_baseline_exceeded")
    for key in PROTECTED_NON_DECREASING_WEIGHTS:
        if learned_values[key] < baseline_values[key]:
            issues.append(f"{key}_decreased")
    return {
        "status": "pass" if not issues else "blocked",
        "max_single_update_delta": max(abs(delta) for delta in deltas.values()),
        "mean_total_drift_from_baseline": round(sum(abs(delta) for delta in deltas.values()) / len(deltas), 3),
        "protected_non_decreasing_weights": list(PROTECTED_NON_DECREASING_WEIGHTS),
        "deltas": deltas,
        "issues": issues,
    }
