from __future__ import annotations

from dataclasses import dataclass

from v1700.graph_nexus.narrative_graph import NarrativeGraph
from .drse import DRSEInputNode


@dataclass(frozen=True)
class SceneFocusContext:
    scene_id: str
    nodes: tuple[DRSEInputNode, ...]
    relation_count: int

    def to_dict(self) -> dict:
        return {
            "scene_id": self.scene_id,
            "relation_count": self.relation_count,
            "nodes": [node.__dict__ for node in self.nodes],
        }


class SceneGraphQueryEngine:
    def focus(self, graph: NarrativeGraph, scene_id: str) -> SceneFocusContext:
        selected: list[DRSEInputNode] = []
        connected = {edge.target for edge in graph.edges if edge.source == scene_id} | {edge.source for edge in graph.edges if edge.target == scene_id}
        for node in graph.nodes:
            if node.node_id == scene_id or node.node_id in connected:
                selected.append(
                    DRSEInputNode(
                        node_id=node.node_id,
                        node_type=node.node_type,
                        content=node.label,
                        relations=tuple(edge.relation for edge in graph.edges if edge.source == node.node_id or edge.target == node.node_id),
                        tags=tuple(node.motifs),
                    )
                )
        return SceneFocusContext(scene_id=scene_id, nodes=tuple(selected), relation_count=len(selected))
