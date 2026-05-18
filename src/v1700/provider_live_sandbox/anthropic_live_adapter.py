from __future__ import annotations
import json, os, time, urllib.request
from .contracts import ProviderSandboxConfig, ProviderPromptPacket
from .live_call_guard import sandbox_live_calls_allowed
from .response_normalizer import normalize_response

PROVIDER_ID = "anthropic"

def contract_status(config: ProviderSandboxConfig) -> dict:
    return {"provider_id": PROVIDER_ID, "status": "pass", "live_adapter_present": True, "release_safe_default": True, "raw_manuscript_allowed": False, "endpoint_family": "anthropic_messages"}

def _extract_text(body: dict) -> str:
    parts = []
    for item in body.get("content", []) if isinstance(body.get("content"), list) else []:
        if isinstance(item, dict) and item.get("type") == "text":
            parts.append(str(item.get("text", "")))
    return "\n".join(parts) if parts else str(body)[:1000]

def generate(packet: ProviderPromptPacket, prompt: str, config: ProviderSandboxConfig) -> dict:
    allowed, _ = sandbox_live_calls_allowed(config)
    model_id = config.model_aliases.get(PROVIDER_ID) or os.environ.get("ANTHROPIC_MODEL_ID") or "env:ANTHROPIC_MODEL_ID"
    if not allowed:
        text = f"anthropic contract-ready dry-run response for {packet.mode}. No live provider call was executed."
        return normalize_response(PROVIDER_ID, model_id, packet.mode, text, live_call_performed=False, status="PASS").to_dict()
    if packet.raw_manuscript_included or packet.credential_included:
        return normalize_response(PROVIDER_ID, model_id, packet.mode, "blocked unsafe payload", live_call_performed=False, status="BLOCK", error="unsafe_payload").to_dict()
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        return normalize_response(PROVIDER_ID, model_id, packet.mode, "missing ANTHROPIC_API_KEY", live_call_performed=False, status="ERROR", error="missing_api_key").to_dict()
    base = (os.environ.get("ANTHROPIC_BASE_URL") or "https://api.anthropic.com").rstrip("/")
    payload = {"model": model_id, "max_tokens": packet.max_output_tokens, "messages": [{"role":"user", "content": prompt[:config.max_prompt_chars]}]}
    start = time.time()
    try:
        req = urllib.request.Request(base + "/v1/messages", data=json.dumps(payload).encode("utf-8"), headers={"Content-Type": "application/json", "x-api-key": api_key, "anthropic-version": os.environ.get("ANTHROPIC_VERSION", "2023-06-01")})
        with urllib.request.urlopen(req, timeout=60) as resp:
            body = json.loads(resp.read().decode("utf-8"))
        return normalize_response(PROVIDER_ID, model_id, packet.mode, _extract_text(body), live_call_performed=True, latency_ms=int((time.time()-start)*1000), status="PASS").to_dict()
    except Exception as exc:
        return normalize_response(PROVIDER_ID, model_id, packet.mode, "anthropic live call error", live_call_performed=False, latency_ms=int((time.time()-start)*1000), status="ERROR", error=type(exc).__name__).to_dict()
