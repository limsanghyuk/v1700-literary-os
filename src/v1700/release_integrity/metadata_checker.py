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
    return IntegrityCheck(name=name, status="pass" if condition else "blocked", expected=expected, actual=actual, path=path.as_posix())


def _excerpt(text: str, token: str) -> str:
    index = text.find(token)
    return text[:160] if index < 0 else text[max(0, index - 40): index + 120]
