from pathlib import Path

from v1700.stage100.gitnexus_rc_preflight import run_stage100_rc_preflight

ROOT = Path(__file__).resolve().parents[1]


def test_stage100_rc_preflight_preserves_gitnexus_and_branchpoints():
    report = run_stage100_rc_preflight(ROOT)
    assert report["status"] == "pass"
    assert report["index_freshness_status"] == "pass"
    assert report["survival_matrix_status"] == "pass"
    assert report["symbol_to_branchpoint_trace_status"] == "pass"
    assert report["metadata"]["p0_coverage"] == 1.0

