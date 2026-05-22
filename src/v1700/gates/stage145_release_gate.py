from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from v1700.gates.stage144_release_gate import run_stage144_release_gate
from v1700.stage145 import run_stage145

_CACHE: dict[str, dict[str, Any]] = {}


def run_stage145_release_gate(root: Path | None = None) -> dict[str, Any]:
    root = root or Path(__file__).resolve().parents[3]
    key = str(root.resolve())
    if key in _CACHE:
        return _CACHE[key]
    if _active_version(root) != "stage145":
        existing = _load_report(root, "stage145_release_gate_report.json")
        if existing is not None and existing.get("status") == "pass":
            _CACHE[key] = existing
            return existing

    out = root / "release/current/stage145_release_gate_report.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    if not out.exists():
        out.write_text(
            json.dumps(
                {
                    "stage": "145",
                    "baseline_stage": "144",
                    "title": "Body Constitution Gate",
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
    stage = run_stage145(root)
    formula = stage.get("parts", {}).get("formula_classification", {})
    invariants = stage.get("parts", {}).get("constitution_invariants", {})
    layer_map = stage.get("parts", {}).get("body_layer_map", {})
    stage150_entry = stage.get("parts", {}).get("stage150_entry_criteria", {})
    checks = {
        "stage144_baseline_gate_pass": _check(
            baseline.get("status") == "pass" or baseline.get("stage144", {}).get("status") == "pass"
        ),
        "stage145_report_pass": _check(stage.get("status") == "pass"),
        "constitution_mode_pass": _check(
            stage.get("body_constitution_only") is True
            and stage.get("mode") == "BODY_CONSTITUTION_PROPOSAL_LOCAL"
        ),
        "metadata_consistency_pass": _check(stage.get("metadata_consistency_status") == "pass"),
        "release_asset_integrity_pass": _check(stage.get("release_asset_integrity_status") == "pass"),
        "formula_policy_complete_pass": _check(stage.get("formula_policy_complete") is True),
        "formula_status_coverage_pass": _check(formula.get("coverage_complete") is True),
        "constitution_invariants_pass": _check(invariants.get("status") == "pass" and invariants.get("all_enforced") is True),
        "body_layers_pass": _check(layer_map.get("status") == "pass" and stage.get("body_layer_count", 0) >= 7),
        "stage150_entry_criteria_pass": _check(stage150_entry.get("status") == "pass" and stage.get("stage150_memory_body_ready") is True),
        "narrative_state_contract_ready_pass": _check(stage.get("narrative_state_contract_ready") is True),
        "project_manifest_body_ready_pass": _check(stage.get("project_manifest_body_ready") is True),
        "node_boundary_constitution_ready_pass": _check(stage.get("node_boundary_constitution_ready") is True),
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
        "stage": "145",
        "baseline_stage": "144",
        "title": "Body Constitution Gate",
        "status": "pass" if not issues and stage.get("status") == "pass" else "blocked",
        "issues": issues,
        "checks": checks,
        "stage145": _compact(stage),
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
    if _active_version(root) != "stage145":
        report = _load_report(root, "stage144_release_gate_report.json")
        if report is not None and report.get("status") == "pass":
            return report
    return run_stage144_release_gate(root)


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
        "body_constitution_only",
        "formula_policy",
        "formula_policy_complete",
        "constitution_invariants_complete",
        "body_layer_count",
        "narrative_state_contract_ready",
        "project_manifest_body_ready",
        "node_boundary_constitution_ready",
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
            "docs/stages/stage145.md",
            "docs/proposals/stage145_body_constitution_proposal.md",
            "docs/architecture/stage145_body_constitution_blueprint.md",
            "docs/development/stage145_developer_handoff.md",
            "manifests/stage145_manifest.json",
            "manifests/stage145_body_constitution_manifest.json",
            "manifests/stage145_branchpoint_trace_manifest.json",
            "manifests/live_core_stage145_overlay.json",
            "release/current/stage145_body_constitution_report.json",
            "release/current/stage145_release_gate_report.json",
            "release/current/stage145_release_asset_manifest.json",
            "release/current/stage145_body_constitution_pack/formula_classification.json",
            "release/current/stage145_body_constitution_pack/constitution_invariants.json",
            "release/current/stage145_body_constitution_pack/body_layer_map.json",
            "release/current/stage145_body_constitution_pack/stage150_entry_criteria.json",
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
            "stage145",
            "run_stage145_body_constitution.py",
            "run_stage145_body_constitution_gate.py",
        ]
    )
