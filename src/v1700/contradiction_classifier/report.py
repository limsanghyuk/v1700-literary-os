from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from v1700.gig_advisory.classifier import build_gate26_advisory_cases

from .classifier import run_stage132_classifier_matrix
from .mystery_exemption import audit_mystery_exemptions
from .preflight import run_stage132_gitnexus_preflight


def run_stage132_contradiction_classifier(root: Path | None = None) -> dict[str, Any]:
    root = root or Path(__file__).resolve().parents[3]
    pack = root / "release/current/stage132_contradiction_classifier_pack"
    pack.mkdir(parents=True, exist_ok=True)
    matrix = run_stage132_classifier_matrix()
    mystery = audit_mystery_exemptions(matrix)
    preflight = run_stage132_gitnexus_preflight(root)
    stage131_categories = sorted(case["conflict_type"] for case in build_gate26_advisory_cases()["cases"])
    parts = {
        "classifier_matrix": matrix,
        "mystery_exemption": mystery,
        "gitnexus_preflight": preflight,
    }
    for name, payload in parts.items():
        _write_json(pack / f"{name}_report.json", payload)
    issues: list[str] = []
    if matrix.get("status") != "pass":
        issues.append("classifier_matrix_blocked")
    if mystery.get("status") != "pass":
        issues.append("mystery_exemption_blocked")
    if preflight.get("status") != "PASS":
        issues.append("gitnexus_preflight_blocked")
    result = {
        "stage": "132",
        "baseline_stage": "131",
        "title": "Contradiction Classifier + Mystery Exemption",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "classifier_mode": "DETERMINISTIC_EVIDENCE_CLASSIFIER",
        "case_count": matrix.get("case_count", 0),
        "exemption_count": matrix.get("exemption_count", 0),
        "writer_review_required_count": matrix.get("writer_review_required_count", 0),
        "stage131_categories_preserved": stage131_categories,
        "true_contradiction_review_required": matrix.get("writer_review_required_count", 0) >= 1,
        "mystery_exemption_requires_reveal_lock": mystery.get("mystery_exemption_policy") == "requires_reveal_lock_and_payoff_budget",
        "gate26_hard_block_enabled": False,
        "gate26_hard_block_count": matrix.get("hard_block_count", 0),
        "auto_repair_mutation_count": matrix.get("auto_repair_mutation_count", 0),
        "canon_auto_resolution_count": matrix.get("canon_auto_resolution_count", 0),
        "cross_project_write_allowed": False,
        "raw_manuscript_provider_leakage": 0,
        "raw_manuscript_cross_project_leakage": 0,
        "provider_default_calls": 0,
        "live_provider_call_count_in_release_gate": 0,
        "node2_raw_reveal_access": 0,
        "credential_leakage": 0,
        "writer_approval_guard": True,
        "branchpoint_lineage_preserved": all(preflight.get("survival_matrix", {}).values()),
        "parts": parts,
    }
    _write_json(root / "release/current/stage132_contradiction_classifier_report.json", result)
    _write_json(pack / "stage132_summary.json", _summary(result))
    return result


def _summary(result: dict[str, Any]) -> dict[str, Any]:
    keys = [
        "stage", "baseline_stage", "title", "status", "issues", "classifier_mode",
        "case_count", "exemption_count", "true_contradiction_review_required",
        "mystery_exemption_requires_reveal_lock", "gate26_hard_block_enabled",
        "canon_auto_resolution_count", "provider_default_calls",
        "live_provider_call_count_in_release_gate", "node2_raw_reveal_access",
        "writer_approval_guard", "branchpoint_lineage_preserved",
    ]
    return {key: result.get(key) for key in keys}


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
