from v1700.provider_runtime import ProviderCallContext


def test_provider_call_context_defaults_are_safe():
    ctx = ProviderCallContext(narrative_fitness=1.4)
    assert ctx.release_mode is True
    assert ctx.allow_live_provider_calls is False
    assert ctx.raw_manuscript_allowed is False
    assert ctx.clamp_fitness() == 1.0
