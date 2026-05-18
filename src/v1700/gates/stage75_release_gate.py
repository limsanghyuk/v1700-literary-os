from __future__ import annotations
from pathlib import Path
from v1700.lineage import build_branchpoint_registry, build_core_logic_survival_matrix, build_missing_required_logic_manifest, build_organic_relation_graph
from v1700.lineage.core_logic_survival import stage75_truthful_status


def run_stage75_release_gate(root: Path | None = None) -> dict:
    root = root or Path(__file__).resolve().parents[3]
    truth = stage75_truthful_status()
    registry = [item.to_dict() for item in build_branchpoint_registry()]
    matrix = [item.to_dict() for item in build_core_logic_survival_matrix()]
    missing = build_missing_required_logic_manifest()
    organic = [item.to_dict() for item in build_organic_relation_graph()]
    issues = list(truth.get("issues", []))
    return {
        "stage": "75",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "truthful_stage75_status": truth,
        "branchpoint_registry": registry,
        "core_logic_survival_matrix": matrix,
        "missing_required_logic_manifest": missing,
        "organic_relation_graph": organic,
        "provider_default_calls": 0,
        "node2_raw_reveal_access_count": 0,
    }
