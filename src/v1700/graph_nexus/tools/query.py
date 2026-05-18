from __future__ import annotations

from pathlib import Path

from v1700.graph_nexus.registry import GraphNexusRegistry
from v1700.graph_nexus.tools.contracts import GraphNexusQueryRequest, GraphNexusQueryResult
from v1700.sidecars.gitnexus.cli_adapter import GitNexusCliAdapter


def run_graph_nexus_query(root: Path, request: GraphNexusQueryRequest) -> GraphNexusQueryResult:
    registry = GraphNexusRegistry.build(root)
    gitnexus = {}
    if request.use_gitnexus:
        gitnexus = GitNexusCliAdapter().query(
            root,
            request.query,
            context=request.context,
            goal=request.goal,
            limit=request.limit,
        )

    matches = _fallback_matches(registry, request.query, request.limit)
    source = "gitnexus_cli_enriched_python_fallback" if gitnexus.get("available") else "python_fallback"
    return GraphNexusQueryResult(
        status="pass",
        query=request.query,
        source=source,
        matches=tuple(matches),
        gitnexus=gitnexus,
    )


def _fallback_matches(registry: GraphNexusRegistry, query: str, limit: int) -> list[dict]:
    matches: list[dict] = []
    for node in registry.code_graph.find(query):
        matches.append(
            {
                "kind": "code",
                "path": node.path,
                "defines": list(node.defines),
                "tested_by": list(node.tested_by),
                "gated_by": list(node.gated_by),
                "stage_origin": node.stage_origin,
            }
        )
    for stage in registry.stage_lineage_graph.nodes:
        if query.lower() in stage.stage_id.lower() or query.lower() in stage.title.lower():
            matches.append(
                {
                    "kind": "stage",
                    "stage_id": stage.stage_id,
                    "title": stage.title,
                    "surviving_runtime_value": stage.surviving_runtime_value,
                }
            )
    return matches[: max(1, limit)]
