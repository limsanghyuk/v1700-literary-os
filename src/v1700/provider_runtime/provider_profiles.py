from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ProviderProfile:
    provider_id: str
    tier: str
    provider_kind: str
    model: str
    base_url: str = ""
    estimated_input_cost_per_1k: float | None = None
    estimated_output_cost_per_1k: float | None = None


DEFAULT_PROVIDER_PROFILES: dict[str, ProviderProfile] = {
    "fixture": ProviderProfile("fixture", "fixture", "fixture", "fixture-provider"),
    "mock": ProviderProfile("mock", "fixture", "mock", "mock-provider"),
    "ollama": ProviderProfile("ollama", "local", "openai-compatible", "llama3.2", "http://localhost:11434/v1", 0.0, 0.0),
    "lmstudio": ProviderProfile("lmstudio", "local", "openai-compatible", "local-model", "http://localhost:1234/v1", 0.0, 0.0),
    "vllm": ProviderProfile("vllm", "local", "openai-compatible", "local-model", "http://localhost:8000/v1", 0.0, 0.0),
    "gpt": ProviderProfile("gpt", "quality", "gpt", "gpt-compatible"),
    "claude": ProviderProfile("claude", "quality", "claude", "claude-compatible"),
    "gemini": ProviderProfile("gemini", "speed", "gemini", "gemini-compatible"),
}
