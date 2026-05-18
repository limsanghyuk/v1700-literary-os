import inspect

from v1700.provider_runtime.context import ProviderCallContext
from v1700.provider_runtime.ollama_adapter import OllamaAdapter, make_ollama_adapter


def test_ollama_adapter_signature_uses_provider_context_not_kwargs():
    adapter = make_ollama_adapter()
    assert isinstance(adapter, OllamaAdapter.__mro__[1]) or adapter.get_provider_id() == "ollama"
    sig = inspect.signature(OllamaAdapter().generate)
    assert list(sig.parameters)[:2] == ["prompt", "context"]
    assert not any(p.kind == inspect.Parameter.VAR_KEYWORD for p in sig.parameters.values())
    assert sig.parameters["context"].annotation in {ProviderCallContext, "ProviderCallContext"}
