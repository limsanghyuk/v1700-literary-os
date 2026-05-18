from pathlib import Path

from tools.run_mandatory_predevelopment_check import run_mandatory_predevelopment_check


ROOT = Path(__file__).resolve().parents[1]


def test_mandatory_predevelopment_check_passes_for_stage101_repository():
    report = run_mandatory_predevelopment_check(ROOT)
    assert report["status"] == "pass"
    assert "gitnexus_index_freshness" in report["must_check"]
    assert report["invariant_checks"]["stage101_gate_pass"] is True
    assert report["invariant_checks"]["active_stage_gate_pass"] is True
    assert report["invariant_checks"]["main_release_gate_pass"] is True
    assert report["invariant_checks"]["gitnexus_runtime_dependency_required_false"] is True
