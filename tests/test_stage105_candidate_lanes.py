from v1700.creative_arbitration.candidate_lanes import build_candidate_lanes


def test_stage105_candidate_lanes_are_feature_only():
    report = build_candidate_lanes()
    assert report["status"] == "pass"
    assert report["candidate_count"] >= 5
    assert report["raw_manuscript_provider_leakage"] == 0
    assert all(candidate["contains_raw_manuscript"] is False for candidate in report["candidates"])
    assert all(candidate["live_call_count"] == 0 for candidate in report["candidates"])
