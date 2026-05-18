from v1700.author_profile.drift_guard import run_style_drift_guard

def test_stage106_drift_guard_allows_bounded_delta():
    report = run_style_drift_guard(candidate_delta=0.1, allowed_delta=0.2)
    assert report["status"] == "pass"
    assert report["action"] == "ALLOW"

def test_stage106_drift_guard_blocks_excess_delta():
    report = run_style_drift_guard(candidate_delta=0.4, allowed_delta=0.2)
    assert report["status"] == "blocked"
    assert report["action"] == "BLOCK"
