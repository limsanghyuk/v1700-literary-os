from __future__ import annotations

from pathlib import Path

from v1700.evaluation_regression.report import run_stage170_regression_negative_fixture_harness
from v1700.gates.stage170_release_gate import run_stage170_release_gate

ROOT = Path(__file__).resolve().parents[1]


def test_stage170_regression_negative_fixture_harness_passes() -> None:
    result = run_stage170_regression_negative_fixture_harness(ROOT)
    assert result["status"] == "pass"
    assert result["safe_fixture_pass"] is True
    assert result["negative_fixture_blocks"] is True
    assert result["regression_snapshot_pass"] is True
    assert result["fixture_coverage_pass"] is True
    assert result["boundary_fixture_pass"] is True
    assert result["determinism_channel_pass"] is True
    assert result["stage171_boundary_preflight_ready"] is True
    assert result["provider_default_calls"] == 0
    assert result["evaluation_write_enabled"] is False
    assert result["node2_raw_reveal_access"] == 0


def test_stage170_release_gate_passes() -> None:
    result = run_stage170_release_gate(ROOT)
    assert result["status"] == "pass"
    assert result["stage170"]["negative_fixture_blocks"] is True
    assert result["provider_default_calls"] == 0
    assert result["node2_raw_reveal_access"] == 0


def test_stage170_negative_fixtures_block_expected_channels() -> None:
    result = run_stage170_regression_negative_fixture_harness(ROOT)
    entries = {entry["fixture_id"]: entry for entry in result["parts"]["negative_fixture_results"]["entries"]}
    for fixture_id in (
        "quality_drop_fixture",
        "continuity_break_fixture",
        "raw_reveal_leak_fixture",
        "hidden_memory_projection_fixture",
        "provider_call_fixture",
        "mutation_command_fixture",
        "stale_stage166_evidence_fixture",
        "checksum_drift_fixture",
    ):
        assert entries[fixture_id]["actual_status"] == "blocked"
        assert entries[fixture_id]["expectation_status"] == "pass"
    assert entries["safe_baseline_fixture"]["actual_status"] == "pass"


def test_stage170_fixture_coverage_contains_required_channels() -> None:
    result = run_stage170_regression_negative_fixture_harness(ROOT)
    coverage = result["parts"]["fixture_coverage_matrix"]
    assert coverage["status"] == "pass"
    assert set(coverage["required_channels"]) <= set(coverage["covered_channels"])


def test_stage170_boundary_fixtures_are_not_overridable() -> None:
    result = run_stage170_regression_negative_fixture_harness(ROOT)
    boundary = result["parts"]["boundary_negative_fixture_matrix"]
    assert boundary["status"] == "pass"
    assert boundary["boundary_fixture_count"] >= 4
    assert all(entry["actual_status"] == "blocked" for entry in boundary["entries"])


def test_stage170_outputs_release_evidence_files() -> None:
    run_stage170_regression_negative_fixture_harness(ROOT)
    expected = [
        "release/current/stage170_regression_negative_fixture_harness_pack/negative_fixture_catalog.json",
        "release/current/stage170_regression_negative_fixture_harness_pack/negative_fixture_results.json",
        "release/current/stage170_regression_negative_fixture_harness_pack/fixture_coverage_matrix.json",
        "release/current/stage170_regression_negative_fixture_harness_pack/regression_snapshot.json",
        "release/current/stage170_regression_negative_fixture_harness_pack/fixture_replay_determinism.json",
        "release/current/stage170_regression_negative_fixture_harness_pack/boundary_negative_fixture_matrix.json",
        "release/current/stage170_regression_negative_fixture_harness_pack/stage171_entry_criteria.json",
    ]
    assert all((ROOT / rel).exists() for rel in expected)
