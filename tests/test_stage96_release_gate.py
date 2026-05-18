from pathlib import Path

from v1700.gates.stage96_release_gate import run_stage96_release_gate
from v1700.stage96.orchestrator import run_stage96_pipeline


def test_stage96_pipeline_runs_all_three_phases():
    report = run_stage96_pipeline(Path(__file__).resolve().parents[1])
    assert report["status"] == "pass"
    assert report["checks"]["narrative_optimization"]["status"] == "pass"
    assert report["checks"]["manuscript_learning"]["status"] == "pass"
    assert report["checks"]["provider_ensemble"]["status"] == "pass"


def test_stage96_release_gate_preserves_provider_zero_boundaries():
    report = run_stage96_release_gate(Path(__file__).resolve().parents[1])
    assert report["status"] == "pass"
    assert report["provider_call_count"] == 0
    assert report["live_provider_call_count"] == 0
    assert report["node2_raw_reveal_access"] == 0
    assert report["coefficient_drift_summary"]["status"] == "pass"
