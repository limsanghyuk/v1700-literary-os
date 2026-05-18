from __future__ import annotations

from v1700.nie.stability.contracts import TemporalCIMReport


class TemporalCIMAdapter:
    """Tracks cross-episode CIM stability without mutating Stage115 CIM."""

    def evaluate(self, role_tiers_by_episode: list[dict[str, str]], volatility_values: list[float]) -> TemporalCIMReport:
        issues: list[str] = []
        if not role_tiers_by_episode:
            return TemporalCIMReport("blocked", 0, 1.0, 0.0, [], ["no_temporal_cim_snapshots"])
        mean_volatility = sum(volatility_values) / len(volatility_values) if volatility_values else 0.0
        first = role_tiers_by_episode[0]
        latest = role_tiers_by_episode[-1]
        names = sorted(set(first) | set(latest))
        stable = sum(1 for name in names if first.get(name) == latest.get(name))
        role_continuity = stable / len(names) if names else 1.0
        unstable = [name for name in names if first.get(name) != latest.get(name)]
        if mean_volatility > 0.25:
            issues.append("temporal_cim_volatility_too_high")
        if role_continuity < 0.60:
            issues.append("role_continuity_too_low")
        return TemporalCIMReport(
            status="pass" if not issues else "blocked",
            episode_count=len(role_tiers_by_episode),
            mean_volatility=mean_volatility,
            role_continuity=role_continuity,
            unstable_roles=unstable,
            issues=issues,
        )
