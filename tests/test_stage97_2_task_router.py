from v1700.provider_runtime import FixtureProvider, ProviderCallContext, ProviderHealthMonitor, ProviderTaskRouter


def test_task_router_release_mode_uses_fixture_and_calls_no_generate():
    fixture = FixtureProvider()
    providers = {"fixture": fixture}
    router = ProviderTaskRouter(providers, ProviderHealthMonitor(providers, {"fixture": True}))
    selected = router.route(ProviderCallContext(release_mode=True, provider_hint="quality", narrative_fitness=0.99))
    assert selected.get_provider_id() == "fixture"
    assert fixture.generate_call_count == 0


def test_task_router_fallbacks_to_fixture_when_local_unhealthy():
    fixture = FixtureProvider()
    local = FixtureProvider(provider_id="ollama")
    providers = {"fixture": fixture, "ollama": local}
    router = ProviderTaskRouter(providers, ProviderHealthMonitor(providers, {"fixture": True, "ollama": False}))
    selected = router.route(ProviderCallContext(release_mode=False, narrative_fitness=0.1))
    assert selected.get_provider_id() == "fixture"
