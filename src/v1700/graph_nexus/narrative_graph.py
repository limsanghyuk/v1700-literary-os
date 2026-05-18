from __future__ import annotations

from dataclasses import dataclass

from v1700.ir.scene_intent import SceneIntentIR


@dataclass(frozen=True)
class NarrativeNode:
    node_id: str
    node_type: str
    label: str
    forbidden_reveals: tuple[str, ...] = ()
    motifs: tuple[str, ...] = ()

    def to_dict(self) -> dict:
        return {
            "node_id": self.node_id,
            "node_type": self.node_type,
            "label": self.label,
            "forbidden_reveals": list(self.forbidden_reveals),
            "motifs": list(self.motifs),
        }


@dataclass(frozen=True)
class NarrativeEdge:
    source: str
    target: str
    relation: str
    weight: float = 1.0

    def to_dict(self) -> dict:
        return {
            "source": self.source,
            "target": self.target,
            "relation": self.relation,
            "weight": self.weight,
        }


@dataclass(frozen=True)
class NarrativeGraph:
    nodes: tuple[NarrativeNode, ...] = ()
    edges: tuple[NarrativeEdge, ...] = ()

    @classmethod
    def from_scene_intents(cls, scenes: list[SceneIntentIR]) -> "NarrativeGraph":
        nodes: list[NarrativeNode] = []
        edges: list[NarrativeEdge] = []
        previous_id = ""
        for scene in scenes:
            nodes.append(
                NarrativeNode(
                    node_id=scene.scene_id,
                    node_type="SceneIntent",
                    label=scene.scene_goal,
                    forbidden_reveals=scene.forbidden_reveals,
                    motifs=tuple(item for item in (scene.setting_seed, scene.dialogue_seed) if item),
                )
            )
            for reveal in scene.forbidden_reveals:
                reveal_id = f"{scene.scene_id}:forbidden:{reveal}"
                nodes.append(NarrativeNode(reveal_id, "ForbiddenReveal", reveal))
                edges.append(NarrativeEdge(scene.scene_id, reveal_id, "FORBIDS", 1.0))
            if previous_id:
                edges.append(NarrativeEdge(previous_id, scene.scene_id, "NEXT_SCENE", 0.5))
            previous_id = scene.scene_id
        return cls(tuple(nodes), tuple(edges))

    def forbidden_reveals_for_scene(self, scene_id: str) -> tuple[str, ...]:
        for node in self.nodes:
            if node.node_id == scene_id:
                return node.forbidden_reveals
        return ()

    def to_dict(self) -> dict:
        return {
            "node_count": len(self.nodes),
            "edge_count": len(self.edges),
            "nodes": [node.to_dict() for node in self.nodes],
            "edges": [edge.to_dict() for edge in self.edges],
        }
