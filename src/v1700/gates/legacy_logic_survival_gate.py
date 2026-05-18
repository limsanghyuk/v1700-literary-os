from __future__ import annotations

from pathlib import Path

from v1700.graph_nexus.stage_lineage_graph import StageLineageGraph


def run_legacy_logic_survival_gate(root: Path) -> dict:
    lineage = StageLineageGraph.from_manifest(root)
    concepts = set(lineage.concepts_for("STAGE61-66"))
    required = {"graph sidecar", "authority boundaries", "feature flag integration"}
    missing = sorted(required - concepts)
    return {
        "status": "pass" if not missing else "blocked",
        "stage": "STAGE61-66",
        "required_concepts": sorted(required),
        "missing_concepts": missing,
        "current_status": "restored_as_optional_graphnexus_layer" if not missing else "incomplete",
    }
