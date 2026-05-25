from __future__ import annotations

import shutil
from pathlib import Path

from v1700.gates.stage154_release_gate import run_stage154_release_gate
from v1700.page02_release_seal import run_stage154_page02_release_seal

ROOT = Path(__file__).resolve().parents[1]


def test_stage154_page02_release_seal_passes() -> None:
    result = run_stage154_page02_release_seal(ROOT)
    assert result["status"] == "pass"
    assert result["page02_sealed"] is True
    assert result["page02_stage_count"] == 5
    assert result["page02_total_stage_count"] == 5
    assert result["page02_upstream_stage_count"] == 4
    assert result["provider_default_calls"] == 0
    assert result["node2_raw_reveal_access"] == 0


def test_stage154_page02_stage_chain_is_complete() -> None:
    result = run_stage154_page02_release_seal(ROOT)
    chain = result["parts"]["page02_stage_chain"]
    assert chain["status"] == "pass"
    assert chain["sealed_count"] == 4
    assert [item["stage"] for item in chain["stages"]] == ["150", "151", "152", "153"]


def test_stage154_blocker_registry_freezes_privilege_expansion() -> None:
    result = run_stage154_page02_release_seal(ROOT)
    registry = result["parts"]["page02_blocker_registry"]
    assert registry["status"] == "pass"
    assert registry["blocker_count"] == registry["blocked_capability_count"]
    assert registry["blocker_count"] >= 10


def test_stage154_boundary_freeze_has_zero_leakage() -> None:
    result = run_stage154_page02_release_seal(ROOT)
    freeze = result["parts"]["page02_boundary_freeze"]
    assert freeze["status"] == "pass"
    assert result["boundary_violation_count"] == 0
    assert result["credential_leakage"] == 0
    check_names = {check["name"] for check in freeze["checks"]}
    assert "raw_manuscript_provider_leakage_zero" in check_names
    assert "raw_manuscript_cross_project_leakage_zero" in check_names


def test_stage154_artifact_index_records_real_existence() -> None:
    result = run_stage154_page02_release_seal(ROOT)
    index = result["parts"]["page02_artifact_index"]
    assert index["status"] == "pass"
    assert index["missing_count"] == 0
    assert index["asset_count"] == index["required_count"]
    assert index["generated_by_stage154_count"] >= 1
    assets = {asset["path"]: asset for asset in index["assets"]}
    assert assets["docs/stages/stage154.md"]["exists"] is True
    assert assets["release/current/stage154_page02_release_seal_pack/page02_artifact_index.json"]["generated_by_stage154"] is True


def test_stage154_artifact_index_blocks_missing_historical_asset(tmp_path: Path) -> None:
    work = tmp_path / "repo"
    ignore = shutil.ignore_patterns("__pycache__", ".pytest_cache")
    shutil.copytree(ROOT, work, ignore=ignore)
    missing = work / "docs/stages/stage153.md"
    missing.unlink()
    report = work / "release/current/stage154_page02_release_seal_report.json"
    if report.exists():
        report.unlink()
    result = run_stage154_page02_release_seal(work)
    assert result["status"] == "blocked"
    assert "page02_artifact_index_blocked" in result["issues"]
    assert any("docs/stages/stage153.md" in issue for issue in result["issues"])


def test_stage154_release_gate_passes() -> None:
    result = run_stage154_release_gate(ROOT)
    assert result["status"] == "pass"
    assert result["provider_default_calls"] == 0
    assert result["node2_raw_reveal_access"] == 0
    assert result["memory_write_enabled"] is False
    assert result["runtime_training_enabled"] is False
