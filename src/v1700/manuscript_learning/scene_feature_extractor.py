from __future__ import annotations

from v1700.manuscript_learning.contracts import SceneFeature


def extract_scene_features(corpus: tuple[dict, ...]) -> tuple[SceneFeature, ...]:
    features: list[SceneFeature] = []
    for index, scene in enumerate(corpus, start=1):
        reveal_count = int(scene.get("reveal_events", 0))
        hook = 1 if scene.get("curiosity_hook") else 0
        features.append(
            SceneFeature(
                scene_id=scene["scene_id"],
                episode_id=scene["episode_id"],
                word_count=220 + (index % 7) * 17,
                character_count=len(scene.get("characters", ())),
                active_characters=tuple(scene.get("characters", ())),
                goal_conflict_count=1 + (index % 3 == 0),
                belief_state_change_count=1 if index % 4 == 0 else 0,
                reveal_event_count=reveal_count,
                foreshadow_event_count=int(scene.get("foreshadow_events", 0)),
                emotional_delta=round(0.2 + (index % 5) * 0.11, 3),
                scene_energy_input=round(0.45 + (index % 4) * 0.1, 3),
                scene_energy_output=round(0.55 + (index % 4) * 0.1 + reveal_count * 0.05, 3),
                motif_count=1 if index % 5 == 0 else 0,
                callback_count=1 if index % 9 == 0 else 0,
                curiosity_hook_count=hook,
                surface_safety_flags=(),
                branchpoint_touchpoints=("surface_only_node2", "branchpoint_survival"),
            )
        )
    return tuple(features)
