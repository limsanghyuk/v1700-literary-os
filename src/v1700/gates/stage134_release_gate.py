from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from v1700.gates.stage133_release_gate import run_stage133_release_gate
from v1700.stage134 import run_stage134

_CACHE: dict[str, dict[str, Any]] = {}


def run_stage134_release_gate(root: Path | None = None) -> dict[str, Any]:
    root = root or Path(__file__).resolve().parents[3]
    key = str(root.resolve())
    if key in _CACHE:
        return _CACHE[key]
    baseline = run_stage133_release_gate(root)
    stage = run_stage134(root)
    parts = stage.get("parts", {})
    audit = parts.get("meta_learner_audit", {})
    preflight = parts.get("gitnexus_preflight", {})
    checks = {
        "stage133_baseline_gate_pass": _check(baseline.get("status") == "pass"),
        "audit_report_pass": _check(audit.get("status") == "pass"),
        "audit_only_mode_pass": _check(stage.get("audit_only") is True and stage.get("mode") == "META_LEARNER_AUDIT_ONLY_NO_TRAINING"),
        "training_disabled_pass": _check(stage.get("runtime_training_enabled") is False and stage.get("training_allowed_count") == 0 and stage.get("model_weight_update_count") == 0),
        "active_learning_disabled_pass": _check(stage.get("active_meta_learning_enabled") is False and stage.get("active_learning_allowed_count") == 0),
        "mutation_blocked_pass": _check(stage.get("auto_repair_mutation_count") == 0 and stage.get("mutation_allowed_count") == 0),
        "review_recommendation_pass": _check(stage.get("review_recommendation_count", 0) >= 1),
        "gitnexus_python_fallback_preflight_pass": _check(preflight.get("python_fallback", {}).get("status") == "PASS"),
        "symbol_to_branchpoint_trace_pass": _check(preflight.get("release_gate_integration", {}).get("stage134_gate_registered") is True),
        "gate26_advisory_only_pass": _check(stage.get("gate26_hard_block_enabled") is False),
        "canon_auto_resolution_blocked": _check(stage.get("canon_auto_resolution_count") == 0),
        "cross_project_write_blocked": _check(stage.get("cross_project_write_allowed") is False),
        "provider_zero_pass": _check(stage.get("provider_default_calls") == 0 and stage.get("live_provider_call_count_in_release_gate") == 0),
        "node2_boundary_pass": _check(stage.get("node2_raw_reveal_access") == 0),
        "raw_manuscript_leakage_zero": _check(stage.get("raw_manuscript_provider_leakage") == 0 and stage.get("raw_manuscript_cross_project_leakage") == 0),
        "credential_leakage_zero_pass": _check(stage.get("credential_leakage") == 0),
        "branchpoint_survival_pass": _check(stage.get("branchpoint_lineage_preserved") is True),
        "docs_manifest_pass": _check(_docs_manifest_ok(root)),
        "repo_doctor_active_stage_ready": _check(_repo_doctor_ready(root)),
    }
    issues = [name for name, value in checks.items() if value["status"] != "pass"]
    result = {
        "stage": "134",
        "baseline_stage": "133",
        "title": "MetaLearner Audit Mode Gate",
        "status": "pass" if not issues and stage.get("status") == "pass" else "blocked",
        "issues": issues,
        "checks": checks,
        "stage134": _compact(stage),
        "provider_default_calls": 0,
        "live_provider_call_count_in_release_gate": 0,
        "node2_raw_reveal_access": 0,
        "raw_manuscript_provider_leakage": 0,
        "raw_manuscript_cross_project_leakage": 0,
        "credential_leakage": 0,
        "branchpoint_lineage_preserved": not issues,
    }
    out = root / "release/current/stage134_release_gate_report.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    _CACHE[key] = result
    return result


def _check(condition: bool) -> dict[str, str]:
    return {"status": "pass" if condition else "blocked"}


def _compact(stage: dict[str, Any]) -> dict[str, Any]:
    keep = (
        "status", "stage", "baseline_stage", "title", "issues", "mode", "audit_only",
        "case_count", "review_recommendation_count", "weight_candidate_count",
        "training_allowed_count", "mutation_allowed_count", "active_learning_allowed_count",
        "runtime_training_enabled", "active_meta_learning_enabled", "model_weight_update_count",
        "gate26_hard_block_enabled", "auto_repair_mutation_count", "canon_auto_resolution_count",
        "cross_project_write_allowed", "raw_manuscript_provider_leakage",
        "raw_manuscript_cross_project_leakage", "provider_default_calls",
        "live_provider_call_count_in_release_gate", "node2_raw_reveal_access",
        "credential_leakage", "writer_review_required_for_true_contradiction",
        "mystery_exemption_requires_reveal_lock", "branchpoint_lineage_preserved",
    )
    return {key: stage.get(key) for key in keep if key in stage}


def _docs_manifest_ok(root: Path) -> bool:
    return all((root / rel).exists() for rel in [
        "docs/stages/stage134.md",
        "docs/proposals/stage134_proposal.md",
        "docs/architecture/stage134_blueprint.md",
        "docs/roadmaps/stage134_roadmap.md",
        "manifests/stage134_manifest.json",
        "manifests/stage134_meta_learner_audit_manifest.json",
        "manifests/stage134_branchpoint_trace_manifest.json",
        "release/current/stage134_meta_learner_audit_report.json",
        "release/current/stage134_meta_learner_audit_pack/meta_learner_audit_report.json",
        "release/current/stage134_meta_learner_audit_pack/gitnexus_preflight_report.json",
    ])


def _repo_doctor_ready(root: Path) -> bool:
    path = root / "tools/run_stage72_repo_doctor.py"
    text = path.read_text(encoding="utf-8", errors="ignore") if path.exists() else ""
    return "stage134" in text and "stage134_release_gate" in text and "stage134_meta_learner_audit" in text
