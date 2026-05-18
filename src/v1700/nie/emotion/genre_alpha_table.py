from __future__ import annotations

from v1700.nie.emotion.contracts import DIMENSIONS, GenreName, MomentumDimension, clamp

ALPHA_MIN = 0.30
ALPHA_MAX = 0.80
DEFAULT_LR = 0.005
MAX_SINGLE_ALPHA_SHIFT = 0.03
MAX_RUN_TOTAL_ALPHA_SHIFT = 0.10

GENRE_ALPHA_TABLE: dict[GenreName, dict[MomentumDimension, float]] = {
    "melodrama": {"tension": 0.50, "sympathy": 0.65, "dread": 0.35, "catharsis": 0.55},
    "thriller": {"tension": 0.70, "sympathy": 0.40, "dread": 0.65, "catharsis": 0.35},
    "family": {"tension": 0.45, "sympathy": 0.70, "dread": 0.30, "catharsis": 0.60},
    "generic": {"tension": 0.55, "sympathy": 0.55, "dread": 0.45, "catharsis": 0.50},
}


def act_influence(act_pos: float, dim: MomentumDimension) -> float:
    """Small deterministic four-act correction.

    The correction is deliberately bounded so AMW remains a calibration layer, not
    an uncontrolled optimizer. It gives later crisis/release positions slightly
    more process weight for the dimensions that normally dominate there.
    """

    t = clamp(act_pos, 0.0, 1.0)
    if dim == "tension":
        if 0.50 <= t < 0.75:
            return 0.05
        if t >= 0.75:
            return -0.02
    if dim == "sympathy":
        if t < 0.50:
            return 0.04
        if t >= 0.75:
            return 0.02
    if dim == "dread":
        if 0.25 <= t < 0.75:
            return 0.05
    if dim == "catharsis":
        if t >= 0.75:
            return 0.05
        if t < 0.25:
            return -0.03
    return 0.0


def initial_alpha(genre: GenreName, dim: MomentumDimension, act_pos: float = 0.5) -> float:
    table = GENRE_ALPHA_TABLE.get(genre, GENRE_ALPHA_TABLE["generic"])
    return clamp(table[dim] + act_influence(act_pos, dim), ALPHA_MIN, ALPHA_MAX)


def initial_alpha_state(genre: GenreName = "generic", act_pos: float = 0.5) -> dict[str, float]:
    return {dim: initial_alpha(genre, dim, act_pos) for dim in DIMENSIONS}
