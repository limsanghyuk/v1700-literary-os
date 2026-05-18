from __future__ import annotations

from dataclasses import dataclass, field

from v1700.arc_reveal_knowledge.arc_contracts import ArcAct, ArcPlotEdge, ArcPlotEdgeType, ArcPlotNode


@dataclass
class CausalPlotGraph:
    nodes: dict[str, ArcPlotNode] = field(default_factory=dict)
    _edges: list[ArcPlotEdge] = field(default_factory=list)

    def add_node(self, node: ArcPlotNode) -> None:
        self.nodes[node.episode_id] = node

    def get_node(self, episode_id: str) -> ArcPlotNode:
        return self.nodes[episode_id]

    def add_edge(
        self,
        source_episode_id: str,
        target_episode_id: str,
        edge_type: ArcPlotEdgeType,
        reason: str,
    ) -> None:
        if source_episode_id not in self.nodes:
            raise KeyError(f"unknown source episode: {source_episode_id}")
        if target_episode_id not in self.nodes:
            raise KeyError(f"unknown target episode: {target_episode_id}")
        edge = ArcPlotEdge(source_episode_id, target_episode_id, edge_type, reason)
        if edge not in self._edges:
            self._edges.append(edge)

    def edges(self, edge_type: ArcPlotEdgeType | None = None) -> tuple[ArcPlotEdge, ...]:
        if edge_type is None:
            return tuple(self._edges)
        return tuple(edge for edge in self._edges if edge.edge_type == edge_type)

    def ordered_nodes(self) -> tuple[ArcPlotNode, ...]:
        return tuple(sorted(self.nodes.values(), key=lambda node: node.episode_index))

    def infer_causal_edges(self) -> None:
        for node in self.ordered_nodes():
            for source in node.causal_inputs:
                if source in self.nodes:
                    self.add_edge(source, node.episode_id, ArcPlotEdgeType.CAUSAL, "declared_causal_input")

    def infer_foreshadow_edges(self) -> None:
        ordered = self.ordered_nodes()
        for node in ordered:
            if not node.forbidden_reveals:
                continue
            target = next(
                (
                    later
                    for later in ordered
                    if later.episode_index > node.episode_index and later.act in {ArcAct.JEON, ArcAct.GYEOL}
                ),
                None,
            )
            if target is not None:
                self.add_edge(
                    node.episode_id,
                    target.episode_id,
                    ArcPlotEdgeType.FORESHADOW,
                    "forbidden_reveal_reserved_for_later_turn",
                )

    def infer_callback_edges(self) -> None:
        for node in self.ordered_nodes():
            for source in node.required_callbacks:
                if source in self.nodes:
                    self.add_edge(source, node.episode_id, ArcPlotEdgeType.CALLBACK, "required_callback")

    def infer_emotional_escalation_edges(self, minimum_delta: float = 0.08) -> None:
        ordered = self.ordered_nodes()
        for previous, current in zip(ordered, ordered[1:]):
            if current.tension_level - previous.tension_level >= minimum_delta:
                self.add_edge(
                    previous.episode_id,
                    current.episode_id,
                    ArcPlotEdgeType.EMOTIONAL_ESCALATION,
                    "tension_rises_across_adjacent_episodes",
                )

    def infer_all_edges(self) -> None:
        self.infer_causal_edges()
        self.infer_foreshadow_edges()
        self.infer_callback_edges()
        self.infer_emotional_escalation_edges()

    def tension_curve(self) -> tuple[float, ...]:
        return tuple(node.tension_level for node in self.ordered_nodes())

    def validate_act_structure(self) -> dict:
        acts = {node.act for node in self.nodes.values()}
        missing = sorted(act.value for act in ArcAct if act not in acts)
        ordered = self.ordered_nodes()
        monotonic_episode_ids = [node.episode_id for node in ordered]
        return {
            "status": "pass" if not missing and len(ordered) == len(self.nodes) else "blocked",
            "missing_acts": missing,
            "episode_count": len(ordered),
            "ordered_episode_ids": monotonic_episode_ids,
        }

    def to_dict(self) -> dict:
        return {
            "nodes": [node.to_dict() for node in self.ordered_nodes()],
            "edges": [edge.to_dict() for edge in self._edges],
            "edge_counts": {
                edge_type.value: len(self.edges(edge_type))
                for edge_type in ArcPlotEdgeType
            },
            "act_structure": self.validate_act_structure(),
        }
