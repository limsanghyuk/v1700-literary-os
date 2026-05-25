from __future__ import annotations

import hashlib
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
    "stage144": {
        "package": "V1700_stage144_split_ci_runtime_strategy_release_integrated_repository_with_artifacts.zip",
        "release_report": "release/current/stage144_split_ci_runtime_strategy_report.json",
        "release_gate_report": "release/current/stage144_release_gate_report.json",
    },
    "stage145": {
        "package": "V1700_stage145_body_constitution_release_integrated_repository_with_artifacts.zip",
        "release_report": "release/current/stage145_body_constitution_report.json",
        "release_gate_report": "release/current/stage145_release_gate_report.json",
    },
    "stage146": {
        "package": "V1700_stage146_narrative_state_contract_release_integrated_repository_with_artifacts.zip",
        "release_report": "release/current/stage146_narrative_state_contract_report.json",
        "release_gate_report": "release/current/stage146_release_gate_report.json",
    },
    "stage147": {
        "package": "V1700_stage147_project_manifest_body_release_integrated_repository_with_artifacts.zip",
        "release_report": "release/current/stage147_project_manifest_body_report.json",
        "release_gate_report": "release/current/stage147_release_gate_report.json",
    },
    "stage148": {
        "package": "V1700_stage148_node_boundary_constitution_release_integrated_repository_with_artifacts.zip",
        "release_report": "release/current/stage148_node_boundary_constitution_report.json",
        "release_gate_report": "release/current/stage148_release_gate_report.json",
    },
    "stage149": {
        "package": "V1700_stage149_body_constitution_release_gate_release_integrated_repository_with_artifacts.zip",
        "release_report": "release/current/stage149_body_constitution_release_gate_report.json",
        "release_gate_report": "release/current/stage149_release_gate_report.json",
    },
    "stage150": {
        "package": "V1700_stage150_memory_contract_release_integrated_repository_with_artifacts.zip",
        "release_report": "release/current/stage150_memory_contract_report.json",
        "release_gate_report": "release/current/stage150_release_gate_report.json",
    },
    "stage151": {
        "package": "V1700_stage151_local_read_only_memory_store_release_integrated_repository_with_artifacts.zip",
        "release_report": "release/current/stage151_local_read_only_memory_store_report.json",
        "release_gate_report": "release/current/stage151_release_gate_report.json",
    },
    "stage152": {
        "package": "V1700_stage152_memory_query_interface_release_integrated_repository_with_artifacts.zip",
        "release_report": "release/current/stage152_memory_query_interface_report.json",
        "release_gate_report": "release/current/stage152_release_gate_report.json",
    },
    "stage153": {
        "package": "V1700_stage153_memory_health_leakage_boundary_release_integrated_repository_with_artifacts.zip",
        "release_report": "release/current/stage153_memory_health_leakage_boundary_report.json",
        "release_gate_report": "release/current/stage153_release_gate_report.json",
    },

    "stage157": {
        "package": "V1700_stage157_deterministic_plan_graph_builder_release_integrated_repository_with_artifacts.zip",
        "release_report": "release/current/stage157_deterministic_plan_graph_builder_report.json",
        "release_gate_report": "release/current/stage157_release_gate_report.json",
    },
    "stage154": {
        "package": "V1700_stage154_page02_release_seal_release_integrated_repository_with_artifacts.zip",
        "release_report": "release/current/stage154_page02_release_seal_report.json",
        "release_gate_report": "release/current/stage154_release_gate_report.json",
    },
    "stage155": {
        "package": "V1700_stage155_execution_contract_release_integrated_repository_with_artifacts.zip",
        "release_report": "release/current/stage155_execution_contract_report.json",
        "release_gate_report": "release/current/stage155_release_gate_report.json",
    },
    "stage156": {
        "package": "V1700_stage156_local_execution_packet_store_release_integrated_repository_with_artifacts.zip",
        "release_report": "release/current/stage156_local_execution_packet_store_report.json",
        "release_gate_report": "release/current/stage156_release_gate_report.json",
    },
    "stage158": {
        "package": "V1700_stage158_dependency_conflict_preflight_release_integrated_repository_with_artifacts.zip",
        "release_report": "release/current/stage158_dependency_conflict_preflight_report.json",
        "release_gate_report": "release/current/stage158_release_gate_report.json",
    },
    "stage159": {
        "package": "V1700_stage159_execution_dry_run_trace_release_integrated_repository_with_artifacts.zip",
        "release_report": "release/current/stage159_execution_dry_run_trace_report.json",
        "release_gate_report": "release/current/stage159_release_gate_report.json",
    },
    "stage160": {
        "package": "V1700_stage160_page03_release_seal_release_integrated_repository_with_artifacts.zip",
        "release_report": "release/current/stage160_page03_release_seal_report.json",
        "release_gate_report": "release/current/stage160_release_gate_report.json",
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
    checks.extend(_checksum_ledger_checks(root, asset))
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


def _checksum_ledger_checks(root: Path, asset: dict[str, Any]) -> list[IntegrityCheck]:
    filelist_path = root / str(asset.get("filelist", "FILELIST.txt"))
    sums_path = root / str(asset.get("sha256_sums", "SHA256SUMS.txt"))
    checks = [
        _check("filelist_present", filelist_path.exists(), "exists", "exists" if filelist_path.exists() else "missing", filelist_path),
        _check("sha256_sums_present", sums_path.exists(), "exists", "exists" if sums_path.exists() else "missing", sums_path),
    ]
    if not filelist_path.exists() or not sums_path.exists():
        return checks

    filelist_entries = _read_lines(filelist_path)
    sums = _read_sha256_sums(sums_path)
    digest_exempt = _digest_exempt_entries(asset, filelist_entries)
    missing = [entry for entry in filelist_entries if entry not in sums]
    extra = [entry for entry in sums if entry not in set(filelist_entries)]
    mismatches = []
    missing_files = []
    for entry in filelist_entries:
        path = root / entry
        if not path.is_file():
            missing_files.append(entry)
            continue
        digest = _stable_file_sha256(path)
        if entry not in digest_exempt and sums.get(entry) != digest:
            mismatches.append(entry)

    policy_ok = "SHA256SUMS.txt" not in filelist_entries
    checks.extend(
        [
            _check(
                "sha256_sums_self_reference_policy",
                policy_ok,
                "SHA256SUMS.txt is excluded from FILELIST to avoid self-referential checksum drift",
                "excluded" if policy_ok else "listed",
                filelist_path,
            ),
            _check(
                "filelist_checksum_coverage",
                not missing,
                "all FILELIST entries covered by SHA256SUMS",
                _sample(missing),
                sums_path,
            ),
            _check(
                "sha256_sums_no_extra_entries",
                not extra,
                "no SHA256SUMS entries outside FILELIST",
                _sample(extra),
                sums_path,
            ),
            _check(
                "filelist_entries_exist",
                not missing_files,
                "all FILELIST entries exist",
                _sample(missing_files),
                filelist_path,
            ),
            _check(
                "generated_report_digest_exemption_policy",
                all(entry in filelist_entries for entry in digest_exempt),
                "mutable generated reports remain listed but are not content-digest blocking during gate execution",
                _sample(sorted(digest_exempt - set(filelist_entries))),
                filelist_path,
            ),
            _check(
                "sha256_sums_content_match",
                not mismatches,
                "all SHA256SUMS digests match current normalized file contents",
                _sample(mismatches),
                sums_path,
            ),
        ]
    )
    return checks


def _digest_exempt_entries(asset: dict[str, Any], filelist_entries: list[str]) -> set[str]:
    entries = {
        str(asset.get("release_report", "")).replace("\\", "/"),
        str(asset.get("release_gate_report", "")).replace("\\", "/"),
        "release/current/release_gate_report.json",
    }
    entries.update(
        entry
        for entry in filelist_entries
        if entry.startswith("release/current/")
        and (entry.endswith("_report.json") or entry.endswith("_summary.json"))
    )
    return {entry for entry in entries if entry}


def _stable_file_sha256(path: Path) -> str:
    data = path.read_bytes()
    if b"\0" not in data:
        data = data.replace(b"\r\n", b"\n")
    return hashlib.sha256(data).hexdigest()


def _read_lines(path: Path) -> list[str]:
    return [line.strip().replace("\\", "/") for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def _read_sha256_sums(path: Path) -> dict[str, str]:
    sums: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        parts = line.strip().split(maxsplit=1)
        if len(parts) == 2:
            sums[parts[1].replace("\\", "/")] = parts[0].lower()
    return sums


def _sample(items: list[str]) -> str:
    if not items:
        return "none"
    sample = ", ".join(items[:5])
    if len(items) > 5:
        sample += f", ... (+{len(items) - 5})"
    return sample


def _check(name: str, condition: bool, expected: str, actual: str, path: Path) -> IntegrityCheck:
    return IntegrityCheck(name=name, status="pass" if condition else "blocked", expected=expected, actual=actual, path=_display_path(path))


def _display_path(path: Path) -> str:
    try:
        return path.relative_to(Path.cwd()).as_posix()
    except ValueError:
        return path.as_posix()
