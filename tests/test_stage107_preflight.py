from pathlib import Path
from v1700.stage107.orchestrator import run_stage107_0_production_suite_preflight

def test_stage107_preflight_keeps_gitnexus_fallback_visible():
    report = run_stage107_0_production_suite_preflight(Path(__file__).resolve().parents[1])
    assert report['status'] == 'pass'
    assert report['gitnexus_preflight_status'] == 'python_fallback_visible'
    assert report['provider_zero'] is True
