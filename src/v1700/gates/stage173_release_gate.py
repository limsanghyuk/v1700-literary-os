from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from v1700.governance_contract import run_stage173_governance_contract


def run_stage173_release_gate(root: Path | None = None) -> dict[str, Any]:
    root = root or Path(__file__).resolve().parents[3]
    stage = run_stage173_governance_contract(root)
    parts = stage.get("parts", {})
    readiness = parts.get("page06_readiness_matrix", {})
    catalog = parts.get("governance_contract_catalog", {})
    precedence = parts.get("policy_precedence_matrix", {})
    registry = parts.get("authority_scope_registry", {})
    approvals = parts.get("approval_requirement_matrix", {})
    criteria = parts.get("stage174_entry_criteria", {})
    checks = {
        "baseline_stage172_gate_pass": _check(readiness.get("checks", {}).get("stage172_release_gate_pass", {}).get("status") == "pass"),
        "page05_sealed_pass": _check(readiness.get("checks", {}).get("page05_sealed", {}).get("status") == "pass"),
        "governance_contract_pass": _check(stage.get("status") == "pass" and catalog.get("status") == "pass"),
        "default_deny_pass": _check(stage.get("default_authority_decision") == "DENY" and stage.get("deny_by_default") is True),
        "unknown_request_denies_pass": _check(stage.get("unknown_request_decision") == "DENY"),
        "policy_precedence_pass": _check(precedence.get("status") == "pass" and precedence.get("deny_overrides_allow") is True),
        "authority_registry_pass": _check(registry.get("status") == "pass" and registry.get("automatic_promotion_enabled") is False),
        "approval_requirement_pass": _check(approvals.get("status") == "pass" and approvals.get("sensitive_authority_requires_approval") is True),
        "stage174_ready_pass": _check(criteria.get("status") == "pass" and stage.get("stage174_release_policy_registry_ready") is True),
        "preflight_execution_report_pass": _check(_report_pass(root, "release/current/stage173_preflight_execution_report.json", required_true="preflight_guide_read")),
        "package_comparison_report_pass": _check(_report_pass(root, "release/current/stage173_package_comparison_report.json", required_true="procedure_evidence_enforced")),
        "gitnexus_preflight_analysis_pass": _check(_gitnexus_analysis_ok(root)),
        "provider_zero_pass": _check(stage.get("provider_default_calls") == 0 and stage.get("provider_generation_enabled") is False),
        "write_zero_pass": _check(stage.get("write_operation_count") == 0 and stage.get("governance_write_enabled") is False and stage.get("memory_write_enabled") is False),
        "training_mutation_disabled_pass": _check(stage.get("runtime_training_enabled") is False and stage.get("canon_mutation_enabled") is False),
        "node2_boundary_pass": _check(stage.get("node2_raw_reveal_access") == 0 and stage.get("boundary_violation_count") == 0),
        "docs_manifest_pass": _check(_docs_manifest_ok(root)),
        "procedure_alignment_pass": _check(_procedure_alignment_ok(root)),
    }
    issues = [name for name, value in checks.items() if value["status"] != "pass"]
    result = {
        "stage": "173",
        "baseline_stage": "172",
        "title": "Governance Contract",
        "status": "pass" if not issues and stage.get("status") == "pass" else "blocked",
        "issues": issues,
        "checks": checks,
        "stage173": _compact(stage),
        "default_authority_decision": "DENY",
        "deny_by_default": True,
        "automatic_promotion_enabled": False,
        "stage174_release_policy_registry_ready": not issues,
        "provider_default_calls": 0,
        "live_provider_call_count_in_release_gate": 0,
        "runtime_execution_count": 0,
        "provider_generation_count": 0,
        "write_operation_count": 0,
        "node2_raw_reveal_access": 0,
        "boundary_violation_count": 0,
        "credential_leakage": 0,
        "provider_generation_enabled": False,
        "provider_evaluation_enabled": False,
        "governance_write_enabled": False,
        "memory_write_enabled": False,
        "cross_project_write_enabled": False,
        "canon_mutation_enabled": False,
        "runtime_training_enabled": False,
        "auto_repair_apply_enabled": False,
        "branchpoint_lineage_preserved": not issues,
    }
    out = root / "release/current/stage173_release_gate_report.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return result


def _check(condition: bool) -> dict[str, str]:
    return {"status": "pass" if condition else "blocked"}


def _report_pass(root: Path, rel: str, required_true: str | None = None) -> bool:
    path = root / rel
    if not path.exists():
        return False
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return False
    if data.get("status") != "pass":
        return False
    if required_true and data.get(required_true) is not True:
        return False
    return True


def _gitnexus_analysis_ok(root: Path) -> bool:
    path = root / "release/current/stage173_gitnexus_preflight_analysis_report.json"
    if not path.exists():
        return False
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return False
    if data.get("status") != "pass":
        return False
    if data.get("seven_key_perspectives_count") != 7:
        return False
    if data.get("twelve_design_development_items_count") != 12:
        return False
    if data.get("runtime") not in {"gitnexus", "python_fallback"}:
        return False
    perspectives = data.get("seven_key_perspectives", [])
    items = data.get("twelve_design_development_items", [])
    return (
        len(perspectives) == 7
        and len(items) == 12
        and all(item.get("status") == "pass" and item.get("applied_to_stage173") is True for item in perspectives)
        and all(item.get("status") == "pass" and item.get("applied_to_stage173") is True for item in items)
    )


def _docs_manifest_ok(root: Path) -> bool:
    expected = [
        "docs/stages/stage173.md",
        "docs/proposals/stage173_governance_contract_proposal.md",
        "docs/architecture/stage173_governance_contract_blueprint.md",
        "docs/development/stage173_developer_handoff.md",
        "docs/proposals/page06_governance_body_proposal.md",
        "docs/architecture/page06_governance_body_blueprint.md",
        "docs/development/page06_developer_handoff.md",
        "manifests/stage173_manifest.json",
        "manifests/stage173_governance_contract_manifest.json",
        "manifests/stage173_branchpoint_trace_manifest.json",
        "manifests/live_core_stage173_overlay.json",
        "release/current/stage173_release_asset_manifest.json",
        "release/current/stage173_governance_contract_report.json",
        "release/current/stage173_release_gate_report.json",
        "release/current/stage173_preflight_execution_report.json",
        "release/current/stage173_package_comparison_report.json",
        "release/current/stage173_gitnexus_preflight_analysis_report.json",
        "release/current/stage173_governance_contract_pack/page06_readiness_matrix.json",
        "release/current/stage173_governance_contract_pack/governance_contract_catalog.json",
        "release/current/stage173_governance_contract_pack/policy_precedence_matrix.json",
        "release/current/stage173_governance_contract_pack/authority_scope_registry.json",
        "release/current/stage173_governance_contract_pack/approval_requirement_matrix.json",
        "release/current/stage173_governance_contract_pack/stage174_entry_criteria.json",
    ]
    return all((root / rel).exists() for rel in expected)


def _procedure_alignment_ok(root: Path) -> bool:
    targets = [root / "README.md", root / "RELEASE_NOTES.md", root / "package_manifest.json"]
    if not all(path.exists() for path in targets):
        return False
    text = "\n".join(path.read_text(encoding="utf-8") for path in targets)
    return all(token in text for token in ["stage173", "run_stage173_governance_contract.py", "run_stage173_release_gate.py"])


def _compact(stage: dict[str, Any]) -> dict[str, Any]:
    keep = (
        "status", "stage", "baseline_stage", "title", "issues", "mode", "governance_contract_only",
        "stage172_page05_seal_inherited", "default_authority_decision", "deny_by_default",
        "policy_precedence_defined", "sensitive_authority_requires_approval",
        "stage174_release_policy_registry_ready", "contract_count", "policy_rule_count",
        "provider_default_calls", "node2_raw_reveal_access", "branchpoint_lineage_preserved",
    )
    return {key: stage.get(key) for key in keep if key in stage}
