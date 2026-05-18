from __future__ import annotations

from pathlib import Path

from v1700.graph_nexus.impact import compute_graph_nexus_impact
from v1700.graph_nexus.registry import GraphNexusRegistry


def run_graph_nexus_impact_gate(root: Path, target: str = "ALL") -> dict:
    registry = GraphNexusRegistry.build(root)
    impact = compute_graph_nexus_impact(
        target,
        registry.code_graph,
        registry.narrative_graph,
        registry.stage_lineage_graph,
    )
    return {
        "status": "pass",
        "impact": impact,
        "requires_human_attention": impact["risk_level"] in {"high", "critical"},
    }
