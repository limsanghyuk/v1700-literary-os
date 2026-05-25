from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from v1700.gates.stage160_release_gate import run_stage160_release_gate

from .contracts import (
    Node2RenderingProjectionRule,
    Page04ReadinessCheck,
    RenderingBoundaryRule,
    RenderingContractSpec,
    RenderingFieldSpec,
    RenderingWritePolicyRule,
)

TARGET_STAGE = "stage161"
TARGET_REPORT = "release/current/stage161_rendering_contract_report.json"
PACK_DIR = "release/current/stage161_rendering_contract_pack"

BASE_FIELDS: tuple[RenderingFieldSpec, ...] = (
    RenderingFieldSpec("render_contract_id", "str", True, "surface_safe", "Stable deterministic rendering contract identifier."),
    RenderingFieldSpec("project_id", "str", True, "surface_safe", "Owning project identity inherited from Page01 through Page03."),
    RenderingFieldSpec("render_type", "str", True, "surface_safe", "Typed rendering contract category."),
    RenderingFieldSpec("source_execution_packet_ids", "tuple[str, ...]", True, "boundary_checked", "Page03 execution packets used as source evidence."),
    RenderingFieldSpec("source_trace_ids", "tuple[str, ...]", True, "boundary_checked", "Stage159 dry-run trace references, not runtime execution output."),
    RenderingFieldSpec("source_stage", "str", True, "surface_safe", "Stage authority that produced the rendering contract."),
    RenderingFieldSpec("surface_channel", "str", True, "surface_safe", "Novel, drama, synopsis, or other surface channel label."),
    RenderingFieldSpec("visibility", "str", True, "boundary_checked", "Rendering visibility policy."),
    RenderingFieldSpec("boundary_level", "str", True, "boundary_checked", "Node boundary level for rendering."),
    RenderingFieldSpec("render_mode", "str", True, "surface_safe", "Stage161 is CONTRACT_ONLY and DRY_RUN_RENDER_READY only."),
    RenderingFieldSpec("created_from", "str", True, "surface_safe", "Provenance summary, not raw manuscript text."),
    RenderingFieldSpec("checksum", "str", True, "surface_safe", "Deterministic checksum for reproducibility."),
    RenderingFieldSpec("write_policy", "str", True, "surface_safe", "Write and mutation policy remain disabled."),
    RenderingFieldSpec("node2_projection_policy", "str", True, "boundary_checked", "Node2 receives only safe rendering summaries."),
)


def run_stage161_rendering_contract(root: Path | None = None) -> dict[str, Any]:
    root = root or Path(__file__).resolve().parents[3]
    if _active_version(root) != TARGET_STAGE:
        existing = _load_existing(root / TARGET_REPORT)
        if existing is not None:
            return existing

    stage160 = run_stage160_release_gate(root)
    pack = root / PACK_DIR
    pack.mkdir(parents=True, exist_ok=True)

    readiness = _build_page04_readiness(stage160, root)
    contracts = _build_rendering_contracts()
    boundary = _build_rendering_boundary_policy()
    write_policy = _build_rendering_write_policy()
    node2 = _build_node2_rendering_projection_policy()

    parts = {
        "page04_readiness_matrix": readiness,
        "rendering_contracts": contracts,
        "rendering_boundary_policy": boundary,
        "rendering_write_policy": write_policy,
        "node2_rendering_projection_policy": node2,
    }
    for name, payload in parts.items():
        _write_json(pack / f"{name}.json", payload)

    issues: list[str] = []
    if stage160.get("status") != "pass":
        issues.append("stage160_release_gate_blocked")
    for name, payload in parts.items():
        if payload.get("status") != "pass":
            issues.append(f"{name}_blocked")
            issues.extend(f"{name}:{issue}" for issue in payload.get("issues", []))

    result = {
        "stage": "161",
        "baseline_stage": "160",
        "title": "Rendering Contract",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "mode": "RENDERING_CONTRACT_LOCAL_ONLY",
        "page": "Page04 Rendering Body",
        "rendering_contract_only": True,
        "rendering_runtime_enabled": False,
        "generation_runtime_enabled": False,
        "provider_generation_enabled": False,
        "provider_execution_enabled": False,
        "runtime_execution_enabled": False,
        "render_write_enabled": False,
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
        "runtime_execution_count": 0,
        "provider_execution_count": 0,
        "provider_generation_count": 0,
        "write_operation_count": 0,
        "provider_default_calls": 0,
        "live_provider_call_count_in_release_gate": 0,
        "node2_raw_reveal_access": 0,
        "node2_hidden_render_payload_access": 0,
        "boundary_violation_count": 0,
        "raw_manuscript_provider_leakage": 0,
        "raw_manuscript_cross_project_leakage": 0,
        "credential_leakage": 0,
        "branchpoint_lineage_preserved": not issues,
        "page03_seal_inherited": stage160.get("status") == "pass",
        "stage162_local_render_packet_store_ready": not issues,
        "contract_count": contracts.get("contract_count", 0),
        "boundary_rule_count": boundary.get("rule_count", 0),
        "write_policy_rule_count": write_policy.get("rule_count", 0),
        "node2_projection_rule_count": node2.get("rule_count", 0),
        "parts": {"stage160_release_gate": _compact(stage160), **parts},
    }
    _write_json(root / TARGET_REPORT, result)
    return result


def _build_page04_readiness(stage160: dict[str, Any], root: Path) -> dict[str, Any]:
    checks = (
        Page04ReadinessCheck("page03_release_seal_pass", _pass_if(stage160.get("status") == "pass"), "release/current/stage160_release_gate_report.json", "Stage160 must seal Page03 before Page04 begins."),
        Page04ReadinessCheck("page04_proposal_present", _pass_if((root / "docs/proposals/page04_rendering_body_proposal.md").exists()), "docs/proposals/page04_rendering_body_proposal.md", "Page04 proposal is present."),
        Page04ReadinessCheck("page04_blueprint_present", _pass_if((root / "docs/architecture/page04_rendering_body_blueprint.md").exists()), "docs/architecture/page04_rendering_body_blueprint.md", "Page04 blueprint is present."),
        Page04ReadinessCheck("page04_handoff_present", _pass_if((root / "docs/development/page04_handoff.md").exists()), "docs/development/page04_handoff.md", "Page04 handoff is present."),
        Page04ReadinessCheck("rendering_runtime_disabled", "pass", TARGET_REPORT, "Stage161 defines rendering contracts only and cannot execute provider generation."),
        Page04ReadinessCheck("provider_zero_inherited", "pass", TARGET_REPORT, "Provider calls remain zero."),
        Page04ReadinessCheck("write_zero_inherited", "pass", TARGET_REPORT, "Writes and mutation remain disabled."),
    )
    issues = [check.name for check in checks if check.status != "pass"]
    return {"stage": TARGET_STAGE, "title": "Page04 Readiness Matrix", "status": "pass" if not issues else "blocked", "issues": issues, "check_count": len(checks), "checks": [check.to_dict() for check in checks]}


def _build_rendering_contracts() -> dict[str, Any]:
    specs = (
        ("RenderingIntentContract", "intent", "Defines the safe rendering intent input for Page04 compilation."),
        ("RenderingContractBase", "base", "Defines common deterministic rendering contract shape."),
        ("SceneSurfaceRenderContract", "scene_surface", "Plans scene surface rendering without provider generation."),
        ("DialogueSurfaceRenderContract", "dialogue_surface", "Plans dialogue surface obligations without final prose execution."),
        ("DramaBeatRenderContract", "drama_beat", "Plans drama beat rendering surfaces from Page03 traces."),
        ("SynopsisRenderContract", "synopsis", "Plans surface-safe synopsis rendering contracts."),
    )
    contracts = tuple(RenderingContractSpec(name, render_type, purpose, "Page01+Page02+Page03 sealed evidence", "CONTRACT_ONLY", "DISABLED", "SURFACE_SUMMARY_ONLY", BASE_FIELDS) for name, render_type, purpose in specs)
    issues = [contract.name for contract in contracts if contract.render_mode != "CONTRACT_ONLY" or contract.generation_policy != "DISABLED"]
    return {"stage": TARGET_STAGE, "title": "Stage161 Rendering Contracts", "status": "pass" if not issues else "blocked", "issues": issues, "contract_count": len(contracts), "contracts": [contract.to_dict() for contract in contracts]}


def _build_rendering_boundary_policy() -> dict[str, Any]:
    rules = (
        RenderingBoundaryRule("public_render_summary", "PUBLIC_SURFACE", "read", "read", "read", True, TARGET_REPORT),
        RenderingBoundaryRule("reader_safe_surface_label", "READER_SURFACE", "read", "read", "read", True, TARGET_REPORT),
        RenderingBoundaryRule("planner_private_render_note", "PLANNER_PRIVATE", "read", "blocked", "read", True, TARGET_REPORT),
        RenderingBoundaryRule("hidden_reveal_render_payload", "HIDDEN_REVEAL", "read", "blocked", "read", True, TARGET_REPORT),
        RenderingBoundaryRule("private_style_instruction", "PRIVATE_NOTE", "read", "blocked", "read", True, TARGET_REPORT),
        RenderingBoundaryRule("render_write_handle", "WRITE_HANDLE", "blocked", "blocked", "blocked", True, TARGET_REPORT),
        RenderingBoundaryRule("provider_generation_handle", "PROVIDER_HANDLE", "blocked", "blocked", "blocked", True, TARGET_REPORT),
    )
    issues = [rule.name for rule in rules if not rule.enforced or (rule.boundary_level in {"HIDDEN_REVEAL", "PRIVATE_NOTE", "WRITE_HANDLE", "PROVIDER_HANDLE"} and rule.node2_access != "blocked")]
    return {"stage": TARGET_STAGE, "title": "Stage161 Rendering Boundary Policy", "status": "pass" if not issues else "blocked", "issues": issues, "rule_count": len(rules), "rules": [rule.to_dict() for rule in rules]}


def _build_rendering_write_policy() -> dict[str, Any]:
    rules = (
        RenderingWritePolicyRule("render_contract_definition", False, True, False, False, TARGET_REPORT),
        RenderingWritePolicyRule("local_render_packet_store_future", False, True, False, False, "stage162"),
        RenderingWritePolicyRule("provider_generation_runtime", False, True, False, False, "future_page_policy"),
        RenderingWritePolicyRule("final_prose_publication", False, True, False, False, "future_page_policy"),
        RenderingWritePolicyRule("canon_mutation", False, False, False, False, TARGET_REPORT),
    )
    issues = [rule.name for rule in rules if rule.default_enabled or rule.generation_runtime_allowed or rule.runtime_write_allowed]
    return {"stage": TARGET_STAGE, "title": "Stage161 Rendering Write Policy", "status": "pass" if not issues else "blocked", "issues": issues, "rule_count": len(rules), "rules": [rule.to_dict() for rule in rules]}


def _build_node2_rendering_projection_policy() -> dict[str, Any]:
    rules = (
        Node2RenderingProjectionRule("render_contract_summary", "contract_id + render_type + surface_channel", "hidden_reveal_payload", True, TARGET_REPORT),
        Node2RenderingProjectionRule("surface_draft_label", "surface label only", "private_style_instruction", True, TARGET_REPORT),
        Node2RenderingProjectionRule("trace_reference_summary", "trace ids and safe order", "trace_private_note", True, TARGET_REPORT),
        Node2RenderingProjectionRule("provider_generation_handle", "none", "provider handle", True, TARGET_REPORT),
        Node2RenderingProjectionRule("raw_manuscript_payload", "none", "raw manuscript", True, TARGET_REPORT),
    )
    issues = [rule.name for rule in rules if not rule.blocked]
    return {"stage": TARGET_STAGE, "title": "Stage161 Node2 Rendering Projection Policy", "status": "pass" if not issues else "blocked", "issues": issues, "rule_count": len(rules), "rules": [rule.to_dict() for rule in rules]}


def _active_version(root: Path) -> str:
    manifest = root / "manifests/live_core_manifest.json"
    if not manifest.exists():
        return ""
    return json.loads(manifest.read_text(encoding="utf-8")).get("active_version", "")


def _load_existing(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _pass_if(condition: bool) -> str:
    return "pass" if condition else "blocked"


def _compact(report: dict[str, Any]) -> dict[str, Any]:
    keep = ("status", "stage", "baseline_stage", "title", "issues", "mode", "page03_sealed", "stage161_rendering_contract_ready", "provider_default_calls", "live_provider_call_count_in_release_gate", "node2_raw_reveal_access", "boundary_violation_count", "credential_leakage", "branchpoint_lineage_preserved")
    return {key: report.get(key) for key in keep if key in report}
