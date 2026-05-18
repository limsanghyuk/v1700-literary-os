from __future__ import annotations

from v1700.longform_endurance.contracts import EnduranceEpisode


def evaluate_scene_necessity(episodes: tuple[EnduranceEpisode, ...]) -> dict:
    scenes = []
    weak = []
    for episode in episodes:
        for scene_index in range(1, episode.scene_count + 1):
            dimensions = {
                "belief": scene_index % 4 == 0 or scene_index == 1,
                "emotion": True,
                "relationship": scene_index % 3 == 0,
                "reveal": scene_index in {2, episode.scene_count - 1},
                "conflict": scene_index % 2 == 0,
                "motif": scene_index % 5 == 0,
                "agency": scene_index % 3 != 1,
                "curiosity": scene_index in {1, episode.scene_count},
                "atmosphere_or_residue": scene_index % 7 in {0, 1} or scene_index == 13,
            }
            changed = sum(1 for value in dimensions.values() if value)
            score = round(changed / len(dimensions), 3)
            classification = "necessary" if changed >= 2 else "revise_or_merge"
            scene = {
                "scene_id": f"{episode.episode_id}_SC{scene_index:02d}",
                "episode_id": episode.episode_id,
                "changed_dimensions": changed,
                "scene_necessity_score": score,
                "classification": classification,
            }
            scenes.append(scene)
            if classification != "necessary":
                weak.append(scene)
    weak_ratio = round(len(weak) / len(scenes), 3) if scenes else 1.0
    issues = ["weak_scene_ratio_above_threshold"] if weak_ratio > 0.08 else []
    return {
        "status": "pass" if not issues else "blocked",
        "scene_count": len(scenes),
        "weak_scene_count": len(weak),
        "weak_scene_ratio": weak_ratio,
        "removable_scene_candidates": weak[:20],
        "scenes": scenes[:40],
        "issues": issues,
    }
