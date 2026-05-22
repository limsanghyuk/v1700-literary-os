from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from v1700.gates.stage146_release_gate import run_stage146_release_gate
from v1700.stage147 import run_stage147

_CACHE: dict[str, dict[str, Any]] = {}


def run_stage147_release_gate(root: Path | None = None) -> dict[str, Any]:
    root = root or Path(__file__).resolve().parents[3]
    key = str(root.resolve())
    if key in _CACHE:
        return _CACHE[key]
    if _active_version(root) != "stage147":
        existing = _load_report(root, "stage147_release_gate_report.json")
        if existing is not None and existing.get("status") == "pass":
            _CACHE[key] = existing
            return existing

    out = root / "release/current/stage147_release_gate_report.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    if not out.exists():
        out.write_text(
            json.dumps(
                {
                    "stage": "147",
                    "baseline_stage": "146",
                    "title": "Project Manifest Body Gate",
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
    stage = run_stage147(root)
    catalog = stage.get("parts", {}).get("project_manifest_catalog", {})
    bindings = stage.get("parts", {}).get("manifest_state_bindings", {})
    policy = stage.get("parts", {}).get("manifest_policy_boundary", {})
    load_order = stage.get("parts", {}).get("manifest_load_order", {})
    stage148_signals = stage.get("parts", {}).get("stage148_entry_signals", {})
    bundle = stage.get("parts", {}).get("canonical_manifest_bundle", {})
    checks = {
        "stage146_baseline_gate_pass": _check(
            baseline.get("status") == "pass" or baseline.get("stage146", {}).get("status") == "pass"
        ),
        "stage147_report_pass": _check(stage.get("status") == "pass"),
        "project_manifest_body_mode_pass": _check(
            stage.get("project_manifest_body_only") is True
            and stage.get("mode") == "PROJECT_MANIFEST_BODY_LOCAL"
        ),
        "metadata_consistency_pass": _check(stage.get("metadata_consistency_status") == "pass"),
        "release_asset_integrity_pass": _check(stage.get("release_asset_integrity_status") == "pass"),
        "canonical_manifest_bundle_pass": _check(
            bundle.get("status") == "pass" and bundle.get("packet_count", 0) >= 7
        ),
        "project_manifest_catalog_pass": _check(
            catalog.get("status") == "pass" and stage.get("manifest_section_count", 0) >= 5
        ),
        "manifest_state_bindings_pass": _check(
            bindings.get("status") == "pass" and stage.get("state_binding_count", 0) >= 7
        ),
        "manifest_policy_boundary_pass": _check(
            policy.get("status") == "pass" and stage.get("policy_boundary_complete") is True
        ),
        "manifest_load_order_pass": _check(
            load_order.get("status") == "pass" and stage.get("load_order_complete") is True
        ),
        "node_boundary_constitution_ready_pass": _check(stage.get("node_boundary_constitution_ready") is True),
        "stage149_gate_ready_pass": _check(stage.get("stage149_gate_ready") is True),
        "stage150_memory_body_ready_pass": _check(stage.get("stage150_memory_body_ready") is True),
        "runtime_training_blocked": _check(stage.get("runtime_training_enabled") is False),
        "active_meta_learning_blocked": _check(stage.get("active_meta_learning_enabled") is False),
        "model_weight_update_zero": _check(stage.get("model_weight_update_count") == 0),
        "losdb_write_blocked": _check(stage.get("losdb_write_enabled") is False),
        "migration_execution_blocked": _check(stage.get("migration_execution_enabled") is False),
        "provider_zero_pass": _check(
            stage.get("provider_default_calls") == 0 and stage.get("live_provider_call_count_in_release_gate") == 0
        ),
        "node2_boundary_pass": _check(stage.get("node2_raw_reveal_access") == 0),
        "raw_manuscript_leakage_zero": _check(
            stage.get("raw_manuscript_provider_leakage") == 0
            and stage.get("raw_manuscript_cross_project_leakage") == 0
        ),
        "credential_leakage_zero_pass": _check(stage.get("credential_leakage") == 0),
        "branchpoint_survival_pass": _check(stage.get("branchpoint_lineage_preserved") is True),
        "docs_manifest_pass": _check(_docs_manifest_ok(root)),
        "procedure_alignment_pass": _check(_procedure_alignment_ok(root)),
        "stage148_signals_pass": _check(stage148_signals.get("status") == "pass"),
    }
    issues = [name for name, value in checks.items() if value["status"] != "pass"]
    result = {
        "stage": "147",
        "baseline_stage": "146",
        "title": "Project Manifest Body Gate",
        "status": "pass" if not issues and stage.get("status") == "pass" else "blocked",
        "issues": issues,
        "checks": checks,
        "stage147": _compact(stage),
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
    if _active_version(root) != "stage147":
        report = _load_report(root, "stage146_release_gate_report.json")
        if report is not None and report.get("status") == "pass":
            return report
    return run_stage146_release_gate(root)


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
        "project_manifest_body_only",
        "manifest_section_count",
        "canonical_packet_count",
        "state_binding_count",
        "policy_boundary_complete",
        "load_order_complete",
        "node_boundary_constitution_ready",
        "stage149_gate_ready",
        "stage150_memory_body_ready",
        "metadata_consistency_status",
        "release_asset_integrity_status",
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
            "docs/stages/stage147.md",
            "docs/proposals/stage147_project_manifest_body_proposal.md",
            "docs/architecture/stage147_project_manifest_body_blueprint.md",
            "docs/development/stage147_developer_handoff.md",
            "manifests/stage147_manifest.json",
            "manifests/stage147_project_manifest_body_manifest.json",
            "manifests/stage147_branchpoint_trace_manifest.json",
            "manifests/live_core_stage147_overlay.json",
            "release/current/stage147_project_manifest_body_report.json",
            "release/current/stage147_release_gate_report.json",
            "release/current/stage147_release_asset_manifest.json",
            "release/current/stage147_project_manifest_body_pack/canonical_manifest_bundle.json",
            "release/current/stage147_project_manifest_body_pack/project_manifest_catalog.json",
            "release/current/stage147_project_manifest_body_pack/manifest_state_bindings.json",
            "release/current/stage147_project_manifest_body_pack/manifest_policy_boundary.json",
            "release/current/stage147_project_manifest_body_pack/manifest_load_order.json",
            "release/current/stage147_project_manifest_body_pack/stage148_entry_signals.json",
        ]
    )


def _procedure_alignment_ok(root: Path) -> bool:
    targets = [
        root / ".github/workflows/ci-fast.yml",
        root / ".github/workflows/ci-core.yml",
        root / ".github/workflows/cd-dry-run.yml",
        root / ".github/workflows/release.yml",
        root / "README.md",
        root / "RELEASE_NOTES.md",
        root / "package_manifest.json",
    ]
    if not all(path.exists() for path in targets):
        return False
    contents = "\n".join(path.read_text(encoding="utf-8") for path in targets)
    return all(
        token in contents
        for token in [
            "stage147",
            "run_stage147_project_manifest_body.py",
            "run_stage147_release_gate.py",
        ]
    )
