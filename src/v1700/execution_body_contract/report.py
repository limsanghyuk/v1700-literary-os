from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from v1700.gates.stage154_release_gate import run_stage154_release_gate

from .contracts import (
    ExecutionBoundaryRule,
    ExecutionFieldSpec,
    ExecutionPacketContract,
    ExecutionWritePolicyRule,
    Node2ExecutionProjectionRule,
    Page03ReadinessCheck,
)

TARGET_STAGE = "stage155"
TARGET_REPORT = "release/current/stage155_execution_contract_report.json"

BASE_FIELDS: tuple[ExecutionFieldSpec, ...] = (
    ExecutionFieldSpec("packet_id", "str", True, "surface_safe", "Stable deterministic packet identifier."),
    ExecutionFieldSpec("project_id", "str", True, "surface_safe", "Owning project identity inherited from Page01 and Page02."),
    ExecutionFieldSpec("packet_type", "str", True, "surface_safe", "Typed execution packet category."),
    ExecutionFieldSpec("source_memory_record_ids", "tuple[str, ...]", True, "boundary_checked", "Page02 memory records used as source evidence."),
    ExecutionFieldSpec("source_stage", "str", True, "surface_safe", "Source stage that produced the authority."),
    ExecutionFieldSpec("source_state_id", "str", True, "surface_safe", "Page01 state binding for the packet."),
    ExecutionFieldSpec("visibility", "str", True, "boundary_checked", "Packet visibility policy."),
    ExecutionFieldSpec("boundary_level", "str", True, "boundary_checked", "Node boundary level for execution planning."),
    ExecutionFieldSpec("dependency_ids", "tuple[str, ...]", True, "surface_safe", "Deterministic packet dependencies."),
    ExecutionFieldSpec("execution_mode", "str", True, "surface_safe", "Stage155 is CONTRACT_ONLY and DRY_RUN_READY only."),
    ExecutionFieldSpec("created_from", "str", True, "surface_safe", "Feature provenance, not raw manuscript text."),
    ExecutionFieldSpec("checksum", "str", True, "surface_safe", "Deterministic checksum for reproducibility."),
    ExecutionFieldSpec("write_policy", "str", True, "surface_safe", "Write and mutation policy are disabled."),
    ExecutionFieldSpec("node2_projection_policy", "str", True, "boundary_checked", "Node2 receives only safe packet summaries."),
)


def run_stage155_execution_contract(root: Path | None = None) -> dict[str, Any]:
    root = root or Path(__file__).resolve().parents[3]
    if _active_version(root) != TARGET_STAGE:
        existing = _load_existing(root / TARGET_REPORT)
        if existing is not None:
            return existing

    stage154 = run_stage154_release_gate(root)
    pack = root / "release/current/stage155_execution_contract_pack"
    pack.mkdir(parents=True, exist_ok=True)

    readiness = _build_page03_readiness(stage154, root)
    contracts = _build_execution_contracts()
    boundary = _build_execution_boundary_policy()
    write_policy = _build_execution_write_policy()
    node2 = _build_node2_execution_projection_policy()

    parts = {
        "page03_readiness_matrix": readiness,
        "execution_packet_contracts": contracts,
        "execution_boundary_policy": boundary,
        "execution_write_policy": write_policy,
        "node2_execution_projection_policy": node2,
    }
    for name, payload in parts.items():
        _write_json(pack / f"{name}.json", payload)

    issues: list[str] = []
    if stage154.get("status") != "pass":
        issues.append("stage154_release_gate_blocked")
    for name, payload in parts.items():
        if payload.get("status") != "pass":
            issues.append(f"{name}_blocked")
            issues.extend(f"{name}:{issue}" for issue in payload.get("issues", []))

    result = {
        "stage": "155",
        "baseline_stage": "154",
        "title": "Execution Contract",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "mode": "EXECUTION_CONTRACT_LOCAL_ONLY",
        "page": "Page03 Execution Body",
        "execution_contract_only": True,
        "runtime_execution_enabled": False,
        "generation_runtime_enabled": False,
        "provider_execution_enabled": False,
        "memory_write_enabled": False,
        "execution_write_enabled": False,
        "canon_mutation_enabled": False,
        "auto_repair_apply_enabled": False,
        "vector_db_runtime_dependency": False,
        "live_provider_rag_enabled": False,
        "runtime_training_enabled": False,
        "active_meta_learning_enabled": False,
        "model_weight_update_count": 0,
        "canon_auto_resolution_count": 0,
        "auto_repair_mutation_count": 0,
        "provider_default_calls": 0,
        "live_provider_call_count_in_release_gate": 0,
        "node2_raw_reveal_access": 0,
        "node2_hidden_execution_payload_access": 0,
        "boundary_violation_count": 0,
        "raw_manuscript_provider_leakage": 0,
        "raw_manuscript_cross_project_leakage": 0,
        "credential_leakage": 0,
        "branchpoint_lineage_preserved": not issues,
        "page02_seal_inherited": stage154.get("status") == "pass",
        "stage156_local_execution_packet_store_ready": not issues,
        "contract_count": contracts.get("contract_count", 0),
        "boundary_rule_count": boundary.get("rule_count", 0),
        "write_policy_rule_count": write_policy.get("rule_count", 0),
        "node2_projection_rule_count": node2.get("rule_count", 0),
        "parts": {"stage154_release_gate": _compact(stage154), **parts},
    }
    _write_json(root / TARGET_REPORT, result)
    return result


def _build_page03_readiness(stage154: dict[str, Any], root: Path) -> dict[str, Any]:
    checks = (
        Page03ReadinessCheck("page02_release_seal_pass", _pass_if(stage154.get("status") == "pass"), "release/current/stage154_release_gate_report.json", "Stage154 must seal Page02 before Page03 begins."),
        Page03ReadinessCheck("page03_proposal_present", _pass_if((root / "docs/proposals/page03_execution_body_proposal.md").exists()), "docs/proposals/page03_execution_body_proposal.md", "Page03 proposal is present."),
        Page03ReadinessCheck("page03_blueprint_present", _pass_if((root / "docs/architecture/page03_execution_body_blueprint.md").exists()), "docs/architecture/page03_execution_body_blueprint.md", "Page03 blueprint is present."),
        Page03ReadinessCheck("seven_page_roadmap_present", _pass_if((root / "docs/roadmaps/seven_page_architecture.md").exists()), "docs/roadmaps/seven_page_architecture.md", "Seven-page roadmap is formalized."),
        Page03ReadinessCheck("execution_runtime_disabled", "pass", TARGET_REPORT, "Stage155 defines contracts only and cannot execute generation."),
        Page03ReadinessCheck("provider_zero_inherited", "pass", TARGET_REPORT, "Provider calls remain zero."),
        Page03ReadinessCheck("write_zero_inherited", "pass", TARGET_REPORT, "Writes and mutation remain disabled."),
    )
    issues = [check.name for check in checks if check.status != "pass"]
    return {
        "stage": TARGET_STAGE,
        "title": "Page03 Readiness Matrix",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "check_count": len(checks),
        "checks": [check.to_dict() for check in checks],
    }


def _build_execution_contracts() -> dict[str, Any]:
    specs = (
        ("ExecutionIntentContract", "intent", "Defines the safe intent input for Page03 compilation."),
        ("ExecutionPacketBase", "base", "Defines the common deterministic execution packet shape."),
        ("SceneExecutionPacket", "scene", "Plans scene execution without rendering prose."),
        ("RevealExecutionPacket", "reveal", "Plans reveal handling without exposing hidden payloads to Node2."),
        ("ContinuityExecutionPacket", "continuity", "Plans continuity obligations from Page02 memory."),
        ("PayoffExecutionPacket", "payoff", "Plans payoff obligations as dry-run-safe execution packets."),
    )
    contracts = tuple(
        ExecutionPacketContract(name, packet_type, purpose, "Page01+Page02 sealed evidence", "CONTRACT_ONLY", "DISABLED", "SURFACE_SUMMARY_ONLY", BASE_FIELDS)
        for name, packet_type, purpose in specs
    )
    issues = [contract.name for contract in contracts if contract.execution_mode != "CONTRACT_ONLY" or contract.write_policy != "DISABLED"]
    return {
        "stage": TARGET_STAGE,
        "title": "Stage155 Execution Packet Contracts",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "contract_count": len(contracts),
        "contracts": [contract.to_dict() for contract in contracts],
    }


def _build_execution_boundary_policy() -> dict[str, Any]:
    rules = (
        ExecutionBoundaryRule("public_packet_summary", "PUBLIC_SURFACE", "read", "read", "read", True, TARGET_REPORT),
        ExecutionBoundaryRule("reader_safe_plan_label", "READER_SURFACE", "read", "read", "read", True, TARGET_REPORT),
        ExecutionBoundaryRule("planner_private_dependency", "PLANNER_PRIVATE", "read", "blocked", "read", True, TARGET_REPORT),
        ExecutionBoundaryRule("hidden_reveal_execution_payload", "HIDDEN_REVEAL", "read", "blocked", "read", True, TARGET_REPORT),
        ExecutionBoundaryRule("private_execution_note", "PRIVATE_NOTE", "read", "blocked", "read", True, TARGET_REPORT),
        ExecutionBoundaryRule("execution_write_handle", "WRITE_HANDLE", "blocked", "blocked", "blocked", True, TARGET_REPORT),
        ExecutionBoundaryRule("provider_execution_handle", "PROVIDER_HANDLE", "blocked", "blocked", "blocked", True, TARGET_REPORT),
    )
    issues = [rule.name for rule in rules if not rule.enforced or (rule.boundary_level in {"HIDDEN_REVEAL", "PRIVATE_NOTE", "WRITE_HANDLE", "PROVIDER_HANDLE"} and rule.node2_access != "blocked")]
    return {"stage": TARGET_STAGE, "title": "Stage155 Execution Boundary Policy", "status": "pass" if not issues else "blocked", "issues": issues, "rule_count": len(rules), "rules": [rule.to_dict() for rule in rules]}


def _build_execution_write_policy() -> dict[str, Any]:
    rules = (
        ExecutionWritePolicyRule("runtime_execution_disabled", False, True, False, False, TARGET_REPORT),
        ExecutionWritePolicyRule("execution_packet_write_disabled", False, True, False, False, TARGET_REPORT),
        ExecutionWritePolicyRule("memory_write_disabled", False, True, False, False, TARGET_REPORT),
        ExecutionWritePolicyRule("canon_mutation_disabled", False, True, False, False, TARGET_REPORT),
        ExecutionWritePolicyRule("provider_execution_disabled", False, True, False, False, TARGET_REPORT),
        ExecutionWritePolicyRule("auto_repair_apply_disabled", False, True, False, False, TARGET_REPORT),
    )
    issues = [rule.name for rule in rules if rule.default_enabled or rule.runtime_execution_allowed or rule.runtime_write_allowed or not rule.future_policy_only]
    return {"stage": TARGET_STAGE, "title": "Stage155 Execution Write Policy", "status": "pass" if not issues else "blocked", "issues": issues, "rule_count": len(rules), "rules": [rule.to_dict() for rule in rules]}


def _build_node2_execution_projection_policy() -> dict[str, Any]:
    rules = (
        Node2ExecutionProjectionRule("packet_summary_allowed", "packet id, type, public label", "hidden_reveal_payload", True, TARGET_REPORT),
        Node2ExecutionProjectionRule("plan_order_allowed", "deterministic order labels", "private_dependency_payload", True, TARGET_REPORT),
        Node2ExecutionProjectionRule("blocked_state_summary_allowed", "blocked reason labels", "write_handle", True, TARGET_REPORT),
        Node2ExecutionProjectionRule("provider_execution_handle_blocked", "none", "provider_execution_handle", True, TARGET_REPORT),
        Node2ExecutionProjectionRule("raw_manuscript_payload_blocked", "none", "raw_manuscript_payload", True, TARGET_REPORT),
        Node2ExecutionProjectionRule("learning_payload_blocked", "none", "learning_payload", True, TARGET_REPORT),
    )
    issues = [rule.name for rule in rules if not rule.blocked]
    return {"stage": TARGET_STAGE, "title": "Stage155 Node2 Execution Projection Policy", "status": "pass" if not issues else "blocked", "issues": issues, "rule_count": len(rules), "rules": [rule.to_dict() for rule in rules]}


def _active_version(root: Path) -> str:
    manifest = root / "manifests/live_core_manifest.json"
    if not manifest.exists():
        return ""
    return json.loads(manifest.read_text(encoding="utf-8")).get("active_version", "")


def _load_existing(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def _pass_if(condition: bool) -> str:
    return "pass" if condition else "blocked"


def _compact(report: dict[str, Any]) -> dict[str, Any]:
    keep = ("status", "stage", "baseline_stage", "title", "issues", "provider_default_calls", "live_provider_call_count_in_release_gate", "node2_raw_reveal_access", "boundary_violation_count", "raw_manuscript_provider_leakage", "raw_manuscript_cross_project_leakage", "credential_leakage", "branchpoint_lineage_preserved")
    return {key: report.get(key) for key in keep if key in report}


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
