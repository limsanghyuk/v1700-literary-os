from v1700.author_profile.node2_profile_bridge import build_node2_author_profile_bridge

def test_stage106_node2_bridge_has_no_raw_reveal_access():
    report = build_node2_author_profile_bridge()
    assert report["status"] == "pass"
    assert report["raw_reveal_access"] == 0
    assert report["provider_call_count"] == 0
    assert "raw_reveal" in report["forbidden_controls"]
