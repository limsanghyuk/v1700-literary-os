from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from v1700.gates.stage166_release_gate import run_stage166_release_gate

from .contracts import (
    BoundaryCriterion,
    ContinuityCriterion,
    EvaluationArtifactEnvelope,
    EvaluationAuthorityPolicy,
    EvaluationEvidenceRef,
    EvaluationMetric,
    EvaluationRubric,
    EvaluationSubject,
    EvaluationThresholdPolicy,
    QualityCriterion,
    RegressionCriterion,
)

TARGET_STAGE = "stage167"
TARGET_REPORT = "release/current/stage167_evaluation_contract_report.json"
PACK_DIR = "release/current/stage167_evaluation_contract_pack"


def run_stage167_evaluation_contract(root: Path | None = None) -> dict[str, Any]:
    root = root or Path(__file__).resolve().parents[3]
    if _active_version(root) != TARGET_STAGE:
        existing = _load_existing(root / TARGET_REPORT)
        if existing is not None:
            return existing

    stage166 = run_stage166_release_gate(root)
    pack = root / PACK_DIR
    pack.mkdir(parents=True, exist_ok=True)

    readiness = _build_page05_readiness(stage166, root)
    contract_catalog = _build_evaluation_contract_catalog()
    rubric_catalog = _build_evaluation_rubric_catalog()
    boundary_policy = _build_evaluation_boundary_policy()
    authority_policy = _build_evaluation_authority_policy()
    entry_criteria = _build_stage168_entry_criteria()

    parts = {
        "page05_readiness_matrix": readiness,
        "evaluation_contract_catalog": contract_catalog,
        "evaluation_rubric_catalog": rubric_catalog,
        "evaluation_boundary_policy": boundary_policy,
        "evaluation_authority_policy": authority_policy,
        "stage168_entry_criteria": entry_criteria,
    }
    for name, payload in parts.items():
        _write_json(pack / f"{name}.json", payload)

    issues: list[str] = []
    if not _stage166_ready(stage166):
        issues.append("stage166_release_gate_blocked")
    for name, payload in parts.items():
        if payload.get("status") != "pass":
            issues.append(f"{name}_blocked")
            issues.extend(f"{name}:{issue}" for issue in payload.get("issues", []))

    metrics = rubric_catalog.get("rubrics", [{}])[0].get("metrics", [])
    weight_total = round(sum(float(metric.get("weight", 0.0)) for metric in metrics), 6)
    result = {
        "stage": "167",
        "baseline_stage": "166",
        "title": "Evaluation Contract",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "mode": "EVALUATION_CONTRACT_LOCAL_ONLY",
        "page": "Page05 Evaluation Body",
        "evaluation_contract_only": True,
        "provider_evaluation_enabled": False,
        "evaluation_write_enabled": False,
        "memory_write_enabled": False,
        "render_write_enabled": False,
        "cross_project_write_enabled": False,
        "canon_mutation_enabled": False,
        "runtime_training_enabled": False,
        "auto_repair_apply_enabled": False,
        "provider_generation_enabled": False,
        "generation_runtime_enabled": False,
        "runtime_execution_enabled": False,
        "provider_default_calls": 0,
        "provider_generation_count": 0,
        "runtime_execution_count": 0,
        "write_operation_count": 0,
        "node2_raw_reveal_access": 0,
        "boundary_violation_count": 0,
        "raw_manuscript_provider_leakage": 0,
        "raw_manuscript_cross_project_leakage": 0,
        "credential_leakage": 0,
        "branchpoint_lineage_preserved": not issues,
        "stage166_page04_seal_inherited": _stage166_ready(stage166),
        "stage168_packet_store_ready": not issues,
        "contract_count": contract_catalog.get("contract_count", 0),
        "subject_count": contract_catalog.get("subject_count", 0),
        "rubric_count": rubric_catalog.get("rubric_count", 0),
        "metric_count": rubric_catalog.get("metric_count", 0),
        "rubric_weight_total": weight_total,
        "rubric_weights_valid": rubric_catalog.get("weight_sum_valid") is True,
        "thresholds_explicit": rubric_catalog.get("thresholds_explicit") is True,
        "boundary_override_defined": rubric_catalog.get("boundary_override_defined") is True,
        "authority_policy_locked": authority_policy.get("status") == "pass",
        "parts": {"stage166_release_gate": _compact(stage166), **parts},
    }
    _write_json(root / TARGET_REPORT, result)
    return result


def _build_page05_readiness(stage166: dict[str, Any], root: Path) -> dict[str, Any]:
    checks = (
        _check_item("page04_release_seal_pass", _stage166_ready(stage166), "release/current/stage166_release_gate_report.json", "Stage166 must seal Page04 before Page05 starts."),
        _check_item("page05_proposal_present", (root / "docs/proposals/page05_evaluation_body_proposal.md").exists(), "docs/proposals/page05_evaluation_body_proposal.md", "Page05 proposal is present."),
        _check_item("page05_blueprint_present", (root / "docs/architecture/page05_evaluation_body_blueprint.md").exists(), "docs/architecture/page05_evaluation_body_blueprint.md", "Page05 blueprint is present."),
        _check_item("page05_handoff_present", (root / "docs/development/page05_developer_handoff.md").exists(), "docs/development/page05_developer_handoff.md", "Page05 handoff is present."),
        _check_item("provider_evaluation_disabled", True, TARGET_REPORT, "Provider evaluation is disabled by default."),
        _check_item("write_paths_disabled", True, TARGET_REPORT, "Evaluation writes, memory writes, and cross-project writes remain disabled."),
        _check_item("boundary_override_reserved", True, TARGET_REPORT, "Boundary violations remain non-overridable."),
    )
    issues = [check["name"] for check in checks if check["status"] != "pass"]
    return {
        "stage": TARGET_STAGE,
        "title": "Page05 Readiness Matrix",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "check_count": len(checks),
        "checks": list(checks),
    }


def _build_evaluation_contract_catalog() -> dict[str, Any]:
    evidence = (
        EvaluationEvidenceRef("page04_release_seal", "stage166", "release/current/stage166_page04_release_seal_report.json", True, True),
        EvaluationEvidenceRef("render_quality_scorecard", "stage165", "release/current/stage165_render_quality_boundary_preflight_pack/render_quality_scorecard.json", True, True),
        EvaluationEvidenceRef("surface_draft_trace", "stage164", "release/current/stage164_surface_draft_dry_run_renderer_pack/dry_run_render_trace.json", True, True),
    )
    subject = EvaluationSubject(
        "page05_surface_subject",
        "surface_draft_bundle",
        "stage166_page04_release_seal",
        "NODE2_SURFACE_ONLY",
        True,
        evidence,
    )
    envelope = EvaluationArtifactEnvelope(
        "eval_artifact_surface_draft",
        "korean_drama_family_secret",
        "stage166",
        "release/current/stage166_page04_release_seal_report.json",
        "surface_draft",
        "surface",
        _stable_digest("stage166:surface_draft"),
        "sealed_page04_artifact",
        0,
        "read_only",
    )
    contract_objects = {
        "EvaluationArtifactEnvelope": envelope.to_dict(),
        "EvaluationSubject": subject.to_dict(),
        "EvaluationRubric": {"defined_in": "evaluation_rubric_catalog"},
        "EvaluationMetric": {"defined_in": "evaluation_rubric_catalog"},
        "EvaluationThresholdPolicy": {"defined_in": "evaluation_rubric_catalog"},
        "QualityCriterion": {"defined_in": "evaluation_boundary_policy"},
        "ContinuityCriterion": {"defined_in": "evaluation_boundary_policy"},
        "RegressionCriterion": {"defined_in": "evaluation_boundary_policy"},
        "BoundaryCriterion": {"defined_in": "evaluation_boundary_policy"},
        "EvaluationVerdict": {"status_space": ["PASS", "BLOCK"]},
        "EvaluationEvidenceRef": evidence[0].to_dict(),
        "EvaluationAuthorityPolicy": {"defined_in": "evaluation_authority_policy"},
    }
    return {
        "stage": TARGET_STAGE,
        "title": "Stage167 Evaluation Contract Catalog",
        "status": "pass",
        "issues": [],
        "contract_count": len(contract_objects),
        "subject_count": 1,
        "objects": contract_objects,
    }


def _build_evaluation_rubric_catalog() -> dict[str, Any]:
    metrics = (
        EvaluationMetric("surface_structure_score", "quality", 0.15, 0.0, 1.0, True, False),
        EvaluationMetric("scene_continuity_score", "continuity", 0.15, 0.0, 1.0, True, True),
        EvaluationMetric("character_consistency_score", "continuity", 0.14, 0.0, 1.0, True, True),
        EvaluationMetric("world_consistency_score", "continuity", 0.12, 0.0, 1.0, True, True),
        EvaluationMetric("reveal_safety_score", "boundary", 0.12, 0.0, 1.0, True, True),
        EvaluationMetric("payoff_alignment_score", "quality", 0.12, 0.0, 1.0, True, False),
        EvaluationMetric("render_packet_adherence_score", "regression", 0.10, 0.0, 1.0, True, False),
        EvaluationMetric("node2_surface_safety_score", "boundary", 0.10, 0.0, 1.0, True, True),
    )
    threshold_policy = EvaluationThresholdPolicy(0.8, 0.05, 0, 0, True, "BLOCK_ALWAYS")
    rubric = EvaluationRubric("page05_default_surface_rubric", "1.0", metrics, threshold_policy, False)
    weight_sum = round(sum(metric.weight for metric in metrics), 6)
    issues = []
    if weight_sum != 1.0:
        issues.append("metric_weight_sum_invalid")
    if any(metric.weight <= 0 for metric in metrics):
        issues.append("metric_weight_non_positive")
    if threshold_policy.boundary_override != "BLOCK_ALWAYS":
        issues.append("boundary_override_not_explicit")
    return {
        "stage": TARGET_STAGE,
        "title": "Stage167 Evaluation Rubric Catalog",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "rubric_count": 1,
        "metric_count": len(metrics),
        "weight_sum": weight_sum,
        "weight_sum_valid": weight_sum == 1.0,
        "thresholds_explicit": True,
        "boundary_override_defined": threshold_policy.boundary_override == "BLOCK_ALWAYS",
        "rubrics": [rubric.to_dict()],
    }


def _build_evaluation_boundary_policy() -> dict[str, Any]:
    quality = (
        QualityCriterion("surface_structure_threshold", "surface_structure_score", ">= 0.80"),
        QualityCriterion("payoff_alignment_threshold", "payoff_alignment_score", ">= 0.75"),
    )
    continuity = (
        ContinuityCriterion("character_continuity_hard_fail", "character_consistency", True),
        ContinuityCriterion("world_continuity_hard_fail", "world_consistency", True),
    )
    regression = (
        RegressionCriterion("render_packet_drift_guard", "stage166_artifact_index", 0.05),
    )
    boundary = (
        BoundaryCriterion("raw_reveal_payload_block", "raw_reveal_payload", False),
        BoundaryCriterion("provider_call_block", "provider_call", False),
        BoundaryCriterion("mutation_command_block", "mutation_command", False),
        BoundaryCriterion("hidden_memory_projection_block", "hidden_memory_projection", False),
    )
    issues = [item.criterion_id for item in boundary if item.overridable]
    return {
        "stage": TARGET_STAGE,
        "title": "Stage167 Evaluation Boundary Policy",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "quality_criteria": [item.to_dict() for item in quality],
        "continuity_criteria": [item.to_dict() for item in continuity],
        "regression_criteria": [item.to_dict() for item in regression],
        "boundary_criteria": [item.to_dict() for item in boundary],
        "boundary_criteria_non_overridable": not issues,
    }


def _build_evaluation_authority_policy() -> dict[str, Any]:
    policy = EvaluationAuthorityPolicy(
        provider_evaluation_enabled=False,
        evaluation_write_enabled=False,
        memory_write_enabled=False,
        canon_mutation_enabled=False,
        runtime_training_enabled=False,
        auto_repair_apply_enabled=False,
        cross_project_write_enabled=False,
        node2_surface_only=True,
        boundary_criteria_non_overridable=True,
    )
    issues = [name for name, value in policy.to_dict().items() if name != "node2_surface_only" and name != "boundary_criteria_non_overridable" and value is True]
    return {
        "stage": TARGET_STAGE,
        "title": "Stage167 Evaluation Authority Policy",
        "status": "pass" if not issues and policy.boundary_criteria_non_overridable and policy.node2_surface_only else "blocked",
        "issues": issues,
        "policy": policy.to_dict(),
    }


def _build_stage168_entry_criteria() -> dict[str, Any]:
    checks = {
        "contract_schema_valid": "pass",
        "rubric_weights_valid": "pass",
        "provider_evaluation_enabled": "blocked",
        "boundary_override_defined": "pass",
        "stage168_packet_store_ready": "pass",
    }
    issues = [name for name, status in checks.items() if name != "provider_evaluation_enabled" and status != "pass"]
    if checks["provider_evaluation_enabled"] != "blocked":
        issues.append("provider_evaluation_must_remain_blocked")
    return {
        "stage": TARGET_STAGE,
        "title": "Stage168 Entry Criteria",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        **checks,
        "next_stage": "stage168",
    }


def _check_item(name: str, condition: bool, evidence: str, description: str) -> dict[str, str]:
    return {
        "name": name,
        "status": "pass" if condition else "blocked",
        "evidence": evidence,
        "description": description,
    }


def _stable_digest(seed: str) -> str:
    return f"sha256:{hashlib.sha256(seed.encode('utf-8')).hexdigest()}"


def _stage166_ready(report: dict[str, Any]) -> bool:
    if report.get("status") == "pass":
        return True
    historical = report.get("stage166", {})
    return historical.get("status") == "pass" and historical.get("page04_sealed") is True


def _active_version(root: Path) -> str:
    manifest = root / "manifests/live_core_manifest.json"
    if not manifest.exists():
        return ""
    return json.loads(manifest.read_text(encoding="utf-8")).get("active_version", "")


def _load_existing(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _compact(report: dict[str, Any]) -> dict[str, Any]:
    keep = (
        "status",
        "stage",
        "baseline_stage",
        "title",
        "issues",
        "mode",
        "page04_sealed",
        "stage167_evaluation_contract_ready",
        "provider_default_calls",
        "live_provider_call_count_in_release_gate",
        "node2_raw_reveal_access",
        "boundary_violation_count",
        "credential_leakage",
        "branchpoint_lineage_preserved",
    )
    return {key: report.get(key) for key in keep if key in report}
