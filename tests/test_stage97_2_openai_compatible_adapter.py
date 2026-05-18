from v1700.provider_runtime.context import ProviderCallContext
from v1700.provider_runtime.openai_compatible_adapter import OpenAICompatibleProviderAdapter


def test_openai_compatible_adapter_blocks_live_call_in_release_mode():
    adapter = OpenAICompatibleProviderAdapter.for_ollama()
    assert adapter.get_provider_id() == "ollama"
    try:
        adapter.generate("hello", ProviderCallContext(release_mode=True))
    except RuntimeError as exc:
        assert "live_provider_call_blocked" in str(exc)
    else:
        raise AssertionError("release-mode live provider call was not blocked")
