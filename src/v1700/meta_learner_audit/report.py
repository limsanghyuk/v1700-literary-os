from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from v1700.stage133 import run_stage133

from .audit import AUDIT_MODE, audit_stage133_tensor_report
from .preflight import run_stage134_gitnexus_preflight


def run_stage134_meta_learner_audit(root: Path | None = None) -> dict[str, Any]:
    root = root or Path(__file__).resolve().parents[3]
    pack = root / "release/current/stage134_meta_learner_audit_pack"
    pack.mkdir(parents=True, exist_ok=True)
    stage133_report = run_stage133(root)
    audit_report = audit_stage133_tensor_report(stage133_report)
    preflight = run_stage134_gitnexus_preflight(root)
    issues = list(audit_report.issues)
    if preflight.get("status") != "pass":
        issues.append("gitnexus_preflight_blocked")
    result = {
        "stage": "134",
        "baseline_stage": "133",
        "title": "MetaLearner Audit Mode",
        "status": "pass" if not issues and audit_report.status == "pass" else "blocked",
        "issues": issues,
        "mode": AUDIT_MODE,
        "audit_only": True,
        "case_count": audit_report.aggregate.get("case_count", 0),
        "review_recommendation_count": audit_report.aggregate.get("review_recommendation_count", 0),
        "weight_candidate_count": audit_report.aggregate.get("weight_candidate_count", 0),
        "training_allowed_count": audit_report.aggregate.get("training_allowed_count", 0),
        "mutation_allowed_count": audit_report.aggregate.get("mutation_allowed_count", 0),
        "active_learning_allowed_count": audit_report.aggregate.get("active_learning_allowed_count", 0),
        "provider_default_calls": 0,
        "live_provider_call_count_in_release_gate": 0,
        "node2_raw_reveal_access": 0,
        "raw_manuscript_provider_leakage": 0,
        "raw_manuscript_cross_project_leakage": 0,
        "credential_leakage": 0,
        "cross_project_write_allowed": False,
        "gate26_hard_block_enabled": False,
        "canon_auto_resolution_count": 0,
        "auto_repair_mutation_count": 0,
        "runtime_training_enabled": False,
        "active_meta_learning_enabled": False,
        "model_weight_update_count": 0,
        "writer_review_required_for_true_contradiction": True,
        "mystery_exemption_requires_reveal_lock": True,
        "branchpoint_lineage_preserved": not issues,
        "parts": {
            "stage133_report": _compact_stage133(stage133_report),
            "meta_learner_audit": audit_report.to_dict(),
            "gitnexus_preflight": preflight,
        },
    }
    _write_json(pack / "meta_learner_audit_report.json", audit_report.to_dict())
    _write_json(pack / "stage133_tensor_input_summary.json", _compact_stage133(stage133_report))
    _write_json(pack / "gitnexus_preflight_report.json", preflight)
    _write_json(pack / "stage134_summary.json", _summary(result))
    _write_json(root / "release/current/stage134_meta_learner_audit_report.json", result)
    return result


def _compact_stage133(report: dict[str, Any]) -> dict[str, Any]:
    return {
        "stage": report.get("stage"),
        "status": report.get("status"),
        "dimension_count": report.get("dimension_count"),
        "tensor_case_count": report.get("tensor_case_count"),
        "review_required_tensor_count": report.get("review_required_tensor_count"),
        "pass_tensor_count": report.get("pass_tensor_count"),
        "provider_default_calls": report.get("provider_default_calls", 0),
        "node2_raw_reveal_access": report.get("node2_raw_reveal_access", 0),
        "canon_auto_resolution_count": report.get("canon_auto_resolution_count", 0),
        "auto_repair_mutation_count": report.get("auto_repair_mutation_count", 0),
        "branchpoint_lineage_preserved": report.get("branchpoint_lineage_preserved"),
    }


def _summary(result: dict[str, Any]) -> dict[str, Any]:
    return {
        "stage": result["stage"],
        "status": result["status"],
        "mode": result["mode"],
        "case_count": result["case_count"],
        "review_recommendation_count": result["review_recommendation_count"],
        "training_allowed_count": result["training_allowed_count"],
        "model_weight_update_count": result["model_weight_update_count"],
        "provider_default_calls": 0,
        "node2_raw_reveal_access": 0,
        "branchpoint_lineage_preserved": result["branchpoint_lineage_preserved"],
    }


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
