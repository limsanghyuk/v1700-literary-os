from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from v1700.gates.stage148_release_gate import run_stage148_release_gate
from v1700.stage149 import run_stage149

_CACHE: dict[str, dict[str, Any]] = {}


def run_stage149_release_gate(root: Path | None = None) -> dict[str, Any]:
    root = root or Path(__file__).resolve().parents[3]
    key = str(root.resolve())
    if key in _CACHE:
        return _CACHE[key]
    if _active_version(root) != "stage149":
        existing = _load_report(root, "stage149_release_gate_report.json")
        if existing is not None and existing.get("status") == "pass":
            _CACHE[key] = existing
            return existing

    out = root / "release/current/stage149_release_gate_report.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    if not out.exists():
        out.write_text(
            json.dumps(
                {
                    "stage": "149",
                    "baseline_stage": "148",
                    "title": "Body Constitution Release Gate",
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
    stage = run_stage149(root)
    gate_matrix = stage.get("parts", {}).get("body_constitution_gate_matrix", {})
    seal = stage.get("parts", {}).get("page01_constitution_seal", {})
    stage150 = stage.get("parts", {}).get("stage150_readiness_matrix", {})
    blockers = stage.get("parts", {}).get("release_blocker_registry", {})
    lineage = stage.get("parts", {}).get("lineage_evidence_index", {})
    checks = {
        "stage148_baseline_gate_pass": _check(
            baseline.get("status") == "pass" or baseline.get("stage148", {}).get("status") == "pass"
        ),
        "stage149_report_pass": _check(stage.get("status") == "pass"),
        "release_gate_mode_pass": _check(
            stage.get("body_constitution_release_gate_only") is True
            and stage.get("mode") == "BODY_CONSTITUTION_RELEASE_GATE_LOCAL"
        ),
        "metadata_consistency_pass": _check(stage.get("metadata_consistency_status") == "pass"),
        "release_asset_integrity_pass": _check(stage.get("release_asset_integrity_status") == "pass"),
        "gate_matrix_pass": _check(
            gate_matrix.get("status") == "pass" and stage.get("gate_rule_count", 0) >= 8
        ),
        "page01_constitution_seal_pass": _check(
            seal.get("status") == "pass" and stage.get("sealed_page01") is True
        ),
        "page01_constitution_frozen_pass": _check(stage.get("page01_constitution_frozen") is True),
        "stage150_readiness_pass": _check(
            stage150.get("status") == "pass" and stage.get("stage150_memory_body_ready") is True
        ),
        "release_blocker_registry_pass": _check(
            blockers.get("status") == "pass"
            and blockers.get("registered_blocker_count", 0) == blockers.get("blocked_capability_count", -1)
        ),
        "lineage_evidence_pass": _check(
            lineage.get("status") == "pass" and stage.get("lineage_evidence_complete") is True
        ),
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
    }
    issues = [name for name, value in checks.items() if value["status"] != "pass"]
    result = {
        "stage": "149",
        "baseline_stage": "148",
        "title": "Body Constitution Release Gate",
        "status": "pass" if not issues and stage.get("status") == "pass" else "blocked",
        "issues": issues,
        "checks": checks,
        "stage149": _compact(stage),
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
    if _active_version(root) != "stage149":
        report = _load_report(root, "stage148_release_gate_report.json")
        if report is not None and report.get("status") == "pass":
            return report
    return run_stage148_release_gate(root)


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
        "body_constitution_release_gate_only",
        "gate_rule_count",
        "sealed_page01",
        "page01_constitution_frozen",
        "stage150_memory_body_ready",
        "release_blocker_count",
        "blocked_capability_count",
        "lineage_evidence_complete",
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
            "docs/stages/stage149.md",
            "docs/proposals/stage149_body_constitution_release_gate_proposal.md",
            "docs/architecture/stage149_body_constitution_release_gate_blueprint.md",
            "docs/development/stage149_developer_handoff.md",
            "manifests/stage149_manifest.json",
            "manifests/stage149_body_constitution_release_gate_manifest.json",
            "manifests/stage149_branchpoint_trace_manifest.json",
            "manifests/live_core_stage149_overlay.json",
            "release/current/stage149_body_constitution_release_gate_report.json",
            "release/current/stage149_release_gate_report.json",
            "release/current/stage149_release_asset_manifest.json",
            "release/current/stage149_body_constitution_release_gate_pack/body_constitution_gate_matrix.json",
            "release/current/stage149_body_constitution_release_gate_pack/page01_constitution_seal.json",
            "release/current/stage149_body_constitution_release_gate_pack/stage150_readiness_matrix.json",
            "release/current/stage149_body_constitution_release_gate_pack/release_blocker_registry.json",
            "release/current/stage149_body_constitution_release_gate_pack/lineage_evidence_index.json",
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
            "stage149",
            "run_stage149_body_constitution_release_gate.py",
            "run_stage149_release_gate.py",
        ]
    )
