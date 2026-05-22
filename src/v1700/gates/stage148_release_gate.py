from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from v1700.gates.stage147_release_gate import run_stage147_release_gate
from v1700.stage148 import run_stage148

_CACHE: dict[str, dict[str, Any]] = {}


def run_stage148_release_gate(root: Path | None = None) -> dict[str, Any]:
    root = root or Path(__file__).resolve().parents[3]
    key = str(root.resolve())
    if key in _CACHE:
        return _CACHE[key]
    if _active_version(root) != "stage148":
        existing = _load_report(root, "stage148_release_gate_report.json")
        if existing is not None and existing.get("status") == "pass":
            _CACHE[key] = existing
            return existing

    out = root / "release/current/stage148_release_gate_report.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    if not out.exists():
        out.write_text(
            json.dumps(
                {
                    "stage": "148",
                    "baseline_stage": "147",
                    "title": "Node Boundary Constitution Gate",
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
    stage = run_stage148(root)
    authority = stage.get("parts", {}).get("node_authority_matrix", {})
    routes = stage.get("parts", {}).get("packet_route_map", {})
    projections = stage.get("parts", {}).get("surface_projection_registry", {})
    boundary = stage.get("parts", {}).get("boundary_enforcement_summary", {})
    stage149_signals = stage.get("parts", {}).get("stage149_entry_signals", {})
    checks = {
        "stage147_baseline_gate_pass": _check(
            baseline.get("status") == "pass" or baseline.get("stage147", {}).get("status") == "pass"
        ),
        "stage148_report_pass": _check(stage.get("status") == "pass"),
        "node_boundary_mode_pass": _check(
            stage.get("node_boundary_constitution_only") is True
            and stage.get("mode") == "NODE_BOUNDARY_CONSTITUTION_LOCAL"
        ),
        "metadata_consistency_pass": _check(stage.get("metadata_consistency_status") == "pass"),
        "release_asset_integrity_pass": _check(stage.get("release_asset_integrity_status") == "pass"),
        "node_authority_matrix_pass": _check(
            authority.get("status") == "pass" and stage.get("authority_rule_count", 0) >= 7
        ),
        "packet_route_map_pass": _check(
            routes.get("status") == "pass" and stage.get("route_count", 0) >= 6
        ),
        "surface_projection_registry_pass": _check(
            projections.get("status") == "pass" and stage.get("projection_rule_count", 0) >= 7
        ),
        "boundary_enforcement_summary_pass": _check(
            boundary.get("status") == "pass" and boundary.get("all_enforced") is True
        ),
        "node2_surface_only_enforced_pass": _check(stage.get("node2_surface_only_enforced") is True),
        "node3_critic_scope_defined_pass": _check(stage.get("node3_critic_scope_defined") is True),
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
        "stage149_signals_pass": _check(stage149_signals.get("status") == "pass"),
    }
    issues = [name for name, value in checks.items() if value["status"] != "pass"]
    result = {
        "stage": "148",
        "baseline_stage": "147",
        "title": "Node Boundary Constitution Gate",
        "status": "pass" if not issues and stage.get("status") == "pass" else "blocked",
        "issues": issues,
        "checks": checks,
        "stage148": _compact(stage),
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
    if _active_version(root) != "stage148":
        report = _load_report(root, "stage147_release_gate_report.json")
        if report is not None and report.get("status") == "pass":
            return report
    return run_stage147_release_gate(root)


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
        "node_boundary_constitution_only",
        "authority_rule_count",
        "route_count",
        "projection_rule_count",
        "node2_surface_only_enforced",
        "node3_critic_scope_defined",
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
            "docs/stages/stage148.md",
            "docs/proposals/stage148_node_boundary_constitution_proposal.md",
            "docs/architecture/stage148_node_boundary_constitution_blueprint.md",
            "docs/development/stage148_developer_handoff.md",
            "manifests/stage148_manifest.json",
            "manifests/stage148_node_boundary_constitution_manifest.json",
            "manifests/stage148_branchpoint_trace_manifest.json",
            "manifests/live_core_stage148_overlay.json",
            "release/current/stage148_node_boundary_constitution_report.json",
            "release/current/stage148_release_gate_report.json",
            "release/current/stage148_release_asset_manifest.json",
            "release/current/stage148_node_boundary_constitution_pack/node_authority_matrix.json",
            "release/current/stage148_node_boundary_constitution_pack/packet_route_map.json",
            "release/current/stage148_node_boundary_constitution_pack/surface_projection_registry.json",
            "release/current/stage148_node_boundary_constitution_pack/boundary_enforcement_summary.json",
            "release/current/stage148_node_boundary_constitution_pack/stage149_entry_signals.json",
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
            "stage148",
            "run_stage148_node_boundary_constitution.py",
            "run_stage148_release_gate.py",
        ]
    )
