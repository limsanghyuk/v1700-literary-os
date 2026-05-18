from v1700.creative_arbitration.role_matrix import build_provider_role_matrix


def test_stage105_provider_role_matrix_is_fixture_only():
    report = build_provider_role_matrix()
    assert report["status"] == "pass"
    assert report["provider_count"] >= 6
    assert report["live_provider_call_count_in_release"] == 0
    assert all(role["live_call_allowed_in_release"] is False for role in report["roles"])
