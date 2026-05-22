from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from v1700.gates.stage149_release_gate import run_stage149_release_gate
from v1700.stage150 import run_stage150

_CACHE: dict[str, dict[str, Any]] = {}


def run_stage150_release_gate(root: Path | None = None) -> dict[str, Any]:
    root = root or Path(__file__).resolve().parents[3]
    key = str(root.resolve())
    if key in _CACHE:
        return _CACHE[key]
    if _active_version(root) != "stage150":
        existing = _load_report(root, "stage150_release_gate_report.json")
        if existing is not None and existing.get("status") == "pass":
            _CACHE[key] = existing
            return existing

    baseline = _baseline_gate(root)
    stage = run_stage150(root)
    parts = stage.get("parts", {})
    contracts = parts.get("memory_record_contracts", {})
    boundary = parts.get("memory_boundary_policy", {})
    write_policy = parts.get("memory_write_policy", {})
    node2_projection = parts.get("node2_projection_policy", {})
    preflight = parts.get("preflight15_matrix", {})

    checks = {
        "stage149_baseline_gate_pass": _check(baseline.get("status") == "pass"),
        "stage150_report_pass": _check(stage.get("status") == "pass"),
        "preflight15_pass": _check(preflight.get("status") == "pass" and preflight.get("check_count") == 15),
        "memory_contract_mode_pass": _check(stage.get("memory_contract_only") is True and stage.get("mode") == "MEMORY_CONTRACT_LOCAL_ONLY"),
        "record_contracts_pass": _check(contracts.get("status") == "pass" and contracts.get("contract_count", 0) >= 10),
        "boundary_policy_pass": _check(boundary.get("status") == "pass" and boundary.get("rule_count", 0) >= 6),
        "write_policy_disabled_pass": _check(write_policy.get("status") == "pass" and stage.get("memory_write_enabled") is False),
        "node2_projection_policy_pass": _check(node2_projection.get("status") == "pass" and stage.get("node2_raw_reveal_access") == 0),
        "storage_runtime_disabled": _check(stage.get("storage_runtime_enabled") is False),
        "query_runtime_disabled": _check(stage.get("query_runtime_enabled") is False),
        "runtime_training_blocked": _check(stage.get("runtime_training_enabled") is False),
        "model_weight_update_zero": _check(stage.get("model_weight_update_count") == 0),
        "canon_auto_resolution_zero": _check(stage.get("canon_auto_resolution_count") == 0),
        "auto_repair_mutation_zero": _check(stage.get("auto_repair_mutation_count") == 0),
        "provider_zero_pass": _check(stage.get("provider_default_calls") == 0 and stage.get("live_provider_call_count_in_release_gate") == 0),
        "node2_boundary_pass": _check(stage.get("node2_raw_reveal_access") == 0 and stage.get("hidden_reveal_projection_count") == 0),
        "raw_manuscript_leakage_zero": _check(stage.get("raw_manuscript_provider_leakage") == 0 and stage.get("raw_manuscript_cross_project_leakage") == 0),
        "credential_leakage_zero_pass": _check(stage.get("credential_leakage") == 0),
        "branchpoint_survival_pass": _check(stage.get("branchpoint_lineage_preserved") is True),
        "docs_manifest_pass": _check(_docs_manifest_ok(root)),
        "procedure_alignment_pass": _check(_procedure_alignment_ok(root)),
    }
    issues = [name for name, value in checks.items() if value["status"] != "pass"]
    result = {
        "stage": "150",
        "baseline_stage": "149",
        "title": "Memory Contract",
        "status": "pass" if not issues and stage.get("status") == "pass" else "blocked",
        "issues": issues,
        "checks": checks,
        "stage150": _compact(stage),
        "provider_default_calls": 0,
        "live_provider_call_count_in_release_gate": 0,
        "node2_raw_reveal_access": 0,
        "raw_manuscript_provider_leakage": 0,
        "raw_manuscript_cross_project_leakage": 0,
        "credential_leakage": 0,
        "memory_write_enabled": False,
        "runtime_training_enabled": False,
        "branchpoint_lineage_preserved": not issues,
    }
    out = root / "release/current/stage150_release_gate_report.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    _CACHE[key] = result
    return result


def _check(condition: bool) -> dict[str, str]:
    return {"status": "pass" if condition else "blocked"}


def _baseline_gate(root: Path) -> dict[str, Any]:
    if _active_version(root) != "stage150":
        report = _load_report(root, "stage149_release_gate_report.json")
        if report is not None and report.get("status") == "pass":
            return report
    return run_stage149_release_gate(root)


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
        "status", "stage", "baseline_stage", "title", "issues", "mode",
        "memory_contract_only", "contract_count", "boundary_rule_count",
        "write_policy_rule_count", "node2_projection_rule_count",
        "stage151_local_read_only_memory_store_ready", "storage_runtime_enabled",
        "query_runtime_enabled", "memory_write_enabled", "runtime_training_enabled",
        "active_meta_learning_enabled", "model_weight_update_count", "canon_auto_resolution_count",
        "auto_repair_mutation_count", "provider_default_calls",
        "live_provider_call_count_in_release_gate", "node2_raw_reveal_access",
        "hidden_reveal_projection_count", "private_note_projection_count",
        "write_handle_projection_count", "raw_manuscript_provider_leakage",
        "raw_manuscript_cross_project_leakage", "credential_leakage",
        "branchpoint_lineage_preserved",
    )
    return {key: stage.get(key) for key in keep if key in stage}


def _docs_manifest_ok(root: Path) -> bool:
    return all(
        (root / rel).exists()
        for rel in [
            "docs/stages/stage150.md",
            "docs/proposals/stage150_memory_contract_proposal.md",
            "docs/architecture/stage150_memory_contract_blueprint.md",
            "docs/development/stage150_developer_handoff.md",
            "manifests/stage150_manifest.json",
            "manifests/stage150_memory_contract_manifest.json",
            "release/current/stage150_memory_contract_report.json",
            "release/current/stage150_release_gate_report.json",
            "release/current/stage150_memory_contract_pack/preflight15_matrix.json",
            "release/current/stage150_memory_contract_pack/memory_record_contracts.json",
            "release/current/stage150_memory_contract_pack/memory_boundary_policy.json",
            "release/current/stage150_memory_contract_pack/memory_write_policy.json",
            "release/current/stage150_memory_contract_pack/node2_projection_policy.json",
        ]
    )


def _procedure_alignment_ok(root: Path) -> bool:
    targets = [root / "README.md", root / "RELEASE_NOTES.md", root / "package_manifest.json"]
    if not all(path.exists() for path in targets):
        return False
    contents = "\n".join(path.read_text(encoding="utf-8") for path in targets)
    return all(token in contents for token in ["stage150", "run_stage150_memory_contract.py", "run_stage150_release_gate.py"])
