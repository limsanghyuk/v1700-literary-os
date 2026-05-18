from __future__ import annotations

import os
from collections.abc import Iterable

from v1700.provider_adapters.contracts import ProviderAdapterConfig


def build_default_multi_provider_configs(*, allow_live_call: bool | None = None) -> tuple[ProviderAdapterConfig, ...]:
    """Return the canonical four-provider developer workstation config.

    Live calls are opt-in only. By default this reads V1700_ALLOW_PROVIDER_CALLS;
    any value other than "1" keeps all adapters dry-run only.
    """

    allow = os.getenv("V1700_ALLOW_PROVIDER_CALLS", "0") == "1" if allow_live_call is None else allow_live_call
    return (
        ProviderAdapterConfig(
            provider_id="local_ollama",
            provider_kind="ollama",
            model=os.getenv("V1700_OLLAMA_MODEL", "llama3.1"),
            endpoint=os.getenv("V1700_OLLAMA_ENDPOINT", "http://127.0.0.1:11434/api/chat"),
            api_key_env=None,
            allow_live_call=allow,
            priority=10,
            notes="Local workstation adapter. No secret required; live calls require explicit V1700_ALLOW_PROVIDER_CALLS=1.",
        ),
        ProviderAdapterConfig(
            provider_id="gpt_openai",
            provider_kind="gpt",
            model=os.getenv("V1700_GPT_MODEL", "gpt-4.1-mini"),
            endpoint=os.getenv("V1700_GPT_ENDPOINT", "https://api.openai.com/v1/responses"),
            api_key_env="OPENAI_API_KEY",
            allow_live_call=allow,
            priority=20,
            notes="OpenAI GPT adapter. API key is read from OPENAI_API_KEY only when live calls are explicitly enabled.",
        ),
        ProviderAdapterConfig(
            provider_id="claude_anthropic",
            provider_kind="claude",
            model=os.getenv("V1700_CLAUDE_MODEL", "claude-3-5-sonnet-latest"),
            endpoint=os.getenv("V1700_CLAUDE_ENDPOINT", "https://api.anthropic.com/v1/messages"),
            api_key_env="ANTHROPIC_API_KEY",
            allow_live_call=allow,
            priority=30,
            notes="Anthropic Claude adapter. API key is read from ANTHROPIC_API_KEY only when live calls are explicitly enabled.",
        ),
        ProviderAdapterConfig(
            provider_id="gemini_google",
            provider_kind="gemini",
            model=os.getenv("V1700_GEMINI_MODEL", "gemini-1.5-flash"),
            endpoint=os.getenv("V1700_GEMINI_ENDPOINT", "https://generativelanguage.googleapis.com/v1beta"),
            api_key_env="GOOGLE_API_KEY",
            allow_live_call=allow,
            priority=40,
            notes="Google Gemini adapter. API key is read from GOOGLE_API_KEY only when live calls are explicitly enabled.",
        ),
    )


def sorted_enabled_configs(configs: Iterable[ProviderAdapterConfig]) -> tuple[ProviderAdapterConfig, ...]:
    return tuple(sorted((config for config in configs if config.enabled), key=lambda item: (item.priority, item.provider_id)))
