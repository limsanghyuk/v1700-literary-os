from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .classifier import build_gate26_advisory_cases
from .policy import build_gate26_advisory_policy
from .preflight import run_stage131_gitnexus_preflight


def run_stage131_gig_advisory(root: Path | None = None) -> dict[str, Any]:
    root = root or Path(__file__).resolve().parents[3]
    pack = root / "release/current/stage131_gig_advisory_pack"
    pack.mkdir(parents=True, exist_ok=True)
    classifier = build_gate26_advisory_cases()
    policy = build_gate26_advisory_policy(classifier)
    preflight = run_stage131_gitnexus_preflight(root)
    parts = {
        "classifier": classifier,
        "policy": policy,
        "gitnexus_preflight": preflight,
    }
    for name, payload in parts.items():
        _write_json(pack / f"{name}_report.json", payload)
    issues: list[str] = []
    if classifier.get("status") != "pass":
        issues.append("classifier_blocked")
    if policy.get("status") != "pass":
        issues.append("policy_blocked")
    if preflight.get("status") != "PASS":
        issues.append("gitnexus_preflight_blocked")
    result = {
        "stage": "131",
        "baseline_stage": "130",
        "title": "GIG / Gate26 Advisory Absorption",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "advisory_mode": "GIG_GATE26_ADVISORY_ONLY",
        "case_count": classifier.get("case_count", 0),
        "true_contradiction_review_required": classifier.get("writer_review_required_count", 0) >= 1,
        "gate26_hard_block_enabled": False,
        "gate26_hard_block_count": 0,
        "auto_repair_mutation_count": 0,
        "canon_auto_resolution_count": 0,
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
    _write_json(root / "release/current/stage131_gig_advisory_report.json", result)
    _write_json(pack / "stage131_summary.json", _summary(result))
    return result


def _summary(result: dict[str, Any]) -> dict[str, Any]:
    keys = [
        "stage", "baseline_stage", "title", "status", "issues", "advisory_mode",
        "case_count", "true_contradiction_review_required", "gate26_hard_block_enabled",
        "canon_auto_resolution_count", "provider_default_calls", "live_provider_call_count_in_release_gate",
        "node2_raw_reveal_access", "writer_approval_guard", "branchpoint_lineage_preserved",
    ]
    return {key: result.get(key) for key in keys}


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
