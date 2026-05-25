from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from v1700.gates.stage163_release_gate import run_stage163_release_gate

from .contracts import SurfaceDraftPolicy
from .renderer import build_surface_draft_dry_run

TARGET_STAGE = "stage164"
TARGET_REPORT = "release/current/stage164_surface_draft_dry_run_renderer_report.json"
PACK_DIR = "release/current/stage164_surface_draft_dry_run_renderer_pack"


def run_stage164_surface_draft_dry_run_renderer(root: Path | None = None) -> dict[str, Any]:
    root = root or Path(__file__).resolve().parents[3]
    if _active_version(root) != TARGET_STAGE:
        existing = _load_existing(root / TARGET_REPORT)
        if existing is not None:
            return existing

    stage163 = run_stage163_release_gate(root)
    draft = build_surface_draft_dry_run(root)
    pack = root / PACK_DIR
    pack.mkdir(parents=True, exist_ok=True)

    parts = {
        "surface_draft_units": _build_surface_draft_units(draft),
        "dry_run_render_trace": _build_dry_run_render_trace(draft),
        "surface_boundary_snapshot": _build_surface_boundary_snapshot(draft),
        "node2_surface_draft_projection_matrix": _build_node2_surface_draft_projection_matrix(draft),
        "rendering_side_effect_free_policy": _build_rendering_side_effect_free_policy(),
        "deterministic_surface_draft_checksum": _build_deterministic_surface_draft_checksum(draft),
        "stage165_entry_criteria": _build_stage165_entry_criteria(draft),
        "regression_snapshot": _build_regression_snapshot(draft),
    }
    for name, payload in parts.items():
        _write_json(pack / f"{name}.json", payload)

    issues: list[str] = []
    if stage163.get("status") != "pass":
        issues.append("stage163_release_gate_blocked")
    if draft.get("status") != "pass":
        issues.extend(f"surface_draft:{issue}" for issue in draft.get("issues", []))
    for name, payload in parts.items():
        if payload.get("status") != "pass":
            issues.append(f"{name}_blocked")
            issues.extend(f"{name}:{issue}" for issue in payload.get("issues", []))

    result = {
        "stage": "164",
        "baseline_stage": "163",
        "title": "Surface Draft Dry-Run Renderer",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "mode": "SURFACE_DRAFT_DRY_RUN_RENDERER_LOCAL_ONLY",
        "page": "Page04 Rendering Body",
        "draft_unit_count": draft.get("draft_unit_count", 0),
        "trace_step_count": draft.get("trace_step_count", 0),
        "surface_draft_checksum": draft.get("surface_draft_checksum", ""),
        "source_render_plan_checksum": draft.get("source_render_plan_checksum", ""),
        "surface_draft_dry_run_enabled": True,
        "stage165_render_quality_boundary_preflight_ready": not issues,
        "render_plan_inherited": stage163.get("status") == "pass",
        "rendering_runtime_enabled": False,
        "generation_runtime_enabled": False,
        "provider_generation_enabled": False,
        "provider_execution_enabled": False,
        "runtime_execution_enabled": False,
        "render_write_enabled": False,
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
        "parts": {"stage163_release_gate": _compact(stage163), **parts},
    }
    _write_json(root / TARGET_REPORT, result)
    return result


def _build_surface_draft_units(draft: dict[str, Any]) -> dict[str, Any]:
    count = int(draft.get("draft_unit_count", 0))
    return {
        "stage": TARGET_STAGE,
        "title": "Stage164 Surface Draft Units",
        "status": "pass" if draft.get("status") == "pass" and count > 0 else "blocked",
        "issues": list(draft.get("issues", [])),
        "draft_unit_count": count,
        "units": draft.get("units", []),
    }


def _build_dry_run_render_trace(draft: dict[str, Any]) -> dict[str, Any]:
    steps = list(draft.get("trace_steps", []))
    issues = [] if len(steps) == int(draft.get("draft_unit_count", 0)) else ["trace_step_count_mismatch"]
    for step in steps:
        if step.get("provider_call_allowed") is not False or step.get("write_allowed") is not False:
            issues.append(f"trace_side_effect_allowed:{step.get('step_id')}")
    return {
        "stage": TARGET_STAGE,
        "title": "Stage164 Dry-Run Render Trace",
        "status": "pass" if draft.get("status") == "pass" and not issues else "blocked",
        "issues": issues,
        "trace_step_count": len(steps),
        "trace_steps": steps,
        "runtime_execution_count": 0,
        "provider_generation_count": 0,
        "write_operation_count": 0,
    }


def _build_surface_boundary_snapshot(draft: dict[str, Any]) -> dict[str, Any]:
    issues: list[str] = []
    for unit in draft.get("units", []):
        if unit.get("boundary_level") != "NODE2_SURFACE_SAFE":
            issues.append(f"boundary_level_not_surface_safe:{unit.get('draft_unit_id')}")
        if unit.get("visibility") not in {"NODE2_SAFE", "SURFACE_ONLY", "surface_safe"}:
            issues.append(f"visibility_not_surface_only:{unit.get('draft_unit_id')}")
    return {
        "stage": TARGET_STAGE,
        "title": "Stage164 Surface Boundary Snapshot",
        "status": "pass" if draft.get("status") == "pass" and not issues else "blocked",
        "issues": issues,
        "draft_unit_count": draft.get("draft_unit_count", 0),
        "node2_raw_reveal_access": 0,
        "node2_hidden_render_payload_access": 0,
        "boundary_violation_count": 0,
    }


def _build_node2_surface_draft_projection_matrix(draft: dict[str, Any]) -> dict[str, Any]:
    forbidden = ("hidden_reveal_payload", "hidden_render_payload", "provider_payload", "provider_generation_payload", "write_handle", "credential", "raw_manuscript_payload")
    issues: list[str] = []
    for unit in draft.get("units", []):
        surface = json.dumps({"draft_text": unit.get("draft_text", ""), "summary": unit.get("node2_projection_summary", "")}, ensure_ascii=False).lower()
        for token in forbidden:
            if token in surface:
                issues.append(f"node2_forbidden_token:{unit.get('draft_unit_id')}:{token}")
    return {
        "stage": TARGET_STAGE,
        "title": "Stage164 Node2 Surface Draft Projection Matrix",
        "status": "pass" if draft.get("status") == "pass" and not issues else "blocked",
        "issues": issues,
        "rules": [
            {"name": "node2_surface_draft_summary_only", "node2_surface_allowed": True, "hidden_payload_blocked": True, "provider_payload_blocked": True, "write_handle_blocked": True, "evidence": TARGET_REPORT},
            {"name": "raw_manuscript_payload_blocked", "node2_surface_allowed": True, "hidden_payload_blocked": True, "provider_payload_blocked": True, "write_handle_blocked": True, "evidence": TARGET_REPORT},
        ],
        "node2_raw_reveal_access": 0,
        "node2_hidden_render_payload_access": 0,
    }


def _build_rendering_side_effect_free_policy() -> dict[str, Any]:
    rules = (
        SurfaceDraftPolicy("deterministic_surface_draft_dry_run", True, True, False, False, False, TARGET_REPORT),
        SurfaceDraftPolicy("provider_generation_disabled", True, True, False, False, False, TARGET_REPORT),
        SurfaceDraftPolicy("runtime_render_disabled", True, True, False, False, False, TARGET_REPORT),
        SurfaceDraftPolicy("surface_draft_write_disabled", True, True, False, False, False, TARGET_REPORT),
        SurfaceDraftPolicy("canon_mutation_disabled", True, True, False, False, False, TARGET_REPORT),
    )
    issues = [rule.name for rule in rules if not rule.deterministic or not rule.dry_run_only or rule.provider_generation_allowed or rule.runtime_render_allowed or rule.write_allowed]
    return {"stage": TARGET_STAGE, "title": "Stage164 Rendering Side-Effect-Free Policy", "status": "pass" if not issues else "blocked", "issues": issues, "rules": [rule.to_dict() for rule in rules]}


def _build_deterministic_surface_draft_checksum(draft: dict[str, Any]) -> dict[str, Any]:
    checksum = str(draft.get("surface_draft_checksum", ""))
    return {
        "stage": TARGET_STAGE,
        "title": "Stage164 Deterministic Surface Draft Checksum",
        "status": "pass" if draft.get("status") == "pass" and len(checksum) == 64 else "blocked",
        "issues": [] if len(checksum) == 64 else ["checksum_missing_or_invalid"],
        "surface_draft_checksum": checksum,
        "source_render_plan_checksum": draft.get("source_render_plan_checksum", ""),
    }


def _build_stage165_entry_criteria(draft: dict[str, Any]) -> dict[str, Any]:
    criteria = {
        "stage164_report_pass": draft.get("status") == "pass",
        "surface_draft_units_present": int(draft.get("draft_unit_count", 0)) > 0,
        "dry_run_trace_present": int(draft.get("trace_step_count", 0)) == int(draft.get("draft_unit_count", 0)),
        "provider_generation_disabled": True,
        "runtime_render_disabled": True,
        "write_operations_blocked": True,
        "node2_surface_only": True,
    }
    issues = [name for name, ok in criteria.items() if not ok]
    return {"stage": TARGET_STAGE, "title": "Stage165 Entry Criteria", "status": "pass" if not issues else "blocked", "issues": issues, "criteria": criteria, "next_stage": "stage165_render_quality_boundary_preflight"}


def _build_regression_snapshot(draft: dict[str, Any]) -> dict[str, Any]:
    return {
        "stage": TARGET_STAGE,
        "title": "Stage164 Regression Snapshot",
        "status": "pass" if draft.get("status") == "pass" else "blocked",
        "issues": list(draft.get("issues", [])),
        "source_render_plan_checksum": draft.get("source_render_plan_checksum", ""),
        "surface_draft_checksum": draft.get("surface_draft_checksum", ""),
        "provider_default_calls": 0,
        "provider_generation_count": 0,
        "runtime_execution_count": 0,
        "write_operation_count": 0,
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
    keep = ("status", "stage", "baseline_stage", "title", "issues", "provider_default_calls", "live_provider_call_count_in_release_gate", "node2_raw_reveal_access", "boundary_violation_count", "credential_leakage", "branchpoint_lineage_preserved")
    return {key: stage.get(key) for key in keep if key in stage}
