from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from .contracts import IntegrityCheck, IntegrityReport

TARGETS: dict[str, dict[str, Any]] = {
    "stage140": {
        "label": "Stage140",
        "version": "1.40.0",
        "title": "Release Integrity & Product Proof Gate",
        "required_files": [
            "docs/stages/stage140.md",
            "docs/proposals/stage140_release_integrity_product_proof_proposal.md",
            "docs/architecture/stage140_release_integrity_product_proof_blueprint.md",
            "docs/development/stage140_developer_handoff.md",
            "manifests/stage140_manifest.json",
            "manifests/stage140_release_integrity_manifest.json",
            "manifests/stage140_branchpoint_trace_manifest.json",
            "manifests/live_core_stage140_overlay.json",
            "release/current/stage140_release_asset_manifest.json",
            "samples/korean_drama_family_secret/project.json",
            "benchmarks/longform_output/expected_metrics.json",
        ],
    },
    "stage141": {
        "label": "Stage141",
        "version": "1.41.0",
        "title": "Prose Generation E2E Harness",
        "required_files": [
            "docs/stages/stage141.md",
            "docs/proposals/stage141_proposal.md",
            "docs/architecture/stage141_blueprint.md",
            "docs/development/stage141_developer_handoff.md",
            "manifests/stage141_manifest.json",
            "manifests/stage141_prose_generation_e2e_manifest.json",
            "manifests/stage141_branchpoint_trace_manifest.json",
            "manifests/live_core_stage141_overlay.json",
            "release/current/stage141_release_asset_manifest.json",
            "release/current/stage141_prose_generation_e2e_report.json",
            "benchmarks/longform_output/results/stage141_scene_001_benchmark_result.json",
            "benchmarks/longform_output/results/stage141_scene_001_rendered.md",
        ],
    },
    "stage142": {
        "label": "Stage142",
        "version": "1.42.0",
        "title": "Longform Benchmark Pack",
        "required_files": [
            "docs/stages/stage142.md",
            "docs/proposals/stage142_proposal.md",
            "docs/architecture/stage142_blueprint.md",
            "docs/development/stage142_developer_handoff.md",
            "manifests/stage142_manifest.json",
            "manifests/stage142_longform_benchmark_pack_manifest.json",
            "manifests/stage142_branchpoint_trace_manifest.json",
            "manifests/live_core_stage142_overlay.json",
            "release/current/stage142_release_asset_manifest.json",
            "release/current/stage142_longform_benchmark_pack_report.json",
            "benchmarks/longform_output/results/stage142_benchmark_pack_summary.json",
            "benchmarks/longform_output/results/stage142_rendered_samples.json",
        ],
    },
    "stage143": {
        "label": "Stage143",
        "version": "1.43.0",
        "title": "User CLI/API Minimum Docs",
        "required_files": [
            "docs/stages/stage143.md",
            "docs/proposals/stage143_proposal.md",
            "docs/architecture/stage143_blueprint.md",
            "docs/development/stage143_developer_handoff.md",
            "docs/user/cli_quickstart.md",
            "docs/user/api_minimum.md",
            "docs/user/examples/render_request.json",
            "docs/user/examples/render_response.json",
            "manifests/stage143_manifest.json",
            "manifests/stage143_user_cli_api_docs_manifest.json",
            "manifests/stage143_branchpoint_trace_manifest.json",
            "manifests/live_core_stage143_overlay.json",
            "release/current/stage143_release_asset_manifest.json",
            "release/current/stage143_user_cli_api_docs_report.json",
            "release/current/stage143_user_cli_api_docs_pack/cli_contract.json",
            "release/current/stage143_user_cli_api_docs_pack/api_contract.json",
            "release/current/stage143_user_cli_api_docs_pack/user_docs_index.json",
        ],
    },
    "stage144": {
        "label": "Stage144",
        "version": "1.44.0",
        "title": "Split CI Runtime Strategy",
        "required_files": [
            "docs/stages/stage144.md",
            "docs/proposals/stage144_proposal.md",
            "docs/architecture/stage144_blueprint.md",
            "docs/development/stage144_developer_handoff.md",
            "manifests/stage144_manifest.json",
            "manifests/stage144_split_ci_runtime_strategy_manifest.json",
            "manifests/stage144_branchpoint_trace_manifest.json",
            "manifests/live_core_stage144_overlay.json",
            "release/current/stage144_release_asset_manifest.json",
            "release/current/stage144_split_ci_runtime_strategy_report.json",
            "release/current/stage144_split_ci_runtime_strategy_pack/workflow_inventory.json",
            "release/current/stage144_split_ci_runtime_strategy_pack/runtime_lane_matrix.json",
            "release/current/stage144_split_ci_runtime_strategy_pack/workflow_trigger_summary.json",
            "release/current/stage144_split_ci_runtime_strategy_pack/release_surface_contract.json",
            ".github/workflows/ci-fast.yml",
        ],
    },
    "stage145": {
        "label": "Stage145",
        "version": "1.45.0",
        "title": "Body Constitution",
        "required_files": [
            "docs/stages/stage145.md",
            "docs/proposals/stage145_body_constitution_proposal.md",
            "docs/architecture/stage145_body_constitution_blueprint.md",
            "docs/development/stage145_developer_handoff.md",
            "manifests/stage145_manifest.json",
            "manifests/stage145_body_constitution_manifest.json",
            "manifests/stage145_branchpoint_trace_manifest.json",
            "manifests/live_core_stage145_overlay.json",
            "release/current/stage145_release_asset_manifest.json",
            "release/current/stage145_body_constitution_report.json",
            "release/current/stage145_body_constitution_pack/formula_classification.json",
            "release/current/stage145_body_constitution_pack/constitution_invariants.json",
            "release/current/stage145_body_constitution_pack/body_layer_map.json",
            "release/current/stage145_body_constitution_pack/stage150_entry_criteria.json",
            ".github/workflows/ci-fast.yml",
        ],
    },
    "stage146": {
        "label": "Stage146",
        "version": "1.46.0",
        "title": "Narrative State Contract",
        "required_files": [
            "docs/stages/stage146.md",
            "docs/proposals/stage146_narrative_state_contract_proposal.md",
            "docs/architecture/stage146_narrative_state_contract_blueprint.md",
            "docs/development/stage146_developer_handoff.md",
            "manifests/stage146_manifest.json",
            "manifests/stage146_narrative_state_contract_manifest.json",
            "manifests/stage146_branchpoint_trace_manifest.json",
            "manifests/live_core_stage146_overlay.json",
            "release/current/stage146_release_asset_manifest.json",
            "release/current/stage146_narrative_state_contract_report.json",
            "release/current/stage146_narrative_state_contract_pack/state_shape_catalog.json",
            "release/current/stage146_narrative_state_contract_pack/state_hierarchy.json",
            "release/current/stage146_narrative_state_contract_pack/continuity_rulebook.json",
            "release/current/stage146_narrative_state_contract_pack/reveal_boundary_matrix.json",
            "release/current/stage146_narrative_state_contract_pack/stage147_entry_signals.json",
            ".github/workflows/ci-fast.yml",
        ],
    },
    "stage147": {
        "label": "Stage147",
        "version": "1.47.0",
        "title": "Project Manifest Body",
        "required_files": [
            "docs/stages/stage147.md",
            "docs/proposals/stage147_project_manifest_body_proposal.md",
            "docs/architecture/stage147_project_manifest_body_blueprint.md",
            "docs/development/stage147_developer_handoff.md",
            "manifests/stage147_manifest.json",
            "manifests/stage147_project_manifest_body_manifest.json",
            "manifests/stage147_branchpoint_trace_manifest.json",
            "manifests/live_core_stage147_overlay.json",
            "release/current/stage147_release_asset_manifest.json",
            "release/current/stage147_project_manifest_body_report.json",
            "release/current/stage147_project_manifest_body_pack/canonical_manifest_bundle.json",
            "release/current/stage147_project_manifest_body_pack/project_manifest_catalog.json",
            "release/current/stage147_project_manifest_body_pack/manifest_state_bindings.json",
            "release/current/stage147_project_manifest_body_pack/manifest_policy_boundary.json",
            "release/current/stage147_project_manifest_body_pack/manifest_load_order.json",
            "release/current/stage147_project_manifest_body_pack/stage148_entry_signals.json",
            ".github/workflows/ci-fast.yml",
        ],
    },
    "stage148": {
        "label": "Stage148",
        "version": "1.48.0",
        "title": "Node Boundary Constitution",
        "required_files": [
            "docs/stages/stage148.md",
            "docs/proposals/stage148_node_boundary_constitution_proposal.md",
            "docs/architecture/stage148_node_boundary_constitution_blueprint.md",
            "docs/development/stage148_developer_handoff.md",
            "manifests/stage148_manifest.json",
            "manifests/stage148_node_boundary_constitution_manifest.json",
            "manifests/stage148_branchpoint_trace_manifest.json",
            "manifests/live_core_stage148_overlay.json",
            "release/current/stage148_release_asset_manifest.json",
            "release/current/stage148_node_boundary_constitution_report.json",
            "release/current/stage148_node_boundary_constitution_pack/node_authority_matrix.json",
            "release/current/stage148_node_boundary_constitution_pack/packet_route_map.json",
            "release/current/stage148_node_boundary_constitution_pack/surface_projection_registry.json",
            "release/current/stage148_node_boundary_constitution_pack/boundary_enforcement_summary.json",
            "release/current/stage148_node_boundary_constitution_pack/stage149_entry_signals.json",
            ".github/workflows/ci-fast.yml",
        ],
    },
    "stage149": {
        "label": "Stage149",
        "version": "1.49.0",
        "title": "Body Constitution Release Gate",
        "required_files": [
            "docs/stages/stage149.md",
            "docs/proposals/stage149_body_constitution_release_gate_proposal.md",
            "docs/architecture/stage149_body_constitution_release_gate_blueprint.md",
            "docs/development/stage149_developer_handoff.md",
            "manifests/stage149_manifest.json",
            "manifests/stage149_body_constitution_release_gate_manifest.json",
            "manifests/stage149_branchpoint_trace_manifest.json",
            "manifests/live_core_stage149_overlay.json",
            "release/current/stage149_release_asset_manifest.json",
            "release/current/stage149_body_constitution_release_gate_report.json",
            "release/current/stage149_body_constitution_release_gate_pack/body_constitution_gate_matrix.json",
            "release/current/stage149_body_constitution_release_gate_pack/page01_constitution_seal.json",
            "release/current/stage149_body_constitution_release_gate_pack/stage150_readiness_matrix.json",
            "release/current/stage149_body_constitution_release_gate_pack/release_blocker_registry.json",
            "release/current/stage149_body_constitution_release_gate_pack/lineage_evidence_index.json",
            ".github/workflows/ci-fast.yml",
        ],
    },
    "stage150": {
        "label": "Stage150",
        "version": "1.50.0",
        "title": "Memory Contract",
        "required_files": [
            "docs/stages/stage150.md",
            "docs/proposals/stage150_memory_contract_proposal.md",
            "docs/architecture/stage150_memory_contract_blueprint.md",
            "docs/development/stage150_developer_handoff.md",
            "manifests/stage150_manifest.json",
            "manifests/stage150_memory_contract_manifest.json",
            "manifests/stage150_branchpoint_trace_manifest.json",
            "manifests/live_core_stage150_overlay.json",
            "release/current/stage150_release_asset_manifest.json",
            "release/current/stage150_memory_contract_report.json",
            "release/current/stage150_release_gate_report.json",
            "release/current/stage150_memory_contract_pack/preflight15_matrix.json",
            "release/current/stage150_memory_contract_pack/memory_record_contracts.json",
            "release/current/stage150_memory_contract_pack/memory_boundary_policy.json",
            "release/current/stage150_memory_contract_pack/memory_write_policy.json",
            "release/current/stage150_memory_contract_pack/node2_projection_policy.json",
            ".github/workflows/ci-fast.yml",
        ],
    },
}


def run_stage_metadata_consistency(root: Path | None = None) -> dict[str, Any]:
    root = root or Path(__file__).resolve().parents[3]
    live = _read_json(root / "manifests/live_core_manifest.json")
    target_stage = str(live.get("active_version", "stage140"))
    target = TARGETS.get(target_stage, TARGETS["stage140"])
    package = _read_json(root / "package_manifest.json")
    pyproject = _read_text(root / "pyproject.toml")
    readme = _read_text(root / "README.md")
    notes = _read_text(root / "RELEASE_NOTES.md")
    active = str(live.get("active_version", ""))
    package_active = str(package.get("active_version", ""))
    package_stage = str(package.get("stage", ""))
    py_version = _py_value(pyproject, "version")
    py_description = _py_value(pyproject, "description")
    label = str(target["label"])
    version = str(target["version"])
    title = str(target["title"])
    required_files = list(target["required_files"])
    checks = [
        _check("live_manifest_active_stage", active == target_stage, target_stage, active, root / "manifests/live_core_manifest.json"),
        _check("readme_current_stage_matches_live", label in readme and title in readme, f"{label} {title}", _excerpt(readme, label), root / "README.md"),
        _check("package_manifest_active_matches_live", package_active == active == target_stage and package_stage == target_stage, target_stage, f"active={package_active}; stage={package_stage}", root / "package_manifest.json"),
        _check("package_manifest_paths_match_stage", all(target_stage in str(package.get(k, "")) for k in ("canonical_package", "patch_report", "release_gate", "asset_manifest")), f"{target_stage} package paths", json.dumps({k: package.get(k, "") for k in ("canonical_package", "patch_report", "release_gate", "asset_manifest")}, sort_keys=True), root / "package_manifest.json"),
        _check("pyproject_version_matches_stage", py_version == version, version, py_version, root / "pyproject.toml"),
        _check("pyproject_description_matches_stage", label in py_description and title in py_description, f"{label} - {title}", py_description, root / "pyproject.toml"),
        _check("release_notes_match_stage", label in notes and title in notes, f"{label} {title}", _excerpt(notes, label), root / "RELEASE_NOTES.md"),
    ]
    for rel in required_files:
        checks.append(_check(f"required_file_present:{rel}", (root / rel).exists(), "file exists", "exists" if (root / rel).exists() else "missing", root / rel))
    issues = tuple(c.name for c in checks if c.status != "pass")
    return IntegrityReport(
        stage=target_stage,
        title="Stage Metadata Consistency",
        status="pass" if not issues else "blocked",
        checks=tuple(checks),
        issues=issues,
        counters={"check_count": len(checks), "pass_count": sum(1 for c in checks if c.status == "pass"), "blocked_count": len(issues)},
    ).to_dict()


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}


def _py_value(text: str, name: str) -> str:
    match = re.search(rf"(?m)^\s*{re.escape(name)}\s*=\s*\"([^\"]*)\"", text)
    return match.group(1) if match else ""


def _check(name: str, condition: bool, expected: str, actual: str, path: Path) -> IntegrityCheck:
    return IntegrityCheck(name=name, status="pass" if condition else "blocked", expected=expected, actual=actual, path=_display_path(path))


def _display_path(path: Path) -> str:
    try:
        return path.relative_to(Path.cwd()).as_posix()
    except ValueError:
        return path.as_posix()


def _excerpt(text: str, token: str) -> str:
    index = text.find(token)
    return text[:160] if index < 0 else text[max(0, index - 40): index + 120]
