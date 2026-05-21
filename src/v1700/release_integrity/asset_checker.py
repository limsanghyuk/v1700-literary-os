from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .contracts import IntegrityCheck, IntegrityReport

ASSET_TARGETS = {
    "stage140": {
        "package": "V1700_stage140_release_integrity_product_proof_gate_release_integrated_repository_with_artifacts.zip",
        "release_report": "release/current/stage140_release_integrity_report.json",
        "release_gate_report": "release/current/stage140_release_gate_report.json",
    },
    "stage141": {
        "package": "V1700_stage141_prose_generation_e2e_harness_release_integrated_repository_with_artifacts.zip",
        "release_report": "release/current/stage141_prose_generation_e2e_report.json",
        "release_gate_report": "release/current/stage141_release_gate_report.json",
    },
    "stage142": {
        "package": "V1700_stage142_longform_benchmark_pack_release_integrated_repository_with_artifacts.zip",
        "release_report": "release/current/stage142_longform_benchmark_pack_report.json",
        "release_gate_report": "release/current/stage142_release_gate_report.json",
    },
    "stage143": {
        "package": "V1700_stage143_user_cli_api_minimum_docs_release_integrated_repository_with_artifacts.zip",
        "release_report": "release/current/stage143_user_cli_api_docs_report.json",
        "release_gate_report": "release/current/stage143_release_gate_report.json",
    },
}


def expected_stage140_asset_manifest() -> dict[str, Any]:
    return expected_release_asset_manifest("stage140")


def expected_release_asset_manifest(stage: str) -> dict[str, Any]:
    target = ASSET_TARGETS.get(stage, ASSET_TARGETS["stage140"])
    expected_package = str(target["package"])
    expected_sidecar = f"{expected_package}.sha256"
    return {
        "stage": stage,
        "active_version": stage,
        "canonical_package": expected_package,
        "sha256_sidecar": expected_sidecar,
        "sha256_authority": "release sidecar file is authoritative",
        "filelist": "FILELIST.txt",
        "sha256_sums": "SHA256SUMS.txt",
        "release_report": str(target["release_report"]),
        "release_gate_report": str(target["release_gate_report"]),
        "package_manifest": "package_manifest.json",
        "product_proof_sample": "samples/korean_drama_family_secret/project.json",
        "benchmark_contract": "benchmarks/longform_output/expected_metrics.json",
        "provider_default_calls": 0,
        "live_provider_call_count_in_release_gate": 0,
        "node2_raw_reveal_access": 0,
    }


def run_release_asset_integrity(root: Path | None = None) -> dict[str, Any]:
    root = root or Path(__file__).resolve().parents[3]
    live = _read_json(root / "manifests" / "live_core_manifest.json")
    target_stage = str(live.get("active_version", "stage140"))
    expected = expected_release_asset_manifest(target_stage)
    expected_package = str(expected["canonical_package"])
    expected_sidecar = str(expected["sha256_sidecar"])
    package_path = root / "package_manifest.json"
    asset_path = root / "release" / "current" / f"{target_stage}_release_asset_manifest.json"
    package = _read_json(package_path)
    asset = _read_json(asset_path)
    checks = [
        _check("asset_manifest_present", asset_path.exists(), "exists", "exists" if asset_path.exists() else "missing", asset_path),
        _check("asset_manifest_stage", asset.get("stage") == target_stage, target_stage, str(asset.get("stage", "")), asset_path),
        _check("canonical_package_name", asset.get("canonical_package") == expected_package, expected_package, str(asset.get("canonical_package", "")), asset_path),
        _check("sha256_sidecar_name", asset.get("sha256_sidecar") == expected_sidecar, expected_sidecar, str(asset.get("sha256_sidecar", "")), asset_path),
        _check("package_manifest_canonical_matches", package.get("canonical_package") == asset.get("canonical_package"), str(asset.get("canonical_package", "")), str(package.get("canonical_package", "")), package_path),
        _check("package_manifest_sidecar_matches", package.get("sha256_sidecar") == asset.get("sha256_sidecar"), str(asset.get("sha256_sidecar", "")), str(package.get("sha256_sidecar", "")), package_path),
        _check("filelist_declared", bool(asset.get("filelist")), "filelist declared", str(asset.get("filelist", "")), asset_path),
        _check("release_sidecar_authoritative", asset.get("sha256_authority") == "release sidecar file is authoritative", "release sidecar file is authoritative", str(asset.get("sha256_authority", "")), asset_path),
    ]
    issues = tuple(c.name for c in checks if c.status != "pass")
    return IntegrityReport(
        stage=target_stage,
        title="Current Stage Release Asset Integrity",
        status="pass" if not issues else "blocked",
        checks=tuple(checks),
        issues=issues,
        counters={"check_count": len(checks), "pass_count": sum(1 for c in checks if c.status == "pass"), "blocked_count": len(issues)},
    ).to_dict()


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}


def _check(name: str, condition: bool, expected: str, actual: str, path: Path) -> IntegrityCheck:
    return IntegrityCheck(name=name, status="pass" if condition else "blocked", expected=expected, actual=actual, path=path.as_posix())
