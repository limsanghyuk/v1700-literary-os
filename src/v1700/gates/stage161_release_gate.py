from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from v1700.gates.stage160_release_gate import run_stage160_release_gate
from v1700.stage161 import run_stage161

_CACHE: dict[str, dict[str, Any]] = {}


def run_stage161_release_gate(root: Path | None = None) -> dict[str, Any]:
    root = root or Path(__file__).resolve().parents[3]
    key = str(root.resolve())
    if key in _CACHE:
        return _CACHE[key]
    if _active_version(root) != "stage161":
        existing = _load_report(root, "stage161_release_gate_report.json")
        if existing is not None and existing.get("status") == "pass":
            _CACHE[key] = existing
            return existing

    baseline = _baseline_gate(root)
    stage = run_stage161(root)
    parts = stage.get("parts", {})
    readiness = parts.get("page04_readiness_matrix", {})
    contracts = parts.get("rendering_contracts", {})
    boundary = parts.get("rendering_boundary_policy", {})
    write_policy = parts.get("rendering_write_policy", {})
    node2 = parts.get("node2_rendering_projection_policy", {})

    checks = {
        "stage160_baseline_gate_pass": _check(baseline.get("status") == "pass"),
        "stage161_report_pass": _check(stage.get("status") == "pass"),
        "rendering_contract_mode_pass": _check(stage.get("rendering_contract_only") is True and stage.get("mode") == "RENDERING_CONTRACT_LOCAL_ONLY"),
        "page04_readiness_pass": _check(readiness.get("status") == "pass" and readiness.get("check_count", 0) >= 7),
        "rendering_contracts_pass": _check(contracts.get("status") == "pass" and contracts.get("contract_count", 0) >= 6),
        "rendering_boundary_policy_pass": _check(boundary.get("status") == "pass" and boundary.get("rule_count", 0) >= 7),
        "rendering_write_policy_disabled_pass": _check(write_policy.get("status") == "pass" and stage.get("render_write_enabled") is False),
        "node2_rendering_projection_policy_pass": _check(node2.get("status") == "pass" and stage.get("node2_raw_reveal_access") == 0),
        "rendering_runtime_disabled": _check(stage.get("rendering_runtime_enabled") is False and stage.get("generation_runtime_enabled") is False),
        "provider_generation_disabled": _check(stage.get("provider_generation_enabled") is False and stage.get("provider_generation_count") == 0),
        "runtime_execution_disabled": _check(stage.get("runtime_execution_enabled") is False and stage.get("runtime_execution_count") == 0),
        "write_operations_blocked": _check(stage.get("render_write_enabled") is False and stage.get("write_operation_count") == 0),
        "memory_execution_write_blocked": _check(stage.get("memory_write_enabled") is False and stage.get("execution_write_enabled") is False),
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
        "stage": "161",
        "baseline_stage": "160",
        "title": "Rendering Contract",
        "status": "pass" if not issues and stage.get("status") == "pass" else "blocked",
        "issues": issues,
        "checks": checks,
        "stage161": _compact(stage),
        "provider_default_calls": 0,
        "live_provider_call_count_in_release_gate": 0,
        "runtime_execution_count": 0,
        "provider_execution_count": 0,
        "provider_generation_count": 0,
        "write_operation_count": 0,
        "node2_raw_reveal_access": 0,
        "boundary_violation_count": 0,
        "raw_manuscript_provider_leakage": 0,
        "raw_manuscript_cross_project_leakage": 0,
        "credential_leakage": 0,
        "rendering_runtime_enabled": False,
        "generation_runtime_enabled": False,
        "provider_generation_enabled": False,
        "runtime_execution_enabled": False,
        "memory_write_enabled": False,
        "runtime_training_enabled": False,
        "branchpoint_lineage_preserved": not issues,
    }
    out = root / "release/current/stage161_release_gate_report.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    _CACHE[key] = result
    return result


def _check(condition: bool) -> dict[str, str]:
    return {"status": "pass" if condition else "blocked"}


def _baseline_gate(root: Path) -> dict[str, Any]:
    if _active_version(root) != "stage161":
        report = _load_report(root, "stage160_release_gate_report.json")
        if report is not None and report.get("status") == "pass":
            return report
    return run_stage160_release_gate(root)


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
    keep = ("status", "stage", "baseline_stage", "title", "issues", "mode", "rendering_contract_only", "page03_seal_inherited", "stage162_local_render_packet_store_ready", "contract_count", "boundary_rule_count", "write_policy_rule_count", "node2_projection_rule_count", "rendering_runtime_enabled", "generation_runtime_enabled", "provider_generation_enabled", "runtime_execution_enabled", "provider_execution_enabled", "memory_write_enabled", "render_write_enabled", "canon_mutation_enabled", "auto_repair_apply_enabled", "runtime_training_enabled", "model_weight_update_count", "canon_auto_resolution_count", "auto_repair_mutation_count", "provider_default_calls", "live_provider_call_count_in_release_gate", "node2_raw_reveal_access", "boundary_violation_count", "raw_manuscript_provider_leakage", "raw_manuscript_cross_project_leakage", "credential_leakage", "branchpoint_lineage_preserved")
    return {key: stage.get(key) for key in keep if key in stage}


def _docs_manifest_ok(root: Path) -> bool:
    return all((root / rel).exists() for rel in [
        "docs/stages/stage161.md",
        "docs/proposals/stage161_rendering_contract_proposal.md",
        "docs/architecture/stage161_rendering_contract_blueprint.md",
        "docs/development/stage161_developer_handoff.md",
        "docs/proposals/page04_rendering_body_proposal.md",
        "docs/architecture/page04_rendering_body_blueprint.md",
        "docs/development/page04_handoff.md",
        "manifests/stage161_manifest.json",
        "manifests/stage161_rendering_contract_manifest.json",
        "manifests/stage161_branchpoint_trace_manifest.json",
        "manifests/live_core_stage161_overlay.json",
        "release/current/stage161_rendering_contract_report.json",
        "release/current/stage161_release_gate_report.json",
        "release/current/stage161_rendering_contract_pack/page04_readiness_matrix.json",
        "release/current/stage161_rendering_contract_pack/rendering_contracts.json",
        "release/current/stage161_rendering_contract_pack/rendering_boundary_policy.json",
        "release/current/stage161_rendering_contract_pack/rendering_write_policy.json",
        "release/current/stage161_rendering_contract_pack/node2_rendering_projection_policy.json",
    ])


def _procedure_alignment_ok(root: Path) -> bool:
    targets = [root / "README.md", root / "RELEASE_NOTES.md", root / "package_manifest.json"]
    if not all(path.exists() for path in targets):
        return False
    contents = "\n".join(path.read_text(encoding="utf-8") for path in targets)
    return all(token in contents for token in ["stage161", "run_stage161_rendering_contract.py", "run_stage161_release_gate.py"])
