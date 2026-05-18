from __future__ import annotations

from pathlib import Path

from v1700.graph_nexus.registry import GraphNexusRegistry
from v1700.graph_nexus.tools.contracts import GraphNexusContextRequest
from v1700.sidecars.gitnexus.cli_adapter import GitNexusCliAdapter


def build_graph_nexus_context(root: Path, request: GraphNexusContextRequest) -> dict:
    registry = GraphNexusRegistry.build(root)
    packet = registry.context_packet(request.target).to_dict()
    code_hits = registry.code_graph.find(request.target)
    gitnexus = {}
    if request.use_gitnexus and request.target != "ALL":
        gitnexus = GitNexusCliAdapter().context(root, request.target)
    return {
        "status": "pass",
        "target": request.target,
        "source": "gitnexus_cli_enriched_python_fallback" if gitnexus.get("available") else "python_fallback",
        "packet": packet,
        "code_hits": [node.to_dict() for node in code_hits],
        "gitnexus": gitnexus,
    }
