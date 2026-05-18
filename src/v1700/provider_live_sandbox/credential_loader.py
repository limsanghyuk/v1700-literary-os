from __future__ import annotations
import os

def credential_status(provider_id: str) -> dict:
    env_map = {
        'openai': 'OPENAI_API_KEY',
        'anthropic': 'ANTHROPIC_API_KEY',
        'gemini': 'GEMINI_API_KEY',
        'ollama': 'OLLAMA_BASE_URL',
    }
    name = env_map.get(provider_id, '')
    present = bool(os.environ.get(name)) if name else False
    # Do not return the credential value. The report only records presence.
    return {'provider_id': provider_id, 'credential_env': name, 'present': present, 'value_recorded': False}

def all_credential_status(provider_ids: tuple[str, ...]) -> list[dict]:
    return [credential_status(p) for p in provider_ids]
