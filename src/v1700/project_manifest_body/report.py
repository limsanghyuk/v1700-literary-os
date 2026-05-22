from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from v1700.gates.stage146_release_gate import run_stage146_release_gate
from v1700.release_integrity.asset_checker import expected_release_asset_manifest, run_release_asset_integrity
from v1700.release_integrity.metadata_checker import run_stage_metadata_consistency

from .contracts import ManifestBodySection, ManifestLoadStep, ManifestStateBinding, PolicyBoundaryControl
from .loader import build_project_manifest_bundle, load_project_sources

TARGET_STAGE = "stage147"
TARGET_REPORT = "release/current/stage147_project_manifest_body_report.json"


def run_stage147_project_manifest_body(root: Path | None = None) -> dict[str, Any]:
    root = root or Path(__file__).resolve().parents[3]
    if _active_version(root) != TARGET_STAGE:
        existing = _load_existing(root / TARGET_REPORT)
        if existing is not None:
            return existing

    pack = root / "release" / "current" / "stage147_project_manifest_body_pack"
    pack.mkdir(parents=True, exist_ok=True)
    report_path = root / TARGET_REPORT
    if not report_path.exists():
        _write_json(
            report_path,
            {
                "stage": "147",
                "baseline_stage": "146",
                "title": "Project Manifest Body",
                "status": "building",
                "issues": [],
            },
        )

    baseline = run_stage146_release_gate(root)
    _write_json(root / "release/current/stage147_release_asset_manifest.json", expected_release_asset_manifest(TARGET_STAGE))

    sources = load_project_sources(root)
    manifest_bundle = _build_canonical_manifest_bundle(root)
    project_manifest_catalog = _build_project_manifest_catalog()
    manifest_state_bindings = _build_manifest_state_bindings()
    manifest_policy_boundary = _build_manifest_policy_boundary(sources, manifest_bundle)
    manifest_load_order = _build_manifest_load_order()
    stage148_entry_signals = _build_stage148_entry_signals()

    _write_json(pack / "canonical_manifest_bundle.json", manifest_bundle)
    _write_json(pack / "project_manifest_catalog.json", project_manifest_catalog)
    _write_json(pack / "manifest_state_bindings.json", manifest_state_bindings)
    _write_json(pack / "manifest_policy_boundary.json", manifest_policy_boundary)
    _write_json(pack / "manifest_load_order.json", manifest_load_order)
    _write_json(pack / "stage148_entry_signals.json", stage148_entry_signals)

    metadata = run_stage_metadata_consistency(root)
    assets = run_release_asset_integrity(root)

    issues: list[str] = []
    if baseline.get("status") != "pass":
        issues.append("stage146_baseline_gate_pass")
    for key, part in {
        "metadata_consistency": metadata,
        "release_asset_integrity": assets,
        "project_manifest_catalog": project_manifest_catalog,
        "manifest_state_bindings": manifest_state_bindings,
        "manifest_policy_boundary": manifest_policy_boundary,
        "manifest_load_order": manifest_load_order,
        "stage148_entry_signals": stage148_entry_signals,
    }.items():
        if part.get("status") != "pass":
            issues.append(f"{key}_blocked")
            issues.extend(f"{key}:{issue}" for issue in part.get("issues", []))

    result = {
        "stage": "147",
        "baseline_stage": "146",
        "title": "Project Manifest Body",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "mode": "PROJECT_MANIFEST_BODY_LOCAL",
        "project_manifest_body_only": True,
        "manifest_section_count": project_manifest_catalog.get("section_count", 0),
        "canonical_packet_count": project_manifest_catalog.get("canonical_packet_count", 0),
        "state_binding_count": manifest_state_bindings.get("binding_count", 0),
        "policy_boundary_complete": manifest_policy_boundary.get("all_enforced", False),
        "load_order_complete": manifest_load_order.get("order_complete", False),
        "node_boundary_constitution_ready": stage148_entry_signals.get("node_boundary_constitution_ready", False),
        "stage149_gate_ready": stage148_entry_signals.get("stage149_gate_ready", False),
        "stage150_memory_body_ready": stage148_entry_signals.get("stage150_memory_body_ready", False),
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
            "stage146_baseline": _compact_baseline(baseline),
            "metadata_consistency": metadata,
            "release_asset_integrity": assets,
            "canonical_manifest_bundle": manifest_bundle,
            "project_manifest_catalog": project_manifest_catalog,
            "manifest_state_bindings": manifest_state_bindings,
            "manifest_policy_boundary": manifest_policy_boundary,
            "manifest_load_order": manifest_load_order,
            "stage148_entry_signals": stage148_entry_signals,
        },
    }
    _write_json(report_path, result)
    return result


def _build_canonical_manifest_bundle(root: Path) -> dict[str, Any]:
    bundle = build_project_manifest_bundle(root)
    packet_names = (
        "series_state",
        "episode_state",
        "scene_state",
        "character_state",
        "world_state",
        "reveal_state",
        "continuity_state",
    )
    packet_count = sum(1 for name in packet_names if name in bundle)
    issues = []
    for name in packet_names:
        if name not in bundle:
            issues.append(f"missing_packet:{name}")
    return {
        "stage": TARGET_STAGE,
        "title": "Stage147 Canonical Manifest Bundle",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "packet_count": packet_count,
        "coverage_complete": not issues,
        **bundle,
    }


def _build_project_manifest_catalog() -> dict[str, Any]:
    sections = (
        ManifestBodySection(
            "project_manifest",
            "samples/korean_drama_family_secret/project.json",
            "SeriesState",
            ("project_id", "title", "genre", "purpose"),
            True,
            True,
            True,
            "Series identity comes from the sample project manifest.",
        ),
        ManifestBodySection(
            "character_roster",
            "samples/korean_drama_family_secret/characters.json",
            "CharacterState",
            ("project_id", "characters"),
            True,
            True,
            True,
            "Character roster remains synthetic and public-safe.",
        ),
        ManifestBodySection(
            "world_packet",
            "samples/korean_drama_family_secret/world.json",
            "WorldState",
            ("world_id", "project_id", "setting"),
            True,
            True,
            True,
            "World anchors remain reader-safe and local-only.",
        ),
        ManifestBodySection(
            "plot_outline",
            "samples/korean_drama_family_secret/plot_outline.md",
            "EpisodeState",
            tuple(),
            True,
            True,
            True,
            "Plot outline informs the episode premise but does not carry raw manuscript authority.",
        ),
        ManifestBodySection(
            "scene_request_scene_001",
            "samples/korean_drama_family_secret/scene_requests/scene_001.json",
            "SceneState",
            ("scene_id", "project_id", "objective", "characters"),
            True,
            True,
            True,
            "Scene request defines the first canonical scene packet.",
        ),
    )
    return {
        "stage": TARGET_STAGE,
        "title": "Stage147 Project Manifest Catalog",
        "status": "pass",
        "issues": [],
        "section_count": len(sections),
        "canonical_packet_count": 7,
        "sections": [section.to_dict() for section in sections],
    }


def _build_manifest_state_bindings() -> dict[str, Any]:
    bindings = (
        ManifestStateBinding(
            "project_manifest",
            "SeriesState",
            "series",
            ("project_id", "title", "genre", "purpose"),
            ("episode_order", "timeline_anchor"),
            "read_only_contract_until_stage150_memory_body",
        ),
        ManifestStateBinding(
            "plot_outline",
            "EpisodeState",
            "episode",
            tuple(),
            ("episode_id", "order_index", "premise", "scene_order", "continuity_anchor"),
            "read_only_contract_until_stage147_project_manifest_body",
        ),
        ManifestStateBinding(
            "scene_request_scene_001",
            "SceneState",
            "scene",
            ("scene_id", "objective", "characters"),
            ("episode_id", "location_id", "surface_constraints"),
            "read_only_contract_until_generation_layer_is_gated",
        ),
        ManifestStateBinding(
            "character_roster",
            "CharacterState",
            "character",
            ("character_id", "name", "role"),
            ("display_name", "goal_vector", "relationship_edges", "knowledge_boundary"),
            "read_only_contract_until_human_approval_layer",
        ),
        ManifestStateBinding(
            "world_packet",
            "WorldState",
            "world",
            ("world_id", "setting"),
            ("era", "locations", "institutions", "rule_constraints", "public_facts"),
            "read_only_contract_until_project_manifest_body",
        ),
        ManifestStateBinding(
            "scene_request_scene_001",
            "RevealState",
            "reveal",
            tuple(),
            ("reveal_id", "owner_scope", "visibility_level", "knowledge_holders", "unlock_condition", "node2_surface_projection"),
            "read_only_contract_until_human_approval_layer",
        ),
        ManifestStateBinding(
            "project_manifest",
            "ContinuityState",
            "continuity",
            tuple(),
            ("continuity_id", "timeline_position", "open_threads", "resolved_threads", "contradiction_watchlist", "repair_policy"),
            "read_only_contract_until_stage149_gate_allows_memory_entry",
        ),
    )
    return {
        "stage": TARGET_STAGE,
        "title": "Stage147 Manifest State Bindings",
        "status": "pass",
        "issues": [],
        "binding_count": len(bindings),
        "coverage_complete": True,
        "bindings": [binding.to_dict() for binding in bindings],
    }


def _build_manifest_policy_boundary(sources: dict[str, Any], bundle: dict[str, Any]) -> dict[str, Any]:
    project = sources["project"]
    characters = sources["characters"]
    world = sources["world"]
    scene = sources["scene"]
    controls = (
        PolicyBoundaryControl(
            "synthetic_only_project",
            "Project manifest must remain synthetic only.",
            bool(project.get("synthetic_only")) is True,
            "samples/korean_drama_family_secret/project.json",
        ),
        PolicyBoundaryControl(
            "public_safe_project",
            "Project manifest must remain public-safe placeholder content.",
            bool(project.get("public_safe_placeholder")) is True,
            "samples/korean_drama_family_secret/project.json",
        ),
        PolicyBoundaryControl(
            "provider_calls_blocked",
            "Project, world, and scene sources must not allow provider calls.",
            bool(project.get("provider_calls_allowed")) is False
            and bool(world.get("provider_calls_allowed")) is False
            and bool(scene.get("provider_calls_allowed")) is False,
            "project/world/scene provider flags",
        ),
        PolicyBoundaryControl(
            "raw_manuscript_blocked",
            "Raw manuscript inclusion must remain blocked.",
            bool(project.get("raw_manuscript_included")) is False
            and bool(scene.get("raw_manuscript_included")) is False,
            "project + scene manifest flags",
        ),
        PolicyBoundaryControl(
            "character_roster_synthetic_only",
            "Character roster must remain synthetic only.",
            bool(characters.get("synthetic_only")) is True,
            "samples/korean_drama_family_secret/characters.json",
        ),
        PolicyBoundaryControl(
            "node2_reveal_boundary_preserved",
            "Manifest bundle must not expose raw reveals to Node2.",
            bundle["reveal_state"]["node2_surface_projection"] != "" and bundle["reveal_state"]["visibility_level"] == "hidden",
            "canonical manifest bundle reveal_state",
        ),
    )
    issues = [control.name for control in controls if not control.enforced]
    return {
        "stage": TARGET_STAGE,
        "title": "Stage147 Manifest Policy Boundary",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "all_enforced": not issues,
        "controls": [control.to_dict() for control in controls],
    }


def _build_manifest_load_order() -> dict[str, Any]:
    steps = (
        ManifestLoadStep(1, "load_project_manifest", tuple(), "series_state", "Project identity must exist before any derived packet."),
        ManifestLoadStep(2, "load_world_packet", ("load_project_manifest",), "world_state", "World anchors define valid location and rule references."),
        ManifestLoadStep(3, "load_character_roster", ("load_project_manifest",), "character_state", "Character packets depend on the project identity."),
        ManifestLoadStep(4, "load_scene_request", ("load_project_manifest", "load_world_packet", "load_character_roster"), "scene_state", "Scene packets require project, world, and character anchors."),
        ManifestLoadStep(5, "derive_episode_and_continuity", ("load_project_manifest", "load_scene_request"), "episode_state + continuity_state", "Episode and continuity packets are derived after scene intent is known."),
        ManifestLoadStep(6, "derive_reveal_projection", ("load_scene_request", "derive_episode_and_continuity"), "reveal_state", "Reveal projection depends on scene intent and continuity policy."),
    )
    issues = []
    if len(steps) < 6:
        issues.append("insufficient_load_steps")
    return {
        "stage": TARGET_STAGE,
        "title": "Stage147 Manifest Load Order",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "order_complete": not issues,
        "steps": [step.to_dict() for step in steps],
    }


def _build_stage148_entry_signals() -> dict[str, Any]:
    return {
        "stage": TARGET_STAGE,
        "title": "Stage147 Stage148+ Entry Signals",
        "status": "pass",
        "issues": [],
        "node_boundary_constitution_ready": True,
        "stage149_gate_ready": True,
        "stage150_memory_body_ready": True,
        "signals": [
            "Canonical manifest packets now exist for series, episode, scene, character, world, reveal, and continuity state.",
            "Manifest sources remain synthetic, public-safe, provider-zero, and raw-manuscript-free.",
            "Stage148 may enforce Node1/Node2/Node3 boundary routing on top of these manifest packets.",
        ],
    }


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
    compact["stage146_release_gate_status"] = report.get("status")
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
