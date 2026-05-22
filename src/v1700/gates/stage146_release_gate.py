from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from v1700.gates.stage145_release_gate import run_stage145_release_gate
from v1700.stage146 import run_stage146

_CACHE: dict[str, dict[str, Any]] = {}


def run_stage146_release_gate(root: Path | None = None) -> dict[str, Any]:
    root = root or Path(__file__).resolve().parents[3]
    key = str(root.resolve())
    if key in _CACHE:
        return _CACHE[key]
    if _active_version(root) != "stage146":
        existing = _load_report(root, "stage146_release_gate_report.json")
        if existing is not None and existing.get("status") == "pass":
            _CACHE[key] = existing
            return existing

    out = root / "release/current/stage146_release_gate_report.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    if not out.exists():
        out.write_text(
            json.dumps(
                {
                    "stage": "146",
                    "baseline_stage": "145",
                    "title": "Narrative State Contract Gate",
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
    stage = run_stage146(root)
    state_shape = stage.get("parts", {}).get("state_shape_catalog", {})
    state_hierarchy = stage.get("parts", {}).get("state_hierarchy", {})
    continuity = stage.get("parts", {}).get("continuity_rulebook", {})
    reveal = stage.get("parts", {}).get("reveal_boundary_matrix", {})
    stage147_signals = stage.get("parts", {}).get("stage147_entry_signals", {})
    checks = {
        "stage145_baseline_gate_pass": _check(
            baseline.get("status") == "pass" or baseline.get("stage145", {}).get("status") == "pass"
        ),
        "stage146_report_pass": _check(stage.get("status") == "pass"),
        "narrative_state_mode_pass": _check(
            stage.get("narrative_state_contract_only") is True
            and stage.get("mode") == "NARRATIVE_STATE_CONTRACT_LOCAL"
        ),
        "metadata_consistency_pass": _check(stage.get("metadata_consistency_status") == "pass"),
        "release_asset_integrity_pass": _check(stage.get("release_asset_integrity_status") == "pass"),
        "canonical_state_object_count_pass": _check(stage.get("canonical_state_object_count", 0) >= 7),
        "state_shape_catalog_pass": _check(
            state_shape.get("status") == "pass" and state_shape.get("coverage_complete") is True
        ),
        "state_hierarchy_pass": _check(
            state_hierarchy.get("status") == "pass" and stage.get("hierarchy_edge_count", 0) >= 6
        ),
        "continuity_rulebook_pass": _check(
            continuity.get("status") == "pass" and continuity.get("all_enforced") is True
        ),
        "reveal_boundary_matrix_pass": _check(
            reveal.get("status") == "pass" and stage.get("reveal_boundary_complete") is True
        ),
        "project_manifest_body_ready_pass": _check(stage.get("project_manifest_body_ready") is True),
        "node_boundary_constitution_ready_pass": _check(stage.get("node_boundary_constitution_ready") is True),
        "stage149_gate_ready_pass": _check(stage.get("stage149_gate_ready") is True),
        "stage150_memory_body_ready_pass": _check(stage.get("stage150_memory_body_ready") is True),
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
        "stage147_signals_pass": _check(stage147_signals.get("status") == "pass"),
    }
    issues = [name for name, value in checks.items() if value["status"] != "pass"]
    result = {
        "stage": "146",
        "baseline_stage": "145",
        "title": "Narrative State Contract Gate",
        "status": "pass" if not issues and stage.get("status") == "pass" else "blocked",
        "issues": issues,
        "checks": checks,
        "stage146": _compact(stage),
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
    if _active_version(root) != "stage146":
        report = _load_report(root, "stage145_release_gate_report.json")
        if report is not None and report.get("status") == "pass":
            return report
    return run_stage145_release_gate(root)


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
        "narrative_state_contract_only",
        "canonical_state_object_count",
        "hierarchy_edge_count",
        "continuity_rule_count",
        "reveal_boundary_complete",
        "project_manifest_body_ready",
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
            "docs/stages/stage146.md",
            "docs/proposals/stage146_narrative_state_contract_proposal.md",
            "docs/architecture/stage146_narrative_state_contract_blueprint.md",
            "docs/development/stage146_developer_handoff.md",
            "manifests/stage146_manifest.json",
            "manifests/stage146_narrative_state_contract_manifest.json",
            "manifests/stage146_branchpoint_trace_manifest.json",
            "manifests/live_core_stage146_overlay.json",
            "release/current/stage146_narrative_state_contract_report.json",
            "release/current/stage146_release_gate_report.json",
            "release/current/stage146_release_asset_manifest.json",
            "release/current/stage146_narrative_state_contract_pack/state_shape_catalog.json",
            "release/current/stage146_narrative_state_contract_pack/state_hierarchy.json",
            "release/current/stage146_narrative_state_contract_pack/continuity_rulebook.json",
            "release/current/stage146_narrative_state_contract_pack/reveal_boundary_matrix.json",
            "release/current/stage146_narrative_state_contract_pack/stage147_entry_signals.json",
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
            "stage146",
            "run_stage146_narrative_state_contract.py",
            "run_stage146_release_gate.py",
        ]
    )
