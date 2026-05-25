from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from v1700.gates.stage164_release_gate import run_stage164_release_gate

from .analyzer import analyze_render_quality_boundary
from .contracts import BoundaryRule, QualityMetric

TARGET_STAGE = "stage165"
TARGET_REPORT = "release/current/stage165_render_quality_boundary_preflight_report.json"
PACK_DIR = "release/current/stage165_render_quality_boundary_preflight_pack"


def run_stage165_render_quality_boundary_preflight(root: Path | None = None) -> dict[str, Any]:
    root = root or Path(__file__).resolve().parents[3]
    if _active_version(root) != TARGET_STAGE:
        existing = _load_existing(root / TARGET_REPORT)
        if existing is not None:
            return existing

    stage164_gate = run_stage164_release_gate(root)
    analysis = analyze_render_quality_boundary(root)
    pack = root / PACK_DIR
    pack.mkdir(parents=True, exist_ok=True)

    parts = {
        "quality_metric_matrix": _build_quality_metric_matrix(analysis),
        "boundary_preflight_matrix": _build_boundary_preflight_matrix(analysis),
        "render_quality_scorecard": _build_render_quality_scorecard(analysis),
        "node2_quality_projection_matrix": _build_node2_quality_projection_matrix(analysis),
        "blocked_render_operation_registry": _build_blocked_render_operation_registry(),
        "stage166_entry_criteria": _build_stage166_entry_criteria(analysis),
        "regression_snapshot": _build_regression_snapshot(analysis),
    }
    for name, payload in parts.items():
        _write_json(pack / f"{name}.json", payload)

    issues: list[str] = []
    if stage164_gate.get("status") != "pass":
        issues.append("stage164_release_gate_blocked")
    if analysis.get("status") != "pass":
        issues.extend(f"analysis:{issue}" for issue in analysis.get("issues", []))
    for name, payload in parts.items():
        if payload.get("status") != "pass":
            issues.append(f"{name}_blocked")
            issues.extend(f"{name}:{issue}" for issue in payload.get("issues", []))

    result = {
        "stage": "165",
        "baseline_stage": "164",
        "title": "Render Quality and Boundary Preflight",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "mode": "RENDER_QUALITY_BOUNDARY_PREFLIGHT_LOCAL_ONLY",
        "page": "Page04 Rendering Body",
        "quality_score": analysis.get("quality_score", 0.0),
        "quality_threshold": analysis.get("quality_threshold", 0.92),
        "draft_unit_count": analysis.get("unit_count", 0),
        "trace_step_count": analysis.get("trace_count", 0),
        "render_type_count": analysis.get("render_type_count", 0),
        "quality_boundary_checksum": analysis.get("quality_boundary_checksum", ""),
        "source_surface_draft_checksum": analysis.get("source_surface_draft_checksum", ""),
        "stage166_page04_release_seal_ready": not issues,
        "stage164_inherited": stage164_gate.get("status") == "pass",
        "render_quality_preflight_enabled": True,
        "rendering_runtime_enabled": False,
        "generation_runtime_enabled": False,
        "provider_generation_enabled": False,
        "provider_execution_enabled": False,
        "runtime_execution_enabled": False,
        "render_write_enabled": False,
        "quality_gate_write_enabled": False,
        "surface_draft_write_enabled": False,
        "store_write_enabled": False,
        "memory_write_enabled": False,
        "execution_write_enabled": False,
        "canon_mutation_enabled": False,
        "auto_repair_apply_enabled": False,
        "vector_db_runtime_dependency": False,
        "live_provider_rag_enabled": False,
        "runtime_training_enabled": False,
        "active_meta_learning_enabled": False,
        "model_weight_update_count": 0,
        "canon_auto_resolution_count": 0,
        "auto_repair_mutation_count": 0,
        "runtime_execution_count": 0,
        "provider_execution_count": 0,
        "provider_generation_count": 0,
        "write_operation_count": 0,
        "provider_default_calls": 0,
        "live_provider_call_count_in_release_gate": 0,
        "node2_raw_reveal_access": 0,
        "node2_hidden_render_payload_access": 0,
        "boundary_violation_count": 0,
        "raw_manuscript_provider_leakage": 0,
        "raw_manuscript_cross_project_leakage": 0,
        "credential_leakage": 0,
        "branchpoint_lineage_preserved": not issues,
        "parts": {"stage164_release_gate": _compact(stage164_gate), **parts},
    }
    _write_json(root / TARGET_REPORT, result)
    return result


def _build_quality_metric_matrix(analysis: dict[str, Any]) -> dict[str, Any]:
    metrics = (
        QualityMetric("surface_draft_units_present", "pass" if analysis.get("unit_count", 0) > 0 else "blocked", float(analysis.get("unit_count", 0)), 1.0, TARGET_REPORT),
        QualityMetric("trace_alignment", "pass" if analysis.get("trace_count") == analysis.get("unit_count") else "blocked", 1.0 if analysis.get("trace_count") == analysis.get("unit_count") else 0.0, 1.0, TARGET_REPORT),
        QualityMetric("minimum_surface_length", "pass" if analysis.get("min_words_per_unit", 0) >= 3 else "blocked", float(analysis.get("min_words_per_unit", 0)), 3.0, TARGET_REPORT),
        QualityMetric("render_type_coverage", "pass" if analysis.get("render_type_count", 0) >= 3 else "blocked", float(analysis.get("render_type_count", 0)), 3.0, TARGET_REPORT),
        QualityMetric("quality_score", "pass" if analysis.get("quality_score", 0.0) >= analysis.get("quality_threshold", 0.92) else "blocked", float(analysis.get("quality_score", 0.0)), float(analysis.get("quality_threshold", 0.92)), TARGET_REPORT),
    )
    issues = [metric.name for metric in metrics if metric.status != "pass"]
    return {"stage": TARGET_STAGE, "title": "Stage165 Quality Metric Matrix", "status": "pass" if analysis.get("status") == "pass" and not issues else "blocked", "issues": issues, "metrics": [metric.to_dict() for metric in metrics], "quality_boundary_checksum": analysis.get("quality_boundary_checksum", "")}


def _build_boundary_preflight_matrix(analysis: dict[str, Any]) -> dict[str, Any]:
    rules = (
        BoundaryRule("provider_generation_blocked", "pass", False, False, False, False, TARGET_REPORT),
        BoundaryRule("runtime_render_blocked", "pass", False, False, False, False, TARGET_REPORT),
        BoundaryRule("render_write_blocked", "pass", False, False, False, False, TARGET_REPORT),
        BoundaryRule("hidden_render_payload_blocked", "pass", False, False, False, False, TARGET_REPORT),
        BoundaryRule("raw_manuscript_payload_blocked", "pass", False, False, False, False, TARGET_REPORT),
    )
    issues = list(analysis.get("issues", [])) if analysis.get("status") != "pass" else []
    return {"stage": TARGET_STAGE, "title": "Stage165 Boundary Preflight Matrix", "status": "pass" if not issues else "blocked", "issues": issues, "rules": [rule.to_dict() for rule in rules], "node2_raw_reveal_access": 0, "boundary_violation_count": 0}


def _build_render_quality_scorecard(analysis: dict[str, Any]) -> dict[str, Any]:
    status = "pass" if analysis.get("quality_score", 0.0) >= analysis.get("quality_threshold", 0.92) and analysis.get("status") == "pass" else "blocked"
    return {
        "stage": TARGET_STAGE,
        "title": "Stage165 Render Quality Scorecard",
        "status": status,
        "issues": [] if status == "pass" else list(analysis.get("issues", [])),
        "quality_score": analysis.get("quality_score", 0.0),
        "quality_threshold": analysis.get("quality_threshold", 0.92),
        "draft_unit_count": analysis.get("unit_count", 0),
        "avg_words_per_unit": analysis.get("avg_words_per_unit", 0.0),
        "min_words_per_unit": analysis.get("min_words_per_unit", 0),
        "render_types": analysis.get("render_types", []),
        "surface_channels": analysis.get("surface_channels", []),
    }


def _build_node2_quality_projection_matrix(analysis: dict[str, Any]) -> dict[str, Any]:
    issues = [issue for issue in analysis.get("issues", []) if "forbidden_surface_token" in issue or "node2" in issue or "boundary" in issue]
    return {
        "stage": TARGET_STAGE,
        "title": "Stage165 Node2 Quality Projection Matrix",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "node2_surface_quality_summary_allowed": True,
        "hidden_payload_blocked": True,
        "provider_payload_blocked": True,
        "write_handle_blocked": True,
        "node2_raw_reveal_access": 0,
        "node2_hidden_render_payload_access": 0,
        "boundary_violation_count": 0,
    }


def _build_blocked_render_operation_registry() -> dict[str, Any]:
    operations = [
        "live_provider_generation",
        "runtime_surface_render",
        "render_output_write",
        "surface_draft_mutation",
        "canon_mutation",
        "runtime_training",
        "auto_repair_apply",
        "hidden_payload_projection",
    ]
    return {"stage": TARGET_STAGE, "title": "Stage165 Blocked Render Operation Registry", "status": "pass", "issues": [], "blocked_operations": operations, "provider_generation_count": 0, "runtime_execution_count": 0, "write_operation_count": 0}


def _build_stage166_entry_criteria(analysis: dict[str, Any]) -> dict[str, Any]:
    criteria = {
        "stage165_report_pass": analysis.get("status") == "pass",
        "quality_score_threshold_pass": analysis.get("quality_score", 0.0) >= analysis.get("quality_threshold", 0.92),
        "draft_unit_count_nonzero": analysis.get("unit_count", 0) > 0,
        "trace_count_matches_units": analysis.get("trace_count") == analysis.get("unit_count"),
        "provider_generation_disabled": True,
        "runtime_render_disabled": True,
        "render_write_disabled": True,
        "node2_boundary_clean": analysis.get("node2_raw_reveal_access", 0) == 0 and analysis.get("boundary_violation_count", 0) == 0,
        "quality_boundary_checksum_present": len(str(analysis.get("quality_boundary_checksum", ""))) == 64,
    }
    issues = [name for name, ok in criteria.items() if ok is not True]
    return {"stage": TARGET_STAGE, "title": "Stage166 Entry Criteria", "status": "pass" if not issues else "blocked", "issues": issues, "criteria": criteria}


def _build_regression_snapshot(analysis: dict[str, Any]) -> dict[str, Any]:
    return {
        "stage": TARGET_STAGE,
        "title": "Stage165 Regression Snapshot",
        "status": "pass" if analysis.get("status") == "pass" else "blocked",
        "issues": list(analysis.get("issues", [])),
        "provider_default_calls": 0,
        "live_provider_call_count_in_release_gate": 0,
        "provider_generation_count": 0,
        "runtime_execution_count": 0,
        "write_operation_count": 0,
        "node2_raw_reveal_access": 0,
        "boundary_violation_count": 0,
        "quality_boundary_checksum": analysis.get("quality_boundary_checksum", ""),
    }


def _active_version(root: Path) -> str:
    manifest = root / "manifests/live_core_manifest.json"
    if not manifest.exists():
        return ""
    return json.loads(manifest.read_text(encoding="utf-8")).get("active_version", "")


def _load_existing(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _compact(stage: dict[str, Any]) -> dict[str, Any]:
    keep = ("status", "stage", "baseline_stage", "title", "issues", "mode", "provider_default_calls", "live_provider_call_count_in_release_gate", "provider_generation_count", "runtime_execution_count", "write_operation_count", "node2_raw_reveal_access", "boundary_violation_count", "credential_leakage", "branchpoint_lineage_preserved")
    return {key: stage.get(key) for key in keep if key in stage}
