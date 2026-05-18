from pathlib import Path

from v1700.gates.release_gate import run_release_gate
from v1700.gates.stage100_release_gate import run_stage100_release_gate

ROOT = Path(__file__).resolve().parents[1]


def test_stage100_release_gate_inherits_stage99_and_declares_rc():
    gate = run_stage100_release_gate(ROOT)
    assert gate["status"] == "pass"
    assert gate["stage99_release_gate"]["status"] == "pass"
    assert gate["dual_mode_evaluation_status"] == "pass"
    assert gate["provider_certification_status"] == "pass"
    assert gate["v430_comparison_bridge_status"] == "pass"
    assert gate["checks"]["readme_active_stage_consistency_pass"]["status"] == "pass"
    assert gate["checks"]["package_manifest_canonical_reference_pass"]["status"] == "pass"
    assert gate["checks"]["stage100_artifact_export_report_pass"]["status"] == "pass"


def test_main_release_gate_includes_stage100_when_active():
    result = run_release_gate()
    assert result["status"] == "pass"
    assert result["stage100_release_gate"]["status"] == "pass"
