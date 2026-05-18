from v1700.creative_arbitration.sandbox_policy import build_release_provider_policy


def test_stage105_release_policy_preserves_provider_zero():
    report = build_release_provider_policy()
    assert report["status"] == "pass"
    assert report["release_mode_provider"] == "fixture/mock only"
    assert report["live_provider_call_count_in_release"] == 0
    assert report["raw_manuscript_provider_leakage"] == 0
