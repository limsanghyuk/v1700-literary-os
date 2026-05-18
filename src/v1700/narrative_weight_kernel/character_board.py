from __future__ import annotations

from v1700.narrative_weight_kernel.contracts import (
    BoardPieceRole,
    CharacterProfileScore,
    CharacterSeed,
    NarrativeWeightVector,
)

BOARD_PRIORS: dict[BoardPieceRole, dict[str, float]] = {
    "king": {
        "agency": 0.95,
        "desire_pressure": 0.90,
        "wound_pressure": 0.80,
        "knowledge_asymmetry": 0.65,
        "reveal_pressure": 0.70,
        "emotional_momentum": 0.85,
        "reader_attention": 0.95,
    },
    "queen": {
        "agency": 0.92,
        "desire_pressure": 0.84,
        "wound_pressure": 0.68,
        "knowledge_asymmetry": 0.78,
        "reveal_pressure": 0.82,
        "emotional_momentum": 0.80,
        "reader_attention": 0.88,
    },
    "rook": {
        "agency": 0.78,
        "desire_pressure": 0.70,
        "wound_pressure": 0.52,
        "knowledge_asymmetry": 0.58,
        "reveal_pressure": 0.55,
        "emotional_momentum": 0.62,
        "reader_attention": 0.66,
    },
    "bishop": {
        "agency": 0.64,
        "desire_pressure": 0.62,
        "wound_pressure": 0.76,
        "knowledge_asymmetry": 0.84,
        "reveal_pressure": 0.70,
        "emotional_momentum": 0.66,
        "reader_attention": 0.72,
    },
    "knight": {
        "agency": 0.72,
        "desire_pressure": 0.76,
        "wound_pressure": 0.63,
        "knowledge_asymmetry": 0.70,
        "reveal_pressure": 0.62,
        "emotional_momentum": 0.78,
        "reader_attention": 0.74,
    },
    "pawn": {
        "agency": 0.42,
        "desire_pressure": 0.50,
        "wound_pressure": 0.46,
        "knowledge_asymmetry": 0.42,
        "reveal_pressure": 0.34,
        "emotional_momentum": 0.48,
        "reader_attention": 0.38,
    },
    "shadow": {
        "agency": 0.82,
        "desire_pressure": 0.88,
        "wound_pressure": 0.74,
        "knowledge_asymmetry": 0.90,
        "reveal_pressure": 0.88,
        "emotional_momentum": 0.76,
        "reader_attention": 0.83,
    },
}

PROFILE_AXES = (
    "agency",
    "desire_pressure",
    "wound_pressure",
    "knowledge_asymmetry",
    "reveal_pressure",
    "emotional_momentum",
    "reader_attention",
)


def score_character_profile(
    character: CharacterSeed,
    weights: NarrativeWeightVector | None = None,
) -> CharacterProfileScore:
    weights = weights or NarrativeWeightVector()
    priors = BOARD_PRIORS[character.board_piece]
    axis_scores: dict[str, float] = {}
    for axis in PROFILE_AXES:
        base = priors[axis]
        if axis == "agency":
            base = (base + _bounded(character.agency_bias)) / 2
        elif axis == "knowledge_asymmetry":
            base = (base + _bounded(character.knowledge_access)) / 2
        elif axis == "reveal_pressure" and character.secret:
            base = min(1.0, base + 0.08)
        elif axis == "reader_attention" and character.motif_refs:
            base = min(1.0, base + 0.04 * min(3, len(character.motif_refs)))
        axis_scores[axis] = round(base, 4)
    weight_map = weights.to_dict()
    numerator = sum(axis_scores[axis] * weight_map[axis] for axis in PROFILE_AXES)
    denominator = sum(weight_map[axis] for axis in PROFILE_AXES)
    weighted_score = round(numerator / denominator, 4)
    explanation = _explain_profile(character, axis_scores, weighted_score)
    return CharacterProfileScore(
        character_id=character.character_id,
        board_piece=character.board_piece,
        axis_scores=axis_scores,
        weighted_score=weighted_score,
        explanation=explanation,
    )


def score_character_board(
    characters: tuple[CharacterSeed, ...],
    weights: NarrativeWeightVector | None = None,
) -> tuple[CharacterProfileScore, ...]:
    return tuple(score_character_profile(character, weights) for character in characters)


def _bounded(value: float) -> float:
    return max(0.0, min(1.0, float(value)))


def _explain_profile(character: CharacterSeed, axis_scores: dict[str, float], weighted_score: float) -> tuple[str, ...]:
    strongest = max(axis_scores, key=axis_scores.get)
    weakest = min(axis_scores, key=axis_scores.get)
    notes = [
        f"{character.character_id} uses board_piece={character.board_piece}",
        f"strongest_axis={strongest}:{axis_scores[strongest]}",
        f"weakest_axis={weakest}:{axis_scores[weakest]}",
        f"weighted_score={weighted_score}",
    ]
    if character.secret:
        notes.append("secret_increases_reveal_pressure")
    if character.motif_refs:
        notes.append("motif_refs_increase_reader_attention")
    return tuple(notes)
