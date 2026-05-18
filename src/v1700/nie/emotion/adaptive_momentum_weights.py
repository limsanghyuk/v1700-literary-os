from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable

from v1700.nie.emotion.contracts import AMWDriftGuard, AMWInput, AMWUpdate, DIMENSIONS, GenreName, MomentumDimension, clamp
from v1700.nie.emotion.genre_alpha_table import (
    ALPHA_MAX,
    ALPHA_MIN,
    DEFAULT_LR,
    MAX_RUN_TOTAL_ALPHA_SHIFT,
    MAX_SINGLE_ALPHA_SHIFT,
    initial_alpha_state,
)


@dataclass
class AdaptiveMomentumWeights:
    """Bounded calibration layer for emotional momentum mixing ratios.

    Stage114 converts hard-coded emotional momentum ratios into auditable alpha
    parameters. The layer consumes process signals, observation signals, and
    cached MAE dimension scores. It never calls a provider and it never updates
    protected safety/branchpoint coefficients directly.
    """

    genre: GenreName = "generic"
    lr: float = DEFAULT_LR
    alpha: dict[str, float] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.alpha:
            self.alpha = initial_alpha_state(self.genre)
        self.alpha = {dim: clamp(self.alpha.get(dim, initial_alpha_state(self.genre)[dim]), ALPHA_MIN, ALPHA_MAX) for dim in DIMENSIONS}

    def update(self, item: AMWInput) -> AMWUpdate:
        alpha_before = clamp(self.alpha[item.dim], ALPHA_MIN, ALPHA_MAX)
        process = float(item.process_signal)
        observation = float(item.observation_signal)
        mae_score = float(item.mae_dim_score)
        delta = round(alpha_before * process + (1.0 - alpha_before) * observation, 6)
        loss = round((delta - mae_score) ** 2, 6)
        gradient = round(2.0 * (delta - mae_score) * (process - observation), 6)
        raw_after = round(alpha_before - self.lr * gradient, 6)
        raw_shift = raw_after - alpha_before
        bounded_shift = clamp(raw_shift, -MAX_SINGLE_ALPHA_SHIFT, MAX_SINGLE_ALPHA_SHIFT)
        alpha_after = clamp(alpha_before + bounded_shift, ALPHA_MIN, ALPHA_MAX)
        clamped = abs(bounded_shift - raw_shift) > 1e-9 or alpha_after != round(alpha_before + bounded_shift, 6)
        self.alpha[item.dim] = alpha_after
        return AMWUpdate(
            dim=item.dim,
            alpha_before=alpha_before,
            process_signal=round(process, 6),
            observation_signal=round(observation, 6),
            mae_dim_score=round(mae_score, 6),
            delta_dim=delta,
            loss=loss,
            gradient=gradient,
            raw_alpha_after=raw_after,
            alpha_after=alpha_after,
            shift=round(alpha_after - alpha_before, 6),
            clamped=clamped,
            reason="sgd_step_toward_mae_dimension_score_with_bounded_shift",
        )

    def update_many(self, inputs: Iterable[AMWInput]) -> tuple[AMWUpdate, ...]:
        return tuple(self.update(item) for item in inputs)

    def drift_guard(self, updates: tuple[AMWUpdate, ...]) -> AMWDriftGuard:
        issues: list[str] = []
        observed_max = max((abs(u.shift) for u in updates), default=0.0)
        observed_total = sum(abs(u.shift) for u in updates)
        for dim, value in self.alpha.items():
            if not ALPHA_MIN <= value <= ALPHA_MAX:
                issues.append(f"alpha_out_of_bounds:{dim}")
        if observed_max > MAX_SINGLE_ALPHA_SHIFT + 1e-9:
            issues.append("max_single_alpha_shift_exceeded")
        if observed_total > MAX_RUN_TOTAL_ALPHA_SHIFT + 1e-9:
            issues.append("max_run_total_alpha_shift_exceeded")
        protected_policy = {
            "surface_safety_tolerance_can_loosen": False,
            "branchpoint_sensitivity_can_decrease": False,
            "provider_zero_policy_can_change": False,
            "node2_raw_reveal_tolerance": 0,
        }
        return AMWDriftGuard(
            status="pass" if not issues else "blocked",
            alpha_min=ALPHA_MIN,
            alpha_max=ALPHA_MAX,
            max_single_shift=MAX_SINGLE_ALPHA_SHIFT,
            max_run_total_shift=MAX_RUN_TOTAL_ALPHA_SHIFT,
            observed_max_single_shift=round(observed_max, 6),
            observed_run_total_shift=round(observed_total, 6),
            protected_policy=protected_policy,
            issues=tuple(issues),
        )

    def to_dict(self) -> dict[str, float]:
        return {dim: float(self.alpha[dim]) for dim in DIMENSIONS}


def build_amw_inputs(
    dimension_scores: dict[str, float],
    process_signals: dict[str, float] | None = None,
    observation_signals: dict[str, float] | None = None,
    genre: GenreName = "melodrama",
    act_pos: float = 0.56,
) -> tuple[AMWInput, ...]:
    process_signals = process_signals or {
        "tension": 0.82,
        "sympathy": 0.68,
        "dread": 0.58,
        "catharsis": 0.66,
    }
    observation_signals = observation_signals or {
        "tension": 0.63,
        "sympathy": 0.76,
        "dread": 0.52,
        "catharsis": 0.60,
    }
    return tuple(
        AMWInput(
            dim=dim,  # type: ignore[arg-type]
            process_signal=process_signals[dim],
            observation_signal=observation_signals[dim],
            mae_dim_score=dimension_scores[dim],
            genre=genre,
            act_pos=act_pos,
        )
        for dim in DIMENSIONS
    )
