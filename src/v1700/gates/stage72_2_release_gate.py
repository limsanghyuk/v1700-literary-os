from __future__ import annotations

from pathlib import Path

from v1700.gates.graph_nexus_release_gate import run_graph_nexus_release_gate
from v1700.graph_nexus.tools.context import build_graph_nexus_context
from v1700.graph_nexus.tools.contracts import (
    GraphNexusContextRequest,
    GraphNexusImpactRequest,
    GraphNexusQueryRequest,
)
from v1700.graph_nexus.tools.detect_changes import run_graph_nexus_detect_changes
from v1700.graph_nexus.tools.impact import run_graph_nexus_impact
from v1700.graph_nexus.tools.query import run_graph_nexus_query
from v1700.graph_nexus.tools.route_map import build_graph_nexus_route_map
from v1700.graph_nexus.tools.shape_check import run_graph_nexus_shape_check
from v1700.graph_nexus.tools.skill_generator import generate_graph_nexus_skills
from v1700.graph_nexus.tools.tool_map import build_graph_nexus_tool_map
from v1700.graph_nexus.tools.wiki_generator import generate_graph_nexus_wiki
from v1700.sidecars.gitnexus.index_status import (
    get_gitnexus_index_status,
    gitnexus_index_under_workspace,
)
from v1700.sidecars.gitnexus.probe import probe_gitnexus
from v1700.sidecars.gitnexus.stale_index_detector import detect_stale_gitnexus_index


def run_stage72_2_release_gate(root: Path) -> dict:
    probe = probe_gitnexus()
    workspace_root = _find_workspace_root(root)
    index_status = detect_stale_gitnexus_index(root, get_gitnexus_index_status())

    graph_release = run_graph_nexus_release_gate(root)
    query = run_graph_nexus_query(
        root,
        GraphNexusQueryRequest(
            query="GraphNexus",
            context="Stage72.2 release gate",
            goal="verify operational graph tools",
            limit=5,
        ),
    ).to_dict()
    context = build_graph_nexus_context(
        root,
        GraphNexusContextRequest(target="Node2ProseCompiler"),
    )
    impact = run_graph_nexus_impact(
        root,
        GraphNexusImpactRequest(target="Node2ProseCompiler", include_tests=True),
    )
    detect_changes = run_graph_nexus_detect_changes(root).to_dict()
    route_map = build_graph_nexus_route_map(root).to_dict()
    tool_map = build_graph_nexus_tool_map(root).to_dict()
    generated_skills = generate_graph_nexus_skills(root)
    generated_wiki = generate_graph_nexus_wiki(root)
    shape_check = run_graph_nexus_shape_check(root).to_dict()

    checks = {
        "graph_nexus_release_gate": graph_release,
        "query": query,
        "context": context,
        "impact": impact,
        "detect_changes": detect_changes,
        "route_map": route_map,
        "tool_map": tool_map,
        "generated_skills": generated_skills,
        "generated_wiki": generated_wiki,
        "shape_check": shape_check,
    }

    issues = [
        name
        for name, report in checks.items()
        if report.get("status") != "pass"
    ]
    if probe.installed and index_status.registered:
        if not gitnexus_index_under_workspace(index_status, workspace_root):
            issues.append("gitnexus_index_outside_gpt_workspace")

    return {
        "stage": "72.2",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "gitnexus": probe.to_dict(),
        "gitnexus_index_status": index_status.to_dict(),
        "gitnexus_index_under_gpt_workspace": (
            gitnexus_index_under_workspace(index_status, workspace_root)
            if index_status.registered
            else False
        ),
        "manual_reindex_recommended": bool(index_status.stale),
        "gitnexus_optional_only": True,
        "python_fallback_available": True,
        "provider_default_calls": 0,
        "node2_raw_reveal_access_count": 0,
        "checks": checks,
    }


def _find_workspace_root(root: Path) -> Path:
    matches = [parent for parent in (root, *root.parents) if parent.name.lower() == "gpt"]
    if matches:
        # Release ZIP probes can contain a nested `gpt/active/...` tree inside the
        # real GPT workspace. Use the outermost GPT folder so registered sidecar
        # indexes under the developer workspace are not mistaken for foreign paths.
        return matches[-1]
    return root
