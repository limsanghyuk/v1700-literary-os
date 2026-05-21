from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from .contracts import IntegrityCheck, IntegrityReport

TARGET_STAGE = "stage140"
TARGET_LABEL = "Stage140"
TARGET_VERSION = "1.40.0"
TARGET_TITLE = "Release Integrity & Product Proof Gate"


def run_stage_metadata_consistency(root: Path | None = None) -> dict[str, Any]:
    root = root or Path(__file__).resolve().parents[3]
    live = _read_json(root / "manifests/live_core_manifest.json")
    package = _read_json(root / "package_manifest.json")
    pyproject = _read_text(root / "pyproject.toml")
    readme = _read_text(root / "README.md")
    notes = _read_text(root / "RELEASE_NOTES.md")
    active = str(live.get("active_version", ""))
    package_active = str(package.get("active_version", ""))
    package_stage = str(package.get("stage", ""))
    py_version = _py_value(pyproject, "version")
    py_description = _py_value(pyproject, "description")
    required_files = [
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
    ]
    checks = [
        _check("live_manifest_active_stage", active == TARGET_STAGE, TARGET_STAGE, active, root / "manifests/live_core_manifest.json"),
        _check("readme_current_stage_matches_live", TARGET_LABEL in readme and TARGET_TITLE in readme, f"{TARGET_LABEL} {TARGET_TITLE}", _excerpt(readme, TARGET_LABEL), root / "README.md"),
        _check("package_manifest_active_matches_live", package_active == active == TARGET_STAGE and package_stage == TARGET_STAGE, TARGET_STAGE, f"active={package_active}; stage={package_stage}", root / "package_manifest.json"),
        _check("package_manifest_paths_match_stage", all(TARGET_STAGE in str(package.get(k, "")) for k in ("canonical_package", "patch_report", "release_gate", "asset_manifest")), "stage140 package paths", json.dumps({k: package.get(k, "") for k in ("canonical_package", "patch_report", "release_gate", "asset_manifest")}, sort_keys=True), root / "package_manifest.json"),
        _check("pyproject_version_matches_stage", py_version == TARGET_VERSION, TARGET_VERSION, py_version, root / "pyproject.toml"),
        _check("pyproject_description_matches_stage", TARGET_LABEL in py_description and TARGET_TITLE in py_description, f"{TARGET_LABEL} - {TARGET_TITLE}", py_description, root / "pyproject.toml"),
        _check("release_notes_match_stage", TARGET_LABEL in notes and TARGET_TITLE in notes, f"{TARGET_LABEL} {TARGET_TITLE}", _excerpt(notes, TARGET_LABEL), root / "RELEASE_NOTES.md"),
    ]
    for rel in required_files:
        checks.append(_check(f"required_file_present:{rel}", (root / rel).exists(), "file exists", "exists" if (root / rel).exists() else "missing", root / rel))
    issues = tuple(c.name for c in checks if c.status != "pass")
    return IntegrityReport(
        stage=TARGET_STAGE,
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
