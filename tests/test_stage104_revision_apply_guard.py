from pathlib import Path
from v1700.stage104.orchestrator import run_stage104_3_review_decision_loop
ROOT = Path(__file__).resolve().parents[1]

def test_revision_apply_guard_report_passes():
    report = run_stage104_3_review_decision_loop(ROOT)
    assert report["status"] == "pass"
    assert report["checks"]["unauthorized_apply_zero"] is True
