from __future__ import annotations

from pathlib import Path

from v1700.gates.graph_nexus_impact_gate import run_graph_nexus_impact_gate
from v1700.gates.legacy_logic_survival_gate import run_legacy_logic_survival_gate
from v1700.gates.lineage_preflight_gate import run_lineage_preflight_gate
from v1700.gates.node_projection_gate import run_node_projection_gate
from v1700.graph_nexus.registry import GraphNexusRegistry
from v1700.sidecars.gitnexus.probe import probe_gitnexus


def run_graph_nexus_release_gate(root: Path) -> dict:
    registry = GraphNexusRegistry.build(root)
    probe = probe_gitnexus()
    checks = {
        "lineage_preflight": run_lineage_preflight_gate(root),
        "impact": run_graph_nexus_impact_gate(root, "Node2ProseCompiler"),
        "legacy_logic_survival": run_legacy_logic_survival_gate(root),
        "node_projection": run_node_projection_gate(root),
    }
    issues = [
        name
        for name, report in checks.items()
        if report.get("status") != "pass"
    ]
    packet = registry.context_packet("Node2ProseCompiler").to_dict()
    return {
        "stage": "72.1",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "gitnexus": probe.to_dict(),
        "gitnexus_optional_only": True,
        "python_fallback_available": True,
        "provider_default_calls": 0,
        "code_graph_available": packet["code_summary"]["available"],
        "narrative_graph_available": packet["narrative_summary"]["available"],
        "stage_lineage_graph_available": packet["lineage_summary"]["available"],
        "node2_raw_reveal_access_count": 0,
        "checks": checks,
        "context_packet": packet,
    }
