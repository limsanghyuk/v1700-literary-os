from __future__ import annotations

from v1700.longform_endurance.contracts import EnduranceEpisode


def evaluate_agency_conservation(episodes: tuple[EnduranceEpisode, ...]) -> dict:
    characters = ("protagonist", "antagonist", "mentor", "rival")
    curves = {}
    for character in characters:
        modifier = {"protagonist": 0.25, "antagonist": 0.15, "mentor": -0.05, "rival": 0.05}[character]
        curves[character] = [
            {
                "episode_id": episode.episode_id,
                "agency_delta": round(episode.agency_load + modifier + (0.08 if episode.act in {"jeon", "gyeol"} else 0.0), 3),
                "agency_events": ["choice", "refusal", "consequence"],
            }
            for episode in episodes
        ]
    protagonist_floor = min(item["agency_delta"] for item in curves["protagonist"]) if episodes else 0.0
    passive_episode_count = sum(1 for item in curves["protagonist"] if item["agency_delta"] < 0.55)
    issues = []
    if protagonist_floor < 0.55:
        issues.append("protagonist_agency_floor_failed")
    if passive_episode_count > 1:
        issues.append("passive_episode_count_above_threshold")
    return {
        "status": "pass" if not issues else "blocked",
        "agency_floor_status": "pass" if not issues else "blocked",
        "protagonist_agency_floor": round(protagonist_floor, 3),
        "passive_episode_count": passive_episode_count,
        "character_agency_curves": curves,
        "issues": issues,
    }
