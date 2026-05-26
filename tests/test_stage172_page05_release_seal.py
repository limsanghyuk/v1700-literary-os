from __future__ import annotations

import copy
import json
from pathlib import Path

from v1700.gates.stage172_release_gate import run_stage172_release_gate
from v1700.page05_release_seal import run_stage172_page05_release_seal

ROOT = Path(__file__).resolve().parents[1]


def test_stage172_page05_release_seal_passes() -> None:
    result = run_stage172_page05_release_seal(ROOT)
    assert result["status"] == "pass"
    assert result["page05_sealed"] is True
    assert result["page05_total_stage_count"] == 6
    assert result["page05_stage_chain_pass"] is True
    assert result["page05_invariant_freeze_pass"] is True
    assert result["page05_evaluation_evidence_pass"] is True
    assert result["page05_regression_snapshot_pass"] is True
    assert result["stage173_governance_contract_ready"] is True
    assert result["provider_default_calls"] == 0
    assert result["node2_raw_reveal_access"] == 0


def test_stage172_release_gate_passes() -> None:
    result = run_stage172_release_gate(ROOT)
    assert result["status"] == "pass"
    assert result["page05_sealed"] is True
    assert result["stage173_governance_contract_ready"] is True
    assert result["checks"]["quality_channel_pass"]["status"] == "pass"
    assert result["checks"]["boundary_channel_pass"]["status"] == "pass"


def test_stage172_outputs_release_evidence_files() -> None:
    run_stage172_page05_release_seal(ROOT)
    expected = [
        "release/current/stage172_page05_release_seal_pack/page05_stage_chain.json",
        "release/current/stage172_page05_release_seal_pack/page05_release_seal_matrix.json",
        "release/current/stage172_page05_release_seal_pack/page05_artifact_index.json",
        "release/current/stage172_page05_release_seal_pack/page05_invariant_freeze.json",
        "release/current/stage172_page05_release_seal_pack/page05_evaluation_evidence_matrix.json",
        "release/current/stage172_page05_release_seal_pack/page05_transition_criteria.json",
        "release/current/stage172_page05_release_seal_pack/page05_release_seal.json",
        "release/current/stage172_page05_release_seal_pack/regression_snapshot.json",
    ]
    assert all((ROOT / rel).exists() for rel in expected)


def test_stage172_blocks_upstream_boundary_drift(tmp_path: Path) -> None:
    scratch = tmp_path / "repo"
    scratch.mkdir()
    for rel in [
        "manifests/live_core_manifest.json",
        "FILELIST.txt",
        "release/current/stage167_evaluation_contract_report.json",
        "release/current/stage167_release_gate_report.json",
        "release/current/stage168_local_evaluation_packet_store_report.json",
        "release/current/stage168_release_gate_report.json",
        "release/current/stage169_deterministic_quality_continuity_evaluator_report.json",
        "release/current/stage169_release_gate_report.json",
        "release/current/stage170_regression_negative_fixture_harness_report.json",
        "release/current/stage170_release_gate_report.json",
        "release/current/stage171_evaluation_boundary_leakage_preflight_report.json",
        "release/current/stage171_release_gate_report.json",
    ]:
        src = ROOT / rel
        dst = scratch / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_bytes(src.read_bytes())
    live = json.loads((scratch / "manifests/live_core_manifest.json").read_text(encoding="utf-8"))
    live["active_version"] = "stage172"
    (scratch / "manifests/live_core_manifest.json").write_text(json.dumps(live), encoding="utf-8")
    report_path = scratch / "release/current/stage171_release_gate_report.json"
    payload = json.loads(report_path.read_text(encoding="utf-8"))
    payload["node2_raw_reveal_access"] = 1
    report_path.write_text(json.dumps(payload), encoding="utf-8")
    result = run_stage172_page05_release_seal(scratch)
    assert result["status"] == "blocked"
    assert any("invariant_drift" in issue for issue in result["issues"])


def test_stage172_blocks_missing_regression_channel(tmp_path: Path) -> None:
    scratch = tmp_path / "repo"
    scratch.mkdir()
    for rel in [
        "manifests/live_core_manifest.json",
        "FILELIST.txt",
        "release/current/stage167_evaluation_contract_report.json",
        "release/current/stage167_release_gate_report.json",
        "release/current/stage168_local_evaluation_packet_store_report.json",
        "release/current/stage168_release_gate_report.json",
        "release/current/stage169_deterministic_quality_continuity_evaluator_report.json",
        "release/current/stage169_release_gate_report.json",
        "release/current/stage170_regression_negative_fixture_harness_report.json",
        "release/current/stage170_release_gate_report.json",
        "release/current/stage171_evaluation_boundary_leakage_preflight_report.json",
        "release/current/stage171_release_gate_report.json",
    ]:
        src = ROOT / rel
        dst = scratch / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_bytes(src.read_bytes())
    live = json.loads((scratch / "manifests/live_core_manifest.json").read_text(encoding="utf-8"))
    live["active_version"] = "stage172"
    (scratch / "manifests/live_core_manifest.json").write_text(json.dumps(live), encoding="utf-8")
    path = scratch / "release/current/stage170_regression_negative_fixture_harness_report.json"
    payload = json.loads(path.read_text(encoding="utf-8"))
    payload["regression_snapshot_pass"] = False
    path.write_text(json.dumps(payload), encoding="utf-8")
    result = run_stage172_page05_release_seal(scratch)
    assert result["status"] == "blocked"
    assert "page05_evaluation_evidence_matrix_blocked" in result["issues"]


def test_stage172_artifact_index_is_complete() -> None:
    result = run_stage172_page05_release_seal(ROOT)
    index = result["parts"]["page05_artifact_index"]
    assert index["status"] == "pass"
    assert index["artifact_count"] >= 20
