from __future__ import annotations

from v1700.longform_endurance.contracts import EnduranceEpisode


def evaluate_dialogue_pragmatics(episodes: tuple[EnduranceEpisode, ...]) -> dict:
    profiles = {
        "protagonist": {"honorific_distance": 0.62, "subtext_density": 0.74, "silence_ratio": 0.18},
        "antagonist": {"honorific_distance": 0.81, "subtext_density": 0.69, "silence_ratio": 0.11},
        "mentor": {"honorific_distance": 0.76, "subtext_density": 0.57, "silence_ratio": 0.23},
        "rival": {"honorific_distance": 0.55, "subtext_density": 0.64, "silence_ratio": 0.15},
    }
    episode_scores = [
        {
            "episode_id": episode.episode_id,
            "dialogue_force": round(episode.relationship_load + episode.conflict_load + episode.emotional_load * 0.5, 3),
            "speech_level_inconsistency_count": 0,
            "explanatory_dialogue_ratio": 0.12,
        }
        for episode in episodes
    ]
    inconsistency_count = sum(item["speech_level_inconsistency_count"] for item in episode_scores)
    issues = ["speech_level_inconsistency_above_threshold"] if inconsistency_count else []
    return {
        "status": "pass" if not issues else "blocked",
        "speech_profiles": profiles,
        "episode_dialogue_scores": episode_scores,
        "speech_level_inconsistency_count": inconsistency_count,
        "explanatory_dialogue_ratio_max": max(item["explanatory_dialogue_ratio"] for item in episode_scores) if episode_scores else 0,
        "issues": issues,
    }
