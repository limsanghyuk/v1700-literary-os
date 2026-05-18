from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class CuratedNode:
    node_id: str
    score: float
    last_episode_idx: int
    protected: bool = False
    node_type: str = "memory"


@dataclass
class CurationReport:
    status: str
    dry_run: bool
    removed_count: int
    stale_removed: int
    weak_removed: int
    protected_preserved: int
    reason: str
    episode_idx: int


class NarrativeMemoryCurator:
    MIN_SCORE_THRESHOLD = 0.15
    MAX_AGE_EPISODES = 20
    PROTECTED_TYPES = {"branchpoint", "payoff_debt", "credential_boundary"}

    def curate(self, nodes: Iterable[CuratedNode], current_episode: int, dry_run: bool = True) -> CurationReport:
        stale = []
        weak = []
        protected = []
        for node in nodes:
            is_protected = node.protected or node.node_type in self.PROTECTED_TYPES
            if is_protected:
                protected.append(node)
                continue
            if current_episode - node.last_episode_idx > self.MAX_AGE_EPISODES:
                stale.append(node)
            if node.score < self.MIN_SCORE_THRESHOLD:
                weak.append(node)
        removed_ids = {n.node_id for n in stale + weak}
        return CurationReport(
            status="pass",
            dry_run=dry_run,
            removed_count=len(removed_ids),
            stale_removed=len({n.node_id for n in stale}),
            weak_removed=len({n.node_id for n in weak}),
            protected_preserved=len(protected),
            reason="dry_run_auto_curation" if dry_run else "auto_curation",
            episode_idx=current_episode,
        )
