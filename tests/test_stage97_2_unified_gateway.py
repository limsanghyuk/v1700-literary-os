from v1700.provider_runtime import FixtureProvider, ProviderCallContext, ProviderCostLedger, ProviderHealthMonitor, ProviderTaskRouter, UnifiedProviderGateway


def test_unified_gateway_records_fixture_call_without_live_provider():
    fixture = FixtureProvider()
    providers = {"fixture": fixture}
    monitor = ProviderHealthMonitor(providers, {"fixture": True})
    router = ProviderTaskRouter(providers, monitor)
    ledger = ProviderCostLedger("S", 1)
    gateway = UnifiedProviderGateway(router, monitor, ledger)
    response = gateway.call("prompt", ProviderCallContext(release_mode=True))
    assert response.provider_id == "fixture"
    assert gateway.live_provider_call_count == 0
    assert ledger.records["fixture"].call_count == 1
