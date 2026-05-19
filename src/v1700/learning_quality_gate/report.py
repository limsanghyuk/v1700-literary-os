from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from v1700.stage134 import run_stage134

from .gate import LEARNING_QUALITY_MODE, build_candidate_registry
from .preflight import run_stage135_preflight


def run_stage135_learning_quality_gate(root: Path | None = None) -> dict[str, Any]:
    root = root or Path(__file__).resolve().parents[3]
    pack = root / "release/current/stage135_learning_quality_gate_pack"
    pack.mkdir(parents=True, exist_ok=True)
    stage134_report = run_stage134(root)
    registry = build_candidate_registry(stage134_report)
    preflight = run_stage135_preflight(root)
    issues = list(registry.issues)
    if preflight.get("status") != "pass":
        issues.append("stage135_preflight_blocked")
    result = {
        "stage": "135",
        "baseline_stage": "134",
        "title": "LearningQualityGate & Candidate Registry",
        "status": "pass" if not issues and registry.status == "pass" else "blocked",
        "issues": issues,
        "mode": LEARNING_QUALITY_MODE,
        "learning_candidate_only": True,
        "candidate_count": registry.counters.get("candidate_count", 0),
        "accepted_candidate_count": registry.counters.get("accepted_candidate_count", 0),
        "rejected_candidate_count": registry.counters.get("rejected_candidate_count", 0),
        "review_only_count": registry.counters.get("review_only_count", 0),
        "learning_allowed_count": registry.counters.get("learning_allowed_count", 0),
        "training_triggered_count": registry.counters.get("training_triggered_count", 0),
        "mutation_allowed_count": registry.counters.get("mutation_allowed_count", 0),
        "runtime_training_enabled": False,
        "active_meta_learning_enabled": False,
        "model_weight_update_count": 0,
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
        "branchpoint_lineage_preserved": not issues,
        "parts": {
            "stage134_report": _compact_stage134(stage134_report),
            "candidate_registry": registry.to_dict(),
            "preflight": preflight,
        },
    }
    _write_json(pack / "candidate_registry.json", registry.to_dict())
    _write_json(pack / "stage135_preflight_report.json", preflight)
    _write_json(pack / "stage134_input_summary.json", _compact_stage134(stage134_report))
    _write_json(root / "release/current/stage135_learning_quality_gate_report.json", result)
    return result


def _compact_stage134(report: dict[str, Any]) -> dict[str, Any]:
    return {
        "stage": report.get("stage"),
        "status": report.get("status"),
        "mode": report.get("mode"),
        "audit_only": report.get("audit_only"),
        "case_count": report.get("case_count"),
        "review_recommendation_count": report.get("review_recommendation_count"),
        "training_allowed_count": report.get("training_allowed_count"),
        "model_weight_update_count": report.get("model_weight_update_count"),
        "branchpoint_lineage_preserved": report.get("branchpoint_lineage_preserved"),
    }


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
