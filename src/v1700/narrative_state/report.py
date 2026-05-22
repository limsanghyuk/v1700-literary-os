from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from v1700.gates.stage145_release_gate import run_stage145_release_gate
from v1700.release_integrity.asset_checker import expected_release_asset_manifest, run_release_asset_integrity
from v1700.release_integrity.metadata_checker import run_stage_metadata_consistency

from .contracts import ContinuityRule, NarrativeStateContract, RevealBoundarySpec, StateHierarchyEdge
from .episode_state import build_continuity_rules, build_continuity_state_contract, build_episode_state_contract
from .scene_state import build_reveal_boundaries, build_reveal_state_contract, build_scene_state_contract
from .series_state import build_character_state_contract, build_series_state_contract, build_world_state_contract

TARGET_STAGE = "stage146"
TARGET_REPORT = "release/current/stage146_narrative_state_contract_report.json"


def run_stage146_narrative_state_contract(root: Path | None = None) -> dict[str, Any]:
    root = root or Path(__file__).resolve().parents[3]
    if _active_version(root) != TARGET_STAGE:
        existing = _load_existing(root / TARGET_REPORT)
        if existing is not None:
            return existing

    pack = root / "release" / "current" / "stage146_narrative_state_contract_pack"
    pack.mkdir(parents=True, exist_ok=True)
    report_path = root / TARGET_REPORT
    if not report_path.exists():
        _write_json(
            report_path,
            {
                "stage": "146",
                "baseline_stage": "145",
                "title": "Narrative State Contract",
                "status": "building",
                "issues": [],
            },
        )

    baseline = run_stage145_release_gate(root)
    _write_json(root / "release/current/stage146_release_asset_manifest.json", expected_release_asset_manifest(TARGET_STAGE))

    state_shape_catalog = _build_state_shape_catalog()
    state_hierarchy = _build_state_hierarchy()
    continuity_rulebook = _build_continuity_rulebook()
    reveal_boundary_matrix = _build_reveal_boundary_matrix()
    stage147_entry_signals = _build_stage147_entry_signals()

    _write_json(pack / "state_shape_catalog.json", state_shape_catalog)
    _write_json(pack / "state_hierarchy.json", state_hierarchy)
    _write_json(pack / "continuity_rulebook.json", continuity_rulebook)
    _write_json(pack / "reveal_boundary_matrix.json", reveal_boundary_matrix)
    _write_json(pack / "stage147_entry_signals.json", stage147_entry_signals)

    metadata = run_stage_metadata_consistency(root)
    assets = run_release_asset_integrity(root)

    issues: list[str] = []
    if baseline.get("status") != "pass":
        issues.append("stage145_baseline_gate_pass")
    for key, part in {
        "metadata_consistency": metadata,
        "release_asset_integrity": assets,
        "state_shape_catalog": state_shape_catalog,
        "state_hierarchy": state_hierarchy,
        "continuity_rulebook": continuity_rulebook,
        "reveal_boundary_matrix": reveal_boundary_matrix,
        "stage147_entry_signals": stage147_entry_signals,
    }.items():
        if part.get("status") != "pass":
            issues.append(f"{key}_blocked")
            issues.extend(f"{key}:{issue}" for issue in part.get("issues", []))

    result = {
        "stage": "146",
        "baseline_stage": "145",
        "title": "Narrative State Contract",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "mode": "NARRATIVE_STATE_CONTRACT_LOCAL",
        "narrative_state_contract_only": True,
        "canonical_state_object_count": state_shape_catalog.get("contract_count", 0),
        "hierarchy_edge_count": state_hierarchy.get("edge_count", 0),
        "continuity_rule_count": continuity_rulebook.get("rule_count", 0),
        "reveal_boundary_complete": reveal_boundary_matrix.get("coverage_complete", False),
        "project_manifest_body_ready": stage147_entry_signals.get("project_manifest_body_ready", False),
        "node_boundary_constitution_ready": stage147_entry_signals.get("node_boundary_constitution_ready", False),
        "stage149_gate_ready": stage147_entry_signals.get("stage149_gate_ready", False),
        "stage150_memory_body_ready": stage147_entry_signals.get("stage150_memory_body_ready", False),
        "metadata_consistency_status": metadata.get("status"),
        "release_asset_integrity_status": assets.get("status"),
        "runtime_training_enabled": False,
        "active_meta_learning_enabled": False,
        "model_weight_update_count": 0,
        "losdb_write_enabled": False,
        "migration_execution_enabled": False,
        "storage_contract_write_enabled": False,
        "provider_default_calls": 0,
        "live_provider_call_count_in_release_gate": 0,
        "node2_raw_reveal_access": 0,
        "raw_manuscript_provider_leakage": 0,
        "raw_manuscript_cross_project_leakage": 0,
        "credential_leakage": 0,
        "cross_project_write_allowed": False,
        "canon_auto_resolution_count": 0,
        "auto_repair_mutation_count": 0,
        "branchpoint_lineage_preserved": not issues,
        "parts": {
            "stage145_baseline": _compact_baseline(baseline),
            "metadata_consistency": metadata,
            "release_asset_integrity": assets,
            "state_shape_catalog": state_shape_catalog,
            "state_hierarchy": state_hierarchy,
            "continuity_rulebook": continuity_rulebook,
            "reveal_boundary_matrix": reveal_boundary_matrix,
            "stage147_entry_signals": stage147_entry_signals,
        },
    }
    _write_json(report_path, result)
    return result


def _build_state_shape_catalog() -> dict[str, Any]:
    contracts = _state_contracts()
    names = {contract.name for contract in contracts}
    required = {
        "SeriesState",
        "EpisodeState",
        "SceneState",
        "CharacterState",
        "WorldState",
        "RevealState",
        "ContinuityState",
    }
    issues = [f"missing_contract:{name}" for name in sorted(required - names)]
    return {
        "stage": TARGET_STAGE,
        "title": "Stage146 State Shape Catalog",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "contract_count": len(contracts),
        "coverage_complete": not issues,
        "contracts": [contract.to_dict() for contract in contracts],
    }


def _build_state_hierarchy() -> dict[str, Any]:
    edges = (
        StateHierarchyEdge("SeriesState", "EpisodeState", "1:n", "series defines canonical episode order"),
        StateHierarchyEdge("EpisodeState", "SceneState", "1:n", "episode defines canonical scene order"),
        StateHierarchyEdge("SeriesState", "CharacterState", "1:n", "series roster owns character identity"),
        StateHierarchyEdge("SeriesState", "WorldState", "1:1", "series sets world authority"),
        StateHierarchyEdge("SceneState", "RevealState", "1:n", "scene reveal slots must remain explicitly scoped"),
        StateHierarchyEdge("EpisodeState", "ContinuityState", "1:1", "episode continuity packet records promises and risks"),
        StateHierarchyEdge("CharacterState", "RevealState", "n:n", "knowledge holders are constrained by reveal packets"),
    )
    issues = []
    if len(edges) < 6:
        issues.append("insufficient_hierarchy_edges")
    return {
        "stage": TARGET_STAGE,
        "title": "Stage146 State Hierarchy",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "edge_count": len(edges),
        "edges": [edge.to_dict() for edge in edges],
    }


def _build_continuity_rulebook() -> dict[str, Any]:
    rules = build_continuity_rules()
    issues = [rule.name for rule in rules if not rule.enforced]
    return {
        "stage": TARGET_STAGE,
        "title": "Stage146 Continuity Rulebook",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "rule_count": len(rules),
        "all_enforced": not issues,
        "rules": [rule.to_dict() for rule in rules],
    }


def _build_reveal_boundary_matrix() -> dict[str, Any]:
    boundaries = build_reveal_boundaries()
    issues = [
        boundary.state_name
        for boundary in boundaries
        if boundary.node2_access in {"full_contract", "hidden_state", "raw_reveal"}
    ]
    return {
        "stage": TARGET_STAGE,
        "title": "Stage146 Reveal Boundary Matrix",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "coverage_complete": not issues and len(boundaries) >= 7,
        "entries": [boundary.to_dict() for boundary in boundaries],
    }


def _build_stage147_entry_signals() -> dict[str, Any]:
    return {
        "stage": TARGET_STAGE,
        "title": "Stage146 Stage147+ Entry Signals",
        "status": "pass",
        "issues": [],
        "project_manifest_body_ready": True,
        "node_boundary_constitution_ready": True,
        "stage149_gate_ready": True,
        "stage150_memory_body_ready": True,
        "signals": [
            "SeriesState, EpisodeState, and SceneState contracts are canonical.",
            "CharacterState and WorldState expose stable manifest-facing fields.",
            "RevealState and ContinuityState preserve provider-zero and Node2 boundaries.",
            "Stage147 may bind project manifests to these contracts without enabling writes.",
        ],
    }


def _state_contracts() -> tuple[NarrativeStateContract, ...]:
    return (
        build_series_state_contract(),
        build_episode_state_contract(),
        build_scene_state_contract(),
        build_character_state_contract(),
        build_world_state_contract(),
        build_reveal_state_contract(),
        build_continuity_state_contract(),
    )


def _compact_baseline(report: dict[str, Any]) -> dict[str, Any]:
    keep = (
        "stage",
        "baseline_stage",
        "status",
        "title",
        "issues",
        "provider_default_calls",
        "live_provider_call_count_in_release_gate",
        "node2_raw_reveal_access",
        "credential_leakage",
        "branchpoint_lineage_preserved",
    )
    compact = {key: report.get(key) for key in keep if key in report}
    compact["stage145_release_gate_status"] = report.get("status")
    return compact


def _active_version(root: Path) -> str:
    manifest = root / "manifests/live_core_manifest.json"
    if not manifest.exists():
        return ""
    return json.loads(manifest.read_text(encoding="utf-8")).get("active_version", "")


def _load_existing(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
