from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from v1700.gates.stage154_release_gate import run_stage154_release_gate
from v1700.stage155 import run_stage155

_CACHE: dict[str, dict[str, Any]] = {}


def run_stage155_release_gate(root: Path | None = None) -> dict[str, Any]:
    root = root or Path(__file__).resolve().parents[3]
    key = str(root.resolve())
    if key in _CACHE:
        return _CACHE[key]
    if _active_version(root) != "stage155":
        existing = _load_report(root, "stage155_release_gate_report.json")
        if existing is not None and existing.get("status") == "pass":
            _CACHE[key] = existing
            return existing

    baseline = _baseline_gate(root)
    stage = run_stage155(root)
    parts = stage.get("parts", {})
    readiness = parts.get("page03_readiness_matrix", {})
    contracts = parts.get("execution_packet_contracts", {})
    boundary = parts.get("execution_boundary_policy", {})
    write_policy = parts.get("execution_write_policy", {})
    node2 = parts.get("node2_execution_projection_policy", {})

    checks = {
        "stage154_baseline_gate_pass": _check(baseline.get("status") == "pass"),
        "stage155_report_pass": _check(stage.get("status") == "pass"),
        "execution_contract_mode_pass": _check(stage.get("execution_contract_only") is True and stage.get("mode") == "EXECUTION_CONTRACT_LOCAL_ONLY"),
        "page03_readiness_pass": _check(readiness.get("status") == "pass" and readiness.get("check_count", 0) >= 7),
        "execution_packet_contracts_pass": _check(contracts.get("status") == "pass" and contracts.get("contract_count", 0) >= 6),
        "execution_boundary_policy_pass": _check(boundary.get("status") == "pass" and boundary.get("rule_count", 0) >= 7),
        "execution_write_policy_disabled_pass": _check(write_policy.get("status") == "pass" and stage.get("execution_write_enabled") is False),
        "node2_execution_projection_policy_pass": _check(node2.get("status") == "pass" and stage.get("node2_raw_reveal_access") == 0),
        "runtime_execution_disabled": _check(stage.get("runtime_execution_enabled") is False and stage.get("generation_runtime_enabled") is False),
        "provider_execution_disabled": _check(stage.get("provider_execution_enabled") is False),
        "memory_write_blocked": _check(stage.get("memory_write_enabled") is False and stage.get("execution_write_enabled") is False),
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
        "stage": "155",
        "baseline_stage": "154",
        "title": "Execution Contract",
        "status": "pass" if not issues and stage.get("status") == "pass" else "blocked",
        "issues": issues,
        "checks": checks,
        "stage155": _compact(stage),
        "provider_default_calls": 0,
        "live_provider_call_count_in_release_gate": 0,
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
    out = root / "release/current/stage155_release_gate_report.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    _CACHE[key] = result
    return result


def _check(condition: bool) -> dict[str, str]:
    return {"status": "pass" if condition else "blocked"}


def _baseline_gate(root: Path) -> dict[str, Any]:
    if _active_version(root) != "stage155":
        report = _load_report(root, "stage154_release_gate_report.json")
        if report is not None and report.get("status") == "pass":
            return report
    return run_stage154_release_gate(root)


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
    keep = ("status", "stage", "baseline_stage", "title", "issues", "mode", "execution_contract_only", "page02_seal_inherited", "stage156_local_execution_packet_store_ready", "contract_count", "boundary_rule_count", "write_policy_rule_count", "node2_projection_rule_count", "runtime_execution_enabled", "generation_runtime_enabled", "provider_execution_enabled", "memory_write_enabled", "execution_write_enabled", "canon_mutation_enabled", "auto_repair_apply_enabled", "runtime_training_enabled", "model_weight_update_count", "canon_auto_resolution_count", "auto_repair_mutation_count", "provider_default_calls", "live_provider_call_count_in_release_gate", "node2_raw_reveal_access", "boundary_violation_count", "raw_manuscript_provider_leakage", "raw_manuscript_cross_project_leakage", "credential_leakage", "branchpoint_lineage_preserved")
    return {key: stage.get(key) for key in keep if key in stage}


def _docs_manifest_ok(root: Path) -> bool:
    return all((root / rel).exists() for rel in [
        "docs/stages/stage155.md",
        "docs/proposals/stage155_execution_contract_proposal.md",
        "docs/architecture/stage155_execution_contract_blueprint.md",
        "docs/development/stage155_developer_handoff.md",
        "docs/proposals/page03_execution_body_proposal.md",
        "docs/architecture/page03_execution_body_blueprint.md",
        "docs/development/page03_developer_handoff.md",
        "docs/roadmaps/seven_page_architecture.md",
        "manifests/stage155_manifest.json",
        "manifests/stage155_execution_contract_manifest.json",
        "manifests/stage155_branchpoint_trace_manifest.json",
        "manifests/live_core_stage155_overlay.json",
        "release/current/stage155_execution_contract_report.json",
        "release/current/stage155_release_gate_report.json",
        "release/current/stage155_execution_contract_pack/page03_readiness_matrix.json",
        "release/current/stage155_execution_contract_pack/execution_packet_contracts.json",
        "release/current/stage155_execution_contract_pack/execution_boundary_policy.json",
        "release/current/stage155_execution_contract_pack/execution_write_policy.json",
        "release/current/stage155_execution_contract_pack/node2_execution_projection_policy.json",
    ])


def _procedure_alignment_ok(root: Path) -> bool:
    targets = [root / "README.md", root / "RELEASE_NOTES.md", root / "package_manifest.json"]
    if not all(path.exists() for path in targets):
        return False
    contents = "\n".join(path.read_text(encoding="utf-8") for path in targets)
    return all(token in contents for token in ["stage155", "run_stage155_execution_contract.py", "run_stage155_release_gate.py"])
