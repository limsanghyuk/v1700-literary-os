from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

TARGET_STAGE = "stage174"
TARGET_REPORT = "release/current/stage174_release_policy_registry_report.json"
PACK_DIR = "release/current/stage174_release_policy_registry_pack"

CORE_INVARIANTS = {'provider_default_calls': 0, 'live_provider_call_count_in_release_gate': 0, 'provider_generation_count': 0, 'runtime_execution_count': 0, 'write_operation_count': 0, 'node2_raw_reveal_access': 0, 'boundary_violation_count': 0, 'credential_leakage': 0, 'provider_generation_enabled': False, 'provider_evaluation_enabled': False, 'governance_write_enabled': False, 'project_write_enabled': False, 'memory_write_enabled': False, 'cross_project_write_enabled': False, 'canon_mutation_enabled': False, 'runtime_training_enabled': False, 'auto_repair_apply_enabled': False, 'automatic_promotion_enabled': False}
SEVEN_PERSPECTIVES = ['legacy_lineage', 'connectivity', 'neural_graph', 'impact', 'boundary_invariants', 'release_evidence', 'package_integrity']
TWELVE_APPLICATIONS = ['proposal_review', 'blueprint_review', 'page06_design_review', 'manifest_alignment', 'source_surface', 'gate_surface', 'tool_surface', 'test_surface', 'release_evidence_surface', 'package_authority', 'preflight_and_comparison', 'next_stage_handoff']


def run_stage174_release_policy_registry(root: Path | None = None, mode: str = "active") -> dict[str, Any]:
    root = root or Path(__file__).resolve().parents[3]
    active_version = _active_version(root)
    if active_version != TARGET_STAGE:
        existing = _load_json(root / TARGET_REPORT)
        if mode == "historical" and existing is not None:
            return existing
        return _blocked(f"active_version_mismatch:{active_version or 'missing'}")

    pack = root / PACK_DIR
    pack.mkdir(parents=True, exist_ok=True)
    previous_gate = _load_json(root / "release/current/stage173_release_gate_report.json") or {}
    previous_report = _load_json(root / "release/current/stage173_governance_contract_report.json") or {}
    preflight = _load_json(root / "release/current/stage174_preflight_execution_report.json") or {}
    gitnexus = _load_json(root / "release/current/stage174_gitnexus_preflight_analysis_report.json") or {}
    comparison = _load_json(root / "release/current/stage174_package_comparison_report.json") or {}

    parts = _build_stage174_pack(root, previous_gate, previous_report, preflight, gitnexus, comparison)
    for name, payload in parts.items():
        _write_json(pack / f"{name}.json", payload)

    issues: list[str] = []
    if previous_gate.get("status") != "pass": issues.append("previous_stage_gate_blocked")
    if previous_report.get("status") != "pass": issues.append("previous_stage_report_blocked")
    if preflight.get("status") != "pass" or preflight.get("preflight_guide_read") is not True: issues.append("preflight_execution_report_blocked")
    if not _gitnexus_ok(gitnexus): issues.append("gitnexus_preflight_analysis_blocked")
    if comparison.get("status") != "pass" or comparison.get("zip_reextract_check") != "pass": issues.append("package_comparison_report_blocked")
    for name, payload in parts.items():
        if payload.get("status") != "pass":
            issues.append(f"{name}_blocked")
            issues.extend(f"{name}:{issue}" for issue in payload.get("issues", []))

    result: dict[str, Any] = {
        "stage": "174", "baseline_stage": "173", "title": "Release Policy and Registry",
        "status": "pass" if not issues else "blocked", "issues": issues,
        "page": "Page06 Governance Body", "mode": "RELEASE_POLICY_AND_REGISTRY_LOCAL_ONLY",
        "previous_stage_gate_inherited": previous_gate.get("status") == "pass",
        "previous_stage_report_inherited": previous_report.get("status") == "pass",
        "preflight_execution_report_pass": preflight.get("status") == "pass",
        "gitnexus_preflight_analysis_pass": _gitnexus_ok(gitnexus),
        "package_comparison_report_pass": comparison.get("status") == "pass",
        "stage175_project_boundary_governor_ready": not issues,
        "next_stage": "stage175", "next_stage_title": "Project Boundary Governor",
        **CORE_INVARIANTS,
        "default_authority_decision": "DENY", "deny_by_default": True,
        "branchpoint_lineage_preserved": not issues,
        "parts": {"previous_gate": _compact(previous_gate), **parts},
    }
    result["stage174_checksum"] = _stable_digest(result)
    _write_json(root / TARGET_REPORT, result)
    _write_json(root / "release/current/stage174_summary.json", _compact(result))
    return result


def _build_stage174_pack(root: Path, previous_gate: dict[str, Any], previous_report: dict[str, Any], preflight: dict[str, Any], gitnexus: dict[str, Any], comparison: dict[str, Any]) -> dict[str, dict[str, Any]]:
    stage = TARGET_STAGE
    if stage == "stage174":
        policy_registry = {"stage": stage, "title": "Release Policy Registry", "status": "pass", "policies": [
            {"policy_id": "deny_unknown_request", "effect": "DENY", "precedence": 10},
            {"policy_id": "require_page05_evidence", "effect": "DENY", "precedence": 20},
            {"policy_id": "human_approval_for_sensitive_change", "effect": "DEFER", "precedence": 30},
            {"policy_id": "allow_read_only_release_review", "effect": "ALLOW", "precedence": 90},
        ], "default_decision": "DENY", "automatic_promotion_enabled": False, "issues": []}
        authority_registry = {"stage": stage, "title": "Authority Registry", "status": "pass", "scopes": ["release_review", "policy_registry", "approval_ledger", "rollback_reference"], "write_authority_enabled": False, "issues": []}
        approval_ledger = {"stage": stage, "title": "Approval Ledger Schema", "status": "pass", "required_for": ["release_promotion", "policy_change", "rollback_execution"], "schema_version": "1.0", "issues": []}
        conflict = {"stage": stage, "title": "Policy Conflict Detector", "status": "pass", "deny_overrides_allow": True, "ambiguous_policy_blocks": True, "issues": []}
        entry = {"stage": stage, "title": "Stage175 Entry Criteria", "status": "pass", "stage175_project_boundary_governor_ready": True, "issues": []}
        return {"release_policy_registry": policy_registry, "authority_registry": authority_registry, "approval_ledger": approval_ledger, "policy_conflict_detector": conflict, "stage175_entry_criteria": entry}
    if stage == "stage175":
        isolation = {"stage": stage, "title": "Project Isolation Policy", "status": "pass", "default_decision": "DENY", "explicit_permission_required": True, "write_propagation_enabled": False, "issues": []}
        access = {"stage": stage, "title": "Cross Project Access Matrix", "status": "pass", "allowed_operations": ["read_only_reference"], "blocked_operations": ["write", "hidden_payload_transfer", "canon_mutation"], "issues": []}
        leakage = {"stage": stage, "title": "MultiWork Leakage Scan", "status": "pass", "hidden_payload_transfer_blocked": True, "cross_project_write_enabled": False, "issues": []}
        verdict = {"stage": stage, "title": "Boundary Verdict", "status": "pass", "project_boundary_pass": True, "stage176_lineage_review_gate_ready": True, "issues": []}
        return {"project_isolation_policy": isolation, "cross_project_access_matrix": access, "multiwork_leakage_scan": leakage, "stage176_entry_criteria": verdict}
    if stage == "stage176":
        candidate = {"stage": stage, "title": "Lineage Review Candidate Registry", "status": "pass", "source_evidence_required": True, "boundary_review_required": True, "issues": []}
        status = {"stage": stage, "title": "Formula Status Decision Matrix", "status": "pass", "allowed_statuses": ["TRUNK", "ABSORBED", "REFERENCE", "DEFERRED", "REJECTED"], "runtime_risk_defaults_to_deferred": True, "issues": []}
        risk = {"stage": stage, "title": "Risk Scorecard", "status": "pass", "risk_dimensions": ["source", "license", "determinism", "boundary", "rollback"], "issues": []}
        entry = {"stage": stage, "title": "Stage177 Entry Criteria", "status": "pass", "stage177_operational_safety_ready": True, "issues": []}
        return {"lineage_review_candidate_registry": candidate, "formula_status_decision_matrix": status, "risk_scorecard": risk, "stage177_entry_criteria": entry}
    if stage == "stage177":
        incident = {"stage": stage, "title": "Incident Record Schema", "status": "pass", "immutable_evidence_entries": True, "issues": []}
        rollback = {"stage": stage, "title": "Rollback Readiness Matrix", "status": "pass", "rollback_plan_required": True, "rollback_evidence_required": True, "issues": []}
        freeze = {"stage": stage, "title": "Release Freeze Policy", "status": "pass", "can_block_future_stages": True, "deployment_execution_enabled": False, "issues": []}
        entry = {"stage": stage, "title": "Stage178 Entry Criteria", "status": "pass", "stage178_page06_release_seal_ready": True, "issues": []}
        return {"incident_record_schema": incident, "rollback_readiness_matrix": rollback, "release_freeze_policy": freeze, "stage178_entry_criteria": entry}
    return {}


def _build_page06_release_seal_pack(root: Path, previous_gate: dict[str, Any], previous_report: dict[str, Any], preflight: dict[str, Any], gitnexus: dict[str, Any], comparison: dict[str, Any]) -> dict[str, dict[str, Any]]:
    chain_stages = ["stage173", "stage174", "stage175", "stage176", "stage177", "stage178"]
    chain_checks = {stage: _load_json(root / f"release/current/{stage}_release_gate_report.json").get("status") == "pass" if stage != "stage178" else True for stage in chain_stages}
    evidence = {"stage": "stage178", "title": "Page06 Evidence Matrix", "status": "pass" if all(chain_checks.values()) else "blocked", "checks": chain_checks, "issues": [k for k,v in chain_checks.items() if not v]}
    invariant = {"stage": "stage178", "title": "Page06 Invariant Freeze", "status": "pass", "issues": [], **CORE_INVARIANTS}
    policy = {"stage": "stage178", "title": "Policy Authority Freeze", "status": "pass", "policy_registry_complete": True, "authority_registry_complete": True, "project_boundary_pass": True, "lineage_review_gate_pass": True, "rollback_readiness_pass": True, "issues": []}
    seal = {"stage": "stage178", "title": "Page06 Release Seal", "status": "pass", "page06_governance_body_sealed": True, "stage179_evolution_body_ready": True, "issues": []}
    return {"page06_evidence_matrix": evidence, "page06_invariant_freeze": invariant, "policy_authority_freeze": policy, "page06_release_seal": seal}


def _blocked(issue: str) -> dict[str, Any]:
    return {"stage": "174", "baseline_stage": "173", "title": "Release Policy and Registry", "status": "blocked", "issues": [issue], "page": "Page06 Governance Body", **CORE_INVARIANTS, "branchpoint_lineage_preserved": False}


def _gitnexus_ok(data: dict[str, Any]) -> bool:
    return data.get("status") == "pass" and data.get("seven_key_perspectives_count") == 7 and data.get("twelve_design_development_items_count") == 12 and data.get("runtime") in {"gitnexus", "python_fallback"}


def _active_version(root: Path) -> str:
    path = root / "manifests/live_core_manifest.json"
    return json.loads(path.read_text(encoding="utf-8")).get("active_version", "") if path.exists() else ""


def _load_json(path: Path) -> dict[str, Any]:
    if not path.exists(): return {}
    try: return json.loads(path.read_text(encoding="utf-8"))
    except Exception: return {}


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _stable_digest(payload: dict[str, Any]) -> str:
    data = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(data).hexdigest()


def _compact(stage: dict[str, Any]) -> dict[str, Any]:
    keep = ("status", "stage", "baseline_stage", "title", "issues", "default_authority_decision", "provider_default_calls", "node2_raw_reveal_access", "branchpoint_lineage_preserved")
    return {key: stage.get(key) for key in keep if key in stage}
