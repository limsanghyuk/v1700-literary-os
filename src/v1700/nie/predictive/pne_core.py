from __future__ import annotations

import math
from collections import defaultdict
from collections.abc import Iterable

from v1700.nie.predictive.contracts import CategoryStats, PatternLibrarySnapshot, RepairOutcome


class PatternLibrary:
    """Stage124 adapter for V555 PNE PatternLibrary.

    The library stores frozen/deterministic repair outcomes only. It does not
    train models or mutate narrative graph state in release mode.
    """

    def __init__(self) -> None:
        self._outcomes: list[RepairOutcome] = []

    def record(self, outcome: RepairOutcome) -> None:
        self._outcomes.append(outcome)

    def record_batch(self, outcomes: Iterable[RepairOutcome]) -> None:
        for outcome in outcomes:
            self.record(outcome)

    def all_outcomes(self) -> tuple[RepairOutcome, ...]:
        return tuple(self._outcomes)

    def total_outcomes(self) -> int:
        return len(self._outcomes)

    def categories(self) -> tuple[str, ...]:
        return tuple(sorted({o.category for o in self._outcomes}))

    def get_stats(self, category: str) -> CategoryStats | None:
        selected = [o for o in self._outcomes if o.category == category]
        if not selected:
            return None
        total = len(selected)
        successes = sum(1 for o in selected if o.success)
        mean_severity = sum(o.severity for o in selected) / total
        mean_blast = sum(o.blast_ratio for o in selected) / total
        return CategoryStats(category, total, successes, mean_severity, mean_blast)

    def feature_vector(self, category: str) -> tuple[float, float, float, float]:
        stats = self.get_stats(category)
        if stats is None:
            return (0.0, 0.0, 0.0, 0.0)
        return (
            stats.success_rate(),
            round(stats.mean_severity, 6),
            round(stats.mean_blast_ratio, 6),
            round(math.log1p(stats.total), 6),
        )

    def global_feature_vector(self) -> tuple[float, float, float, float]:
        total = self.total_outcomes()
        if not total:
            return (0.0, 0.0, 0.0, 0.0)
        successes = sum(1 for o in self._outcomes if o.success)
        mean_severity = sum(o.severity for o in self._outcomes) / total
        mean_blast = sum(o.blast_ratio for o in self._outcomes) / total
        return (
            round(successes / total, 6),
            round(mean_severity, 6),
            round(mean_blast, 6),
            round(math.log1p(total), 6),
        )

    def snapshot(self) -> PatternLibrarySnapshot:
        categories = {
            category: self.get_stats(category).to_dict()
            for category in self.categories()
            if self.get_stats(category) is not None
        }
        return PatternLibrarySnapshot(self.total_outcomes(), categories, self.global_feature_vector())


class PNECore:
    """V555 PNECore concept absorbed as frozen outcome collector."""

    def __init__(self) -> None:
        self.library = PatternLibrary()

    def ingest_outcome(self, outcome: RepairOutcome) -> None:
        self.library.record(outcome)

    def ingest_outcomes(self, outcomes: Iterable[RepairOutcome]) -> None:
        self.library.record_batch(outcomes)

    def total_ingested(self) -> int:
        return self.library.total_outcomes()

    def category_stats(self, category: str) -> CategoryStats | None:
        return self.library.get_stats(category)

    def feature_vector(self, category: str) -> tuple[float, float, float, float]:
        return self.library.feature_vector(category)

    def global_feature_vector(self) -> tuple[float, float, float, float]:
        return self.library.global_feature_vector()

    def snapshot(self) -> dict:
        return self.library.snapshot().to_dict()
