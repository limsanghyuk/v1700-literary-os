from __future__ import annotations

from pathlib import Path

from v1700.graph_nexus.registry import GraphNexusRegistry
from v1700.graph_nexus.tools.contracts import GraphNexusDetectChangesReport
from v1700.sidecars.gitnexus.cli_adapter import GitNexusCliAdapter
from v1700.sidecars.gitnexus.index_status import get_gitnexus_index_status
from v1700.sidecars.gitnexus.stale_index_detector import detect_stale_gitnexus_index


def run_graph_nexus_detect_changes(root: Path, *, use_gitnexus: bool = True) -> GraphNexusDetectChangesReport:
    registry = GraphNexusRegistry.build(root)
    gitnexus = {}
    if use_gitnexus and _is_git_worktree(root):
        gitnexus = GitNexusCliAdapter().detect_changes(root, scope="all")
    elif use_gitnexus:
        gitnexus = {
            "provider": "gitnexus_cli",
            "capability": "detect_changes",
            "available": False,
            "reason": "active_repo_is_not_git_worktree; python fallback used",
        }
    status = detect_stale_gitnexus_index(root, get_gitnexus_index_status())
    impacted_tests = sorted(
        {
            test
            for node in registry.code_graph.nodes
            if "graph_nexus" in node.path or "sidecars/gitnexus" in node.path
            for test in node.tested_by
        }
    )
    changed_paths = tuple(
        node.path
        for node in registry.code_graph.nodes
        if "graph_nexus" in node.path or "sidecars/gitnexus" in node.path
    )
    return GraphNexusDetectChangesReport(
        status="pass",
        source="gitnexus_cli_enriched_python_fallback" if gitnexus.get("available") else "python_fallback",
        mode="stage72_2_structural_scan",
        changed_paths=changed_paths,
        impacted_tests=tuple(impacted_tests),
        stale_index=status.stale,
        gitnexus={
            "command": gitnexus,
            "index_status": status.to_dict(),
        },
    )


def _is_git_worktree(root: Path) -> bool:
    return (root / ".git").exists()
