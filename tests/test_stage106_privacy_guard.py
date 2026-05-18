from v1700.author_profile.privacy_guard import run_author_profile_privacy_guard

def test_stage106_privacy_guard_blocks_raw_text_fields():
    report = run_author_profile_privacy_guard({"raw_text":"this should not be here"})
    assert report["status"] == "blocked"

def test_stage106_privacy_guard_passes_feature_payload():
    report = run_author_profile_privacy_guard({"feature_vector": {"rhythm": 0.7}})
    assert report["status"] == "pass"
