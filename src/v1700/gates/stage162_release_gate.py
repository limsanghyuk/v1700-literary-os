from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from v1700.gates.stage161_release_gate import run_stage161_release_gate
from v1700.stage162 import run_stage162

_CACHE: dict[str, dict[str, Any]] = {}


def run_stage162_release_gate(root: Path | None = None) -> dict[str, Any]:
    root = root or Path(__file__).resolve().parents[3]
    key = str(root.resolve())
    if key in _CACHE:
        return _CACHE[key]
    if _active_version(root) != "stage162":
        existing = _load_report(root, "stage162_release_gate_report.json")
        if existing is not None and existing.get("status") == "pass":
            _CACHE[key] = existing
            return existing

    baseline = _baseline_gate(root)
    stage = run_stage162(root)
    parts = stage.get("parts", {})
    catalog = parts.get("render_packet_store_catalog", {})
    schema = parts.get("render_packet_schema_validation", {})
    checksum = parts.get("render_packet_checksum_index", {})
    policy = parts.get("read_only_render_access_policy", {})
    node2 = parts.get("node2_render_packet_projection_matrix", {})
    lineage = parts.get("render_packet_lineage_matrix", {})
    regression = parts.get("regression_snapshot", {})

    checks = {
        "stage161_baseline_gate_pass": _check(baseline.get("status") == "pass"),
        "stage162_report_pass": _check(stage.get("status") == "pass"),
        "render_packet_store_mode_pass": _check(stage.get("mode") == "LOCAL_RENDER_PACKET_STORE_READ_ONLY" and stage.get("read_only_store_enabled") is True),
        "render_packet_catalog_pass": _check(catalog.get("status") == "pass" and catalog.get("render_packet_count", 0) >= 6),
        "render_packet_schema_validation_pass": _check(schema.get("status") == "pass"),
        "render_packet_checksum_index_pass": _check(checksum.get("status") == "pass" and checksum.get("checksum_count", 0) >= 6),
        "read_only_render_access_policy_pass": _check(policy.get("status") == "pass" and stage.get("store_write_enabled") is False),
        "node2_render_projection_pass": _check(node2.get("status") == "pass" and stage.get("node2_raw_reveal_access") == 0),
        "render_packet_lineage_pass": _check(lineage.get("status") == "pass" and lineage.get("entry_count", 0) >= 6),
        "regression_snapshot_pass": _check(regression.get("status") == "pass"),
        "rendering_runtime_disabled": _check(stage.get("rendering_runtime_enabled") is False and stage.get("generation_runtime_enabled") is False),
        "provider_generation_disabled": _check(stage.get("provider_generation_enabled") is False and stage.get("provider_generation_count") == 0),
        "runtime_execution_disabled": _check(stage.get("runtime_execution_enabled") is False and stage.get("runtime_execution_count") == 0),
        "write_operations_blocked": _check(stage.get("render_write_enabled") is False and stage.get("write_operation_count") == 0 and stage.get("store_write_enabled") is False),
        "memory_execution_write_blocked": _check(stage.get("memory_write_enabled") is False and stage.get("execution_write_enabled") is False),
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
        "stage": "162",
        "baseline_stage": "161",
        "title": "Local Render Packet Store",
        "status": "pass" if not issues and stage.get("status") == "pass" else "blocked",
        "issues": issues,
        "checks": checks,
        "stage162": _compact(stage),
        "provider_default_calls": 0,
        "live_provider_call_count_in_release_gate": 0,
        "runtime_execution_count": 0,
        "provider_execution_count": 0,
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
        "store_write_enabled": False,
        "memory_write_enabled": False,
        "runtime_training_enabled": False,
        "branchpoint_lineage_preserved": not issues,
    }
    out = root / "release/current/stage162_release_gate_report.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    _CACHE[key] = result
    return result


def _check(condition: bool) -> dict[str, str]:
    return {"status": "pass" if condition else "blocked"}


def _baseline_gate(root: Path) -> dict[str, Any]:
    if _active_version(root) != "stage162":
        report = _load_report(root, "stage161_release_gate_report.json")
        if report is not None and report.get("status") == "pass":
            return report
    return run_stage161_release_gate(root)


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
    keep = ("status", "stage", "baseline_stage", "title", "issues", "mode", "render_packet_count", "checksum_count", "read_only_store_enabled", "render_packet_store_enabled", "rendering_contract_inherited", "stage163_render_plan_builder_ready", "rendering_runtime_enabled", "generation_runtime_enabled", "provider_generation_enabled", "runtime_execution_enabled", "provider_execution_enabled", "memory_write_enabled", "render_write_enabled", "store_write_enabled", "canon_mutation_enabled", "auto_repair_apply_enabled", "runtime_training_enabled", "model_weight_update_count", "canon_auto_resolution_count", "auto_repair_mutation_count", "provider_default_calls", "live_provider_call_count_in_release_gate", "node2_raw_reveal_access", "boundary_violation_count", "raw_manuscript_provider_leakage", "raw_manuscript_cross_project_leakage", "credential_leakage", "branchpoint_lineage_preserved")
    return {key: stage.get(key) for key in keep if key in stage}


def _docs_manifest_ok(root: Path) -> bool:
    return all((root / rel).exists() for rel in [
        "docs/stages/stage162.md",
        "docs/proposals/stage162_local_render_packet_store_proposal.md",
        "docs/architecture/stage162_local_render_packet_store_blueprint.md",
        "docs/development/stage162_developer_handoff.md",
        "docs/proposals/page04_rendering_body_proposal.md",
        "docs/architecture/page04_rendering_body_blueprint.md",
        "docs/development/page04_handoff.md",
        "docs/development/MANDATORY_PRE_DEVELOPMENT_PROTOCOL.md",
        "docs/workflow/PREFLIGHT_GUIDE_v1.1_STAGE160.md",
        "docs/workflow/BRANCH_STRATEGY.md",
        "manifests/stage162_manifest.json",
        "manifests/stage162_local_render_packet_store_manifest.json",
        "manifests/stage162_branchpoint_trace_manifest.json",
        "manifests/live_core_stage162_overlay.json",
        "release/current/stage162_local_render_packet_store_report.json",
        "release/current/stage162_release_gate_report.json",
        "release/current/stage162_local_render_packet_store_pack/render_packet_store_catalog.json",
        "release/current/stage162_local_render_packet_store_pack/render_packet_schema_validation.json",
        "release/current/stage162_local_render_packet_store_pack/render_packet_checksum_index.json",
        "release/current/stage162_local_render_packet_store_pack/read_only_render_access_policy.json",
        "release/current/stage162_local_render_packet_store_pack/node2_render_packet_projection_matrix.json",
        "release/current/stage162_local_render_packet_store_pack/render_packet_lineage_matrix.json",
        "release/current/stage162_local_render_packet_store_pack/regression_snapshot.json",
    ])


def _procedure_alignment_ok(root: Path) -> bool:
    targets = [root / "README.md", root / "RELEASE_NOTES.md", root / "package_manifest.json"]
    if not all(path.exists() for path in targets):
        return False
    contents = "\n".join(path.read_text(encoding="utf-8") for path in targets)
    return all(token in contents for token in ["stage162", "run_stage162_local_render_packet_store.py", "run_stage162_release_gate.py"])
