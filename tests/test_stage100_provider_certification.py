from pathlib import Path

from v1700.stage100.provider_certification import run_stage100_provider_certification

ROOT = Path(__file__).resolve().parents[1]


def test_stage100_provider_certification_keeps_release_provider_zero():
    report = run_stage100_provider_certification(ROOT)
    assert report["status"] == "pass"
    assert report["providers_certified"] == 6
    assert report["live_provider_call_count_in_release"] == 0
    assert report["raw_manuscript_provider_leakage"] == 0

