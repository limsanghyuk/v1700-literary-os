from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from v1700.contradiction_classifier.classifier import run_stage132_classifier_matrix

from .measurement import DIMENSIONS, measure_stage132_classifier_output
from .preflight import run_stage133_gitnexus_preflight


def run_stage133_narrative_state_tensor(root: Path | None = None) -> dict[str, Any]:
    root = root or Path(__file__).resolve().parents[3]
    pack = root / "release/current/stage133_narrative_state_tensor_pack"
    pack.mkdir(parents=True, exist_ok=True)
    classifier_matrix = run_stage132_classifier_matrix()
    tensor_report = measure_stage132_classifier_output(classifier_matrix)
    preflight = run_stage133_gitnexus_preflight(root)
    issues = list(tensor_report.issues)
    if preflight.get("status") != "pass":
        issues.append("gitnexus_preflight_blocked")
    result = {
        "stage": "133",
        "baseline_stage": "132",
        "title": "NarrativeStateTensor 8D Measurement Layer",
        "status": "pass" if not issues and tensor_report.status == "pass" else "blocked",
        "issues": issues,
        "measurement_mode": "DETERMINISTIC_8D_LOCAL_ONLY",
        "dimension_count": len(DIMENSIONS),
        "dimensions": list(DIMENSIONS),
        "tensor_case_count": len(tensor_report.tensors),
        "review_required_tensor_count": sum(1 for item in tensor_report.tensors if item.status == "REVIEW_REQUIRED"),
        "pass_tensor_count": sum(1 for item in tensor_report.tensors if item.status == "PASS"),
        "average_vector": tensor_report.average_vector,
        "lowest_observed_dimension": _lowest_dimension(tensor_report.to_dict()["tensors"]),
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
        "writer_review_required_for_true_contradiction": True,
        "mystery_exemption_requires_reveal_lock": True,
        "branchpoint_lineage_preserved": not issues,
        "parts": {
            "classifier_matrix": classifier_matrix,
            "tensor_measurement": tensor_report.to_dict(),
            "gitnexus_preflight": preflight,
        },
    }
    _write_json(pack / "tensor_measurement_report.json", tensor_report.to_dict())
    _write_json(pack / "stage132_classifier_input_report.json", classifier_matrix)
    _write_json(pack / "gitnexus_preflight_report.json", preflight)
    _write_json(pack / "stage133_summary.json", _summary(result))
    _write_json(root / "release/current/stage133_narrative_state_tensor_report.json", result)
    return result


def _lowest_dimension(tensors: list[dict[str, Any]]) -> dict[str, Any]:
    if not tensors:
        return {"dimension": "", "score": 0.0}
    lowest = min(tensors, key=lambda item: item["lowest_score"])
    return {
        "case_id": lowest["case_id"],
        "dimension": lowest["lowest_dimension"],
        "score": lowest["lowest_score"],
        "classification": lowest["classification"],
    }


def _summary(result: dict[str, Any]) -> dict[str, Any]:
    return {
        "stage": result["stage"],
        "status": result["status"],
        "dimension_count": result["dimension_count"],
        "tensor_case_count": result["tensor_case_count"],
        "review_required_tensor_count": result["review_required_tensor_count"],
        "provider_default_calls": 0,
        "node2_raw_reveal_access": 0,
        "branchpoint_lineage_preserved": result["branchpoint_lineage_preserved"],
    }


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
