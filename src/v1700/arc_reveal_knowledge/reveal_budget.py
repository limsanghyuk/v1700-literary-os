from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from v1700.arc_reveal_knowledge.causal_plot_graph import CausalPlotGraph


class RevealPolicy(str, Enum):
    ALLOW = "allow"
    DELAY = "delay"
    FORESHADOW_ONLY = "foreshadow_only"
    BLOCK = "block"


class RevealBudgetViolationError(AssertionError):
    pass


class RevealBlockedError(RevealBudgetViolationError):
    pass


class RevealForeshadowOnlyError(RevealBudgetViolationError):
    pass


@dataclass(frozen=True)
class EpisodeRevealPolicy:
    episode_id: str
    fact_id: str
    policy: RevealPolicy
    delay_until_episode_id: str | None = None
    reason: str = ""

    def to_dict(self) -> dict:
        return {
            "episode_id": self.episode_id,
            "fact_id": self.fact_id,
            "policy": self.policy.value,
            "delay_until_episode_id": self.delay_until_episode_id,
            "reason": self.reason,
        }


class EpisodeRevealBudget:
    def __init__(self):
        self._policies: dict[tuple[str, str], EpisodeRevealPolicy] = {}
        self._globally_blocked: set[str] = set()

    def set_policy(
        self,
        episode_id: str,
        fact_id: str,
        policy: RevealPolicy,
        *,
        delay_until_episode_id: str | None = None,
        reason: str = "",
    ) -> None:
        self._policies[(episode_id, fact_id)] = EpisodeRevealPolicy(
            episode_id=episode_id,
            fact_id=fact_id,
            policy=policy,
            delay_until_episode_id=delay_until_episode_id,
            reason=reason,
        )

    def block_globally(self, fact_id: str) -> None:
        self._globally_blocked.add(fact_id)

    def get_policy(self, episode_id: str, fact_id: str) -> EpisodeRevealPolicy:
        return self._policies.get(
            (episode_id, fact_id),
            EpisodeRevealPolicy(episode_id, fact_id, RevealPolicy.ALLOW),
        )

    def assert_allowed(self, episode_id: str, fact_id: str, *, direct_reveal: bool = True) -> None:
        if fact_id in self._globally_blocked:
            raise RevealBlockedError(f"{fact_id} is globally blocked")
        policy = self.get_policy(episode_id, fact_id)
        if policy.policy == RevealPolicy.BLOCK:
            raise RevealBlockedError(f"{fact_id} is blocked in {episode_id}")
        if policy.policy == RevealPolicy.FORESHADOW_ONLY and direct_reveal:
            raise RevealForeshadowOnlyError(f"{fact_id} can only be foreshadowed in {episode_id}")
        if policy.policy == RevealPolicy.DELAY and direct_reveal:
            raise RevealBlockedError(f"{fact_id} is delayed until {policy.delay_until_episode_id}")

    def is_allowed(self, episode_id: str, fact_id: str, *, direct_reveal: bool = True) -> bool:
        try:
            self.assert_allowed(episode_id, fact_id, direct_reveal=direct_reveal)
        except RevealBudgetViolationError:
            return False
        return True

    def episode_summary(self, episode_id: str) -> dict:
        policies = [
            policy.to_dict()
            for policy in self._policies.values()
            if policy.episode_id == episode_id
        ]
        return {
            "episode_id": episode_id,
            "policy_count": len(policies),
            "policies": sorted(policies, key=lambda item: item["fact_id"]),
        }

    def to_dict(self) -> dict:
        return {
            "policies": [
                policy.to_dict()
                for policy in sorted(self._policies.values(), key=lambda item: (item.episode_id, item.fact_id))
            ],
            "globally_blocked": sorted(self._globally_blocked),
        }

    @classmethod
    def from_arc_graph(cls, graph: CausalPlotGraph) -> "EpisodeRevealBudget":
        budget = cls()
        for node in graph.ordered_nodes():
            for fact_id in node.forbidden_reveals:
                budget.set_policy(
                    node.episode_id,
                    fact_id,
                    RevealPolicy.FORESHADOW_ONLY,
                    reason="arc_node_forbidden_reveal",
                )
        return budget
