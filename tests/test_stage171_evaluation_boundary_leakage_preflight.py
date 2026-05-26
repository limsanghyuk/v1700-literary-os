from __future__ import annotations

import copy
import json
from pathlib import Path

from v1700.evaluation_boundary_preflight.report import run_stage171_evaluation_boundary_leakage_preflight
from v1700.gates.stage171_release_gate import run_stage171_release_gate

ROOT = Path(__file__).resolve().parents[1]


def test_stage171_evaluation_boundary_leakage_preflight_passes() -> None:
    result = run_stage171_evaluation_boundary_leakage_preflight(ROOT)
    assert result["status"] == "pass"
    assert result["stage170_regression_harness_inherited"] is True
    assert result["boundary_invariant_freeze_pass"] is True
    assert result["node2_surface_projection_scan_pass"] is True
    assert result["controlled_negative_fixture_quarantine_pass"] is True
    assert result["leakage_zero_snapshot_pass"] is True
    assert result["stage172_page05_release_seal_ready"] is True
    assert result["provider_default_calls"] == 0
    assert result["node2_raw_reveal_access"] == 0
    assert result["evaluation_write_enabled"] is False


def test_stage171_release_gate_passes() -> None:
    result = run_stage171_release_gate(ROOT)
    assert result["status"] == "pass"
    assert result["stage171"]["stage172_page05_release_seal_ready"] is True
    assert result["checks"]["node2_projection_scan_pass"]["status"] == "pass"
    assert result["provider_default_calls"] == 0
    assert result["node2_raw_reveal_access"] == 0


def test_stage171_quarantines_controlled_negative_fixtures() -> None:
    result = run_stage171_evaluation_boundary_leakage_preflight(ROOT)
    quarantine = result["parts"]["controlled_negative_fixture_quarantine"]
    assert quarantine["status"] == "pass"
    assert quarantine["controlled_fixture_artifact_count"] >= 3
    assert all(entry["counts_as_leakage"] is False for entry in quarantine["entries"])


def test_stage171_node2_surface_scan_has_no_forbidden_hits() -> None:
    result = run_stage171_evaluation_boundary_leakage_preflight(ROOT)
    scan = result["parts"]["node2_surface_projection_scan"]
    assert scan["status"] == "pass"
    assert all(entry["token_hit_count"] == 0 for entry in scan["entries"])


def test_stage171_detects_node2_projection_token_leak(tmp_path: Path) -> None:
    source = ROOT / "release/current/stage169_deterministic_quality_continuity_evaluator_pack/node2_evaluation_projection_verdict.json"
    payload = json.loads(source.read_text(encoding="utf-8"))
    mutated = copy.deepcopy(payload)
    mutated["entries"][0]["surface_projection_note"] = "raw_reveal leaked to surface"
    scratch = tmp_path / "repo"
    scratch.mkdir()
    # minimal copy of required tree files for the scan and pre-existing reports
    for rel in [
        "manifests/live_core_manifest.json",
        "release/current/stage167_release_gate_report.json",
        "release/current/stage168_release_gate_report.json",
        "release/current/stage169_release_gate_report.json",
        "release/current/stage170_release_gate_report.json",
        "release/current/stage167_evaluation_contract_report.json",
        "release/current/stage168_local_evaluation_packet_store_report.json",
        "release/current/stage169_deterministic_quality_continuity_evaluator_report.json",
        "release/current/stage170_regression_negative_fixture_harness_report.json",
        "release/current/stage168_local_evaluation_packet_store_pack/node2_evaluation_packet_projection_matrix.json",
        "release/current/stage170_regression_negative_fixture_harness_pack/negative_fixture_catalog.json",
        "release/current/stage170_regression_negative_fixture_harness_pack/negative_fixture_results.json",
        "release/current/stage170_regression_negative_fixture_harness_pack/boundary_negative_fixture_matrix.json",
    ]:
        src = ROOT / rel
        dst = scratch / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_bytes(src.read_bytes())
    target = scratch / "release/current/stage169_deterministic_quality_continuity_evaluator_pack/node2_evaluation_projection_verdict.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(mutated), encoding="utf-8")
    live = json.loads((scratch / "manifests/live_core_manifest.json").read_text(encoding="utf-8"))
    live["active_version"] = "stage171"
    (scratch / "manifests/live_core_manifest.json").write_text(json.dumps(live), encoding="utf-8")
    result = run_stage171_evaluation_boundary_leakage_preflight(scratch)
    assert result["status"] == "blocked"
    assert "node2_surface_projection_scan_blocked" in result["issues"]


def test_stage171_outputs_release_evidence_files() -> None:
    run_stage171_evaluation_boundary_leakage_preflight(ROOT)
    expected = [
        "release/current/stage171_evaluation_boundary_leakage_preflight_pack/inherited_stage_gate_matrix.json",
        "release/current/stage171_evaluation_boundary_leakage_preflight_pack/boundary_invariant_matrix.json",
        "release/current/stage171_evaluation_boundary_leakage_preflight_pack/node2_surface_projection_scan.json",
        "release/current/stage171_evaluation_boundary_leakage_preflight_pack/forbidden_operation_registry.json",
        "release/current/stage171_evaluation_boundary_leakage_preflight_pack/controlled_negative_fixture_quarantine.json",
        "release/current/stage171_evaluation_boundary_leakage_preflight_pack/leakage_zero_snapshot.json",
        "release/current/stage171_evaluation_boundary_leakage_preflight_pack/stage172_entry_criteria.json",
    ]
    assert all((ROOT / rel).exists() for rel in expected)
