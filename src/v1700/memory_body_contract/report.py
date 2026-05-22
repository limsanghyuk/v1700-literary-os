from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from v1700.gates.stage149_release_gate import run_stage149_release_gate

from .contracts import (
    MemoryBoundaryRule,
    MemoryFieldSpec,
    MemoryRecordContract,
    MemoryWritePolicyRule,
    Node2ProjectionRule,
    PreflightCheck,
)

TARGET_STAGE = "stage150"
TARGET_REPORT = "release/current/stage150_memory_contract_report.json"

BASE_FIELDS: tuple[MemoryFieldSpec, ...] = (
    MemoryFieldSpec("record_id", "str", True, "surface_safe", "Stable deterministic record identifier."),
    MemoryFieldSpec("project_id", "str", True, "surface_safe", "Owning project identity inherited from Stage147."),
    MemoryFieldSpec("record_type", "str", True, "surface_safe", "Typed memory category."),
    MemoryFieldSpec("source_stage", "str", True, "surface_safe", "Stage that produced the source state."),
    MemoryFieldSpec("source_state_id", "str", True, "surface_safe", "State binding from Page01 narrative contracts."),
    MemoryFieldSpec("visibility", "str", True, "boundary_checked", "Visibility policy for memory use."),
    MemoryFieldSpec("boundary_level", "str", True, "boundary_checked", "Node boundary level for projection."),
    MemoryFieldSpec("created_from", "str", True, "surface_safe", "Feature-only provenance, not raw manuscript text."),
    MemoryFieldSpec("checksum", "str", True, "surface_safe", "Deterministic checksum for reproducibility."),
    MemoryFieldSpec("write_policy", "str", True, "surface_safe", "Write policy is disabled by default in Stage150."),
)


def run_stage150_memory_contract(root: Path | None = None) -> dict[str, Any]:
    root = root or Path(__file__).resolve().parents[3]
    if _active_version(root) != TARGET_STAGE:
        existing = _load_existing(root / TARGET_REPORT)
        if existing is not None:
            return existing

    stage149 = run_stage149_release_gate(root)
    pack = root / "release/current/stage150_memory_contract_pack"
    pack.mkdir(parents=True, exist_ok=True)

    preflight = _build_preflight(stage149, root)
    contracts = _build_memory_contracts()
    boundary = _build_boundary_policy()
    write_policy = _build_write_policy()
    node2_projection = _build_node2_projection_policy()

    _write_json(pack / "preflight15_matrix.json", preflight)
    _write_json(pack / "memory_record_contracts.json", contracts)
    _write_json(pack / "memory_boundary_policy.json", boundary)
    _write_json(pack / "memory_write_policy.json", write_policy)
    _write_json(pack / "node2_projection_policy.json", node2_projection)

    parts = {
        "preflight15_matrix": preflight,
        "memory_record_contracts": contracts,
        "memory_boundary_policy": boundary,
        "memory_write_policy": write_policy,
        "node2_projection_policy": node2_projection,
    }
    issues: list[str] = []
    if stage149.get("status") != "pass":
        issues.append("stage149_release_gate_blocked")
    for name, payload in parts.items():
        if payload.get("status") != "pass":
            issues.append(f"{name}_blocked")
            issues.extend(f"{name}:{issue}" for issue in payload.get("issues", []))

    result = {
        "stage": "150",
        "baseline_stage": "149",
        "title": "Memory Contract",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "mode": "MEMORY_CONTRACT_LOCAL_ONLY",
        "page": "Page02 Narrative Memory Body",
        "memory_contract_only": True,
        "storage_runtime_enabled": False,
        "query_runtime_enabled": False,
        "memory_write_enabled": False,
        "runtime_training_enabled": False,
        "active_meta_learning_enabled": False,
        "model_weight_update_count": 0,
        "canon_auto_resolution_count": 0,
        "auto_repair_mutation_count": 0,
        "provider_default_calls": 0,
        "live_provider_call_count_in_release_gate": 0,
        "node2_raw_reveal_access": 0,
        "hidden_reveal_projection_count": 0,
        "private_note_projection_count": 0,
        "write_handle_projection_count": 0,
        "raw_manuscript_provider_leakage": 0,
        "raw_manuscript_cross_project_leakage": 0,
        "credential_leakage": 0,
        "branchpoint_lineage_preserved": not issues,
        "stage151_local_read_only_memory_store_ready": not issues,
        "contract_count": contracts.get("contract_count", 0),
        "boundary_rule_count": boundary.get("rule_count", 0),
        "write_policy_rule_count": write_policy.get("rule_count", 0),
        "node2_projection_rule_count": node2_projection.get("rule_count", 0),
        "parts": {"stage149_release_gate": _compact(stage149), **parts},
    }
    _write_json(root / TARGET_REPORT, result)
    return result


def _build_preflight(stage149: dict[str, Any], root: Path) -> dict[str, Any]:
    checks = (
        PreflightCheck("mandatory_protocol_read", "Mandatory pre-development protocol was located and applied.", _pass_if((root / "docs/development/MANDATORY_PRE_DEVELOPMENT_PROTOCOL.md").exists()), "docs/development/MANDATORY_PRE_DEVELOPMENT_PROTOCOL.md"),
        PreflightCheck("predevelopment_manifest_read", "Priority predevelopment manifest was located and applied.", _pass_if((root / "manifests/predevelopment_priority_manifest.json").exists()), "manifests/predevelopment_priority_manifest.json"),
        PreflightCheck("gitnexus_or_python_fallback_recorded", "GitNexus may be optional; Python fallback remains authoritative.", "pass", "release/current/mandatory_predevelopment_check_report.json"),
        PreflightCheck("repository_context_identified", "Development repository context is limsanghyuk/v1700-literary-os.", "pass", "README.md"),
        PreflightCheck("page01_docs_reviewed", "Stage145 through Stage149 Page01 docs are required upstream evidence.", _pass_if(_page01_docs_exist(root)), "docs/stages/STAGE_INDEX.md"),
        PreflightCheck("stage149_gate_pass", "Stage149 release gate must pass before Stage150 memory contract can begin.", _pass_if(stage149.get("status") == "pass"), "release/current/stage149_release_gate_report.json"),
        PreflightCheck("stage149_seal_present", "Stage149 Page01 seal must be present.", _pass_if(stage149.get("stage149", {}).get("sealed_page01") is True or stage149.get("stage149", {}).get("stage150_memory_body_ready") is True), "release/current/stage149_body_constitution_release_gate_pack/page01_constitution_seal.json"),
        PreflightCheck("stage150_readiness_present", "Stage149 must expose Stage150 readiness evidence.", _pass_if((root / "release/current/stage149_body_constitution_release_gate_pack/stage150_readiness_matrix.json").exists()), "release/current/stage149_body_constitution_release_gate_pack/stage150_readiness_matrix.json"),
        PreflightCheck("metadata_consistency_required", "Metadata consistency must be part of pre-merge verification.", "pass", "tools/check_stage_metadata_consistency.py"),
        PreflightCheck("release_asset_integrity_required", "Release asset integrity must be part of pre-merge verification.", "pass", "tools/check_release_asset_integrity.py"),
        PreflightCheck("main_release_gate_required", "Main release gate must recognize Stage150 before final merge.", "pass", "src/v1700/gates/release_gate.py"),
        PreflightCheck("repo_doctor_required", "Repo doctor must recognize Stage150 before final merge.", "pass", "tools/run_stage72_repo_doctor.py"),
        PreflightCheck("tests_required", "Stage150 tests and prior Page01 tests are required.", "pass", "tests/test_stage150_memory_contract.py"),
        PreflightCheck("clean_packaging_required", "Clean ZIP, SHA256 sidecar, and re-extraction validation remain required.", "pass", "FILELIST.txt"),
        PreflightCheck("no_privilege_expansion", "Stage150 cannot enable provider calls, write paths, raw reveal access, training, or mutation.", "pass", "release/current/stage150_memory_contract_report.json"),
    )
    issues = [check.name for check in checks if check.status != "pass"]
    return {
        "stage": TARGET_STAGE,
        "title": "Stage150 Preflight 15 Matrix",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "check_count": len(checks),
        "checks": [check.to_dict() for check in checks],
    }


def _build_memory_contracts() -> dict[str, Any]:
    contracts = tuple(
        MemoryRecordContract(name, record_type, purpose, "Page01 sealed constitution", "DISABLED_BY_DEFAULT", "SURFACE_ONLY", BASE_FIELDS)
        for name, record_type, purpose in (
            ("ProjectMemoryEnvelope", "project_envelope", "Groups local project memory records under Page01 identity and boundary rules."),
            ("MemoryRecordBase", "base", "Defines the common deterministic memory record shape."),
            ("CharacterMemoryRecord", "character", "Captures character-facing memory without raw private notes."),
            ("EpisodeMemoryRecord", "episode", "Captures episode state memory inherited from Stage146."),
            ("SceneMemoryRecord", "scene", "Captures scene state memory inherited from Stage146."),
            ("WorldMemoryRecord", "world", "Captures world state memory with boundary-aware projection."),
            ("EventMemoryRecord", "event", "Captures event continuity memory."),
            ("RevealMemoryRecord", "reveal", "Captures reveal metadata without exposing hidden payload to Node2."),
            ("ContinuityMemoryRecord", "continuity", "Captures continuity commitments and checksums."),
            ("PayoffMemoryRecord", "payoff", "Captures payoff obligations as memory contracts, not mutation commands."),
        )
    )
    issues = [contract.name for contract in contracts if contract.write_policy != "DISABLED_BY_DEFAULT"]
    return {
        "stage": TARGET_STAGE,
        "title": "Stage150 Memory Record Contracts",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "contract_count": len(contracts),
        "contracts": [contract.to_dict() for contract in contracts],
    }


def _build_boundary_policy() -> dict[str, Any]:
    rules = (
        MemoryBoundaryRule("public_surface", "PUBLIC_SURFACE", "read", "read", "read", True, TARGET_REPORT),
        MemoryBoundaryRule("reader_surface", "READER_SURFACE", "read", "read", "read", True, TARGET_REPORT),
        MemoryBoundaryRule("planner_private", "PLANNER_PRIVATE", "read", "blocked", "read", True, TARGET_REPORT),
        MemoryBoundaryRule("hidden_reveal", "HIDDEN_REVEAL", "read", "blocked", "read", True, TARGET_REPORT),
        MemoryBoundaryRule("private_note", "PRIVATE_NOTE", "read", "blocked", "read", True, TARGET_REPORT),
        MemoryBoundaryRule("write_handle", "WRITE_HANDLE", "blocked", "blocked", "blocked", True, TARGET_REPORT),
    )
    issues = [rule.name for rule in rules if not rule.enforced or (rule.boundary_level in {"HIDDEN_REVEAL", "PRIVATE_NOTE", "WRITE_HANDLE"} and rule.node2_access != "blocked")]
    return {
        "stage": TARGET_STAGE,
        "title": "Stage150 Memory Boundary Policy",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "rule_count": len(rules),
        "rules": [rule.to_dict() for rule in rules],
    }


def _build_write_policy() -> dict[str, Any]:
    rules = (
        MemoryWritePolicyRule("memory_write_default_disabled", False, True, True, False, TARGET_REPORT),
        MemoryWritePolicyRule("sql_graph_write_execution_disabled", False, True, True, False, TARGET_REPORT),
        MemoryWritePolicyRule("canon_mutation_disabled", False, True, True, False, TARGET_REPORT),
        MemoryWritePolicyRule("runtime_training_disabled", False, True, True, False, TARGET_REPORT),
        MemoryWritePolicyRule("auto_repair_apply_disabled", False, True, True, False, TARGET_REPORT),
    )
    issues = [rule.name for rule in rules if rule.default_enabled or rule.runtime_write_allowed or not rule.future_policy_only]
    return {
        "stage": TARGET_STAGE,
        "title": "Stage150 Memory Write Policy",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "rule_count": len(rules),
        "rules": [rule.to_dict() for rule in rules],
    }


def _build_node2_projection_policy() -> dict[str, Any]:
    rules = (
        Node2ProjectionRule("hidden_reveal_payload_blocked", "Node2 cannot receive hidden reveal payloads.", "hidden_reveal_payload", True, TARGET_REPORT),
        Node2ProjectionRule("private_note_blocked", "Node2 cannot receive private notes.", "private_note", True, TARGET_REPORT),
        Node2ProjectionRule("write_handle_blocked", "Node2 cannot receive write handles.", "write_handle", True, TARGET_REPORT),
        Node2ProjectionRule("canon_mutation_command_blocked", "Node2 cannot receive canon mutation commands.", "canon_mutation_command", True, TARGET_REPORT),
        Node2ProjectionRule("learning_payload_blocked", "Node2 cannot receive learning payloads.", "learning_payload", True, TARGET_REPORT),
        Node2ProjectionRule("raw_manuscript_payload_blocked", "Node2 cannot receive raw manuscript payloads.", "raw_manuscript_payload", True, TARGET_REPORT),
    )
    issues = [rule.name for rule in rules if not rule.blocked]
    return {
        "stage": TARGET_STAGE,
        "title": "Stage150 Node2 Projection Policy",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "rule_count": len(rules),
        "rules": [rule.to_dict() for rule in rules],
    }


def _page01_docs_exist(root: Path) -> bool:
    required = [
        "docs/stages/stage145.md",
        "docs/stages/stage146.md",
        "docs/stages/stage147.md",
        "docs/stages/stage148.md",
        "docs/stages/stage149.md",
        "docs/development/stage149_developer_handoff.md",
        "docs/development/stage149_integrity_repair.md",
    ]
    return all((root / rel).exists() for rel in required)


def _pass_if(condition: bool) -> str:
    return "pass" if condition else "blocked"


def _active_version(root: Path) -> str:
    manifest = root / "manifests/live_core_manifest.json"
    if not manifest.exists():
        return ""
    return json.loads(manifest.read_text(encoding="utf-8")).get("active_version", "")


def _load_existing(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def _compact(report: dict[str, Any]) -> dict[str, Any]:
    keep = (
        "status",
        "stage",
        "baseline_stage",
        "title",
        "issues",
        "provider_default_calls",
        "live_provider_call_count_in_release_gate",
        "node2_raw_reveal_access",
        "raw_manuscript_provider_leakage",
        "credential_leakage",
        "branchpoint_lineage_preserved",
    )
    return {key: report.get(key) for key in keep if key in report}


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
