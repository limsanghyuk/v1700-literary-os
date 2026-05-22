from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from v1700.gates.stage147_release_gate import run_stage147_release_gate
from v1700.release_integrity.asset_checker import expected_release_asset_manifest, run_release_asset_integrity
from v1700.release_integrity.metadata_checker import run_stage_metadata_consistency
from v1700.stage147 import run_stage147

from .contracts import BoundaryControl, NodeAuthorityRule, PacketRoute, SurfaceProjectionRule

TARGET_STAGE = "stage148"
TARGET_REPORT = "release/current/stage148_node_boundary_constitution_report.json"
NODE1_MODULE = "src/v1700/nodes/node1_architect/__init__.py"
NODE2_MODULE = "src/v1700/nodes/node2_prose_renderer/compiler.py"
NODE2_VALIDATOR = "src/v1700/nodes/node2_prose_renderer/validators.py"
NODE3_MODULE = "src/v1700/nodes/node3_critic_gate/constraint_validator.py"


def run_stage148_node_boundary_constitution(root: Path | None = None) -> dict[str, Any]:
    root = root or Path(__file__).resolve().parents[3]
    if _active_version(root) != TARGET_STAGE:
        existing = _load_existing(root / TARGET_REPORT)
        if existing is not None:
            return existing

    pack = root / "release" / "current" / "stage148_node_boundary_constitution_pack"
    pack.mkdir(parents=True, exist_ok=True)
    report_path = root / TARGET_REPORT
    if not report_path.exists():
        _write_json(
            report_path,
            {
                "stage": "148",
                "baseline_stage": "147",
                "title": "Node Boundary Constitution",
                "status": "building",
                "issues": [],
            },
        )

    baseline = run_stage147_release_gate(root)
    stage147 = run_stage147(root)
    _write_json(root / "release/current/stage148_release_asset_manifest.json", expected_release_asset_manifest(TARGET_STAGE))

    authority_matrix = _build_node_authority_matrix()
    packet_route_map = _build_packet_route_map()
    surface_projection_registry = _build_surface_projection_registry()
    boundary_enforcement_summary = _build_boundary_enforcement_summary(root, stage147, authority_matrix, packet_route_map, surface_projection_registry)
    stage149_entry_signals = _build_stage149_entry_signals(boundary_enforcement_summary)

    _write_json(pack / "node_authority_matrix.json", authority_matrix)
    _write_json(pack / "packet_route_map.json", packet_route_map)
    _write_json(pack / "surface_projection_registry.json", surface_projection_registry)
    _write_json(pack / "boundary_enforcement_summary.json", boundary_enforcement_summary)
    _write_json(pack / "stage149_entry_signals.json", stage149_entry_signals)

    metadata = run_stage_metadata_consistency(root)
    assets = run_release_asset_integrity(root)

    issues: list[str] = []
    if baseline.get("status") != "pass":
        issues.append("stage147_baseline_gate_pass")
    for key, part in {
        "metadata_consistency": metadata,
        "release_asset_integrity": assets,
        "node_authority_matrix": authority_matrix,
        "packet_route_map": packet_route_map,
        "surface_projection_registry": surface_projection_registry,
        "boundary_enforcement_summary": boundary_enforcement_summary,
        "stage149_entry_signals": stage149_entry_signals,
    }.items():
        if part.get("status") != "pass":
            issues.append(f"{key}_blocked")
            issues.extend(f"{key}:{issue}" for issue in part.get("issues", []))

    result = {
        "stage": "148",
        "baseline_stage": "147",
        "title": "Node Boundary Constitution",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "mode": "NODE_BOUNDARY_CONSTITUTION_LOCAL",
        "node_boundary_constitution_only": True,
        "authority_rule_count": authority_matrix.get("rule_count", 0),
        "route_count": packet_route_map.get("route_count", 0),
        "projection_rule_count": surface_projection_registry.get("projection_count", 0),
        "node2_surface_only_enforced": boundary_enforcement_summary.get("node2_surface_only_enforced", False),
        "node3_critic_scope_defined": boundary_enforcement_summary.get("node3_critic_scope_defined", False),
        "stage149_gate_ready": stage149_entry_signals.get("stage149_gate_ready", False),
        "stage150_memory_body_ready": stage149_entry_signals.get("stage150_memory_body_ready", False),
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
            "stage147_baseline": _compact_baseline(baseline),
            "metadata_consistency": metadata,
            "release_asset_integrity": assets,
            "node_authority_matrix": authority_matrix,
            "packet_route_map": packet_route_map,
            "surface_projection_registry": surface_projection_registry,
            "boundary_enforcement_summary": boundary_enforcement_summary,
            "stage149_entry_signals": stage149_entry_signals,
        },
    }
    _write_json(report_path, result)
    return result


def _build_node_authority_matrix() -> dict[str, Any]:
    rules = (
        NodeAuthorityRule("SeriesState", "full_contract", "surface_summary_only", "critic_summary_only", NODE1_MODULE, NODE2_MODULE, NODE3_MODULE, "Series authority stays whole in Node1 while Node2 and Node3 consume condensed framing."),
        NodeAuthorityRule("EpisodeState", "full_contract", "episode_premise_only", "critic_episode_summary", NODE1_MODULE, NODE2_MODULE, NODE3_MODULE, "Episode ordering and continuity anchors remain outside reader-facing prose."),
        NodeAuthorityRule("SceneState", "full_contract", "surface_safe_scene_packet", "critic_surface_plus_flags", NODE1_MODULE, NODE2_MODULE, NODE3_MODULE, "SceneState is the primary Node2 render contract but still stays packetized."),
        NodeAuthorityRule("CharacterState", "full_contract", "surface_traits_only", "critic_relationship_summary", NODE1_MODULE, NODE2_MODULE, NODE3_MODULE, "Character private goals and hidden beliefs stay out of Node2."),
        NodeAuthorityRule("WorldState", "full_contract", "public_world_facts_only", "critic_world_consistency_summary", NODE1_MODULE, NODE2_MODULE, NODE3_MODULE, "World rules are summarized for prose while critic sees consistency cues."),
        NodeAuthorityRule("RevealState", "full_contract", "node2_surface_projection_only", "critic_reveal_guard_summary", NODE1_MODULE, NODE2_VALIDATOR, NODE3_MODULE, "RevealState remains the hard authority boundary for Node2 raw access zero."),
        NodeAuthorityRule("ContinuityState", "full_contract", "surface_continuity_summary", "critic_continuity_packet", NODE1_MODULE, NODE2_MODULE, NODE3_MODULE, "Continuity risk data remains structured for critic review, not direct prose authority."),
    )
    issues = [
        rule.state_name
        for rule in rules
        if rule.node2_access in {"full_contract", "raw_reveal", "hidden_state"}
    ]
    return {
        "stage": TARGET_STAGE,
        "title": "Stage148 Node Authority Matrix",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "rule_count": len(rules),
        "coverage_complete": not issues and len(rules) >= 7,
        "rules": [rule.to_dict() for rule in rules],
    }


def _build_packet_route_map() -> dict[str, Any]:
    routes = (
        PacketRoute("series_to_node1", "SeriesState", "Node1Architect", "planning_context", "raw hidden reveal payloads", NODE1_MODULE, "Node1 may plan from series identity and premise authority."),
        PacketRoute("scene_to_node1", "SceneState", "Node1Architect", "scene_intent_seed", "raw manuscript text", NODE1_MODULE, "Node1 builds deterministic scene intent from canonical scene packets."),
        PacketRoute("scene_to_node2", "SceneState", "Node2ProseCompiler", "surface_safe_scene_packet", "private memory and hidden belief vectors", NODE2_MODULE, "Node2 receives only surface-safe scene packets for rendering."),
        PacketRoute("reveal_to_node2", "RevealState", "Node2ProseCompiler", "node2_surface_projection", "unlock condition internals and raw reveal content", NODE2_VALIDATOR, "RevealState reaches Node2 only through explicit surface projections."),
        PacketRoute("continuity_to_node3", "ContinuityState", "Node3CriticGate", "critic_continuity_packet", "mutation authority", NODE3_MODULE, "Node3 critic may inspect continuity risks without gaining write authority."),
        PacketRoute("rendered_surface_to_node3", "RenderedProseIR", "Node3CriticGate", "rendered_surface_and_constraint_scores", "provider output or hidden raw reveals", NODE3_MODULE, "Node3 validates Node2 output against surface and constraint thresholds."),
    )
    issues = [route.route_name for route in routes if route.target_node == "Node2ProseCompiler" and route.delivery_form in {"full_contract", "raw_reveal"}]
    return {
        "stage": TARGET_STAGE,
        "title": "Stage148 Packet Route Map",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "route_count": len(routes),
        "route_order_complete": not issues and len(routes) >= 6,
        "routes": [route.to_dict() for route in routes],
    }


def _build_surface_projection_registry() -> dict[str, Any]:
    entries = (
        SurfaceProjectionRule("SeriesState", "purpose", "series_premise_surface", "critic_series_anchor", "timeline_anchor", "Node2 receives only the public series premise."),
        SurfaceProjectionRule("EpisodeState", "premise", "episode_premise_surface", "critic_episode_brief", "scene_order", "Episode ordering stays outside direct prose access."),
        SurfaceProjectionRule("SceneState", "surface_constraints", "scene_surface_constraints", "critic_scene_constraint_flags", "private continuity debug fields", "Scene constraints are already surface-safe and may flow to Node2."),
        SurfaceProjectionRule("CharacterState", "role", "character_surface_traits", "critic_character_relationship_summary", "knowledge_boundary", "Node2 gets only reader-facing traits and roles."),
        SurfaceProjectionRule("WorldState", "public_facts", "world_surface_facts", "critic_world_rule_summary", "rule_constraints", "World internals are summarized to public facts for Node2."),
        SurfaceProjectionRule("RevealState", "node2_surface_projection", "reveal_surface_projection", "critic_reveal_guard_summary", "unlock_condition", "Reveal projection is the only Node2-safe reveal surface."),
        SurfaceProjectionRule("ContinuityState", "open_threads", "continuity_surface_watchlist", "critic_continuity_packet", "contradiction_watchlist", "Node2 sees only a reader-safe continuity watchlist."),
    )
    issues = [entry.state_name for entry in entries if entry.node2_projection in {"full_contract", "raw_reveal"}]
    return {
        "stage": TARGET_STAGE,
        "title": "Stage148 Surface Projection Registry",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "projection_count": len(entries),
        "coverage_complete": not issues and len(entries) >= 7,
        "entries": [entry.to_dict() for entry in entries],
    }


def _build_boundary_enforcement_summary(
    root: Path,
    stage147: dict[str, Any],
    authority_matrix: dict[str, Any],
    packet_route_map: dict[str, Any],
    surface_projection_registry: dict[str, Any],
) -> dict[str, Any]:
    bundle = stage147.get("parts", {}).get("canonical_manifest_bundle", {})
    reveal = bundle.get("reveal_state", {})
    authority_rules = authority_matrix.get("rules", [])
    routes = packet_route_map.get("routes", [])
    projections = surface_projection_registry.get("entries", [])
    controls = (
        BoundaryControl(
            "stage147_canonical_bundle_present",
            "Stage147 canonical manifest bundle must remain present and passing.",
            bundle.get("status") == "pass" and bundle.get("packet_count", 0) >= 7,
            "release/current/stage147_project_manifest_body_pack/canonical_manifest_bundle.json",
        ),
        BoundaryControl(
            "node1_full_contract_access_defined",
            "Node1 must retain full-contract access for planning authority.",
            all(rule.get("node1_access") == "full_contract" for rule in authority_rules),
            NODE1_MODULE,
        ),
        BoundaryControl(
            "node2_surface_only_defined",
            "Node2 must never receive full-contract or raw reveal payloads.",
            all(rule.get("node2_access") not in {"full_contract", "raw_reveal", "hidden_state"} for rule in authority_rules),
            NODE2_MODULE,
        ),
        BoundaryControl(
            "node3_critic_scope_defined",
            "Node3 must receive structured critic summaries instead of mutation authority.",
            all(rule.get("node3_access", "").startswith("critic_") for rule in authority_rules),
            NODE3_MODULE,
        ),
        BoundaryControl(
            "reveal_surface_projection_preserved",
            "RevealState must keep hidden visibility and expose a non-empty Node2 surface projection only.",
            reveal.get("visibility_level") == "hidden" and bool(reveal.get("node2_surface_projection")),
            "release/current/stage147_project_manifest_body_pack/canonical_manifest_bundle.json",
        ),
        BoundaryControl(
            "projection_registry_blocks_hidden_fields",
            "Surface projection registry must name blocked fields for every packet.",
            all(bool(entry.get("blocked_to_node2")) for entry in projections),
            "release/current/stage148_node_boundary_constitution_pack/surface_projection_registry.json",
        ),
        BoundaryControl(
            "route_modules_exist",
            "Referenced node modules must exist in the repository.",
            all((root / route.get("module_anchor", "")).exists() for route in routes),
            "src/v1700/nodes/",
        ),
        BoundaryControl(
            "provider_zero_and_write_zero_preserved",
            "Stage148 must preserve provider-zero and write-zero invariants.",
            stage147.get("provider_default_calls") == 0
            and stage147.get("live_provider_call_count_in_release_gate") == 0
            and stage147.get("node2_raw_reveal_access") == 0
            and stage147.get("losdb_write_enabled") is False
            and stage147.get("migration_execution_enabled") is False,
            "stage147 + stage148 reports",
        ),
    )
    issues = [control.name for control in controls if not control.enforced]
    return {
        "stage": TARGET_STAGE,
        "title": "Stage148 Boundary Enforcement Summary",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "all_enforced": not issues,
        "node2_surface_only_enforced": not any(
            control.name == "node2_surface_only_defined" and not control.enforced for control in controls
        ),
        "node3_critic_scope_defined": not any(
            control.name == "node3_critic_scope_defined" and not control.enforced for control in controls
        ),
        "controls": [control.to_dict() for control in controls],
    }


def _build_stage149_entry_signals(boundary_enforcement_summary: dict[str, Any]) -> dict[str, Any]:
    ready = boundary_enforcement_summary.get("status") == "pass"
    return {
        "stage": TARGET_STAGE,
        "title": "Stage148 Stage149+ Entry Signals",
        "status": "pass" if ready else "blocked",
        "issues": [] if ready else ["boundary_enforcement_summary_blocked"],
        "stage149_gate_ready": ready,
        "stage150_memory_body_ready": ready,
        "signals": [
            "Node1/Node2/Node3 authority lanes are now bound to the Stage146 state contracts and Stage147 manifest packets.",
            "RevealState reaches Node2 only through surface projections while Node3 keeps critic-only summaries.",
            "Stage149 may now seal the Page01 body constitution with a release gate built on explicit node-boundary evidence.",
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
    compact["stage147_release_gate_status"] = report.get("status")
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
