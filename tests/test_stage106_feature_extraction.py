from v1700.author_profile.feature_extractor import extract_feature_only_style_features

def test_stage106_feature_vectors_are_feature_only():
    report = extract_feature_only_style_features()
    assert report["status"] == "pass"
    assert report["feature_vector_count"] >= 3
    assert report["raw_text_retained"] is False
    assert report["raw_manuscript_provider_leakage"] == 0
