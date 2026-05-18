from __future__ import annotations

from pathlib import Path

from v1700.graph_nexus.projection import (
    project_node2_surface_packet,
    project_node3_critic_packet,
)
from v1700.graph_nexus.registry import GraphNexusRegistry


def run_node_projection_gate(root: Path, scene_id: str = "S72_1_SAMPLE") -> dict:
    registry = GraphNexusRegistry.build(root)
    node2_packet = project_node2_surface_packet(scene_id, registry.narrative_graph)
    node2_packet.assert_surface_safe()
    node3_packet = project_node3_critic_packet({"risks": ["forbidden_reveal_projection_required"]})
    return {
        "status": "pass",
        "node2_raw_graph_access": False,
        "node2_packet": node2_packet.to_dict(),
        "node3_packet": node3_packet.to_dict(),
    }
