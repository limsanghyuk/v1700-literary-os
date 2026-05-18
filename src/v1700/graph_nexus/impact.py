from __future__ import annotations

from v1700.graph_nexus.code_graph import CodeGraph
from v1700.graph_nexus.narrative_graph import NarrativeGraph
from v1700.graph_nexus.stage_lineage_graph import StageLineageGraph


def compute_graph_nexus_impact(
    target: str,
    code_graph: CodeGraph,
    narrative_graph: NarrativeGraph,
    lineage_graph: StageLineageGraph,
) -> dict:
    code_hits = code_graph.find(target)
    risks: list[str] = []
    if "node2" in target.lower():
        risks.append("node2_surface_contract_must_hold")
    if not lineage_graph.has_stage("STAGE61-66"):
        risks.append("stage61_66_lineage_missing")
    forbidden_count = sum(len(node.forbidden_reveals) for node in narrative_graph.nodes)
    if forbidden_count:
        risks.append("forbidden_reveal_projection_required")
    return {
        "target": target,
        "risk_level": "medium" if risks else "low",
        "risk_score": min(1.0, 0.2 + 0.2 * len(risks)),
        "code_hits": [node.path for node in code_hits],
        "narrative_node_count": len(narrative_graph.nodes),
        "lineage_node_count": len(lineage_graph.nodes),
        "risks": risks,
    }
