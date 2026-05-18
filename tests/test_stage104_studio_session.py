from v1700.studio_beta.studio_session import open_studio_session

def test_studio_session_is_provider_zero():
    session = open_studio_session()
    assert session["provider_call_count"] == 0
    assert session["live_provider_call_count_in_release_gate"] == 0
