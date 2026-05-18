from v1700.longform_production.release_policy import build_longform_production_release_policy

def test_stage107_release_policy_provider_zero_and_local_only():
    report = build_longform_production_release_policy()
    assert report['status'] == 'pass'
    assert report['live_provider_call_count_in_release_gate'] == 0
    assert report['raw_manuscript_provider_leakage'] == 0
    assert report['full_text_export_default'] is False
