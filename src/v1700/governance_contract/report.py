from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

TARGET_STAGE = "stage173"
TARGET_REPORT = "release/current/stage173_governance_contract_report.json"
PACK_DIR = "release/current/stage173_governance_contract_pack"

CORE_GOVERNANCE_INVARIANTS: dict[str, int | bool | str] = {
    "provider_default_calls": 0,
    "live_provider_call_count_in_release_gate": 0,
    "provider_generation_count": 0,
    "runtime_execution_count": 0,
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
    "automatic_promotion_enabled": False,
    "default_authority_decision": "DENY",
}


def run_stage173_governance_contract(root: Path | None = None, mode: str = "active") -> dict[str, Any]:
    root = root or Path(__file__).resolve().parents[3]
    active_version = _active_version(root)
    if active_version != TARGET_STAGE:
        existing = _load_json(root / TARGET_REPORT)
        if mode == "historical" and existing is not None:
            return existing
        return _blocked(f"active_version_mismatch:{active_version or 'missing'}")

    pack = root / PACK_DIR
    pack.mkdir(parents=True, exist_ok=True)

    stage172_gate = _load_json(root / "release/current/stage172_release_gate_report.json") or {}
    stage172_report = _load_json(root / "release/current/stage172_page05_release_seal_report.json") or {}
    preflight = _load_json(root / "release/current/stage172_preflight_execution_report.json") or {}
    comparison = _load_json(root / "release/current/stage172_package_comparison_report.json") or {}

    page06_readiness = _build_page06_readiness(root, stage172_gate, stage172_report, preflight, comparison)
    contract_catalog = _build_governance_contract_catalog()
    policy_precedence = _build_policy_precedence_matrix()
    authority_registry = _build_authority_scope_registry()
    approval_matrix = _build_approval_requirement_matrix()
    entry_criteria = _build_stage174_entry_criteria(page06_readiness, contract_catalog, policy_precedence, authority_registry, approval_matrix)

    parts = {
        "page06_readiness_matrix": page06_readiness,
        "governance_contract_catalog": contract_catalog,
        "policy_precedence_matrix": policy_precedence,
        "authority_scope_registry": authority_registry,
        "approval_requirement_matrix": approval_matrix,
        "stage174_entry_criteria": entry_criteria,
    }
    for name, payload in parts.items():
        _write_json(pack / f"{name}.json", payload)

    issues: list[str] = []
    for name, payload in parts.items():
        if payload.get("status") != "pass":
            issues.append(f"{name}_blocked")
            issues.extend(f"{name}:{issue}" for issue in payload.get("issues", []))

    result = {
        "stage": "173",
        "baseline_stage": "172",
        "title": "Governance Contract",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "mode": "GOVERNANCE_CONTRACT_LOCAL_ONLY",
        "page": "Page06 Governance Body",
        "governance_contract_only": True,
        "stage172_page05_seal_inherited": page06_readiness.get("stage172_page05_seal_inherited") is True,
        "default_authority_decision": "DENY",
        "deny_by_default": True,
        "policy_precedence_defined": policy_precedence.get("status") == "pass",
        "approval_evidence_schema_valid": approval_matrix.get("status") == "pass",
        "sensitive_authority_requires_approval": approval_matrix.get("sensitive_authority_requires_approval") is True,
        "unknown_request_decision": "DENY",
        "automatic_promotion_enabled": False,
        "stage174_release_policy_registry_ready": entry_criteria.get("stage174_release_policy_registry_ready") is True,
        "contract_count": contract_catalog.get("contract_count", 0),
        "policy_rule_count": policy_precedence.get("policy_rule_count", 0),
        "authority_scope_count": authority_registry.get("authority_scope_count", 0),
        "approval_requirement_count": approval_matrix.get("approval_requirement_count", 0),
        "provider_default_calls": 0,
        "live_provider_call_count_in_release_gate": 0,
        "provider_generation_count": 0,
        "runtime_execution_count": 0,
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
        "next_stage": "stage174",
        "next_stage_title": "Release Policy and Registry",
        "parts": {"stage172_release_gate": _compact(stage172_gate), **parts},
    }
    result["governance_contract_checksum"] = _stable_digest(result)
    _write_json(root / TARGET_REPORT, result)
    _write_json(root / "release/current/stage173_summary.json", _compact(result))
    return result


def _blocked(issue: str) -> dict[str, Any]:
    return {
        "stage": "173",
        "baseline_stage": "172",
        "title": "Governance Contract",
        "status": "blocked",
        "issues": [issue],
        "mode": "GOVERNANCE_CONTRACT_ACTIVE",
        "page": "Page06 Governance Body",
        "governance_contract_only": True,
        "stage172_page05_seal_inherited": False,
        "stage174_release_policy_registry_ready": False,
        "default_authority_decision": "DENY",
        "provider_default_calls": 0,
        "node2_raw_reveal_access": 0,
        "branchpoint_lineage_preserved": False,
    }


def _build_page06_readiness(root: Path, stage172_gate: dict[str, Any], stage172_report: dict[str, Any], preflight: dict[str, Any], comparison: dict[str, Any]) -> dict[str, Any]:
    checks = {
        "stage172_release_gate_pass": _pass(stage172_gate.get("status") == "pass"),
        "page05_sealed": _pass(stage172_report.get("page05_sealed") is True or stage172_gate.get("page05_sealed") is True),
        "stage173_governance_ready": _pass(stage172_gate.get("stage173_governance_contract_ready") is True),
        "preflight_evidence_pass": _pass(preflight.get("status") == "pass" and preflight.get("preflight_guide_read") is True),
        "package_comparison_pass": _pass(comparison.get("status") == "pass" and comparison.get("procedure_evidence_enforced") is True),
        "page06_proposal_present": _pass((root / "docs/proposals/page06_governance_body_proposal.md").exists()),
        "page06_blueprint_present": _pass((root / "docs/architecture/page06_governance_body_blueprint.md").exists()),
        "page06_handoff_present": _pass((root / "docs/development/page06_developer_handoff.md").exists()),
    }
    issues = [name for name, check in checks.items() if check["status"] != "pass"]
    return {
        "stage": TARGET_STAGE,
        "title": "Page06 Readiness Matrix",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "stage172_page05_seal_inherited": not issues,
        "check_count": len(checks),
        "checks": checks,
    }


def _build_governance_contract_catalog() -> dict[str, Any]:
    objects = {
        "GovernanceAuthorityEnvelope": {
            "authority_id": "stage173_governance_authority_envelope",
            "source_stage": "stage172",
            "authority_scope": "release|project_boundary|lineage_review|operational",
            "default_decision": "DENY",
            "requires_approval_evidence": True,
            "provider_runtime_allowed": False,
            "write_runtime_allowed": False,
            "training_runtime_allowed": False,
        },
        "GovernanceDecision": {"status_space": ["ALLOW", "DENY", "DEFER"], "unknown_request": "DENY"},
        "PolicyRule": {"required_fields": ["policy_id", "policy_type", "precedence", "effect", "condition_ref"]},
        "PolicyPrecedence": {"tie_break": "policy_id", "deny_overrides_allow": True},
        "ApprovalRequirement": {"sensitive_authority_requires_approval": True},
        "ApprovalEvidenceRef": {"required": True, "source": "sealed_evidence"},
        "AuthorityScope": {"default_scope": "none", "explicit_scope_required": True},
        "MutationAuthority": {"default_decision": "DENY", "requires_approval_evidence": True},
        "ReleaseAuthority": {"automatic_promotion_enabled": False, "stage172_evidence_required": True},
        "CrossProjectAuthority": {"default_decision": "DENY", "read_only_by_policy": True},
        "LineageReviewAuthority": {"source_evidence_required": True, "rollback_requirement_required": True},
        "OperationalSafetyAuthority": {"rollback_plan_required": True},
        "RollbackAuthority": {"rollback_evidence_required": True},
    }
    return {
        "stage": TARGET_STAGE,
        "title": "Stage173 Governance Contract Catalog",
        "status": "pass",
        "issues": [],
        "contract_count": len(objects),
        "objects": objects,
    }


def _build_policy_precedence_matrix() -> dict[str, Any]:
    policies = [
        {"policy_id": "security_boundary_policy", "precedence": 10, "effect": "DENY", "deny_overrides_allow": True},
        {"policy_id": "source_boundary_policy", "precedence": 20, "effect": "DENY", "deny_overrides_allow": True},
        {"policy_id": "author_scope_policy", "precedence": 30, "effect": "DENY", "deny_overrides_allow": True},
        {"policy_id": "node_boundary_policy", "precedence": 40, "effect": "DENY", "deny_overrides_allow": True},
        {"policy_id": "release_policy", "precedence": 50, "effect": "DEFER", "deny_overrides_allow": True},
        {"policy_id": "lineage_review_policy", "precedence": 60, "effect": "DEFER", "deny_overrides_allow": True},
        {"policy_id": "operational_policy", "precedence": 70, "effect": "DEFER", "deny_overrides_allow": True},
        {"policy_id": "advisory_policy", "precedence": 80, "effect": "ALLOW", "deny_overrides_allow": True},
    ]
    precedence_values = [p["precedence"] for p in policies]
    issues: list[str] = []
    if len(precedence_values) != len(set(precedence_values)):
        issues.append("duplicate_policy_precedence")
    if policies != sorted(policies, key=lambda item: (item["precedence"], item["policy_id"])):
        issues.append("policy_order_not_deterministic")
    if any(p["effect"] not in {"ALLOW", "DENY", "DEFER"} for p in policies):
        issues.append("invalid_policy_effect")
    return {
        "stage": TARGET_STAGE,
        "title": "Stage173 Policy Precedence Matrix",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "default_decision": "DENY",
        "unknown_request_decision": "DENY",
        "deny_overrides_allow": True,
        "policy_rule_count": len(policies),
        "policies": policies,
    }


def _build_authority_scope_registry() -> dict[str, Any]:
    scopes = [
        {"scope": "release", "default_decision": "DENY", "automatic_execution_enabled": False},
        {"scope": "project_boundary", "default_decision": "DENY", "write_enabled": False},
        {"scope": "lineage_review", "default_decision": "DEFER", "source_evidence_required": True},
        {"scope": "operational", "default_decision": "DEFER", "rollback_required": True},
    ]
    issues = [scope["scope"] for scope in scopes if scope.get("default_decision") not in {"DENY", "DEFER"}]
    return {
        "stage": TARGET_STAGE,
        "title": "Stage173 Authority Scope Registry",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "authority_scope_count": len(scopes),
        "scopes": scopes,
        "automatic_promotion_enabled": False,
        "cross_project_write_enabled": False,
        "memory_write_enabled": False,
        "canon_mutation_enabled": False,
        "runtime_training_enabled": False,
    }


def _build_approval_requirement_matrix() -> dict[str, Any]:
    requirements = [
        {"authority": "release_promotion", "approval_required": True, "execution_enabled": False},
        {"authority": "manuscript_change", "approval_required": True, "execution_enabled": False},
        {"authority": "memory_change", "approval_required": True, "execution_enabled": False},
        {"authority": "canon_change", "approval_required": True, "execution_enabled": False},
        {"authority": "training_data_change", "approval_required": True, "execution_enabled": False},
        {"authority": "cross_project_data", "approval_required": True, "execution_enabled": False},
    ]
    issues = [item["authority"] for item in requirements if item.get("approval_required") is not True or item.get("execution_enabled") is not False]
    return {
        "stage": TARGET_STAGE,
        "title": "Stage173 Approval Requirement Matrix",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "approval_requirement_count": len(requirements),
        "sensitive_authority_requires_approval": True,
        "requirements": requirements,
    }


def _build_stage174_entry_criteria(*parts: dict[str, Any]) -> dict[str, Any]:
    issues = [part.get("title", "part") for part in parts if part.get("status") != "pass"]
    return {
        "stage": TARGET_STAGE,
        "title": "Stage174 Entry Criteria",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "stage174_release_policy_registry_ready": not issues,
        "required_next_stage": "stage174",
        "required_next_title": "Release Policy and Registry",
    }


def _pass(condition: bool) -> dict[str, str]:
    return {"status": "pass" if condition else "blocked"}


def _active_version(root: Path) -> str:
    manifest = root / "manifests/live_core_manifest.json"
    if not manifest.exists():
        return ""
    return json.loads(manifest.read_text(encoding="utf-8")).get("active_version", "")


def _load_json(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _stable_digest(payload: Any) -> str:
    data = json.dumps(payload, ensure_ascii=False, sort_keys=True).encode("utf-8")
    return hashlib.sha256(data).hexdigest()


def _compact(report: dict[str, Any]) -> dict[str, Any]:
    keep = (
        "status", "stage", "baseline_stage", "title", "issues", "mode", "page",
        "page05_sealed", "stage173_governance_contract_ready", "governance_contract_only",
        "stage172_page05_seal_inherited", "default_authority_decision",
        "deny_by_default", "stage174_release_policy_registry_ready",
        "provider_default_calls", "node2_raw_reveal_access", "branchpoint_lineage_preserved",
    )
    return {key: report.get(key) for key in keep if key in report}
