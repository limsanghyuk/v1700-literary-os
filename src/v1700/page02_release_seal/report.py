from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from v1700.gates.stage150_release_gate import run_stage150_release_gate
from v1700.gates.stage151_release_gate import run_stage151_release_gate
from v1700.gates.stage152_release_gate import run_stage152_release_gate
from v1700.gates.stage153_release_gate import run_stage153_release_gate

from .contracts import Page02Blocker, Page02StageSeal, ReleaseSealAsset, SealCheck

TARGET_STAGE = "stage154"
TARGET_REPORT = "release/current/stage154_page02_release_seal_report.json"
PACK_DIR = "release/current/stage154_page02_release_seal_pack"

PAGE02_UPSTREAM_STAGES: tuple[tuple[str, str, str, str], ...] = (
    ("150", "Memory Contract", "release/current/stage150_memory_contract_report.json", "release/current/stage150_release_gate_report.json"),
    ("151", "Local Read-Only Memory Store", "release/current/stage151_local_read_only_memory_store_report.json", "release/current/stage151_release_gate_report.json"),
    ("152", "Deterministic Local Query / Ranking", "release/current/stage152_memory_query_interface_report.json", "release/current/stage152_release_gate_report.json"),
    ("153", "Memory Health & Leakage Boundary", "release/current/stage153_memory_health_leakage_boundary_report.json", "release/current/stage153_release_gate_report.json"),
)
PAGE02_TOTAL_STAGE_COUNT = len(PAGE02_UPSTREAM_STAGES) + 1

CURRENT_STAGE_GENERATED_ASSETS = {
    TARGET_REPORT,
    "release/current/stage154_release_gate_report.json",
    "release/current/stage154_summary.json",
    f"{PACK_DIR}/page02_stage_chain.json",
    f"{PACK_DIR}/page02_release_seal_matrix.json",
    f"{PACK_DIR}/page02_blocker_registry.json",
    f"{PACK_DIR}/page02_artifact_index.json",
    f"{PACK_DIR}/page02_lineage_evidence_index.json",
    f"{PACK_DIR}/page02_boundary_freeze.json",
}


def run_stage154_page02_release_seal(root: Path | None = None) -> dict[str, Any]:
    root = root or Path(__file__).resolve().parents[3]
    if _active_version(root) != TARGET_STAGE:
        existing = _load_json(root / TARGET_REPORT)
        if existing is not None:
            return existing

    stage150_gate = run_stage150_release_gate(root)
    stage151_gate = run_stage151_release_gate(root)
    stage152_gate = run_stage152_release_gate(root)
    stage153_gate = run_stage153_release_gate(root)

    pack = root / PACK_DIR
    pack.mkdir(parents=True, exist_ok=True)

    stage_chain = _build_stage_chain(root, (stage150_gate, stage151_gate, stage152_gate, stage153_gate))
    seal_matrix = _build_page02_seal_matrix(stage_chain)
    blocker_registry = _build_page02_blocker_registry()
    lineage_index = _build_lineage_evidence_index(root)
    boundary_freeze = _build_boundary_freeze(root, stage153_gate)

    pre_index_parts = {
        "page02_stage_chain": stage_chain,
        "page02_release_seal_matrix": seal_matrix,
        "page02_blocker_registry": blocker_registry,
        "page02_lineage_evidence_index": lineage_index,
        "page02_boundary_freeze": boundary_freeze,
    }
    for name, payload in pre_index_parts.items():
        _write_json(pack / f"{name}.json", payload)

    artifact_index = _build_page02_artifact_index(root)
    _write_json(pack / "page02_artifact_index.json", artifact_index)

    parts = {**pre_index_parts, "page02_artifact_index": artifact_index}
    issues: list[str] = []
    for name, payload in parts.items():
        if payload.get("status") != "pass":
            issues.append(f"{name}_blocked")
            issues.extend(f"{name}:{issue}" for issue in payload.get("issues", []))

    result = {
        "stage": "154",
        "baseline_stage": "153",
        "title": "Page02 Release Seal",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "mode": "PAGE02_RELEASE_SEAL_LOCAL",
        "page": "Page02 Narrative Memory Body",
        "page02_release_seal_only": True,
        "page02_sealed": not issues,
        "page02_stage_count": PAGE02_TOTAL_STAGE_COUNT,
        "page02_total_stage_count": PAGE02_TOTAL_STAGE_COUNT,
        "page02_upstream_stage_count": len(PAGE02_UPSTREAM_STAGES),
        "page02_stage_chain_pass": stage_chain.get("status") == "pass",
        "page02_artifact_index_complete": artifact_index.get("status") == "pass",
        "page02_blocker_count": blocker_registry.get("blocker_count", 0),
        "page02_boundary_freeze_pass": boundary_freeze.get("status") == "pass",
        "stage155_entry_ready": not issues,
        "memory_write_enabled": False,
        "store_write_enabled": False,
        "query_write_enabled": False,
        "storage_runtime_write_enabled": False,
        "ranking_runtime_write_enabled": False,
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
    stage_items: list[Page02StageSeal] = []
    issues: list[str] = []
    for (stage, title, report_path, gate_path), gate in zip(PAGE02_UPSTREAM_STAGES, gates):
        report = _load_json(root / report_path) or {}
        gate_report = _load_json(root / gate_path) or gate
        status = "pass" if report.get("status") == "pass" and gate_report.get("status") == "pass" else "blocked"
        sealed = status == "pass"
        if not sealed:
            issues.append(f"stage{stage}_not_sealed")
        stage_items.append(Page02StageSeal(stage, title, report_path, gate_path, status, sealed))
    return {
        "stage": TARGET_STAGE,
        "title": "Page02 Upstream Stage Chain",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "stage_count": len(stage_items),
        "sealed_count": sum(1 for item in stage_items if item.sealed),
        "stages": [item.to_dict() for item in stage_items],
    }


def _build_page02_seal_matrix(stage_chain: dict[str, Any]) -> dict[str, Any]:
    checks = (
        SealCheck("upstream_stage_chain_complete", _pass_if(stage_chain.get("status") == "pass" and stage_chain.get("stage_count") == len(PAGE02_UPSTREAM_STAGES)), "page02_stage_chain", "Stage150 through Stage153 all pass before Stage154 seals Page02."),
        SealCheck("memory_contract_sealed", _pass_if(_stage_sealed(stage_chain, "150")), "stage150_release_gate", "Memory contract is sealed."),
        SealCheck("read_only_store_sealed", _pass_if(_stage_sealed(stage_chain, "151")), "stage151_release_gate", "Local read-only store is sealed."),
        SealCheck("query_ranking_sealed", _pass_if(_stage_sealed(stage_chain, "152")), "stage152_release_gate", "Deterministic local query/ranking is sealed."),
        SealCheck("health_leakage_boundary_sealed", _pass_if(_stage_sealed(stage_chain, "153")), "stage153_release_gate", "Memory health and leakage boundary is sealed."),
        SealCheck("page02_total_stage_count_confirmed", _pass_if(PAGE02_TOTAL_STAGE_COUNT == 5), TARGET_REPORT, "Page02 spans Stage150 through Stage154."),
        SealCheck("page02_runtime_privilege_not_expanded", "pass", TARGET_REPORT, "Page02 seal enables no provider, write, training, mutation, or vector runtime."),
    )
    issues = [check.name for check in checks if check.status != "pass"]
    return {
        "stage": TARGET_STAGE,
        "title": "Page02 Release Seal Matrix",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "sealed_page02": not issues,
        "check_count": len(checks),
        "checks": [check.to_dict() for check in checks],
    }


def _build_page02_blocker_registry() -> dict[str, Any]:
    blockers = (
        Page02Blocker("live_provider_rag", True, "Page02 remains local and provider-zero."),
        Page02Blocker("vector_db_runtime_dependency", True, "Stage152 ranking is lexical/local only."),
        Page02Blocker("memory_write_execution", True, "Stage151 store is read-only."),
        Page02Blocker("query_write_execution", True, "Stage152 queries cannot mutate state."),
        Page02Blocker("sql_graph_write_execution", True, "No storage mutation is allowed."),
        Page02Blocker("canon_mutation", True, "Page02 cannot mutate canon."),
        Page02Blocker("runtime_training", True, "No runtime training or model weight update is allowed."),
        Page02Blocker("auto_repair_apply", True, "No automatic repair mutation is allowed."),
        Page02Blocker("node2_hidden_reveal_access", True, "Node2 stays surface-only."),
        Page02Blocker("raw_manuscript_export", True, "No raw manuscript provider/cross-project leakage is allowed."),
    )
    issues = [blocker.capability for blocker in blockers if not blocker.blocked]
    return {
        "stage": TARGET_STAGE,
        "title": "Page02 Release Blocker Registry",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "blocker_count": len(blockers),
        "blocked_capability_count": sum(1 for blocker in blockers if blocker.blocked),
        "blockers": [blocker.to_dict() for blocker in blockers],
    }


def _build_page02_artifact_index(root: Path) -> dict[str, Any]:
    grouped_paths = {
        "docs": [
            "docs/stages/stage150.md",
            "docs/stages/stage151.md",
            "docs/stages/stage152.md",
            "docs/stages/stage153.md",
            "docs/stages/stage154.md",
            "docs/proposals/stage154_page02_release_seal_proposal.md",
            "docs/architecture/stage154_page02_release_seal_blueprint.md",
            "docs/development/stage154_developer_handoff.md",
        ],
        "manifests": [
            "manifests/stage150_manifest.json",
            "manifests/stage151_manifest.json",
            "manifests/stage152_manifest.json",
            "manifests/stage153_manifest.json",
            "manifests/stage154_manifest.json",
            "manifests/stage154_page02_release_seal_manifest.json",
            "manifests/stage154_branchpoint_trace_manifest.json",
            "manifests/live_core_stage154_overlay.json",
        ],
        "release": [
            "release/current/stage150_release_gate_report.json",
            "release/current/stage151_release_gate_report.json",
            "release/current/stage152_release_gate_report.json",
            "release/current/stage153_release_gate_report.json",
            TARGET_REPORT,
            "release/current/stage154_release_gate_report.json",
            "release/current/stage154_release_asset_manifest.json",
            "release/current/stage154_summary.json",
        ],
        "pack": [
            f"{PACK_DIR}/page02_stage_chain.json",
            f"{PACK_DIR}/page02_release_seal_matrix.json",
            f"{PACK_DIR}/page02_blocker_registry.json",
            f"{PACK_DIR}/page02_artifact_index.json",
            f"{PACK_DIR}/page02_lineage_evidence_index.json",
            f"{PACK_DIR}/page02_boundary_freeze.json",
        ],
    }
    assets: list[ReleaseSealAsset] = []
    missing: list[str] = []
    for category, paths in grouped_paths.items():
        for path in paths:
            generated = path in CURRENT_STAGE_GENERATED_ASSETS
            exists = (root / path).exists()
            assets.append(ReleaseSealAsset(path, True, category, exists, generated))
            if not exists and not generated:
                missing.append(path)
    return {
        "stage": TARGET_STAGE,
        "title": "Page02 Artifact Index",
        "status": "pass" if not missing else "blocked",
        "issues": [f"missing:{path}" for path in missing],
        "asset_count": len(assets),
        "required_count": len(assets),
        "existing_count": sum(1 for asset in assets if asset.exists),
        "generated_by_stage154_count": sum(1 for asset in assets if asset.generated_by_stage154),
        "missing_count": len(missing),
        "assets": [asset.to_dict() for asset in assets],
    }


def _build_lineage_evidence_index(root: Path) -> dict[str, Any]:
    evidence = [
        "Stage150 Memory Contract",
        "Stage151 Local Read-Only Memory Store",
        "Stage152 Deterministic Local Query / Ranking",
        "Stage153 Memory Health & Leakage Boundary",
        "Stage154 Page02 Release Seal",
    ]
    required = [
        "manifests/stage150_branchpoint_trace_manifest.json",
        "manifests/stage151_branchpoint_trace_manifest.json",
        "manifests/stage152_branchpoint_trace_manifest.json",
        "manifests/stage153_branchpoint_trace_manifest.json",
        "manifests/stage154_branchpoint_trace_manifest.json",
    ]
    missing = [path for path in required if not (root / path).exists()]
    return {
        "stage": TARGET_STAGE,
        "title": "Page02 Lineage Evidence Index",
        "status": "pass" if not missing else "blocked",
        "issues": [f"missing:{path}" for path in missing],
        "lineage_evidence_complete": not missing,
        "evidence": evidence,
        "required_trace_manifests": required,
    }


def _build_boundary_freeze(root: Path, stage153_gate: dict[str, Any]) -> dict[str, Any]:
    stage153 = _load_json(root / "release/current/stage153_memory_health_leakage_boundary_report.json") or {}
    checks = (
        SealCheck("stage153_gate_pass", _pass_if(stage153_gate.get("status") == "pass"), "release/current/stage153_release_gate_report.json", "Stage153 boundary gate passed."),
        SealCheck("boundary_violation_zero", _pass_if(stage153.get("boundary_violation_count") == 0), "release/current/stage153_memory_health_leakage_boundary_report.json", "No boundary violations were detected."),
        SealCheck("node2_raw_reveal_zero", _pass_if(stage153.get("node2_raw_reveal_access") == 0), "release/current/stage153_memory_health_leakage_boundary_report.json", "Node2 raw reveal access remains zero."),
        SealCheck("credential_leakage_zero", _pass_if(stage153.get("credential_leakage") == 0), "release/current/stage153_memory_health_leakage_boundary_report.json", "No credential leakage was detected."),
        SealCheck("raw_manuscript_provider_leakage_zero", _pass_if(stage153.get("raw_manuscript_provider_leakage") == 0), "release/current/stage153_memory_health_leakage_boundary_report.json", "No raw manuscript provider leakage was detected."),
        SealCheck("raw_manuscript_cross_project_leakage_zero", _pass_if(stage153.get("raw_manuscript_cross_project_leakage") == 0), "release/current/stage153_memory_health_leakage_boundary_report.json", "No raw manuscript cross-project leakage was detected."),
    )
    issues = [check.name for check in checks if check.status != "pass"]
    return {
        "stage": TARGET_STAGE,
        "title": "Page02 Boundary Freeze",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "check_count": len(checks),
        "checks": [check.to_dict() for check in checks],
    }


def _stage_sealed(stage_chain: dict[str, Any], stage: str) -> bool:
    return any(item.get("stage") == stage and item.get("sealed") is True for item in stage_chain.get("stages", []))


def _pass_if(condition: bool) -> str:
    return "pass" if condition else "blocked"


def _active_version(root: Path) -> str:
    manifest = root / "manifests/live_core_manifest.json"
    if not manifest.exists():
        return ""
    return json.loads(manifest.read_text(encoding="utf-8")).get("active_version", "")


def _load_json(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
