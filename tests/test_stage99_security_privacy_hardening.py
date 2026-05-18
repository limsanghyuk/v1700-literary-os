from pathlib import Path

from v1700.security_hardening.report import run_stage99_1_security_privacy_hardening

ROOT = Path(__file__).resolve().parents[1]


def test_stage99_1_replays_security_privacy_boundaries_at_zero():
    report = run_stage99_1_security_privacy_hardening(ROOT)
    assert report["status"] == "pass"
    assert report["credential_leakage"] == 0
    assert report["raw_manuscript_provider_leakage"] == 0
    assert report["provider_live_call_count_in_release"] == 0
    assert report["node2_raw_reveal_access"] == 0
    assert report["internal_marker_leakage"] == 0
    assert (ROOT / "release/current/stage99_security_pack/credential_audit_report.json").exists()
