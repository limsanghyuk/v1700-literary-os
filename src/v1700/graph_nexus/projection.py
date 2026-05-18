from __future__ import annotations

from v1700.graph_nexus.graph_nexus_packet import (
    Node1GraphPacket,
    Node2GraphSurfacePacket,
    Node3GraphCriticPacket,
)
from v1700.graph_nexus.narrative_graph import NarrativeGraph


def project_node1_packet(scene_id: str, narrative_graph: NarrativeGraph, impact: dict) -> Node1GraphPacket:
    return Node1GraphPacket(
        canon_context={"scene_id": scene_id},
        timeline_context={"scene_id": scene_id, "relation": "active_scene"},
        blast_radius=impact,
    )


def project_node2_surface_packet(scene_id: str, narrative_graph: NarrativeGraph) -> Node2GraphSurfacePacket:
    labels = tuple(f"locked_reveal_{index + 1}" for index, _ in enumerate(narrative_graph.forbidden_reveals_for_scene(scene_id)))
    packet = Node2GraphSurfacePacket(
        scene_id=scene_id,
        sensory_anchors=("setting", "gesture"),
        forbidden_reveal_labels=labels,
    )
    packet.assert_surface_safe()
    return packet


def project_node3_critic_packet(impact: dict) -> Node3GraphCriticPacket:
    risks = tuple(impact.get("risks", []))
    leakage = tuple(risk for risk in risks if "reveal" in risk.lower() or "leak" in risk.lower())
    return Node3GraphCriticPacket(contradiction_risks=risks, leakage_risks=leakage, impact=impact)
