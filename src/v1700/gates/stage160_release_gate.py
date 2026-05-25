from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from v1700.gates.stage159_release_gate import run_stage159_release_gate
from v1700.stage160 import run_stage160

_CACHE: dict[str, dict[str, Any]] = {}


def run_stage160_release_gate(root: Path | None = None) -> dict[str, Any]:
    root = root or Path(__file__).resolve().parents[3]
    key = str(root.resolve())
    if key in _CACHE:
        return _CACHE[key]
    if _active_version(root) != "stage160":
        existing = _load_report(root, "stage160_release_gate_report.json")
        if existing is not None and existing.get("status") == "pass":
            _CACHE[key] = existing
            return existing

    baseline = _baseline_gate(root)
    stage = run_stage160(root)
    parts = stage.get("parts", {})
    chain = parts.get("page03_stage_chain", {})
    matrix = parts.get("page03_release_seal_matrix", {})
    artifact_index = parts.get("page03_artifact_index", {})
    freeze = parts.get("page03_invariant_freeze", {})
    connectivity = parts.get("page03_nexus_connectivity_matrix", {})
    transition = parts.get("page03_transition_criteria", {})
    seal = parts.get("page03_release_seal", {})
    regression = parts.get("regression_snapshot", {})

    checks = {
        "stage159_baseline_gate_pass": _check(baseline.get("status") == "pass"),
        "stage160_report_pass": _check(stage.get("status") == "pass"),
        "page03_release_seal_mode_pass": _check(stage.get("mode") == "PAGE03_RELEASE_SEAL_LOCAL"),
        "page03_stage_chain_pass": _check(chain.get("status") == "pass" and stage.get("page03_upstream_stage_count") == 5),
        "page03_total_stage_count_pass": _check(stage.get("page03_total_stage_count") == 6),
        "page03_release_seal_matrix_pass": _check(matrix.get("status") == "pass"),
        "page03_artifact_index_complete": _check(artifact_index.get("status") == "pass" and artifact_index.get("missing_count") == 0),
        "page03_invariant_freeze_pass": _check(freeze.get("status") == "pass"),
        "page03_nexus_connectivity_pass": _check(connectivity.get("status") == "pass"),
        "stage161_transition_ready": _check(transition.get("status") == "pass" and stage.get("stage161_rendering_contract_ready") is True),
        "page03_release_checksum_pass": _check(len(str(stage.get("page03_release_checksum", ""))) == 64 and seal.get("status") == "pass"),
        "regression_snapshot_pass": _check(regression.get("status") == "pass"),
        "runtime_execution_disabled": _check(stage.get("runtime_execution_enabled") is False and stage.get("runtime_execution_count") == 0),
        "generation_runtime_disabled": _check(stage.get("generation_runtime_enabled") is False),
        "provider_execution_disabled": _check(stage.get("provider_execution_enabled") is False and stage.get("provider_execution_count") == 0),
        "write_operations_blocked": _check(stage.get("execution_write_enabled") is False and stage.get("write_operation_count") == 0),
        "memory_store_graph_preflight_write_blocked": _check(stage.get("memory_write_enabled") is False and stage.get("store_write_enabled") is False and stage.get("graph_write_enabled") is False and stage.get("preflight_write_enabled") is False),
        "canon_mutation_blocked": _check(stage.get("canon_mutation_enabled") is False and stage.get("canon_auto_resolution_count") == 0),
        "auto_repair_blocked": _check(stage.get("auto_repair_apply_enabled") is False and stage.get("auto_repair_mutation_count") == 0),
        "vector_db_runtime_dependency_blocked": _check(stage.get("vector_db_runtime_dependency") is False),
        "live_provider_rag_blocked": _check(stage.get("live_provider_rag_enabled") is False),
        "runtime_training_blocked": _check(stage.get("runtime_training_enabled") is False),
        "model_weight_update_zero": _check(stage.get("model_weight_update_count") == 0),
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
        "stage": "160",
        "baseline_stage": "159",
        "title": "Page03 Release Seal",
        "status": "pass" if not issues and stage.get("status") == "pass" else "blocked",
        "issues": issues,
        "checks": checks,
        "stage160": _compact(stage),
        "page03_sealed": not issues,
        "page03_release_checksum": stage.get("page03_release_checksum"),
        "stage161_rendering_contract_ready": not issues,
        "provider_default_calls": 0,
        "live_provider_call_count_in_release_gate": 0,
        "runtime_execution_count": 0,
        "provider_execution_count": 0,
        "write_operation_count": 0,
        "node2_raw_reveal_access": 0,
        "boundary_violation_count": 0,
        "raw_manuscript_provider_leakage": 0,
        "raw_manuscript_cross_project_leakage": 0,
        "credential_leakage": 0,
        "runtime_execution_enabled": False,
        "memory_write_enabled": False,
        "runtime_training_enabled": False,
        "branchpoint_lineage_preserved": not issues,
    }
    out = root / "release/current/stage160_release_gate_report.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    _CACHE[key] = result
    return result


def _check(condition: bool) -> dict[str, str]:
    return {"status": "pass" if condition else "blocked"}


def _baseline_gate(root: Path) -> dict[str, Any]:
    if _active_version(root) != "stage160":
        report = _load_report(root, "stage159_release_gate_report.json")
        if report is not None and report.get("status") == "pass":
            return report
    return run_stage159_release_gate(root)


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
    keep = ("status", "stage", "baseline_stage", "title", "issues", "mode", "page03_sealed", "page03_total_stage_count", "page03_release_checksum", "stage161_rendering_contract_ready", "runtime_execution_enabled", "generation_runtime_enabled", "provider_execution_enabled", "memory_write_enabled", "execution_write_enabled", "store_write_enabled", "graph_write_enabled", "preflight_write_enabled", "dry_run_write_enabled", "canon_mutation_enabled", "auto_repair_apply_enabled", "runtime_training_enabled", "runtime_execution_count", "provider_execution_count", "write_operation_count", "provider_default_calls", "live_provider_call_count_in_release_gate", "node2_raw_reveal_access", "boundary_violation_count", "credential_leakage", "branchpoint_lineage_preserved")
    return {key: stage.get(key) for key in keep if key in stage}


def _docs_manifest_ok(root: Path) -> bool:
    generated = {"release/current/stage160_release_gate_report.json"}
    return all((root / rel).exists() or rel in generated for rel in [
        "docs/stages/stage160.md",
        "docs/proposals/stage160_page03_release_seal_proposal.md",
        "docs/architecture/stage160_page03_release_seal_blueprint.md",
        "docs/development/stage160_developer_handoff.md",
        "manifests/stage160_manifest.json",
        "manifests/stage160_page03_release_seal_manifest.json",
        "manifests/stage160_branchpoint_trace_manifest.json",
        "release/current/stage160_page03_release_seal_report.json",
        "release/current/stage160_release_gate_report.json",
        "release/current/stage160_page03_release_seal_pack/page03_stage_chain.json",
        "release/current/stage160_page03_release_seal_pack/page03_release_seal_matrix.json",
        "release/current/stage160_page03_release_seal_pack/page03_artifact_index.json",
        "release/current/stage160_page03_release_seal_pack/page03_invariant_freeze.json",
        "release/current/stage160_page03_release_seal_pack/page03_nexus_connectivity_matrix.json",
        "release/current/stage160_page03_release_seal_pack/page03_transition_criteria.json",
        "release/current/stage160_page03_release_seal_pack/page03_release_seal.json",
        "release/current/stage160_page03_release_seal_pack/regression_snapshot.json",
    ])


def _procedure_alignment_ok(root: Path) -> bool:
    targets = [root / "README.md", root / "RELEASE_NOTES.md", root / "package_manifest.json"]
    if not all(path.exists() for path in targets):
        return False
    contents = "\n".join(path.read_text(encoding="utf-8") for path in targets)
    return all(token in contents for token in ["stage160", "run_stage160_page03_release_seal.py", "run_stage160_release_gate.py"])
