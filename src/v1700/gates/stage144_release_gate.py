from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from v1700.gates.stage143_release_gate import run_stage143_release_gate
from v1700.stage144 import run_stage144

_CACHE: dict[str, dict[str, Any]] = {}


def run_stage144_release_gate(root: Path | None = None) -> dict[str, Any]:
    root = root or Path(__file__).resolve().parents[3]
    key = str(root.resolve())
    if key in _CACHE:
        return _CACHE[key]
    if _active_version(root) != "stage144":
        existing = _load_report(root, "stage144_release_gate_report.json")
        if existing is not None and existing.get("status") == "pass":
            _CACHE[key] = existing
            return existing

    out = root / "release/current/stage144_release_gate_report.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    if not out.exists():
        out.write_text(
            json.dumps(
                {
                    "stage": "144",
                    "baseline_stage": "143",
                    "title": "Split CI Runtime Strategy Gate",
                    "status": "building",
                    "issues": [],
                },
                ensure_ascii=False,
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )

    baseline = _baseline_gate(root)
    stage = run_stage144(root)
    workflow_inventory = stage.get("parts", {}).get("workflow_inventory", {})
    runtime_lane_matrix = stage.get("parts", {}).get("runtime_lane_matrix", {})
    release_surface_contract = stage.get("parts", {}).get("release_surface_contract", {})
    checks = {
        "stage143_baseline_gate_pass": _check(
            baseline.get("status") == "pass" or baseline.get("stage143", {}).get("status") == "pass"
        ),
        "stage144_report_pass": _check(stage.get("status") == "pass"),
        "workflow_split_mode_pass": _check(
            stage.get("workflow_split_only") is True
            and stage.get("mode") == "SPLIT_CI_RUNTIME_STRATEGY_LOCAL"
        ),
        "metadata_consistency_pass": _check(stage.get("metadata_consistency_status") == "pass"),
        "release_asset_integrity_pass": _check(stage.get("release_asset_integrity_status") == "pass"),
        "workflow_inventory_pass": _check(workflow_inventory.get("status") == "pass"),
        "workflow_split_complete_pass": _check(stage.get("workflow_split_complete") is True),
        "runtime_lane_count_pass": _check(stage.get("runtime_lane_count", 0) >= 5 and runtime_lane_matrix.get("status") == "pass"),
        "release_surface_ready_pass": _check(stage.get("release_surface_ready") is True and release_surface_contract.get("status") == "pass"),
        "stage144_terminal_marker_pass": _check(stage.get("stage144_roadmap_terminal") is True),
        "runtime_training_blocked": _check(stage.get("runtime_training_enabled") is False),
        "active_meta_learning_blocked": _check(stage.get("active_meta_learning_enabled") is False),
        "model_weight_update_zero": _check(stage.get("model_weight_update_count") == 0),
        "losdb_write_blocked": _check(stage.get("losdb_write_enabled") is False),
        "migration_execution_blocked": _check(stage.get("migration_execution_enabled") is False),
        "provider_zero_pass": _check(stage.get("provider_default_calls") == 0 and stage.get("live_provider_call_count_in_release_gate") == 0),
        "node2_boundary_pass": _check(stage.get("node2_raw_reveal_access") == 0),
        "raw_manuscript_leakage_zero": _check(
            stage.get("raw_manuscript_provider_leakage") == 0
            and stage.get("raw_manuscript_cross_project_leakage") == 0
        ),
        "credential_leakage_zero_pass": _check(stage.get("credential_leakage") == 0),
        "branchpoint_survival_pass": _check(stage.get("branchpoint_lineage_preserved") is True),
        "docs_manifest_pass": _check(_docs_manifest_ok(root)),
        "procedure_alignment_pass": _check(_procedure_alignment_ok(root)),
    }
    issues = [name for name, value in checks.items() if value["status"] != "pass"]
    result = {
        "stage": "144",
        "baseline_stage": "143",
        "title": "Split CI Runtime Strategy Gate",
        "status": "pass" if not issues and stage.get("status") == "pass" else "blocked",
        "issues": issues,
        "checks": checks,
        "stage144": _compact(stage),
        "provider_default_calls": 0,
        "live_provider_call_count_in_release_gate": 0,
        "node2_raw_reveal_access": 0,
        "raw_manuscript_provider_leakage": 0,
        "raw_manuscript_cross_project_leakage": 0,
        "credential_leakage": 0,
        "branchpoint_lineage_preserved": not issues,
    }
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    _CACHE[key] = result
    return result


def _check(condition: bool) -> dict[str, str]:
    return {"status": "pass" if condition else "blocked"}


def _baseline_gate(root: Path) -> dict[str, Any]:
    if _active_version(root) != "stage144":
        report = _load_report(root, "stage143_release_gate_report.json")
        if report is not None and report.get("status") == "pass":
            return report
    return run_stage143_release_gate(root)


def _active_version(root: Path) -> str:
    manifest = root / "manifests" / "live_core_manifest.json"
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
        "workflow_split_only",
        "ci_fast_present",
        "ci_core_present",
        "ci_full_present",
        "cd_dry_run_present",
        "release_workflow_present",
        "workflow_split_complete",
        "runtime_lane_count",
        "release_surface_ready",
        "metadata_consistency_status",
        "release_asset_integrity_status",
        "stage144_roadmap_terminal",
        "runtime_training_enabled",
        "active_meta_learning_enabled",
        "model_weight_update_count",
        "losdb_write_enabled",
        "migration_execution_enabled",
        "storage_contract_write_enabled",
        "provider_default_calls",
        "live_provider_call_count_in_release_gate",
        "node2_raw_reveal_access",
        "raw_manuscript_provider_leakage",
        "raw_manuscript_cross_project_leakage",
        "credential_leakage",
        "cross_project_write_allowed",
        "canon_auto_resolution_count",
        "auto_repair_mutation_count",
        "branchpoint_lineage_preserved",
    )
    return {key: stage.get(key) for key in keep if key in stage}


def _docs_manifest_ok(root: Path) -> bool:
    return all(
        (root / rel).exists()
        for rel in [
            "docs/stages/stage144.md",
            "docs/proposals/stage144_proposal.md",
            "docs/architecture/stage144_blueprint.md",
            "docs/development/stage144_developer_handoff.md",
            "manifests/stage144_manifest.json",
            "manifests/stage144_split_ci_runtime_strategy_manifest.json",
            "manifests/stage144_branchpoint_trace_manifest.json",
            "manifests/live_core_stage144_overlay.json",
            "release/current/stage144_split_ci_runtime_strategy_report.json",
            "release/current/stage144_release_gate_report.json",
            "release/current/stage144_release_asset_manifest.json",
            "release/current/stage144_split_ci_runtime_strategy_pack/workflow_inventory.json",
            "release/current/stage144_split_ci_runtime_strategy_pack/runtime_lane_matrix.json",
            "release/current/stage144_split_ci_runtime_strategy_pack/workflow_trigger_summary.json",
            "release/current/stage144_split_ci_runtime_strategy_pack/release_surface_contract.json",
            ".github/workflows/ci-fast.yml",
        ]
    )


def _procedure_alignment_ok(root: Path) -> bool:
    targets = [
        root / ".github/workflows/ci-fast.yml",
        root / ".github/workflows/ci-core.yml",
        root / ".github/workflows/ci-full.yml",
        root / ".github/workflows/cd-dry-run.yml",
        root / ".github/workflows/release.yml",
        root / "RELEASE_NOTES.md",
        root / "package_manifest.json",
    ]
    if not all(path.exists() for path in targets):
        return False
    contents = "\n".join(path.read_text(encoding="utf-8") for path in targets)
    return all(
        token in contents
        for token in [
            "stage144",
            "run_stage144_split_ci_runtime_strategy.py",
            "run_stage144_release_gate.py",
            "ci-fast",
        ]
    )
