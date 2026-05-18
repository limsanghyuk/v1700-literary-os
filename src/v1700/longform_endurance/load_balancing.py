from __future__ import annotations

from statistics import mean

from v1700.longform_endurance.contracts import EnduranceEpisode


def evaluate_dramatic_load(episodes: tuple[EnduranceEpisode, ...]) -> dict:
    loads = [episode.total_load for episode in episodes]
    avg = mean(loads) if loads else 0.0
    overloaded = [episode.episode_id for episode in episodes if episode.total_load > avg * 1.28]
    underloaded = [episode.episode_id for episode in episodes if episode.total_load < avg * 0.72]
    mid = episodes[len(episodes) // 3 : len(episodes) * 2 // 3]
    mid_season_sag_risk = round(max(0.0, avg - mean(ep.total_load for ep in mid)) / avg, 3) if avg and mid else 0.0
    finale_overload_risk = round(max(0.0, episodes[-1].total_load - avg * 1.35) / avg, 3) if episodes and avg else 0.0
    issues = []
    if len(overloaded) > max(2, len(episodes) // 5):
        issues.append("too_many_overloaded_episodes")
    if len(underloaded) > max(1, len(episodes) // 6):
        issues.append("too_many_underloaded_episodes")
    if mid_season_sag_risk > 0.18:
        issues.append("mid_season_sag_risk_above_threshold")
    return {
        "status": "pass" if not issues else "blocked",
        "average_load": round(avg, 3),
        "load_curve": [episode.to_dict() for episode in episodes],
        "overloaded_episodes": overloaded,
        "underloaded_episodes": underloaded,
        "mid_season_sag_risk": mid_season_sag_risk,
        "finale_overload_risk": finale_overload_risk,
        "issues": issues,
    }
