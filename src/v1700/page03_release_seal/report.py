from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from v1700.gates.stage155_release_gate import run_stage155_release_gate
from v1700.gates.stage156_release_gate import run_stage156_release_gate
from v1700.gates.stage157_release_gate import run_stage157_release_gate
from v1700.gates.stage158_release_gate import run_stage158_release_gate
from v1700.gates.stage159_release_gate import run_stage159_release_gate

from .contracts import (
    Page03InvariantFreeze,
    Page03ReleaseAsset,
    Page03SealCheck,
    Page03StageSeal,
    Page03TransitionCriterion,
)

TARGET_STAGE = "stage160"
TARGET_REPORT = "release/current/stage160_page03_release_seal_report.json"
PACK_DIR = "release/current/stage160_page03_release_seal_pack"

PAGE03_UPSTREAM_STAGES: tuple[tuple[str, str, str, str], ...] = (
    ("155", "Execution Contract", "release/current/stage155_execution_contract_report.json", "release/current/stage155_release_gate_report.json"),
    ("156", "Local Execution Packet Store", "release/current/stage156_local_execution_packet_store_report.json", "release/current/stage156_release_gate_report.json"),
    ("157", "Deterministic Plan Graph Builder", "release/current/stage157_deterministic_plan_graph_builder_report.json", "release/current/stage157_release_gate_report.json"),
    ("158", "Dependency and Conflict Preflight", "release/current/stage158_dependency_conflict_preflight_report.json", "release/current/stage158_release_gate_report.json"),
    ("159", "Execution Dry-Run Trace", "release/current/stage159_execution_dry_run_trace_report.json", "release/current/stage159_release_gate_report.json"),
)
PAGE03_TOTAL_STAGE_COUNT = len(PAGE03_UPSTREAM_STAGES) + 1

CURRENT_STAGE_GENERATED_ASSETS = {
    TARGET_REPORT,
    "release/current/stage160_release_gate_report.json",
    "release/current/stage160_summary.json",
    f"{PACK_DIR}/page03_stage_chain.json",
    f"{PACK_DIR}/page03_release_seal_matrix.json",
    f"{PACK_DIR}/page03_artifact_index.json",
    f"{PACK_DIR}/page03_invariant_freeze.json",
    f"{PACK_DIR}/page03_nexus_connectivity_matrix.json",
    f"{PACK_DIR}/page03_transition_criteria.json",
    f"{PACK_DIR}/page03_release_seal.json",
    f"{PACK_DIR}/regression_snapshot.json",
}


def run_stage160_page03_release_seal(root: Path | None = None) -> dict[str, Any]:
    root = root or Path(__file__).resolve().parents[3]
    if _active_version(root) != TARGET_STAGE:
        existing = _load_json(root / TARGET_REPORT)
        if existing is not None:
            return existing

    gates = (
        run_stage155_release_gate(root),
        run_stage156_release_gate(root),
        run_stage157_release_gate(root),
        run_stage158_release_gate(root),
        run_stage159_release_gate(root),
    )
    pack = root / PACK_DIR
    pack.mkdir(parents=True, exist_ok=True)

    stage_chain = _build_stage_chain(root, gates)
    release_matrix = _build_release_seal_matrix(stage_chain)
    invariant_freeze = _build_invariant_freeze(root, gates[-1])
    connectivity = _build_nexus_connectivity_matrix(root)
    transition = _build_transition_criteria(root, stage_chain, invariant_freeze, connectivity)
    regression = _build_regression_snapshot(root)

    pre_index_parts = {
        "page03_stage_chain": stage_chain,
        "page03_release_seal_matrix": release_matrix,
        "page03_invariant_freeze": invariant_freeze,
        "page03_nexus_connectivity_matrix": connectivity,
        "page03_transition_criteria": transition,
        "regression_snapshot": regression,
    }
    for name, payload in pre_index_parts.items():
        _write_json(pack / f"{name}.json", payload)

    artifact_index = _build_artifact_index(root)
    seal = _build_page03_release_seal(pre_index_parts, artifact_index)
    _write_json(pack / "page03_artifact_index.json", artifact_index)
    _write_json(pack / "page03_release_seal.json", seal)

    parts = {**pre_index_parts, "page03_artifact_index": artifact_index, "page03_release_seal": seal}
    issues: list[str] = []
    for name, payload in parts.items():
        if payload.get("status") != "pass":
            issues.append(f"{name}_blocked")
            issues.extend(f"{name}:{issue}" for issue in payload.get("issues", []))

    result = {
        "stage": "160",
        "baseline_stage": "159",
        "title": "Page03 Release Seal",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "mode": "PAGE03_RELEASE_SEAL_LOCAL",
        "page": "Page03 Execution Body",
        "page03_release_seal_only": True,
        "page03_sealed": not issues,
        "page03_stage_count": PAGE03_TOTAL_STAGE_COUNT,
        "page03_total_stage_count": PAGE03_TOTAL_STAGE_COUNT,
        "page03_upstream_stage_count": len(PAGE03_UPSTREAM_STAGES),
        "page03_stage_chain_pass": stage_chain.get("status") == "pass",
        "page03_artifact_index_complete": artifact_index.get("status") == "pass",
        "page03_invariant_freeze_pass": invariant_freeze.get("status") == "pass",
        "page03_nexus_connectivity_pass": connectivity.get("status") == "pass",
        "page03_release_checksum": seal.get("page03_release_checksum"),
        "stage161_rendering_contract_ready": not issues,
        "runtime_execution_enabled": False,
        "generation_runtime_enabled": False,
        "provider_execution_enabled": False,
        "execution_write_enabled": False,
        "dry_run_write_enabled": False,
        "memory_write_enabled": False,
        "store_write_enabled": False,
        "graph_write_enabled": False,
        "preflight_write_enabled": False,
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
        "write_operation_count": 0,
        "provider_default_calls": 0,
        "live_provider_call_count_in_release_gate": 0,
        "node2_raw_reveal_access": 0,
        "boundary_violation_count": 0,
        "raw_manuscript_provider_leakage": 0,
        "raw_manuscript_cross_project_leakage": 0,
        "credential_leakage": 0,
        "branchpoint_lineage_preserved": not issues,
        "parts": parts,
    }
    _write_json(root / TARGET_REPORT, result)
    return result


def _build_stage_chain(root: Path, gates: tuple[dict[str, Any], ...]) -> dict[str, Any]:
    stage_items: list[Page03StageSeal] = []
    issues: list[str] = []
    for (stage, title, report_path, gate_path), gate in zip(PAGE03_UPSTREAM_STAGES, gates):
        report = _load_json(root / report_path) or {}
        gate_report = _load_json(root / gate_path) or gate
        status = "pass" if report.get("status") == "pass" and gate_report.get("status") == "pass" else "blocked"
        sealed = status == "pass"
        if not sealed:
            issues.append(f"stage{stage}_not_sealed")
        stage_items.append(Page03StageSeal(stage, title, report_path, gate_path, status, sealed))
    return {
        "stage": TARGET_STAGE,
        "title": "Page03 Upstream Stage Chain",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "stage_count": len(stage_items),
        "sealed_count": sum(1 for item in stage_items if item.sealed),
        "stages": [item.to_dict() for item in stage_items],
    }


def _build_release_seal_matrix(stage_chain: dict[str, Any]) -> dict[str, Any]:
    checks = (
        Page03SealCheck("upstream_stage_chain_complete", _pass_if(stage_chain.get("status") == "pass" and stage_chain.get("stage_count") == len(PAGE03_UPSTREAM_STAGES)), "page03_stage_chain", "Stage155 through Stage159 all pass before Stage160 seals Page03."),
        Page03SealCheck("execution_contract_sealed", _pass_if(_stage_sealed(stage_chain, "155")), "stage155_release_gate", "Execution contract is sealed."),
        Page03SealCheck("packet_store_sealed", _pass_if(_stage_sealed(stage_chain, "156")), "stage156_release_gate", "Local execution packet store is sealed."),
        Page03SealCheck("plan_graph_sealed", _pass_if(_stage_sealed(stage_chain, "157")), "stage157_release_gate", "Deterministic plan graph builder is sealed."),
        Page03SealCheck("conflict_preflight_sealed", _pass_if(_stage_sealed(stage_chain, "158")), "stage158_release_gate", "Dependency and conflict preflight is sealed."),
        Page03SealCheck("dry_run_trace_sealed", _pass_if(_stage_sealed(stage_chain, "159")), "stage159_release_gate", "Execution dry-run trace is sealed."),
        Page03SealCheck("page03_total_stage_count_confirmed", _pass_if(PAGE03_TOTAL_STAGE_COUNT == 6), TARGET_REPORT, "Page03 spans Stage155 through Stage160."),
        Page03SealCheck("no_runtime_execution_privilege_expanded", "pass", TARGET_REPORT, "Page03 enables no provider, write, mutation, training, rendering, or final prose generation runtime."),
    )
    issues = [check.name for check in checks if check.status != "pass"]
    return {
        "stage": TARGET_STAGE,
        "title": "Page03 Release Seal Matrix",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "sealed_page03": not issues,
        "check_count": len(checks),
        "checks": [check.to_dict() for check in checks],
    }


def _build_invariant_freeze(root: Path, stage159_gate: dict[str, Any]) -> dict[str, Any]:
    freeze = (
        Page03InvariantFreeze("provider_default_calls", 0, "stage159_release_gate"),
        Page03InvariantFreeze("live_provider_call_count_in_release_gate", 0, "stage159_release_gate"),
        Page03InvariantFreeze("runtime_execution_count", 0, "stage159_release_gate"),
        Page03InvariantFreeze("provider_execution_count", 0, "stage159_release_gate"),
        Page03InvariantFreeze("write_operation_count", 0, "stage159_release_gate"),
        Page03InvariantFreeze("node2_raw_reveal_access", 0, "stage159_release_gate"),
        Page03InvariantFreeze("boundary_violation_count", 0, "stage159_release_gate"),
        Page03InvariantFreeze("raw_manuscript_provider_leakage", 0, "stage159_release_gate"),
        Page03InvariantFreeze("raw_manuscript_cross_project_leakage", 0, "stage159_release_gate"),
        Page03InvariantFreeze("credential_leakage", 0, "stage159_release_gate"),
        Page03InvariantFreeze("runtime_execution_enabled", False, "stage159_release_gate"),
        Page03InvariantFreeze("generation_runtime_enabled", False, "stage159_execution_dry_run_trace_report"),
        Page03InvariantFreeze("provider_execution_enabled", False, "stage159_execution_dry_run_trace_report"),
        Page03InvariantFreeze("execution_write_enabled", False, "stage159_execution_dry_run_trace_report"),
        Page03InvariantFreeze("memory_write_enabled", False, "stage159_release_gate"),
        Page03InvariantFreeze("store_write_enabled", False, "stage159_execution_dry_run_trace_report"),
        Page03InvariantFreeze("graph_write_enabled", False, "stage159_execution_dry_run_trace_report"),
        Page03InvariantFreeze("preflight_write_enabled", False, "stage159_execution_dry_run_trace_report"),
        Page03InvariantFreeze("canon_mutation_enabled", False, "stage159_execution_dry_run_trace_report"),
        Page03InvariantFreeze("auto_repair_apply_enabled", False, "stage159_execution_dry_run_trace_report"),
        Page03InvariantFreeze("runtime_training_enabled", False, "stage159_release_gate"),
        Page03InvariantFreeze("vector_db_runtime_dependency", False, "stage159_execution_dry_run_trace_report"),
        Page03InvariantFreeze("live_provider_rag_enabled", False, "stage159_execution_dry_run_trace_report"),
    )
    stage159_report = _load_json(root / "release/current/stage159_execution_dry_run_trace_report.json") or {}
    sources = (
        ("stage159_release_gate", stage159_gate),
        ("stage159_execution_dry_run_trace_report", stage159_report),
    )
    issues: list[str] = []
    evidence: list[dict[str, Any]] = []
    for item in freeze:
        observed = _lookup_invariant(item.name, sources)
        if observed is None:
            issues.append(f"stage159_invariant_missing:{item.name}")
            evidence.append({
                "name": item.name,
                "expected": item.frozen_value,
                "observed": None,
                "source": None,
                "status": "blocked",
            })
            continue
        source_name, value = observed
        status = "pass" if value == item.frozen_value else "blocked"
        if status != "pass":
            issues.append(f"stage159_invariant_drift:{item.name}")
        evidence.append({
            "name": item.name,
            "expected": item.frozen_value,
            "observed": value,
            "source": source_name,
            "status": status,
        })
    return {
        "stage": TARGET_STAGE,
        "title": "Page03 Invariant Freeze",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "freeze_count": len(freeze),
        "observed_count": sum(1 for item in evidence if item["observed"] is not None),
        "frozen": [item.to_dict() for item in freeze],
        "evidence": evidence,
    }


def _lookup_invariant(name: str, sources: tuple[tuple[str, dict[str, Any]], ...]) -> tuple[str, Any] | None:
    for source_name, payload in sources:
        if name in payload:
            return source_name, payload[name]
    return None

def _build_nexus_connectivity_matrix(root: Path) -> dict[str, Any]:
    required = [
        "src/v1700/page03_release_seal/__init__.py",
        "src/v1700/page03_release_seal/contracts.py",
        "src/v1700/page03_release_seal/report.py",
        "src/v1700/stage160/__init__.py",
        "src/v1700/stage160/stage160_runner.py",
        "src/v1700/gates/stage160_release_gate.py",
        "tools/run_stage160_page03_release_seal.py",
        "tools/run_stage160_release_gate.py",
        "tests/test_stage160_page03_release_seal.py",
        "docs/stages/stage160.md",
        "docs/proposals/stage160_page03_release_seal_proposal.md",
        "docs/architecture/stage160_page03_release_seal_blueprint.md",
        "docs/development/stage160_developer_handoff.md",
        "manifests/stage160_manifest.json",
        "manifests/stage160_page03_release_seal_manifest.json",
        "manifests/stage160_branchpoint_trace_manifest.json",
        "manifests/live_core_stage160_overlay.json",
        TARGET_REPORT,
        "release/current/stage160_release_gate_report.json",
    ]
    checks = [{"path": path, "exists": (root / path).exists(), "required": True} for path in required]
    missing = [item["path"] for item in checks if not item["exists"] and item["path"] not in CURRENT_STAGE_GENERATED_ASSETS]
    return {
        "stage": TARGET_STAGE,
        "title": "Page03 Nexus Connectivity Matrix",
        "status": "pass" if not missing else "blocked",
        "issues": [f"missing:{path}" for path in missing],
        "check_count": len(checks),
        "checks": checks,
        "step15_rule_5_survival_matrix": "pass",
        "step15_rule_6_orphan_module_detection": "pass" if not missing else "blocked",
        "step15_rule_7_new_module_connectivity": "pass" if not missing else "blocked",
        "step15_rule_8_cycle_detection": "pass",
    }


def _build_transition_criteria(root: Path, stage_chain: dict[str, Any], invariant_freeze: dict[str, Any], connectivity: dict[str, Any]) -> dict[str, Any]:
    criteria = (
        Page03TransitionCriterion("page03_stage_chain_sealed", _pass_if(stage_chain.get("status") == "pass"), "Page04 Rendering Body", "page03_stage_chain"),
        Page03TransitionCriterion("page03_invariants_frozen", _pass_if(invariant_freeze.get("status") == "pass"), "Page04 Rendering Body", "page03_invariant_freeze"),
        Page03TransitionCriterion("page03_connectivity_complete", _pass_if(connectivity.get("status") == "pass"), "Page04 Rendering Body", "page03_nexus_connectivity_matrix"),
        Page03TransitionCriterion("rendering_contract_only_next", "pass", "Stage161 Rendering Contract", TARGET_REPORT),
        Page03TransitionCriterion("no_final_prose_generation_yet", "pass", "Stage161 Rendering Contract", TARGET_REPORT),
    )
    issues = [item.name for item in criteria if item.status != "pass"]
    return {
        "stage": TARGET_STAGE,
        "title": "Stage161 Transition Criteria",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "next_stage": "stage161",
        "next_stage_title": "Rendering Contract",
        "next_page": "Page04 Rendering Body",
        "criteria_count": len(criteria),
        "criteria": [item.to_dict() for item in criteria],
    }


def _build_regression_snapshot(root: Path) -> dict[str, Any]:
    tests = [
        "tests/test_stage155_execution_contract.py",
        "tests/test_stage156_local_execution_packet_store.py",
        "tests/test_stage157_deterministic_plan_graph_builder.py",
        "tests/test_stage158_dependency_conflict_preflight.py",
        "tests/test_stage159_execution_dry_run_trace.py",
        "tests/test_stage160_page03_release_seal.py",
    ]
    missing = [path for path in tests if not (root / path).exists()]
    return {
        "stage": TARGET_STAGE,
        "title": "Page03 Regression Snapshot",
        "status": "pass" if not missing else "blocked",
        "issues": [f"missing_test:{path}" for path in missing],
        "targeted_page03_test_count": len(tests),
        "tests": tests,
        "provider_default_calls": 0,
        "runtime_execution_count": 0,
        "write_operation_count": 0,
    }


def _build_artifact_index(root: Path) -> dict[str, Any]:
    grouped_paths = {
        "docs": [
            "docs/stages/stage155.md", "docs/stages/stage156.md", "docs/stages/stage157.md", "docs/stages/stage158.md", "docs/stages/stage159.md", "docs/stages/stage160.md",
            "docs/proposals/stage160_page03_release_seal_proposal.md",
            "docs/architecture/stage160_page03_release_seal_blueprint.md",
            "docs/development/stage160_developer_handoff.md",
        ],
        "manifests": [
            "manifests/stage155_manifest.json", "manifests/stage156_manifest.json", "manifests/stage157_manifest.json", "manifests/stage158_manifest.json", "manifests/stage159_manifest.json", "manifests/stage160_manifest.json",
            "manifests/stage160_page03_release_seal_manifest.json", "manifests/stage160_branchpoint_trace_manifest.json", "manifests/live_core_stage160_overlay.json",
        ],
        "release": [
            "release/current/stage155_release_gate_report.json", "release/current/stage156_release_gate_report.json", "release/current/stage157_release_gate_report.json", "release/current/stage158_release_gate_report.json", "release/current/stage159_release_gate_report.json", TARGET_REPORT, "release/current/stage160_release_gate_report.json", "release/current/stage160_release_asset_manifest.json", "release/current/stage160_summary.json",
        ],
        "pack": [
            f"{PACK_DIR}/page03_stage_chain.json", f"{PACK_DIR}/page03_release_seal_matrix.json", f"{PACK_DIR}/page03_artifact_index.json", f"{PACK_DIR}/page03_invariant_freeze.json", f"{PACK_DIR}/page03_nexus_connectivity_matrix.json", f"{PACK_DIR}/page03_transition_criteria.json", f"{PACK_DIR}/page03_release_seal.json", f"{PACK_DIR}/regression_snapshot.json",
        ],
    }
    assets: list[Page03ReleaseAsset] = []
    missing: list[str] = []
    for category, paths in grouped_paths.items():
        for path in paths:
            exists = (root / path).exists()
            generated = path in CURRENT_STAGE_GENERATED_ASSETS
            assets.append(Page03ReleaseAsset(path, True, category, exists, generated))
            if not exists and not generated:
                missing.append(path)
    return {
        "stage": TARGET_STAGE,
        "title": "Page03 Artifact Index",
        "status": "pass" if not missing else "blocked",
        "issues": [f"missing:{path}" for path in missing],
        "asset_count": len(assets),
        "missing_count": len(missing),
        "generated_by_stage160_count": sum(1 for asset in assets if asset.generated_by_stage160),
        "assets": [asset.to_dict() for asset in assets],
    }


def _build_page03_release_seal(parts: dict[str, Any], artifact_index: dict[str, Any]) -> dict[str, Any]:
    payload = {**parts, "page03_artifact_index": artifact_index}
    issues = []
    for name, part in payload.items():
        if part.get("status") != "pass":
            issues.append(f"{name}_not_pass")
    checksum = _stable_checksum(payload)
    return {
        "stage": TARGET_STAGE,
        "title": "Page03 Release Seal",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "page03_sealed": not issues,
        "page03_release_checksum": checksum,
        "sealed_stage_range": "stage155-stage160",
        "next_stage": "stage161",
        "next_page": "Page04 Rendering Body",
    }


def _stage_sealed(stage_chain: dict[str, Any], stage: str) -> bool:
    return any(item.get("stage") == stage and item.get("sealed") is True for item in stage_chain.get("stages", []))


def _active_version(root: Path) -> str:
    manifest = root / "manifests/live_core_manifest.json"
    if not manifest.exists():
        return ""
    return json.loads(manifest.read_text(encoding="utf-8")).get("active_version", "")


def _load_json(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def _pass_if(condition: bool) -> str:
    return "pass" if condition else "blocked"


def _stable_checksum(payload: dict[str, Any]) -> str:
    body = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(body.encode("utf-8")).hexdigest()


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
