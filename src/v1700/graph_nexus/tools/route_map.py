from __future__ import annotations

from pathlib import Path

from v1700.graph_nexus.tools.contracts import GraphNexusRouteMap


def build_graph_nexus_route_map(root: Path) -> GraphNexusRouteMap:
    routes = (
        {
            "name": "runtime_generation_route",
            "steps": [
                "src/v1700/cli.py",
                "src/v1700/nodes/node1_architect/__init__.py",
                "src/v1700/nodes/node2_prose_renderer/compiler.py",
                "src/v1700/nodes/node3_critic_gate/constraint_validator.py",
            ],
        },
        {
            "name": "graph_context_route",
            "steps": [
                "src/v1700/graph_nexus/registry.py",
                "src/v1700/graph_nexus/code_graph.py",
                "src/v1700/graph_nexus/narrative_graph.py",
                "src/v1700/graph_nexus/stage_lineage_graph.py",
            ],
        },
        {
            "name": "stage72_2_operational_route",
            "steps": [
                "src/v1700/sidecars/gitnexus/cli_adapter.py",
                "src/v1700/graph_nexus/tools/query.py",
                "src/v1700/graph_nexus/tools/context.py",
                "src/v1700/graph_nexus/tools/impact.py",
                "src/v1700/graph_nexus/tools/detect_changes.py",
                "src/v1700/gates/stage72_2_release_gate.py",
            ],
        },
        {
            "name": "stage72_3_foundation_lineage_route",
            "steps": [
                "src/v1700/graph_nexus/tools/foundation_lineage.py",
                "src/v1700/graph_nexus/tools/survival_matrix.py",
                "src/v1700/gates/pre_stage40_survival_gate.py",
                "src/v1700/gates/stage72_3_release_gate.py",
            ],
        },
    )
    missing = tuple(
        step
        for route in routes
        for step in route["steps"]
        if not (root / step).exists()
    )
    return GraphNexusRouteMap(
        status="pass" if not missing else "blocked",
        routes=routes,
        missing_paths=missing,
    )
