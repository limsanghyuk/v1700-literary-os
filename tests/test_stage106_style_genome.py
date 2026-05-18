from v1700.author_profile.style_genome import build_style_genome

def test_stage106_style_genome_is_feature_only():
    report = build_style_genome()
    assert report["status"] == "pass"
    assert report["feature_only"] is True
    assert report["raw_manuscript_retained"] is False
    assert report["provider_export_allowed"] is False
