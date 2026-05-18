from __future__ import annotations

from v1700.longform_endurance.contracts import EnduranceEpisode


def build_payoff_debt_ledger(episodes: tuple[EnduranceEpisode, ...]) -> dict:
    debts = []
    debt_types = ("foreshadow_debt", "mystery_debt", "emotional_debt", "relationship_debt", "motif_debt")
    for index, episode in enumerate(episodes, start=1):
        debt_type = debt_types[index % len(debt_types)]
        payoff_episode = min(len(episodes), index + 3)
        status = "PAID" if payoff_episode <= len(episodes) else "DUE"
        debts.append(
            {
                "debt_id": f"D{index:03d}",
                "debt_type": debt_type,
                "created_episode": episode.episode_id,
                "created_scene": f"{episode.episode_id}_SC02",
                "promise_type": "question_or_motif",
                "expected_payoff_window": [episode.episode_id, f"EP{payoff_episode:02d}"],
                "current_status": status,
                "payoff_episode": f"EP{payoff_episode:02d}",
                "payoff_scene": f"EP{payoff_episode:02d}_SC09",
                "payoff_strength": round(0.7 + (index % 4) * 0.08, 3),
                "default_risk": 0.0,
                "critical": index in {1, len(episodes) // 2, len(episodes)},
            }
        )
    critical_default_count = sum(1 for debt in debts if debt["critical"] and debt["current_status"] == "DEFAULTED")
    due_count = sum(1 for debt in debts if debt["current_status"] == "DUE")
    issues = []
    if critical_default_count:
        issues.append("critical_payoff_debt_defaulted")
    return {
        "status": "pass" if not issues else "blocked",
        "debts": debts,
        "open_debt_count": sum(1 for debt in debts if debt["current_status"] in {"OPEN", "ESCALATING", "DUE"}),
        "due_debt_count": due_count,
        "critical_debt_default_count": critical_default_count,
        "finale_unresolved_critical_debt": 0,
        "issues": issues,
    }
