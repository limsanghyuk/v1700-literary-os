from __future__ import annotations

from v1700.nie.predictive.contracts import PreemptiveResult
from v1700.nie.predictive.debt_predictor import DebtPredictor


class PreemptiveGate:
    """V555 PreemptiveGate absorbed as a secondary predictive gate."""

    BLOCK_THRESHOLD = 0.60

    def __init__(self, predictor: DebtPredictor, *, threshold: float = BLOCK_THRESHOLD, horizon: int = 3) -> None:
        self.predictor = predictor
        self.threshold = float(threshold)
        self.horizon = int(horizon)
        self._history: list[PreemptiveResult] = []

    def evaluate(self, scene_id: str, current_severity: float = 0.5, horizon: int | None = None) -> PreemptiveResult:
        h = int(horizon or self.horizon)
        report = self.predictor.predict(scene_id, current_severity=current_severity, horizon=h)
        high = report.high_risk
        issues: list[str] = []
        if report.runtime_training_enabled:
            issues.append("runtime_training_enabled_in_release")
        blocked = bool(high)
        status = "blocked" if blocked else "pass"
        result = PreemptiveResult(
            scene_id=scene_id,
            status=status,
            blocked=blocked,
            threshold=self.threshold,
            horizon=h,
            high_risk_categories=high,
            max_probability=report.max_probability(),
            prediction_report=report,
            authority_mode="secondary_predictive_gate",
            issues=tuple(issues),
        )
        self._history.append(result)
        return result

    def evaluate_batch(self, scene_ids: list[str], severities: list[float] | None = None, horizon: int | None = None) -> list[PreemptiveResult]:
        severities = severities if severities is not None else [0.5] * len(scene_ids)
        return [self.evaluate(scene_id, sev, horizon=horizon) for scene_id, sev in zip(scene_ids, severities)]

    def block_count(self) -> int:
        return sum(1 for r in self._history if r.blocked)

    def total_evaluated(self) -> int:
        return len(self._history)

    def block_rate(self) -> float:
        return round(self.block_count() / max(1, self.total_evaluated()), 6)

    def gate_summary(self) -> dict:
        return {
            "total_evaluated": self.total_evaluated(),
            "block_count": self.block_count(),
            "block_rate": self.block_rate(),
            "threshold": self.threshold,
            "horizon": self.horizon,
            "authority_mode": "secondary_predictive_gate",
        }
