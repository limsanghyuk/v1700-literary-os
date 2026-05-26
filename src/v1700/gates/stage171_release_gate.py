from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from v1700.gates.stage170_release_gate import run_stage170_release_gate
from v1700.stage171 import run_stage171


def run_stage171_release_gate(root: Path | None = None) -> dict[str, Any]:
    root = root or Path(__file__).resolve().parents[3]
    if _active_version(root) != "stage171":
        existing = _load_report(root, "stage171_release_gate_report.json")
        if existing is not None and existing.get("status") == "pass":
            return existing

    baseline = _baseline_gate(root)
    stage = run_stage171(root)
    parts = stage.get("parts", {})
    inherited = parts.get("inherited_stage_gate_matrix", {})
    invariant = parts.get("boundary_invariant_matrix", {})
    node2_scan = parts.get("node2_surface_projection_scan", {})
    forbidden_ops = parts.get("forbidden_operation_registry", {})
    quarantine = parts.get("controlled_negative_fixture_quarantine", {})
    leakage = parts.get("leakage_zero_snapshot", {})
    entry = parts.get("stage172_entry_criteria", {})

    checks = {
        "stage170_baseline_gate_pass": _check(baseline.get("status") == "pass"),
        "stage171_report_pass": _check(stage.get("status") == "pass"),
        "boundary_preflight_mode_pass": _check(stage.get("mode") == "DETERMINISTIC_LOCAL_BOUNDARY_PREFLIGHT_ONLY"),
        "inherited_stage_gate_matrix_pass": _check(inherited.get("status") == "pass"),
        "boundary_invariant_matrix_pass": _check(invariant.get("status") == "pass" and stage.get("boundary_invariant_freeze_pass") is True),
        "node2_projection_scan_pass": _check(node2_scan.get("status") == "pass" and stage.get("node2_surface_projection_scan_pass") is True),
        "forbidden_operation_registry_pass": _check(forbidden_ops.get("status") == "pass"),
        "controlled_negative_fixture_quarantine_pass": _check(quarantine.get("status") == "pass" and stage.get("controlled_negative_fixture_quarantine_pass") is True),
        "leakage_zero_snapshot_pass": _check(leakage.get("status") == "pass" and stage.get("leakage_zero_snapshot_pass") is True),
        "stage172_entry_ready": _check(entry.get("status") == "pass" and stage.get("stage172_page05_release_seal_ready") is True),
        "provider_evaluation_disabled": _check(stage.get("provider_evaluation_enabled") is False and stage.get("provider_default_calls") == 0),
        "runtime_execution_disabled": _check(stage.get("runtime_execution_enabled") is False and stage.get("runtime_execution_count") == 0),
        "write_operations_blocked": _check(stage.get("evaluation_write_enabled") is False and stage.get("write_operation_count") == 0),
        "memory_write_blocked": _check(stage.get("memory_write_enabled") is False and stage.get("cross_project_write_enabled") is False),
        "canon_mutation_blocked": _check(stage.get("canon_mutation_enabled") is False),
        "runtime_training_blocked": _check(stage.get("runtime_training_enabled") is False and stage.get("auto_repair_apply_enabled") is False),
        "node2_boundary_pass": _check(stage.get("node2_raw_reveal_access") == 0 and stage.get("boundary_violation_count") == 0),
        "raw_manuscript_leakage_zero": _check(stage.get("raw_manuscript_provider_leakage") == 0 and stage.get("raw_manuscript_cross_project_leakage") == 0),
        "credential_leakage_zero_pass": _check(stage.get("credential_leakage") == 0),
        "branchpoint_survival_pass": _check(stage.get("branchpoint_lineage_preserved") is True),
        "docs_manifest_pass": _check(_docs_manifest_ok(root)),
        "procedure_alignment_pass": _check(_procedure_alignment_ok(root)),
    }
    issues = [name for name, value in checks.items() if value["status"] != "pass"]
    result = {
        "stage": "171",
        "baseline_stage": "170",
        "title": "Evaluation Boundary and Leakage Preflight",
        "status": "pass" if not issues and stage.get("status") == "pass" else "blocked",
        "issues": issues,
        "checks": checks,
        "stage171": _compact(stage),
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
        "provider_evaluation_enabled": False,
        "evaluation_write_enabled": False,
        "memory_write_enabled": False,
        "cross_project_write_enabled": False,
        "canon_mutation_enabled": False,
        "runtime_training_enabled": False,
        "auto_repair_apply_enabled": False,
        "branchpoint_lineage_preserved": not issues,
    }
    out = root / "release/current/stage171_release_gate_report.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return result


def _check(condition: bool) -> dict[str, str]:
    return {"status": "pass" if condition else "blocked"}


def _baseline_gate(root: Path) -> dict[str, Any]:
    if _active_version(root) != "stage171":
        report = _load_report(root, "stage170_release_gate_report.json")
        if report is not None and report.get("status") == "pass":
            return report
    return run_stage170_release_gate(root)


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
    keep = (
        "status", "stage", "baseline_stage", "title", "issues", "mode", "stage170_regression_harness_inherited",
        "boundary_invariant_freeze_pass", "node2_surface_projection_scan_pass", "controlled_negative_fixture_quarantine_pass",
        "leakage_zero_snapshot_pass", "stage172_page05_release_seal_ready", "provider_evaluation_enabled", "evaluation_write_enabled",
        "memory_write_enabled", "cross_project_write_enabled", "canon_mutation_enabled", "runtime_training_enabled",
        "auto_repair_apply_enabled", "provider_default_calls", "node2_raw_reveal_access", "boundary_violation_count",
        "credential_leakage", "branchpoint_lineage_preserved",
    )
    return {key: stage.get(key) for key in keep if key in stage}


def _docs_manifest_ok(root: Path) -> bool:
    generated = {"release/current/stage171_release_gate_report.json"}
    required = [
        "docs/stages/stage171.md",
        "docs/proposals/stage171_evaluation_boundary_leakage_preflight_proposal.md",
        "docs/architecture/stage171_evaluation_boundary_leakage_preflight_blueprint.md",
        "docs/development/stage171_developer_handoff.md",
        "docs/proposals/page05_evaluation_body_proposal.md",
        "docs/architecture/page05_evaluation_body_blueprint.md",
        "docs/development/page05_developer_handoff.md",
        "manifests/stage171_manifest.json",
        "manifests/stage171_evaluation_boundary_leakage_preflight_manifest.json",
        "manifests/stage171_branchpoint_trace_manifest.json",
        "manifests/live_core_stage171_overlay.json",
        "release/current/stage171_release_asset_manifest.json",
        "release/current/stage171_evaluation_boundary_leakage_preflight_report.json",
        "release/current/stage171_release_gate_report.json",
        "release/current/stage171_evaluation_boundary_leakage_preflight_pack/inherited_stage_gate_matrix.json",
        "release/current/stage171_evaluation_boundary_leakage_preflight_pack/boundary_invariant_matrix.json",
        "release/current/stage171_evaluation_boundary_leakage_preflight_pack/node2_surface_projection_scan.json",
        "release/current/stage171_evaluation_boundary_leakage_preflight_pack/forbidden_operation_registry.json",
        "release/current/stage171_evaluation_boundary_leakage_preflight_pack/controlled_negative_fixture_quarantine.json",
        "release/current/stage171_evaluation_boundary_leakage_preflight_pack/leakage_zero_snapshot.json",
        "release/current/stage171_evaluation_boundary_leakage_preflight_pack/stage172_entry_criteria.json",
    ]
    return all((root / rel).exists() or rel in generated for rel in required)


def _procedure_alignment_ok(root: Path) -> bool:
    targets = [root / "README.md", root / "RELEASE_NOTES.md", root / "package_manifest.json"]
    text = "\n".join(path.read_text(encoding="utf-8") for path in targets if path.exists())
    return "Stage171" in text and "Evaluation Boundary and Leakage Preflight" in text and "stage172" in text.lower()
