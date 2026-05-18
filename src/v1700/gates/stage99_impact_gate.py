from __future__ import annotations

from pathlib import Path

from v1700.stage99.impact_baseline import run_stage99_0_gitnexus_impact_baseline


def run_stage99_impact_gate(root: Path | None = None) -> dict:
    report = run_stage99_0_gitnexus_impact_baseline(root)
    return {
        "status": report.get("status"),
        "stage": "99.0",
        "orphan_critical_nodes": len(report.get("orphan_nodes", [])),
        "broken_gate_edges": len(report.get("broken_edges", [])),
        "branchpoint_survival_status": report.get("branchpoint_survival_status"),
        "issues": report.get("release_blockers", []),
    }
