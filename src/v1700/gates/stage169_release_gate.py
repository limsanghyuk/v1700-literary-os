from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from v1700.gates.stage168_release_gate import run_stage168_release_gate
from v1700.stage169 import run_stage169


def run_stage169_release_gate(root: Path | None = None) -> dict[str, Any]:
    root = root or Path(__file__).resolve().parents[3]
    if _active_version(root) != "stage169":
        existing = _load_report(root, "stage169_release_gate_report.json")
        if existing is not None and existing.get("status") == "pass":
            return existing

    baseline = _baseline_gate(root)
    stage = run_stage169(root)
    parts = stage.get("parts", {})
    metric_matrix = parts.get("evaluation_metric_matrix", {})
    scorecard = parts.get("quality_continuity_scorecard", {})
    continuity = parts.get("continuity_violation_matrix", {})
    boundary = parts.get("boundary_override_matrix", {})
    regression = parts.get("regression_delta_matrix", {})
    node2 = parts.get("node2_evaluation_projection_verdict", {})
    determinism = parts.get("determinism_matrix", {})
    entry = parts.get("stage170_entry_criteria", {})

    checks = {
        "stage168_baseline_gate_pass": _check(baseline.get("status") == "pass"),
        "stage169_report_pass": _check(stage.get("status") == "pass"),
        "deterministic_evaluator_mode_pass": _check(stage.get("mode") == "DETERMINISTIC_LOCAL_EVALUATOR_ONLY"),
        "evaluation_metric_matrix_pass": _check(metric_matrix.get("status") == "pass"),
        "quality_channel_pass": _check(scorecard.get("status") == "pass" and stage.get("quality_channel_pass") is True),
        "continuity_channel_pass": _check(continuity.get("status") == "pass" and stage.get("continuity_channel_pass") is True),
        "regression_channel_pass": _check(regression.get("status") == "pass" and stage.get("regression_channel_pass") is True),
        "boundary_override_pass": _check(boundary.get("status") == "pass" and boundary.get("score_can_override_boundary") is False),
        "node2_projection_pass": _check(node2.get("status") == "pass" and stage.get("node2_raw_reveal_access") == 0),
        "determinism_channel_pass": _check(determinism.get("status") == "pass" and stage.get("determinism_channel_pass") is True),
        "stage170_entry_ready": _check(entry.get("status") == "pass" and stage.get("stage170_regression_harness_ready") is True),
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
        "stage": "169",
        "baseline_stage": "168",
        "title": "Deterministic Quality and Continuity Evaluator",
        "status": "pass" if not issues and stage.get("status") == "pass" else "blocked",
        "issues": issues,
        "checks": checks,
        "stage169": _compact(stage),
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
        "runtime_training_enabled": False,
        "branchpoint_lineage_preserved": not issues,
    }
    out = root / "release/current/stage169_release_gate_report.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return result


def _check(condition: bool) -> dict[str, str]:
    return {"status": "pass" if condition else "blocked"}


def _baseline_gate(root: Path) -> dict[str, Any]:
    if _active_version(root) != "stage169":
        report = _load_report(root, "stage168_release_gate_report.json")
        if report is not None and report.get("status") == "pass":
            return report
    return run_stage168_release_gate(root)


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
        "status",
        "stage",
        "baseline_stage",
        "title",
        "issues",
        "mode",
        "evaluation_packet_count",
        "scorecard_count",
        "quality_channel_pass",
        "continuity_channel_pass",
        "regression_channel_pass",
        "boundary_channel_pass",
        "determinism_channel_pass",
        "stage170_regression_harness_ready",
        "provider_evaluation_enabled",
        "evaluation_write_enabled",
        "memory_write_enabled",
        "cross_project_write_enabled",
        "canon_mutation_enabled",
        "runtime_training_enabled",
        "auto_repair_apply_enabled",
        "provider_default_calls",
        "node2_raw_reveal_access",
        "boundary_violation_count",
        "credential_leakage",
        "branchpoint_lineage_preserved",
    )
    return {key: stage.get(key) for key in keep if key in stage}


def _docs_manifest_ok(root: Path) -> bool:
    generated = {"release/current/stage169_release_gate_report.json"}
    required = [
        "docs/stages/stage169.md",
        "docs/proposals/stage169_deterministic_quality_continuity_evaluator_proposal.md",
        "docs/architecture/stage169_deterministic_quality_continuity_evaluator_blueprint.md",
        "docs/development/stage169_developer_handoff.md",
        "docs/proposals/page05_evaluation_body_proposal.md",
        "docs/architecture/page05_evaluation_body_blueprint.md",
        "docs/development/page05_developer_handoff.md",
        "docs/development/MANDATORY_PRE_DEVELOPMENT_PROTOCOL.md",
        "manifests/stage169_manifest.json",
        "manifests/stage169_deterministic_quality_continuity_evaluator_manifest.json",
        "manifests/stage169_branchpoint_trace_manifest.json",
        "manifests/live_core_stage169_overlay.json",
        "release/current/stage169_release_asset_manifest.json",
        "release/current/stage169_deterministic_quality_continuity_evaluator_report.json",
        "release/current/stage169_release_gate_report.json",
        "release/current/stage169_deterministic_quality_continuity_evaluator_pack/evaluation_metric_matrix.json",
        "release/current/stage169_deterministic_quality_continuity_evaluator_pack/quality_continuity_scorecard.json",
        "release/current/stage169_deterministic_quality_continuity_evaluator_pack/continuity_violation_matrix.json",
        "release/current/stage169_deterministic_quality_continuity_evaluator_pack/boundary_override_matrix.json",
        "release/current/stage169_deterministic_quality_continuity_evaluator_pack/regression_delta_matrix.json",
        "release/current/stage169_deterministic_quality_continuity_evaluator_pack/node2_evaluation_projection_verdict.json",
        "release/current/stage169_deterministic_quality_continuity_evaluator_pack/determinism_matrix.json",
        "release/current/stage169_deterministic_quality_continuity_evaluator_pack/stage170_entry_criteria.json",
    ]
    return all((root / rel).exists() or rel in generated for rel in required)


def _procedure_alignment_ok(root: Path) -> bool:
    targets = [root / "README.md", root / "RELEASE_NOTES.md", root / "package_manifest.json"]
    text = "\n".join(path.read_text(encoding="utf-8") for path in targets if path.exists())
    return "Stage169" in text and "Deterministic Quality and Continuity Evaluator" in text and "stage170" in text.lower()
