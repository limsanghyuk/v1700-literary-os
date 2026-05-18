from __future__ import annotations

from pathlib import Path

from v1700.graph_nexus.tools.contracts import GraphNexusToolMap


def build_graph_nexus_tool_map(root: Path) -> GraphNexusToolMap:
    tools = (
        {"name": "query", "path": "tools/run_graph_nexus_query.py"},
        {"name": "context", "path": "tools/run_graph_nexus_context.py"},
        {"name": "impact", "path": "tools/run_graph_nexus_impact.py"},
        {"name": "detect_changes", "path": "tools/run_graph_nexus_detect_changes.py"},
        {"name": "route_map", "path": "tools/run_graph_nexus_route_map.py"},
        {"name": "tool_map", "path": "tools/run_graph_nexus_tool_map.py"},
        {"name": "shape_check", "path": "tools/run_graph_nexus_shape_check.py"},
        {"name": "generate_skills", "path": "tools/run_graph_nexus_generate_skills.py"},
        {"name": "generate_wiki", "path": "tools/run_graph_nexus_generate_wiki.py"},
        {"name": "stage72_2_release", "path": "tools/run_stage72_2_release_gate.py"},
        {"name": "build_stage72_3_foundation_lineage", "path": "tools/build_stage72_3_foundation_lineage.py"},
        {"name": "pre_stage40_survival_gate", "path": "tools/run_pre_stage40_survival_gate.py"},
        {"name": "stage72_3_release", "path": "tools/run_stage72_3_release_gate.py"},
    )
    gates = (
        {"name": "graph_nexus_release_gate", "path": "src/v1700/gates/graph_nexus_release_gate.py"},
        {"name": "stage72_2_release_gate", "path": "src/v1700/gates/stage72_2_release_gate.py"},
        {"name": "pre_stage40_survival_gate", "path": "src/v1700/gates/pre_stage40_survival_gate.py"},
        {"name": "stage72_3_release_gate", "path": "src/v1700/gates/stage72_3_release_gate.py"},
        {"name": "release_gate", "path": "src/v1700/gates/release_gate.py"},
    )
    tests = tuple(sorted(path.relative_to(root).as_posix() for path in (root / "tests").rglob("test_*.py")))
    missing = tuple(
        item["path"]
        for item in (*tools, *gates)
        if not (root / item["path"]).exists()
    )
    return GraphNexusToolMap(
        status="pass" if not missing and tests else "blocked",
        tools=tools,
        gates=gates,
        tests=tests,
        missing_paths=missing,
    )
