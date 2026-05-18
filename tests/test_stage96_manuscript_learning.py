from pathlib import Path

from v1700.manuscript_learning.learning_report import run_manuscript_learning


def test_stage96_manuscript_learning_feature_only_privacy():
    report = run_manuscript_learning(Path(__file__).resolve().parents[1])
    assert report["status"] == "pass"
    assert report["scene_feature_count"] >= 40
    assert report["privacy_report"]["status"] == "pass"
    assert report["privacy_report"]["raw_manuscript_sent_to_provider"] is False
    assert report["coefficient_memory"]["source_policy"] == "local_feature_only"
    assert report["live_provider_call_count"] == 0
