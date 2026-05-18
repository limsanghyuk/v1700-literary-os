from __future__ import annotations

import math
from typing import Iterable

from v1700.nie.stability.contracts import TIdealReport


class TIdealLearner:
    """Bounded learner for ideal tension curve coefficients.

    Stage122 records the learned proposal as an evidence artifact but keeps
    release-gate runtime deterministic and bounded.
    """

    MAX_COEFF_SHIFT = 0.02

    def ideal(self, t: float, coeffs: dict[str, float]) -> float:
        return (
            coeffs["base"]
            + coeffs["main_amp"] * math.sin(2 * math.pi * t + coeffs["main_phase"])
            + coeffs["micro_amp"] * math.sin(6 * math.pi * t)
        )

    def fit_once(self, actual: Iterable[float], coeffs: dict[str, float] | None = None) -> TIdealReport:
        before = dict(coeffs or {"base": 0.60, "main_amp": 0.40, "main_phase": -0.50, "micro_amp": 0.20})
        values = list(actual)
        if not values:
            return TIdealReport("blocked", before, before, 0.0, 1.0, 1.0, False, ["no_actual_tension_values"])
        ts = [i / max(1, len(values) - 1) for i in range(len(values))]
        predictions = [self.ideal(t, before) for t in ts]
        residual_mean = sum(a - p for a, p in zip(values, predictions)) / len(values)
        after = dict(before)
        shift = max(-self.MAX_COEFF_SHIFT, min(self.MAX_COEFF_SHIFT, 0.1 * residual_mean))
        after["base"] = before["base"] + shift
        loss_before = sum((a - p) ** 2 for a, p in zip(values, predictions)) / len(values)
        after_predictions = [self.ideal(t, after) for t in ts]
        loss_after = sum((a - p) ** 2 for a, p in zip(values, after_predictions)) / len(values)
        max_shift = max(abs(after[k] - before[k]) for k in before)
        issues = []
        if max_shift > self.MAX_COEFF_SHIFT + 1e-9:
            issues.append("t_ideal_shift_exceeds_guard")
        if not (0.30 <= after["base"] <= 0.90):
            issues.append("t_ideal_base_out_of_bounds")
        return TIdealReport(
            status="pass" if not issues else "blocked",
            coefficients_before=before,
            coefficients_after=after,
            max_shift=max_shift,
            loss_before=loss_before,
            loss_after=loss_after,
            applied=True,
            issues=issues,
        )
