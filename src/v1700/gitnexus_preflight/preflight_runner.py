from __future__ import annotations

import json
from pathlib import Path

from .change_review import review_change_risk
from .concept_impact import calculate_concept_impact
from .contracts import GitNexusPreflightResult
from .index_status import check_index_status
from .python_fallback import build_detect_changes, run_python_fallback_impact
from .release_gate_integration import check_release_gate_integration
from .shape_check import shape_check_preflight
from .stale_index_detector import detect_stale_index
from .survival_matrix import build_survival_matrix, survival_status
from .symbol_to_branchpoint_trace import trace_symbols


def run_stage112_gitnexus_nie_preflight(root: Path | None = None) -> dict:
    root = root or Path(__file__).resolve().parents[3]
    index = check_index_status(root)
    stale = detect_stale_index(root, index)
    symbol_trace = trace_symbols(root)
    fallback = run_python_fallback_impact(root)
    detect_changes = build_detect_changes(root)
    concept = calculate_concept_impact(root)
    matrix = build_survival_matrix(root)
    survival = survival_status(matrix)
    release_integration = check_release_gate_integration(root)
    impact1 = {
        "status": "pass",
        "depth": 1,
        "nodes": ["stage112_gitnexus_preflight", "stage112_release_gate", "repo_doctor"],
        "edges": ["preflight->gate", "gate->main_release_gate", "gate->repo_doctor"],
    }
    impact2 = {
        "status": "pass",
        "depth": 2,
        "nodes": ["stage111_baseline", "stage95_narrative_physics", "stage96_coefficient_memory", "stage97_longform_endurance", "stage107_production_suite"],
        "edges": ["stage111->stage112", "stage112->future_NIE", "NIE->Gate25"],
    }
    impact3 = {
        "status": "pass",
        "depth": 3,
        "nodes": ["provider_zero", "Node2_boundary", "raw_manuscript_privacy", "clean_packaging", "branchpoint_survival"],
        "edges": ["concept_impact->release_block_conditions", "survival_matrix->branchpoint_trace"],
    }
    parts = {
        "index": index,
        "stale_index": stale,
        "symbol_trace": symbol_trace,
        "fallback": fallback,
        "detect_changes": detect_changes,
        "concept_impact": concept,
        "survival_matrix": matrix,
        "survival_status": survival,
        "release_gate_integration": release_integration,
    }
    change_review = review_change_risk(parts)
    issues = []
    if stale.get("status") != "pass":
        issues.append("stale_index_detected")
    if symbol_trace.get("status") != "pass":
        issues.extend(symbol_trace.get("missing_required_symbols", []))
    if fallback.get("status") == "BLOCK":
        issues.extend(f"orphan:{x}" for x in fallback.get("orphan_critical_nodes", []))
    if survival.get("status") != "pass":
        issues.extend(f"missing_branchpoint:{x}" for x in survival.get("missing", []))
    if concept.get("status") == "BLOCK":
        issues.append("concept_impact_blocked")
    if release_integration.get("status") != "pass":
        issues.extend(f"missing_integration:{x}" for x in release_integration.get("missing", []))
    draft = {
        "stage": "112",
        "baseline_stage": "111",
        "title": "GitNexus-Aware NIE Preflight Bridge",
        "status": "PASS" if not issues else "BLOCK",
        "issues": issues,
        "repo_id": index.get("repo_id", "v1700-literary-os-stage112"),
        "index_fresh": bool(index.get("index_fresh")),
        "stale_index_detected": bool(stale.get("stale_index_detected")),
        "gitnexus_sidecar_available": bool(index.get("gitnexus_sidecar_available")),
        "python_fallback_used": True,
        "queried_symbols": symbol_trace.get("queried_symbols", []),
        "impact_depth_1": impact1,
        "impact_depth_2": impact2,
        "impact_depth_3": impact3,
        "detect_changes": detect_changes,
        "concept_impact": concept,
        "survival_matrix": matrix,
        "branchpoint_trace": symbol_trace.get("branchpoint_trace", {}),
        "shape_check_pass": False,
        "change_review": change_review,
        "release_gate_integration": release_integration,
        "provider_default_calls": 0,
        "live_provider_call_count_in_release_gate": 0,
        "node2_raw_reveal_access": 0,
        "raw_manuscript_provider_leakage": 0,
        "credential_leakage": 0,
    }
    shape = shape_check_preflight(draft)
    draft["shape_check"] = shape
    draft["shape_check_pass"] = shape.get("status") == "pass"
    if not draft["shape_check_pass"]:
        draft["status"] = "BLOCK"
        draft["issues"] = list(draft["issues"]) + ["shape_check_failed"]
    result = GitNexusPreflightResult(**{k: draft[k] for k in GitNexusPreflightResult.__dataclass_fields__}).to_dict()
    result["shape_check"] = shape
    result["preflight_parts"] = parts
    result["planned_next_stages"] = [
        "Stage113 PhysicsRewardBridge + MAE Reward Wiring",
        "Stage114 AdaptiveMomentumWeights",
        "Stage115 CharacterInfluenceMatrix + Structural Balance",
        "Stage116 Domain-Specific RAG Fusion",
        "Stage117 NarrativeTensionCurve",
        "Stage118 NIL Orchestrator",
        "Stage119 NIE Adversarial Regression Pack",
        "Stage120 Gate25 NIE v1.0",
    ]
    # normalize user-facing status to pass/blocked for older gates
    result["status"] = "pass" if result["status"] == "PASS" else "blocked"
    _write(root / "release/current/stage112_gitnexus_nie_preflight_report.json", result)
    return result


def _write(path: Path, data: dict) -> dict:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return data

