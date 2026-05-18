from v1700.studio_beta.local_telemetry import build_local_telemetry_report

def test_local_telemetry_does_not_include_raw_text_or_credentials():
    report = build_local_telemetry_report()
    assert report["status"] == "pass"
    assert report["raw_manuscript_included"] is False
    assert report["credential_included"] is False
    assert report["provider_payload_included"] is False
