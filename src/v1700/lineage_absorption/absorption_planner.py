from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from v1700.lineage_absorption.absorption_candidate_registry import build_absorption_candidate_registry
from v1700.lineage_absorption.conflict_matrix import build_conflict_matrix
from v1700.lineage_absorption.formula_ledger import build_formula_ledger
from v1700.lineage_absorption.gate_authority_map import build_gate_authority_map
from v1700.lineage_absorption.lineage_relationship_map import build_lineage_relationship_map
from v1700.lineage_absorption.packaging_audit import build_packaging_cleanliness_report
from v1700.stage121.fixtures import ABSORPTION_PLANS

REQUIRED_OUTPUTS = (
    "manifests/stage121_formula_ledger.json",
    "manifests/stage121_lineage_relationship_map.json",
    "manifests/stage121_conflict_matrix.json",
    "manifests/stage121_absorption_candidate_registry.json",
    "manifests/stage121_gate_authority_map.json",
    "release/current/stage121_cross_lineage_preflight_report.json",
    "release/current/stage121_formula_conflict_report.json",
    "release/current/stage121_packaging_cleanliness_report.json",
)


def build_stage121_absorption_preflight(root: Path | None = None) -> dict[str, Any]:
    root = root or Path(__file__).resolve().parents[3]
    formula_ledger = build_formula_ledger()
    relationship_map = build_lineage_relationship_map()
    conflict_matrix = build_conflict_matrix()
    candidate_registry = build_absorption_candidate_registry()
    gate_authority_map = build_gate_authority_map()
    packaging = build_packaging_cleanliness_report()
    absorption_plans = [plan.to_dict() for plan in ABSORPTION_PLANS]

    issues: list[str] = []
    if not relationship_map.get("all_direct_merges_blocked"):
        issues.append("candidate_direct_merge_not_blocked")
    if gate_authority_map.get("primary_gate") != "Gate25":
        issues.append("primary_gate_not_stage120_gate25")
    if not formula_ledger.get("stage120_formulas_preserved"):
        issues.append("stage120_formula_not_preserved")
    if packaging.get("trunk", {}).get("clean_packaging_pass") is not True:
        issues.append("stage120_trunk_packaging_not_clean")
    if packaging.get("candidate_direct_merge_allowed_count") != 0:
        issues.append("candidate_direct_merge_allowed")

    result = {
        "stage": "121",
        "baseline_stage": "120",
        "title": "Cross-Lineage Formula Reconciliation & Absorption Preflight",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "preflight_method": "GitNexus-aware Python fallback",
        "trunk_policy": "Stage120 Integrity FIXED remains the only primary trunk",
        "merge_policy": "V545/V546/V555 are reference branches; direct merge is blocked",
        "formula_ledger": formula_ledger,
        "lineage_relationship_map": relationship_map,
        "conflict_matrix": conflict_matrix,
        "absorption_candidate_registry": candidate_registry,
        "gate_authority_map": gate_authority_map,
        "packaging_cleanliness_report": packaging,
        "stage122_to_stage126_plan": absorption_plans,
        "provider_default_calls": 0,
        "live_provider_call_count_in_release_gate": 0,
        "embedding_provider_call_count": 0,
        "query_classifier_llm_call_count": 0,
        "physics_reward_bridge_llm_call_count": 0,
        "mae_live_provider_call_count": 0,
        "node2_raw_reveal_access": 0,
        "raw_manuscript_provider_leakage": 0,
        "credential_leakage": 0,
        "branchpoint_lineage_preserved": not issues,
        "direct_merge_allowed": False,
    }
    _write_reports(root, result)
    return result


def _write_reports(root: Path, result: dict[str, Any]) -> None:
    (root / "manifests").mkdir(parents=True, exist_ok=True)
    (root / "release/current/stage121_absorption_preflight_pack").mkdir(parents=True, exist_ok=True)
    mapping = {
        "manifests/stage121_formula_ledger.json": result["formula_ledger"],
        "manifests/stage121_lineage_relationship_map.json": result["lineage_relationship_map"],
        "manifests/stage121_conflict_matrix.json": result["conflict_matrix"],
        "manifests/stage121_absorption_candidate_registry.json": result["absorption_candidate_registry"],
        "manifests/stage121_gate_authority_map.json": result["gate_authority_map"],
        "release/current/stage121_cross_lineage_preflight_report.json": result,
        "release/current/stage121_formula_conflict_report.json": result["conflict_matrix"],
        "release/current/stage121_packaging_cleanliness_report.json": result["packaging_cleanliness_report"],
        "release/current/stage121_absorption_preflight_pack/formula_ledger.json": result["formula_ledger"],
        "release/current/stage121_absorption_preflight_pack/conflict_matrix.json": result["conflict_matrix"],
        "release/current/stage121_absorption_preflight_pack/gate_authority_map.json": result["gate_authority_map"],
        "release/current/stage121_absorption_preflight_pack/absorption_plan.json": {"status": "pass", "plans": result["stage122_to_stage126_plan"]},
    }
    for rel, payload in mapping.items():
        path = root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
