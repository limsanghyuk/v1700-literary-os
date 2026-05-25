from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from v1700.gates.stage163_release_gate import run_stage163_release_gate
from v1700.stage164 import run_stage164

_CACHE: dict[str, dict[str, Any]] = {}


def run_stage164_release_gate(root: Path | None = None) -> dict[str, Any]:
    root = root or Path(__file__).resolve().parents[3]
    key = str(root.resolve())
    if key in _CACHE:
        return _CACHE[key]
    if _active_version(root) != "stage164":
        existing = _load_report(root, "stage164_release_gate_report.json")
        if existing is not None and existing.get("status") == "pass":
            _CACHE[key] = existing
            return existing

    baseline = _baseline_gate(root)
    stage = run_stage164(root)
    parts = stage.get("parts", {})
    units = parts.get("surface_draft_units", {})
    trace = parts.get("dry_run_render_trace", {})
    boundary = parts.get("surface_boundary_snapshot", {})
    projection = parts.get("node2_surface_draft_projection_matrix", {})
    policy = parts.get("rendering_side_effect_free_policy", {})
    checksum = parts.get("deterministic_surface_draft_checksum", {})
    criteria = parts.get("stage165_entry_criteria", {})
    regression = parts.get("regression_snapshot", {})

    checks = {
        "stage163_baseline_gate_pass": _check(baseline.get("status") == "pass"),
        "stage164_report_pass": _check(stage.get("status") == "pass"),
        "surface_draft_dry_run_mode_pass": _check(stage.get("mode") == "SURFACE_DRAFT_DRY_RUN_RENDERER_LOCAL_ONLY"),
        "surface_draft_units_pass": _check(units.get("status") == "pass" and units.get("draft_unit_count", 0) >= 6),
        "dry_run_render_trace_pass": _check(trace.get("status") == "pass" and trace.get("trace_step_count", 0) == stage.get("draft_unit_count")),
        "surface_boundary_snapshot_pass": _check(boundary.get("status") == "pass" and stage.get("boundary_violation_count") == 0),
        "node2_surface_draft_projection_pass": _check(projection.get("status") == "pass" and stage.get("node2_raw_reveal_access") == 0),
        "side_effect_free_policy_pass": _check(policy.get("status") == "pass" and stage.get("surface_draft_write_enabled") is False),
        "deterministic_checksum_pass": _check(checksum.get("status") == "pass" and len(str(stage.get("surface_draft_checksum", ""))) == 64),
        "stage165_entry_criteria_pass": _check(criteria.get("status") == "pass"),
        "regression_snapshot_pass": _check(regression.get("status") == "pass"),
        "runtime_render_disabled": _check(stage.get("rendering_runtime_enabled") is False and stage.get("generation_runtime_enabled") is False),
        "provider_generation_disabled": _check(stage.get("provider_generation_enabled") is False and stage.get("provider_generation_count") == 0),
        "runtime_execution_disabled": _check(stage.get("runtime_execution_enabled") is False and stage.get("runtime_execution_count") == 0),
        "write_operations_blocked": _check(stage.get("render_write_enabled") is False and stage.get("surface_draft_write_enabled") is False and stage.get("write_operation_count") == 0),
        "memory_store_write_blocked": _check(stage.get("memory_write_enabled") is False and stage.get("store_write_enabled") is False),
        "canon_mutation_blocked": _check(stage.get("canon_mutation_enabled") is False and stage.get("canon_auto_resolution_count") == 0),
        "auto_repair_blocked": _check(stage.get("auto_repair_apply_enabled") is False and stage.get("auto_repair_mutation_count") == 0),
        "runtime_training_blocked": _check(stage.get("runtime_training_enabled") is False and stage.get("model_weight_update_count") == 0),
        "provider_zero_pass": _check(stage.get("provider_default_calls") == 0 and stage.get("live_provider_call_count_in_release_gate") == 0),
        "node2_boundary_pass": _check(stage.get("node2_raw_reveal_access") == 0 and stage.get("boundary_violation_count") == 0),
        "raw_manuscript_leakage_zero": _check(stage.get("raw_manuscript_provider_leakage") == 0 and stage.get("raw_manuscript_cross_project_leakage") == 0),
        "credential_leakage_zero_pass": _check(stage.get("credential_leakage") == 0),
        "branchpoint_survival_pass": _check(stage.get("branchpoint_lineage_preserved") is True),
        "docs_manifest_pass": _check(_docs_manifest_ok(root)),
        "procedure_alignment_pass": _check(_procedure_alignment_ok(root)),
    }
    issues = [name for name, value in checks.items() if value["status"] != "pass"]
    result = {
        "stage": "164",
        "baseline_stage": "163",
        "title": "Surface Draft Dry-Run Renderer",
        "status": "pass" if not issues and stage.get("status") == "pass" else "blocked",
        "issues": issues,
        "checks": checks,
        "stage164": _compact(stage),
        "provider_default_calls": 0,
        "live_provider_call_count_in_release_gate": 0,
        "runtime_execution_count": 0,
        "provider_generation_count": 0,
        "write_operation_count": 0,
        "node2_raw_reveal_access": 0,
        "boundary_violation_count": 0,
        "raw_manuscript_provider_leakage": 0,
        "raw_manuscript_cross_project_leakage": 0,
        "credential_leakage": 0,
        "rendering_runtime_enabled": False,
        "generation_runtime_enabled": False,
        "provider_generation_enabled": False,
        "runtime_execution_enabled": False,
        "render_write_enabled": False,
        "surface_draft_write_enabled": False,
        "store_write_enabled": False,
        "memory_write_enabled": False,
        "runtime_training_enabled": False,
        "branchpoint_lineage_preserved": not issues,
    }
    out = root / "release/current/stage164_release_gate_report.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    _CACHE[key] = result
    return result


def _check(condition: bool) -> dict[str, str]:
    return {"status": "pass" if condition else "blocked"}


def _baseline_gate(root: Path) -> dict[str, Any]:
    if _active_version(root) != "stage164":
        report = _load_report(root, "stage163_release_gate_report.json")
        if report is not None and report.get("status") == "pass":
            return report
    return run_stage163_release_gate(root)


def _active_version(root: Path) -> str:
    manifest = root / "manifests/live_core_manifest.json"
    if not manifest.exists():
        return ""
    return json.loads(manifest.read_text(encoding="utf-8")).get("active_version", "")


def _load_report(root: Path, name: str) -> dict[str, Any] | None:
    path = root / "release/current" / name
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def _compact(stage: dict[str, Any]) -> dict[str, Any]:
    keep = ("status", "stage", "baseline_stage", "title", "issues", "mode", "draft_unit_count", "trace_step_count", "surface_draft_checksum", "stage165_render_quality_boundary_preflight_ready", "render_plan_inherited", "rendering_runtime_enabled", "generation_runtime_enabled", "provider_generation_enabled", "runtime_execution_enabled", "provider_execution_enabled", "memory_write_enabled", "render_write_enabled", "store_write_enabled", "surface_draft_write_enabled", "canon_mutation_enabled", "auto_repair_apply_enabled", "runtime_training_enabled", "model_weight_update_count", "canon_auto_resolution_count", "auto_repair_mutation_count", "provider_default_calls", "live_provider_call_count_in_release_gate", "node2_raw_reveal_access", "boundary_violation_count", "raw_manuscript_provider_leakage", "raw_manuscript_cross_project_leakage", "credential_leakage", "branchpoint_lineage_preserved")
    return {key: stage.get(key) for key in keep if key in stage}


def _docs_manifest_ok(root: Path) -> bool:
    return all((root / rel).exists() for rel in [
        "docs/stages/stage164.md",
        "docs/proposals/stage164_surface_draft_dry_run_renderer_proposal.md",
        "docs/architecture/stage164_surface_draft_dry_run_renderer_blueprint.md",
        "docs/development/stage164_developer_handoff.md",
        "docs/architecture/page04_rendering_body_blueprint.md",
        "docs/proposals/page04_rendering_body_proposal.md",
        "docs/development/page04_handoff.md",
        "docs/development/MANDATORY_PRE_DEVELOPMENT_PROTOCOL.md",
        "docs/workflow/PREFLIGHT_GUIDE_v1.1_STAGE160.md",
        "docs/workflow/BRANCH_STRATEGY.md",
        "manifests/stage164_manifest.json",
        "manifests/stage164_surface_draft_dry_run_renderer_manifest.json",
        "manifests/stage164_branchpoint_trace_manifest.json",
        "manifests/live_core_stage164_overlay.json",
        "release/current/stage164_release_asset_manifest.json",
        "release/current/stage164_surface_draft_dry_run_renderer_report.json",
        "release/current/stage164_release_gate_report.json",
        "release/current/stage164_surface_draft_dry_run_renderer_pack/surface_draft_units.json",
        "release/current/stage164_surface_draft_dry_run_renderer_pack/dry_run_render_trace.json",
        "release/current/stage164_surface_draft_dry_run_renderer_pack/surface_boundary_snapshot.json",
        "release/current/stage164_surface_draft_dry_run_renderer_pack/node2_surface_draft_projection_matrix.json",
        "release/current/stage164_surface_draft_dry_run_renderer_pack/rendering_side_effect_free_policy.json",
        "release/current/stage164_surface_draft_dry_run_renderer_pack/deterministic_surface_draft_checksum.json",
        "release/current/stage164_surface_draft_dry_run_renderer_pack/stage165_entry_criteria.json",
        "release/current/stage164_surface_draft_dry_run_renderer_pack/regression_snapshot.json",
    ])


def _procedure_alignment_ok(root: Path) -> bool:
    targets = [root / "README.md", root / "RELEASE_NOTES.md", root / "package_manifest.json"]
    if not all(path.exists() for path in targets):
        return False
    contents = "\n".join(path.read_text(encoding="utf-8") for path in targets)
    return all(token in contents for token in ["stage164", "run_stage164_surface_draft_dry_run_renderer.py", "run_stage164_release_gate.py"])
