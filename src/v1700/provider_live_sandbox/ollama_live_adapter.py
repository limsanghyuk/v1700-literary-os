from __future__ import annotations
import json, os, time, urllib.request, urllib.error
from .contracts import ProviderSandboxConfig, ProviderPromptPacket
from .live_call_guard import sandbox_live_calls_allowed
from .response_normalizer import normalize_response

PROVIDER_ID = 'ollama'

def contract_status(config: ProviderSandboxConfig) -> dict:
    return {'provider_id': PROVIDER_ID, 'status': 'pass', 'live_adapter_present': True, 'release_safe_default': True, 'raw_manuscript_allowed': False, 'openai_compatible_local': True}

def generate(packet: ProviderPromptPacket, prompt: str, config: ProviderSandboxConfig) -> dict:
    allowed, issues = sandbox_live_calls_allowed(config)
    model_id = config.model_aliases.get('ollama') or os.environ.get('OLLAMA_MODEL_ID') or 'qwen3:14b'
    if not allowed:
        text = f'ollama contract-ready dry-run response for {packet.mode}. No live provider call was executed.'
        return normalize_response(PROVIDER_ID, model_id, packet.mode, text, live_call_performed=False, status='PASS').to_dict()
    if packet.raw_manuscript_included or packet.credential_included:
        return normalize_response(PROVIDER_ID, model_id, packet.mode, 'blocked unsafe payload', live_call_performed=False, status='BLOCK', error='unsafe_payload').to_dict()
    base = os.environ.get('OLLAMA_BASE_URL') or os.environ.get('V1700_OLLAMA_BASE_URL') or 'http://127.0.0.1:11434'
    url = base.rstrip('/') + '/api/generate'
    payload = {'model': model_id, 'prompt': prompt[:config.max_prompt_chars], 'stream': False}
    start = time.time()
    try:
        req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers={'Content-Type':'application/json'})
        with urllib.request.urlopen(req, timeout=30) as resp:
            body = json.loads(resp.read().decode('utf-8'))
        text = body.get('response') or str(body)[:500]
        return normalize_response(PROVIDER_ID, model_id, packet.mode, text, live_call_performed=True, latency_ms=int((time.time()-start)*1000), status='PASS').to_dict()
    except Exception as exc:
        # Sandbox errors do not affect release gate. They are reportable benchmark evidence.
        return normalize_response(PROVIDER_ID, model_id, packet.mode, 'ollama live call error', live_call_performed=False, latency_ms=int((time.time()-start)*1000), status='ERROR', error=type(exc).__name__).to_dict()
