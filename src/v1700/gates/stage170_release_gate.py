from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from v1700.gates.stage169_release_gate import run_stage169_release_gate
from v1700.stage170 import run_stage170


def run_stage170_release_gate(root: Path | None = None) -> dict[str, Any]:
    root = root or Path(__file__).resolve().parents[3]
    if _active_version(root) != "stage170":
        existing = _load_report(root, "stage170_release_gate_report.json")
        if existing is not None and existing.get("status") == "pass":
            return existing

    baseline = _baseline_gate(root)
    stage = run_stage170(root)
    parts = stage.get("parts", {})
    fixture_catalog = parts.get("negative_fixture_catalog", {})
    fixture_results = parts.get("negative_fixture_results", {})
    coverage = parts.get("fixture_coverage_matrix", {})
    regression = parts.get("regression_snapshot", {})
    determinism = parts.get("fixture_replay_determinism", {})
    boundary = parts.get("boundary_negative_fixture_matrix", {})
    entry = parts.get("stage171_entry_criteria", {})

    checks = {
        "stage169_baseline_gate_pass": _check(baseline.get("status") == "pass"),
        "stage170_report_pass": _check(stage.get("status") == "pass"),
        "regression_harness_mode_pass": _check(stage.get("mode") == "DETERMINISTIC_LOCAL_REGRESSION_HARNESS_ONLY"),
        "fixture_catalog_pass": _check(fixture_catalog.get("status") == "pass" and fixture_catalog.get("fixture_count", 0) >= 9),
        "safe_fixture_pass": _check(fixture_results.get("safe_fixture_pass") is True),
        "negative_fixture_blocks_pass": _check(fixture_results.get("negative_fixture_blocks") is True),
        "fixture_coverage_pass": _check(coverage.get("status") == "pass"),
        "regression_snapshot_pass": _check(regression.get("status") == "pass" and stage.get("regression_snapshot_pass") is True),
        "fixture_determinism_pass": _check(determinism.get("status") == "pass" and stage.get("determinism_channel_pass") is True),
        "boundary_negative_fixture_pass": _check(boundary.get("status") == "pass" and stage.get("boundary_fixture_pass") is True),
        "stage171_entry_ready": _check(entry.get("status") == "pass" and stage.get("stage171_boundary_preflight_ready") is True),
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
        "stage": "170",
        "baseline_stage": "169",
        "title": "Regression and Negative Fixture Harness",
        "status": "pass" if not issues and stage.get("status") == "pass" else "blocked",
        "issues": issues,
        "checks": checks,
        "stage170": _compact(stage),
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
    out = root / "release/current/stage170_release_gate_report.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return result


def _check(condition: bool) -> dict[str, str]:
    return {"status": "pass" if condition else "blocked"}


def _baseline_gate(root: Path) -> dict[str, Any]:
    if _active_version(root) != "stage170":
        report = _load_report(root, "stage169_release_gate_report.json")
        if report is not None and report.get("status") == "pass":
            return report
    return run_stage169_release_gate(root)


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
        "status", "stage", "baseline_stage", "title", "issues", "mode", "fixture_count",
        "negative_fixture_count", "safe_fixture_pass", "negative_fixture_blocks", "regression_snapshot_pass",
        "fixture_coverage_pass", "boundary_fixture_pass", "determinism_channel_pass",
        "stage171_boundary_preflight_ready", "provider_evaluation_enabled", "evaluation_write_enabled",
        "memory_write_enabled", "cross_project_write_enabled", "canon_mutation_enabled", "runtime_training_enabled",
        "auto_repair_apply_enabled", "provider_default_calls", "node2_raw_reveal_access", "boundary_violation_count",
        "credential_leakage", "branchpoint_lineage_preserved",
    )
    return {key: stage.get(key) for key in keep if key in stage}


def _docs_manifest_ok(root: Path) -> bool:
    generated = {"release/current/stage170_release_gate_report.json"}
    required = [
        "docs/stages/stage170.md",
        "docs/proposals/stage170_regression_negative_fixture_harness_proposal.md",
        "docs/architecture/stage170_regression_negative_fixture_harness_blueprint.md",
        "docs/development/stage170_developer_handoff.md",
        "docs/proposals/page05_evaluation_body_proposal.md",
        "docs/architecture/page05_evaluation_body_blueprint.md",
        "docs/development/page05_developer_handoff.md",
        "manifests/stage170_manifest.json",
        "manifests/stage170_regression_negative_fixture_harness_manifest.json",
        "manifests/stage170_branchpoint_trace_manifest.json",
        "manifests/live_core_stage170_overlay.json",
        "release/current/stage170_release_asset_manifest.json",
        "release/current/stage170_regression_negative_fixture_harness_report.json",
        "release/current/stage170_release_gate_report.json",
        "release/current/stage170_regression_negative_fixture_harness_pack/negative_fixture_catalog.json",
        "release/current/stage170_regression_negative_fixture_harness_pack/negative_fixture_results.json",
        "release/current/stage170_regression_negative_fixture_harness_pack/fixture_coverage_matrix.json",
        "release/current/stage170_regression_negative_fixture_harness_pack/regression_snapshot.json",
        "release/current/stage170_regression_negative_fixture_harness_pack/fixture_replay_determinism.json",
        "release/current/stage170_regression_negative_fixture_harness_pack/boundary_negative_fixture_matrix.json",
        "release/current/stage170_regression_negative_fixture_harness_pack/stage171_entry_criteria.json",
    ]
    return all((root / rel).exists() or rel in generated for rel in required)


def _procedure_alignment_ok(root: Path) -> bool:
    targets = [root / "README.md", root / "RELEASE_NOTES.md", root / "package_manifest.json"]
    text = "\n".join(path.read_text(encoding="utf-8") for path in targets if path.exists())
    return "Stage170" in text and "Regression and Negative Fixture Harness" in text and "stage171" in text.lower()
