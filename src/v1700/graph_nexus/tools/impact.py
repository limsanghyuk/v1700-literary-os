from __future__ import annotations

from pathlib import Path

from v1700.graph_nexus.impact import compute_graph_nexus_impact
from v1700.graph_nexus.registry import GraphNexusRegistry
from v1700.graph_nexus.tools.contracts import GraphNexusImpactRequest
from v1700.sidecars.gitnexus.cli_adapter import GitNexusCliAdapter


def run_graph_nexus_impact(root: Path, request: GraphNexusImpactRequest) -> dict:
    registry = GraphNexusRegistry.build(root)
    fallback = compute_graph_nexus_impact(
        request.target,
        registry.code_graph,
        registry.narrative_graph,
        registry.stage_lineage_graph,
    )
    gitnexus = {}
    if request.use_gitnexus:
        gitnexus = GitNexusCliAdapter().impact(
            root,
            request.target,
            include_tests=request.include_tests,
        )
    return {
        "status": "pass",
        "target": request.target,
        "source": "gitnexus_cli_enriched_python_fallback" if gitnexus.get("available") else "python_fallback",
        "fallback_impact": fallback,
        "gitnexus": gitnexus,
        "requires_human_attention": fallback["risk_level"] in {"high", "critical"},
    }
