from __future__ import annotations

from v1700.nie.predictive.contracts import FeedbackReport, MetricsSnapshot, PredictionRecord


class FeedbackLearner:
    """Prediction-vs-actual metrics tracker with no release-time retraining."""

    PRECISION_TARGET = 0.70
    MIN_RETRAIN_SAMPLES = 20

    def __init__(self, *, threshold: float = 0.60, precision_target: float = PRECISION_TARGET, runtime_retraining_enabled: bool = False) -> None:
        self.threshold = float(threshold)
        self.precision_target = float(precision_target)
        self.runtime_retraining_enabled = bool(runtime_retraining_enabled)
        self._records: list[PredictionRecord] = []

    def record(self, scene_id: str, category: str, predicted_probability: float, actual_occurred: bool) -> PredictionRecord:
        rec = PredictionRecord(scene_id, category, float(predicted_probability), bool(actual_occurred), self.threshold)
        self._records.append(rec)
        return rec

    def record_many(self, records: list[tuple[str, str, float, bool]]) -> None:
        for scene_id, category, prob, actual in records:
            self.record(scene_id, category, prob, actual)

    def metrics(self) -> MetricsSnapshot:
        tp = fp = fn = tn = 0
        for rec in self._records:
            if rec.predicted_high and rec.actual_occurred:
                tp += 1
            elif rec.predicted_high and not rec.actual_occurred:
                fp += 1
            elif not rec.predicted_high and rec.actual_occurred:
                fn += 1
            else:
                tn += 1
        return MetricsSnapshot(len(self._records), tp, fp, fn, tn)

    def should_retrain(self) -> bool:
        return self.runtime_retraining_enabled and len(self._records) >= self.MIN_RETRAIN_SAMPLES

    def report(self) -> FeedbackReport:
        metrics = self.metrics()
        issues: list[str] = []
        if self.should_retrain():
            issues.append("runtime_retraining_triggered")
        if not metrics.meets_precision_target(self.precision_target):
            issues.append("precision_target_not_met")
        return FeedbackReport(
            status="pass" if not issues else "blocked",
            metrics=metrics,
            precision_target=self.precision_target,
            records=tuple(self._records),
            runtime_retraining_triggered=self.should_retrain(),
            issues=tuple(issues),
        )
