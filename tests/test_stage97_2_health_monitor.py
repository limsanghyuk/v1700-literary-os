from v1700.provider_runtime import FixtureProvider, ProviderHealthMonitor


def test_provider_health_monitor_fixture_table_and_failures():
    provider = FixtureProvider("fixture")
    monitor = ProviderHealthMonitor({"fixture": provider}, {"fixture": True})
    assert monitor.is_healthy("fixture") is True
    monitor.mark_failed("fixture", "boom")
    assert monitor.is_healthy("fixture") is False
