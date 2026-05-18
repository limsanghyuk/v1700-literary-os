from pathlib import Path

from v1700.longform_adversarial.manuscript_ingest_adapter import run_local_manuscript_ingest_privacy_probe

ROOT = Path(__file__).resolve().parents[1]


def test_local_manuscript_ingest_does_not_export_raw_text():
    report = run_local_manuscript_ingest_privacy_probe(ROOT)
    assert report["status"] == "pass"
    assert report["raw_manuscript_sent_to_provider"] is False
    assert report["raw_manuscript_stored_in_report"] is False
    assert report["raw_manuscript_provider_leakage"] == 0
    assert all(feature["contains_raw_text"] is False for feature in report["features"])
