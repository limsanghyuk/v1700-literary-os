"""Stage86 Arc-Reveal-Knowledge absorption layer.

This package absorbs the useful V380 concepts into the V1700 Branchpoint OS
without making Claude/GitNexus/runtime providers mandatory.
"""

from v1700.arc_reveal_knowledge.arc_contracts import ArcAct, ArcPlotEdge, ArcPlotEdgeType, ArcPlotNode
from v1700.arc_reveal_knowledge.causal_plot_graph import CausalPlotGraph
from v1700.arc_reveal_knowledge.character_knowledge_bridge import CharacterKnowledgeProseBridge
from v1700.arc_reveal_knowledge.knowledge_contracts import KnowledgeStatus
from v1700.arc_reveal_knowledge.reveal_budget import EpisodeRevealBudget, RevealPolicy
from v1700.arc_reveal_knowledge.series_arc_planner import SeriesArcPlanner

__all__ = [
    "ArcAct",
    "ArcPlotEdge",
    "ArcPlotEdgeType",
    "ArcPlotNode",
    "CausalPlotGraph",
    "CharacterKnowledgeProseBridge",
    "EpisodeRevealBudget",
    "KnowledgeStatus",
    "RevealPolicy",
    "SeriesArcPlanner",
]
