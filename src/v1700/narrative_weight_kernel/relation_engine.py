from __future__ import annotations

from v1700.narrative_weight_kernel.contracts import (
    CharacterEventRelationScore,
    CharacterSeed,
    EventSeed,
    NarrativeWeightVector,
    RelationKind,
)

RELATION_PRIORS: dict[RelationKind, dict[str, float]] = {
    "ally": {"relation_tension": 0.48, "emotional_momentum": 0.62, "knowledge_asymmetry": 0.45},
    "rival": {"relation_tension": 0.78, "emotional_momentum": 0.70, "knowledge_asymmetry": 0.58},
    "mentor": {"relation_tension": 0.42, "emotional_momentum": 0.60, "knowledge_asymmetry": 0.76},
    "antagonist": {"relation_tension": 0.92, "emotional_momentum": 0.83, "knowledge_asymmetry": 0.72},
    "family": {"relation_tension": 0.68, "emotional_momentum": 0.84, "knowledge_asymmetry": 0.62},
    "lover": {"relation_tension": 0.73, "emotional_momentum": 0.86, "knowledge_asymmetry": 0.64},
    "debt": {"relation_tension": 0.80, "emotional_momentum": 0.72, "knowledge_asymmetry": 0.60},
    "secret_keeper": {"relation_tension": 0.74, "emotional_momentum": 0.67, "knowledge_asymmetry": 0.92},
    "witness": {"relation_tension": 0.55, "emotional_momentum": 0.52, "knowledge_asymmetry": 0.86},
}

RELATION_AXES = (
    "agency",
    "relation_tension",
    "event_causality",
    "knowledge_asymmetry",
    "reveal_pressure",
    "emotional_momentum",
    "scene_energy",
    "motif_residue",
    "reader_attention",
)


def score_character_event_relation(
    character: CharacterSeed,
    event: EventSeed,
    relation_kind: RelationKind,
    weights: NarrativeWeightVector | None = None,
) -> CharacterEventRelationScore:
    weights = weights or NarrativeWeightVector()
    relation_prior = RELATION_PRIORS[relation_kind]
    involved_bonus = 0.12 if character.character_id in event.involved_characters else -0.08
    secret_overlap = 0.12 if character.secret and event.reveal_refs else 0.0
    motif_overlap = 0.10 if set(character.motif_refs).intersection(event.reveal_refs) else 0.0
    axis_scores = {
        "agency": _bounded((character.agency_bias + event.pressure) / 2 + involved_bonus),
        "relation_tension": _bounded(relation_prior["relation_tension"] + involved_bonus / 2),
        "event_causality": _bounded(event.causal_importance + involved_bonus),
        "knowledge_asymmetry": _bounded((character.knowledge_access + relation_prior["knowledge_asymmetry"]) / 2 + secret_overlap),
        "reveal_pressure": _bounded(len(event.reveal_refs) * 0.18 + secret_overlap + motif_overlap + event.pressure * 0.35),
        "emotional_momentum": _bounded((relation_prior["emotional_momentum"] + event.pressure) / 2),
        "scene_energy": _bounded(event.pressure * 0.78 + event.causal_importance * 0.22),
        "motif_residue": _bounded(0.34 + motif_overlap + min(0.3, len(character.motif_refs) * 0.06)),
        "reader_attention": _bounded(0.30 + event.pressure * 0.33 + event.causal_importance * 0.22 + secret_overlap + motif_overlap),
    }
    weight_map = weights.to_dict()
    numerator = sum(axis_scores[axis] * weight_map[axis] for axis in RELATION_AXES)
    denominator = sum(weight_map[axis] for axis in RELATION_AXES)
    score = round(numerator / denominator, 4)
    learning_tags = _learning_tags(axis_scores, relation_kind, character, event)
    return CharacterEventRelationScore(
        character_id=character.character_id,
        event_id=event.event_id,
        relation_kind=relation_kind,
        axis_scores={axis: round(value, 4) for axis, value in axis_scores.items()},
        weighted_score=score,
        learning_tags=learning_tags,
    )


def score_relation_matrix(
    characters: tuple[CharacterSeed, ...],
    events: tuple[EventSeed, ...],
    relation_map: dict[tuple[str, str], RelationKind],
    weights: NarrativeWeightVector | None = None,
) -> tuple[CharacterEventRelationScore, ...]:
    by_id = {character.character_id: character for character in characters}
    by_event = {event.event_id: event for event in events}
    results: list[CharacterEventRelationScore] = []
    for (character_id, event_id), relation_kind in sorted(relation_map.items()):
        results.append(score_character_event_relation(by_id[character_id], by_event[event_id], relation_kind, weights))
    return tuple(results)


def _bounded(value: float) -> float:
    return max(0.0, min(1.0, float(value)))


def _learning_tags(
    axis_scores: dict[str, float],
    relation_kind: RelationKind,
    character: CharacterSeed,
    event: EventSeed,
) -> tuple[str, ...]:
    tags = [f"relation:{relation_kind}"]
    if axis_scores["reveal_pressure"] >= 0.7:
        tags.append("high_reveal_pressure")
    if axis_scores["event_causality"] >= 0.75:
        tags.append("causal_anchor")
    if axis_scores["agency"] < 0.45:
        tags.append("agency_floor_watch")
    if character.secret and event.reveal_refs:
        tags.append("secret_event_overlap")
    return tuple(tags)
