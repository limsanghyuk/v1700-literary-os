from pathlib import Path

from v1700.gates.release_gate import run_release_gate
from v1700.gates.stage102_release_gate import run_stage102_release_gate
from v1700.traceability.symbol_trace import build_symbol_to_branchpoint_trace_manifest

ROOT = Path(__file__).resolve().parents[1]


def test_stage102_release_gate_promotes_stage101_with_writer_trial_evidence():
    gate = run_stage102_release_gate(ROOT)
    assert gate["status"] == "pass"
    assert gate["stage101_release_gate"]["status"] == "pass"
    assert gate["checks"]["writer_trial_pass"]["status"] == "pass"
    assert gate["checks"]["blind_benchmark_pass"]["status"] == "pass"
    assert gate["checks"]["revision_efficiency_pass"]["status"] == "pass"
    assert gate["provider_default_calls"] == 0
    assert gate["raw_manuscript_provider_leakage"] == 0


def test_stage102_symbol_trace_manifest_covers_trial_branchpoints():
    manifest = build_symbol_to_branchpoint_trace_manifest(ROOT)
    ids = {entry["branchpoint_id"] for entry in manifest["entries"]}
    assert manifest["status"] == "pass"
    assert "BP_STAGE102_REAL_WRITER_TRIAL" in ids
    assert "BP_STAGE102_BLIND_BENCHMARK" in ids
    assert "BP_STAGE102_REVISION_EFFICIENCY" in ids
    assert "BP_STAGE102_PROVIDER_ZERO_PRIVACY" in ids


def test_main_release_gate_includes_stage102_when_active():
    result = run_release_gate()
    assert result["status"] == "pass"
    assert result["stage101_release_gate"]["status"] == "pass"
    assert result["stage102_release_gate"]["status"] == "pass"
