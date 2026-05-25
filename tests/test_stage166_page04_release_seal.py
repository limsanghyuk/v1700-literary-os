from __future__ import annotations

import json
import shutil
from pathlib import Path

from v1700.page04_release_seal import run_stage166_page04_release_seal
from v1700.gates.stage166_release_gate import run_stage166_release_gate

ROOT = Path(__file__).resolve().parents[1]
COPY_IGNORE = shutil.ignore_patterns(
    ".git",
    "__pycache__",
    ".pytest_cache",
    "*.pyc",
    "*.zip",
    "stage8*.json",
    "stage9*.json",
    "stage10*.json",
    "stage11*.json",
    "stage12*.json",
    "stage13*.json",
    "stage14*.json",
    "stage15*.json",
    "stage160*.json",
)


def _copy_repo_to(sandbox: Path) -> None:
    """Copy a lean Stage166 fixture repo for mutation regression tests.

    The full historical repository contains large legacy release reports.
    Mutation tests only need Stage161~166 Page04 evidence, docs, manifests,
    source files for connectivity checks, and package/checksum ledgers.
    """
    sandbox.mkdir(parents=True, exist_ok=True)

    def copy_file(rel: str) -> None:
        src = ROOT / rel
        dst = sandbox / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)

    def copy_tree(rel: str) -> None:
        src = ROOT / rel
        dst = sandbox / rel
        if src.exists():
            shutil.copytree(src, dst, ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".pytest_cache"), dirs_exist_ok=True)

    for rel in ("src", "tools", "docs", "manifests", "benchmarks", "samples"):
        copy_tree(rel)

    for rel in ("README.md", "RELEASE_NOTES.md", "package_manifest.json", "FILELIST.txt", "SHA256SUMS.txt", "pyproject.toml"):
        copy_file(rel)

    release_files = [
        "stage161_rendering_contract_report.json",
        "stage161_release_gate_report.json",
        "stage162_local_render_packet_store_report.json",
        "stage162_release_gate_report.json",
        "stage163_deterministic_render_plan_builder_report.json",
        "stage163_release_gate_report.json",
        "stage164_surface_draft_dry_run_renderer_report.json",
        "stage164_release_gate_report.json",
        "stage165_render_quality_boundary_preflight_report.json",
        "stage165_release_gate_report.json",
        "stage166_page04_release_seal_report.json",
        "stage166_release_gate_report.json",
        "stage166_summary.json",
        "stage166_release_asset_manifest.json",
    ]
    for name in release_files:
        copy_file(f"release/current/{name}")

    copy_tree("release/current/stage166_page04_release_seal_pack")
    copy_file("tests/test_stage166_page04_release_seal.py")


def _force_stage166(root: Path) -> None:
    manifest = root / "manifests/live_core_manifest.json"
    payload = json.loads(manifest.read_text(encoding="utf-8"))
    payload["active_version"] = "stage166"
    manifest.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def test_stage166_report_passes() -> None:
    result = run_stage166_page04_release_seal(ROOT)
    assert result["status"] == "pass"
    assert result["page04_sealed"] is True
    assert result["page04_total_stage_count"] == 6
    assert result["page04_upstream_stage_count"] == 5
    assert len(result["page04_release_checksum"]) == 64
    assert result["stage167_evaluation_contract_ready"] is True
    assert result["provider_generation_count"] == 0
    assert result["write_operation_count"] == 0
    assert result["node2_raw_reveal_access"] == 0


def test_stage166_release_gate_passes() -> None:
    result = run_stage166_release_gate(ROOT)
    assert result["status"] == "pass"
    assert result["page04_sealed"] is True
    assert result["stage167_evaluation_contract_ready"] is True
    assert result["provider_default_calls"] == 0
    assert result["runtime_execution_count"] == 0
    assert result["provider_generation_count"] == 0
    assert result["write_operation_count"] == 0
    assert result["node2_raw_reveal_access"] == 0
    assert result["boundary_violation_count"] == 0


def test_stage166_artifact_index_checks_existence() -> None:
    result = run_stage166_page04_release_seal(ROOT)
    index = result["parts"]["page04_artifact_index"]
    assert index["status"] == "pass"
    assert index["missing_count"] == 0
    assert all(asset["exists"] or asset.get("generated_by_stage166") for asset in index["assets"] if asset["required"])


def test_stage166_invariant_freeze_is_strict() -> None:
    result = run_stage166_page04_release_seal(ROOT)
    freeze = result["parts"]["page04_invariant_freeze"]
    assert freeze["status"] == "pass"
    frozen = {item["name"]: item["frozen_value"] for item in freeze["frozen"]}
    assert frozen["provider_default_calls"] == 0
    assert frozen["provider_generation_count"] == 0
    assert frozen["runtime_execution_count"] == 0
    assert frozen["write_operation_count"] == 0
    assert frozen["rendering_runtime_enabled"] is False
    assert frozen["generation_runtime_enabled"] is False
    assert frozen["provider_generation_enabled"] is False
    assert frozen["render_write_enabled"] is False
    assert frozen["runtime_training_enabled"] is False


def test_stage166_transition_criteria_points_to_stage167() -> None:
    result = run_stage166_page04_release_seal(ROOT)
    transition = result["parts"]["page04_transition_criteria"]
    assert transition["status"] == "pass"
    assert transition["next_stage"] == "stage167"
    assert transition["next_stage_title"] == "Evaluation Contract"
    assert transition["next_page"] == "Page05 Evaluation Body"


def test_stage166_blocks_missing_historical_artifact(tmp_path: Path) -> None:
    sandbox = tmp_path / "repo"
    _copy_repo_to(sandbox)
    _force_stage166(sandbox)
    missing = sandbox / "release/current/stage165_release_gate_report.json"
    missing.unlink()
    report = run_stage166_page04_release_seal(sandbox)
    assert report["status"] == "blocked"
    assert any("stage165_not_sealed" in issue or "missing:release/current/stage165_release_gate_report.json" in issue for issue in report["issues"])


def test_stage166_blocks_stage165_invariant_drift(tmp_path: Path) -> None:
    sandbox = tmp_path / "repo"
    _copy_repo_to(sandbox)
    _force_stage166(sandbox)

    report_path = sandbox / "release/current/stage165_render_quality_boundary_preflight_report.json"
    report = json.loads(report_path.read_text(encoding="utf-8"))
    report["provider_generation_enabled"] = True
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    result = run_stage166_page04_release_seal(sandbox)
    assert result["status"] == "blocked"
    assert any("stage165_report_invariant_drift:provider_generation_enabled" in issue for issue in result["issues"])



def test_stage166_blocks_any_upstream_gate_invariant_drift(tmp_path: Path) -> None:
    sandbox = tmp_path / "repo"
    _copy_repo_to(sandbox)
    _force_stage166(sandbox)

    report_path = sandbox / "release/current/stage164_release_gate_report.json"
    report = json.loads(report_path.read_text(encoding="utf-8"))
    report["provider_generation_enabled"] = True
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    result = run_stage166_page04_release_seal(sandbox)
    assert result["status"] == "blocked"
    assert any("stage164_gate_invariant_drift:provider_generation_enabled" in issue for issue in result["issues"])


def test_stage166_blocks_any_upstream_report_invariant_drift(tmp_path: Path) -> None:
    sandbox = tmp_path / "repo"
    _copy_repo_to(sandbox)
    _force_stage166(sandbox)

    report_path = sandbox / "release/current/stage162_local_render_packet_store_report.json"
    report = json.loads(report_path.read_text(encoding="utf-8"))
    report["write_operation_count"] = 1
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    result = run_stage166_page04_release_seal(sandbox)
    assert result["status"] == "blocked"
    assert any("stage162_report_invariant_drift:write_operation_count" in issue for issue in result["issues"])


def test_stage166_release_gate_rechecks_after_evidence_change(tmp_path: Path) -> None:
    sandbox = tmp_path / "repo"
    _copy_repo_to(sandbox)
    _force_stage166(sandbox)

    first = run_stage166_release_gate(sandbox)
    assert first["status"] == "pass"

    report_path = sandbox / "release/current/stage165_render_quality_boundary_preflight_report.json"
    report = json.loads(report_path.read_text(encoding="utf-8"))
    report["provider_generation_enabled"] = True
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    second = run_stage166_release_gate(sandbox)
    assert second["status"] == "blocked"
    assert any(
        "page04_invariant_freeze:stage165_report_invariant_drift:provider_generation_enabled" in issue
        for issue in second["stage166"]["issues"]
    )


def test_stage166_regression_snapshot_blocks_forbidden_filelist_entries(tmp_path: Path) -> None:
    sandbox = tmp_path / "repo"
    _copy_repo_to(sandbox)
    _force_stage166(sandbox)

    filelist = sandbox / "FILELIST.txt"
    filelist.write_text(filelist.read_text(encoding="utf-8") + "src/v1700/example/__pycache__/bad.pyc\n", encoding="utf-8")

    result = run_stage166_page04_release_seal(sandbox)
    assert result["status"] == "blocked"
    regression = result["parts"]["regression_snapshot"]
    assert regression["status"] == "blocked"
    assert regression["forbidden_cache_entries"] == 1
    assert any("page04_regression_snapshot_pass" in issue for issue in result["issues"])


def test_stage166_transition_ready_blocks_on_upstream_invariant_drift(tmp_path: Path) -> None:
    sandbox = tmp_path / "repo"
    _copy_repo_to(sandbox)
    _force_stage166(sandbox)

    report_path = sandbox / "release/current/stage161_rendering_contract_report.json"
    report = json.loads(report_path.read_text(encoding="utf-8"))
    report["runtime_execution_enabled"] = True
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    result = run_stage166_page04_release_seal(sandbox)
    transition = result["parts"]["page04_transition_criteria"]
    criteria = {item["name"]: item["status"] for item in transition["criteria"]}
    assert result["status"] == "blocked"
    assert result["stage167_evaluation_contract_ready"] is False
    assert criteria["stage167_evaluation_contract_ready"] == "blocked"


def test_stage166_package_manifest_matches_cross_validated_release_name() -> None:
    package = json.loads((ROOT / "package_manifest.json").read_text(encoding="utf-8"))
    asset = json.loads((ROOT / "release/current/stage166_release_asset_manifest.json").read_text(encoding="utf-8"))
    expected = "V1700_stage166_page04_release_seal_triple_validated_hardened_repository_with_artifacts.zip"
    assert package["canonical_package"] == expected
    assert asset["canonical_package"] == expected
    assert package["sha256_sidecar"] == f"{expected}.sha256"
    assert asset["sha256_sidecar"] == f"{expected}.sha256"



def test_stage166_regression_snapshot_blocks_actual_tree_cache_not_in_filelist(tmp_path: Path, monkeypatch) -> None:
    sandbox = tmp_path / "repo"
    _copy_repo_to(sandbox)
    _force_stage166(sandbox)

    cache_dir = sandbox / "src/v1700/page04_release_seal/__pycache__"
    cache_dir.mkdir(parents=True, exist_ok=True)
    (cache_dir / "hidden.pyc").write_bytes(b"cache")

    monkeypatch.setenv("V1700_STAGE166_STRICT_TREE_SCAN", "1")
    result = run_stage166_page04_release_seal(sandbox)
    regression = result["parts"]["regression_snapshot"]
    assert result["status"] == "blocked"
    assert regression["status"] == "blocked"
    assert regression["forbidden_cache_entries"] == 0
    assert regression["workspace_forbidden_cache_entries"] >= 1
    assert any("__pycache__" in issue or ".pyc" in issue for issue in regression["issues"])


def test_stage166_live_manifest_package_authority_matches_package_manifest() -> None:
    live = json.loads((ROOT / "manifests/live_core_manifest.json").read_text(encoding="utf-8"))
    package = json.loads((ROOT / "package_manifest.json").read_text(encoding="utf-8"))
    assert live["canonical_package"] == package["canonical_package"]
    assert live["canonical_sha256_sidecar"] == package["sha256_sidecar"]
