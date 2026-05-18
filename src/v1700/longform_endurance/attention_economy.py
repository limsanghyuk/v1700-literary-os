from __future__ import annotations

from v1700.longform_endurance.contracts import EnduranceEpisode


def evaluate_attention_economy(episodes: tuple[EnduranceEpisode, ...]) -> dict:
    budgets = []
    for episode in episodes:
        reward = round(episode.emotional_load + episode.reveal_load + episode.agency_load + episode.motif_load, 3)
        cost = round(episode.exposition_load + max(0.0, episode.total_load - 5.0) * 0.2, 3)
        value = round(reward - cost, 3)
        fatigue_risk = round(max(0.0, cost - reward * 0.55), 3)
        budgets.append(
            {
                "episode_id": episode.episode_id,
                "attention_budget": round(episode.attention_load + 1.2, 3),
                "attention_value": value,
                "cognitive_load": cost,
                "emotional_reward": episode.emotional_load,
                "curiosity_reward": episode.reveal_load,
                "hook_strength": round(episode.attention_load + (0.15 if episode.position % 4 == 0 else 0.05), 3),
                "fatigue_risk": fatigue_risk,
            }
        )
    max_fatigue = max((item["fatigue_risk"] for item in budgets), default=0.0)
    low_reward_high_cost = [item["episode_id"] for item in budgets if item["attention_value"] < 0.7]
    issues = []
    if max_fatigue > 0.45:
        issues.append("attention_fatigue_risk_above_threshold")
    if len(low_reward_high_cost) > 1:
        issues.append("low_reward_high_cost_episode_count_above_threshold")
    return {
        "status": "pass" if not issues else "blocked",
        "episode_attention_budgets": budgets,
        "attention_fatigue_risk": max_fatigue,
        "low_reward_high_cost_episodes": low_reward_high_cost,
        "issues": issues,
    }
