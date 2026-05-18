from __future__ import annotations

import json
import urllib.error
import urllib.request

from .context import ProviderCallContext
from .interface import ProviderBridgeInterface


class OpenAICompatibleProviderAdapter(ProviderBridgeInterface):
    """OpenAI-compatible adapter for Ollama, LM Studio, vLLM, and compatible APIs.

    The adapter itself can perform a live HTTP call only when the supplied
    ProviderCallContext explicitly opts out of release mode and allows live
    calls. This preserves provider-zero release gates.
    """

    PRESET_URLS = {
        "ollama": "http://localhost:11434/v1",
        "lmstudio": "http://localhost:1234/v1",
        "vllm": "http://localhost:8000/v1",
        "openai": "https://api.openai.com/v1",
    }

    def __init__(self, base_url: str, model: str, api_key: str = "local", provider_id: str = ""):
        self._base_url = base_url.rstrip("/")
        self._model = model
        self._api_key = api_key
        self._provider_id = provider_id or self._infer_provider_id(base_url)

    def generate(self, prompt: str, context: ProviderCallContext) -> str:
        if context.release_mode or not context.allow_live_provider_calls:
            raise RuntimeError("live_provider_call_blocked_by_release_policy")
        payload = {
            "model": self._model,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": context.max_tokens,
            "temperature": context.temperature,
        }
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            f"{self._base_url}/chat/completions",
            data=data,
            method="POST",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self._api_key}",
            },
        )
        with urllib.request.urlopen(req, timeout=context.timeout_seconds) as resp:  # nosec - explicit opt-in only
            body = json.loads(resp.read().decode("utf-8"))
        return body["choices"][0]["message"]["content"]

    def is_available(self) -> bool:
        try:
            req = urllib.request.Request(f"{self._base_url}/models", method="GET")
            with urllib.request.urlopen(req, timeout=5) as resp:  # nosec - availability probe only
                return 200 <= int(resp.status) < 300
        except (urllib.error.URLError, TimeoutError, OSError, ValueError):
            return False

    def get_provider_id(self) -> str:
        return self._provider_id

    @classmethod
    def for_ollama(cls, model: str = "llama3.2") -> "OpenAICompatibleProviderAdapter":
        return cls(cls.PRESET_URLS["ollama"], model=model, api_key="local", provider_id="ollama")

    @classmethod
    def for_lmstudio(cls, model: str = "local-model") -> "OpenAICompatibleProviderAdapter":
        return cls(cls.PRESET_URLS["lmstudio"], model=model, api_key="local", provider_id="lmstudio")

    @classmethod
    def for_vllm(cls, model: str = "local-model") -> "OpenAICompatibleProviderAdapter":
        return cls(cls.PRESET_URLS["vllm"], model=model, api_key="local", provider_id="vllm")

    @classmethod
    def for_openai(cls, model: str, api_key: str) -> "OpenAICompatibleProviderAdapter":
        return cls(cls.PRESET_URLS["openai"], model=model, api_key=api_key, provider_id="openai")

    @staticmethod
    def _infer_provider_id(base_url: str) -> str:
        lowered = base_url.lower()
        if "11434" in lowered:
            return "ollama"
        if "1234" in lowered:
            return "lmstudio"
        if "8000" in lowered:
            return "vllm"
        if "openai" in lowered:
            return "openai"
        return "openai-compatible"
