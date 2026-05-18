from __future__ import annotations

from .openai_compatible_adapter import OpenAICompatibleProviderAdapter


def make_ollama_adapter(model: str = "llama3.2", base_url: str = "http://localhost:11434/v1") -> OpenAICompatibleProviderAdapter:
    return OpenAICompatibleProviderAdapter(base_url=base_url, model=model, api_key="local", provider_id="ollama")


class OllamaAdapter(OpenAICompatibleProviderAdapter):
    """Backward-compatible Stage97.2 Ollama adapter.

    The signature is inherited as generate(prompt: str, context: ProviderCallContext) -> str.
    """

    def __init__(self, model: str = "llama3.2", base_url: str = "http://localhost:11434/v1"):
        super().__init__(base_url=base_url, model=model, api_key="local", provider_id="ollama")
