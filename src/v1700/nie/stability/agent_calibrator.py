from __future__ import annotations

from v1700.nie.stability.contracts import CalibrationReport


class AgentCalibrator:
    """Bounded calibration for MAE agent weights.

    Absorbs V525 agent calibration concept without changing the Stage113 reward
    contract unless all bounds and normalization checks pass.
    """

    MIN_WEIGHT = 0.10
    MAX_WEIGHT = 0.45
    MAX_SHIFT = 0.05

    def calibrate(self, weights: dict[str, float], reliability: dict[str, float]) -> CalibrationReport:
        issues: list[str] = []
        before = dict(weights)
        raw: dict[str, float] = {}
        for agent, weight in weights.items():
            r = max(0.0, min(1.0, float(reliability.get(agent, 0.5))))
            proposed = weight + 0.05 * (r - 0.5)
            proposed = max(self.MIN_WEIGHT, min(self.MAX_WEIGHT, proposed))
            delta = max(-self.MAX_SHIFT, min(self.MAX_SHIFT, proposed - weight))
            raw[agent] = weight + delta
        total = sum(raw.values()) or 1.0
        after = {agent: value / total for agent, value in raw.items()}
        max_shift = max(abs(after.get(a, 0.0) - before.get(a, 0.0)) for a in before)
        total_shift = sum(abs(after.get(a, 0.0) - before.get(a, 0.0)) for a in before)
        if max_shift > self.MAX_SHIFT + 1e-9:
            issues.append("agent_weight_shift_exceeds_guard")
        if any(v < self.MIN_WEIGHT - 1e-9 or v > self.MAX_WEIGHT + 1e-9 for v in after.values()):
            issues.append("agent_weight_bounds_violation")
        if abs(sum(after.values()) - 1.0) > 1e-9:
            issues.append("agent_weight_sum_not_normalized")
        return CalibrationReport(
            status="pass" if not issues else "blocked",
            weights_before=before,
            weights_after=after,
            max_shift=max_shift,
            total_shift=total_shift,
            normalized_sum=sum(after.values()),
            issues=issues,
        )
