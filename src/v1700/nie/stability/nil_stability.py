from __future__ import annotations

from typing import Any

from v1700.nie.stability.contracts import StabilityReport, StabilitySignal


def _score_signal(value: float, target: float, tolerance: float) -> float:
    if tolerance <= 0:
        return 1.0 if value == target else 0.0
    return max(0.0, 1.0 - abs(value - target) / tolerance)


class NILStabilityModule:
    """Deterministic V525-style NIL stability adapter for Stage120 reports.

    This module absorbs the stability idea only. It does not mutate runtime
    coefficients and it never calls providers.
    """

    def evaluate(self, nil_report: dict[str, Any]) -> StabilityReport:
        components = {c.get("name"): c for c in nil_report.get("components", [])}
        reward_summary = components.get("reward_bridge", {}).get("summary", {})
        amw_summary = components.get("adaptive_momentum_weights", {}).get("summary", {})
        cim_summary = components.get("character_influence_matrix", {}).get("summary", {})
        rag_summary = components.get("domain_rag_fusion", {}).get("summary", {})
        tension_summary = components.get("narrative_tension_curve", {}).get("summary", {})

        advantage = float(reward_summary.get("advantage", 0.0))
        amw_shift = float(amw_summary.get("drift_guard", {}).get("observed_run_total_shift", 1.0))
        triangle_count = float(cim_summary.get("triangle_count", 0.0))
        intent_count = float(rag_summary.get("classified_query_count", 0.0))
        loss = float(tension_summary.get("loss", {}).get("final_loss", 1.0))

        signals = [
            StabilitySignal("reward_advantage", advantage, 0.25, 0.25, 0.25, "pass"),
            StabilitySignal("amw_run_drift", amw_shift, 0.20, 0.00, 0.10, "pass" if amw_shift <= 0.10 else "blocked"),
            StabilitySignal("triangle_coverage", triangle_count, 0.20, 10.0, 10.0, "pass" if triangle_count >= 1 else "blocked"),
            StabilitySignal("rag_intent_coverage", intent_count, 0.15, 3.0, 3.0, "pass" if intent_count >= 3 else "blocked"),
            StabilitySignal("tension_final_loss", loss, 0.20, 0.0, 0.05, "pass" if loss <= 0.05 else "blocked"),
        ]
        weighted_score = 0.0
        total_weight = 0.0
        for signal in signals:
            weighted_score += signal.weight * _score_signal(signal.value, signal.target, signal.tolerance)
            total_weight += signal.weight
        score = weighted_score / total_weight if total_weight else 0.0
        issues = [s.name for s in signals if s.status == "blocked"]
        status = "pass" if score >= 0.80 and not issues else "blocked"
        return StabilityReport(status=status, score=score, signals=signals, issues=issues)
