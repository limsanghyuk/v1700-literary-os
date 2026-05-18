from v1700.plugin_marketplace.plugin_catalog import builtin_plugin_manifests
from v1700.plugin_marketplace.sandbox_policy import sandbox_policy_matrix


def test_stage109_plugin_sandbox_policy_blocks_risky_defaults():
    result = sandbox_policy_matrix(builtin_plugin_manifests())
    assert result["status"] == "pass"
    assert result["blockers"] == []
    for row in result["rows"]:
        assert row["network_default"] == "blocked"
        assert row["raw_manuscript_access"] is False
        assert row["credential_access"] is False
        assert row["live_provider_default"] is False
