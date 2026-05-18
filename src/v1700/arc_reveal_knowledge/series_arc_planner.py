from __future__ import annotations

from v1700.arc_reveal_knowledge.arc_contracts import ArcAct, ArcPlotNode
from v1700.arc_reveal_knowledge.causal_plot_graph import CausalPlotGraph


class SeriesArcPlanner:
    """Builds a deterministic season arc that later tools can verify."""

    def __init__(self, total_episodes: int = 16):
        if total_episodes < 4:
            raise ValueError("total_episodes must be at least 4")
        self.total_episodes = total_episodes

    def plan(self) -> CausalPlotGraph:
        graph = CausalPlotGraph()
        for index in range(1, self.total_episodes + 1):
            episode_id = f"EP{index:02d}"
            act = self._act_for_index(index)
            causal_inputs = (f"EP{index - 1:02d}",) if index > 1 else ()
            forbidden_reveals = self._forbidden_reveals(index, act)
            required_callbacks = (f"EP{max(1, index - 4):02d}",) if act in {ArcAct.JEON, ArcAct.GYEOL} else ()
            graph.add_node(
                ArcPlotNode(
                    episode_id=episode_id,
                    episode_index=index,
                    act=act,
                    tension_level=self._tension_for_index(index),
                    emotional_target=self._emotional_target(act),
                    causal_inputs=causal_inputs,
                    forbidden_reveals=forbidden_reveals,
                    required_callbacks=required_callbacks,
                )
            )
        graph.infer_all_edges()
        return graph

    def _act_for_index(self, index: int) -> ArcAct:
        ratio = index / self.total_episodes
        if ratio <= 0.25:
            return ArcAct.GI
        if ratio <= 0.625:
            return ArcAct.SEUNG
        if ratio <= 0.875:
            return ArcAct.JEON
        return ArcAct.GYEOL

    def _tension_for_index(self, index: int) -> float:
        ratio = index / self.total_episodes
        if ratio <= 0.55:
            value = 0.12 + ratio * 1.24
        elif ratio <= 0.78:
            value = 0.84 - (ratio - 0.55) * 0.55
        else:
            value = 0.72 - (ratio - 0.78) * 1.4
        return round(max(0.18, min(0.9, value)), 2)

    def _forbidden_reveals(self, index: int, act: ArcAct) -> tuple[str, ...]:
        if act == ArcAct.GI:
            return (f"truth_seed_{index}",)
        if act == ArcAct.SEUNG and index % 2 == 0:
            return (f"relationship_secret_{index}",)
        return ()

    def _emotional_target(self, act: ArcAct) -> str:
        return {
            ArcAct.GI: "curiosity_and_attachment",
            ArcAct.SEUNG: "pressure_and_misalignment",
            ArcAct.JEON: "recognition_and_reversal",
            ArcAct.GYEOL: "resolution_and_afterimage",
        }[act]
