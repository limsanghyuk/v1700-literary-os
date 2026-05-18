from __future__ import annotations
import os
from .contracts import ProviderSandboxConfig

def _truthy(value: str | None) -> bool:
    return str(value or '').strip().lower() in {'1','true','yes','on'}

def _int_env(name: str, default: int) -> int:
    try: return int(os.environ.get(name, default))
    except Exception: return default

def load_sandbox_config() -> ProviderSandboxConfig:
    aliases = {
        'openai': os.environ.get('OPENAI_MODEL_ID') or os.environ.get('V1700_GPT_MODEL') or 'env:OPENAI_MODEL_ID',
        'anthropic': os.environ.get('ANTHROPIC_MODEL_ID') or os.environ.get('V1700_CLAUDE_MODEL') or 'env:ANTHROPIC_MODEL_ID',
        'gemini': os.environ.get('GEMINI_MODEL_ID') or os.environ.get('V1700_GEMINI_MODEL') or 'env:GEMINI_MODEL_ID',
        'ollama': os.environ.get('OLLAMA_MODEL_ID') or os.environ.get('V1700_OLLAMA_MODEL') or 'qwen3:14b',
    }
    providers = tuple(p.strip() for p in os.environ.get('V1700_PROVIDER_IDS','openai,anthropic,gemini,ollama').split(',') if p.strip())
    return ProviderSandboxConfig(
        sandbox_enabled=_truthy(os.environ.get('V1700_PROVIDER_SANDBOX')),
        allow_live_provider_calls=_truthy(os.environ.get('V1700_ALLOW_PROVIDER_CALLS')),
        release_gate_affected=_truthy(os.environ.get('V1700_RELEASE_GATE_AFFECTED')),
        raw_manuscript_allowed=_truthy(os.environ.get('V1700_RAW_MANUSCRIPT_ALLOWED')),
        provider_ids=providers,
        model_aliases=aliases,
        max_live_calls=_int_env('V1700_PROVIDER_MAX_LIVE_CALLS', 12),
        max_prompt_chars=_int_env('V1700_PROVIDER_MAX_PROMPT_CHARS', 6000),
        store_raw_response=_truthy(os.environ.get('V1700_PROVIDER_STORE_RAW_RESPONSE')),
    )
