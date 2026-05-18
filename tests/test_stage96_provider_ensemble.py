from v1700.provider_ensemble.arbiter import run_provider_ensemble_arbitration


def test_stage96_provider_ensemble_selects_rejects_and_merges_without_live_calls():
    report = run_provider_ensemble_arbitration()
    decisions = [item["decision"] for item in report["decisions"]]
    assert report["status"] == "pass"
    assert report["provider_count"] == 4
    assert "SELECT" in decisions
    assert "REJECT" in decisions
    assert "MERGE" in decisions
    assert report["live_provider_call_count"] == 0
    assert report["provider_default_calls"] == 0
    assert report["node2_raw_reveal_access_count"] == 0
