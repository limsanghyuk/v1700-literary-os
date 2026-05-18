from __future__ import annotations

from pathlib import Path

from v1700.graph_nexus.stage_lineage_graph import StageLineageGraph


def run_lineage_preflight_gate(root: Path, goal: str = "Stage72.1 GraphNexus restoration") -> dict:
    lineage = StageLineageGraph.from_manifest(root)
    required = ["STAGE61-66", "STAGE71", "STAGE72", "STAGE72.1"]
    missing = [stage for stage in required if not lineage.has_stage(stage)]
    return {
        "status": "pass" if not missing else "blocked",
        "goal": goal,
        "missing_stages": missing,
        "stage_count": len(lineage.nodes),
        "graph_intelligence_lineage_present": lineage.has_stage("STAGE61-66"),
    }
