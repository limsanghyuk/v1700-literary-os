from __future__ import annotations

from v1700.nie.predictive.contracts import DebtPrediction, PredictionReport
from v1700.nie.predictive.pne_core import PNECore


def _clip(value: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, float(value)))


class DebtPredictor:
    """Stage124 deterministic V555 DebtPredictor adapter.

    RandomForest training is intentionally disabled in release mode. The class
    uses a transparent heuristic fallback so Gate29 remains reproducible without
    sklearn and without runtime learning.
    """

    DEBT_CATEGORIES = (
        "unresolved_secret",
        "broken_foreshadow",
        "abandoned_thread",
        "arc_not_tracked",
        "arc_post_death",
        "arc_contradiction",
        "arc_inversion",
    )
    BLOCK_THRESHOLD = 0.60
    MIN_SAMPLES = 5

    def __init__(self, pne_core: PNECore | None = None, *, runtime_training_enabled: bool = False) -> None:
        self.pne_core = pne_core
        self.runtime_training_enabled = bool(runtime_training_enabled)
        self.sklearn_available = self._check_sklearn()
        self.trained_categories: dict[str, bool] = {}

    @staticmethod
    def _check_sklearn() -> bool:
        try:
            import sklearn  # noqa: F401
            return True
        except Exception:
            return False

    def train(self, pne_core: PNECore | None = None) -> dict[str, bool]:
        """Training is blocked in Stage124 release mode.

        This method returns category flags for compatibility with the V555 API,
        but it never fits a model while runtime_training_enabled is False.
        """
        if pne_core is not None:
            self.pne_core = pne_core
        if not self.runtime_training_enabled:
            self.trained_categories = {category: False for category in self.DEBT_CATEGORIES}
            return dict(self.trained_categories)
        # Even if explicitly enabled in experiments, keep deterministic fixture
        # behavior in Stage124 by not importing/fitting sklearn here.
        self.trained_categories = {category: False for category in self.DEBT_CATEGORIES}
        return dict(self.trained_categories)

    def predict(self, scene_id: str, current_severity: float = 0.5, horizon: int = 3) -> PredictionReport:
        predictions = tuple(
            self.predict_category(category, scene_id, current_severity=current_severity, horizon=horizon)
            for category in self.DEBT_CATEGORIES
        )
        return PredictionReport(
            scene_id=scene_id,
            horizon=horizon,
            predictions=predictions,
            threshold=self.BLOCK_THRESHOLD,
            sklearn_available=self.sklearn_available,
            runtime_training_enabled=self.runtime_training_enabled,
        )

    def predict_category(self, category: str, scene_id: str, current_severity: float = 0.5, horizon: int = 3) -> DebtPrediction:
        stats = self.pne_core.category_stats(category) if self.pne_core is not None else None
        if stats is None:
            failure_rate = 0.40
            mean_blast = 0.20
            total = 0
        else:
            failure_rate = stats.failure_rate()
            mean_blast = stats.mean_blast_ratio
            total = stats.total
        horizon_pressure = min(0.15, 0.03 * max(1, int(horizon)))
        probability = _clip(0.50 * current_severity + 0.30 * failure_rate + 0.15 * mean_blast + horizon_pressure)
        confidence = _clip(0.45 + min(0.35, total / 30.0) + 0.10 * (1.0 - abs(probability - 0.50)))
        return DebtPrediction(
            category=category,
            probability=round(probability, 6),
            confidence=round(confidence, 6),
            horizon=horizon,
            mode="heuristic_fallback",
        )
