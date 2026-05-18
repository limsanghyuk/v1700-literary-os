from __future__ import annotations
import json, os, time, urllib.parse, urllib.request
from .contracts import ProviderSandboxConfig, ProviderPromptPacket
from .live_call_guard import sandbox_live_calls_allowed
from .response_normalizer import normalize_response

PROVIDER_ID = "gemini"

def contract_status(config: ProviderSandboxConfig) -> dict:
    return {"provider_id": PROVIDER_ID, "status": "pass", "live_adapter_present": True, "release_safe_default": True, "raw_manuscript_allowed": False, "endpoint_family": "gemini_generate_content"}

def _extract_text(body: dict) -> str:
    parts = []
    for cand in body.get("candidates", []) if isinstance(body.get("candidates"), list) else []:
        content = cand.get("content", {}) if isinstance(cand, dict) else {}
        for part in content.get("parts", []) if isinstance(content.get("parts"), list) else []:
            if isinstance(part, dict) and part.get("text"):
                parts.append(str(part["text"]))
    return "\n".join(parts) if parts else str(body)[:1000]

def generate(packet: ProviderPromptPacket, prompt: str, config: ProviderSandboxConfig) -> dict:
    allowed, _ = sandbox_live_calls_allowed(config)
    model_id = config.model_aliases.get(PROVIDER_ID) or os.environ.get("GEMINI_MODEL_ID") or "env:GEMINI_MODEL_ID"
    if not allowed:
        text = f"gemini contract-ready dry-run response for {packet.mode}. No live provider call was executed."
        return normalize_response(PROVIDER_ID, model_id, packet.mode, text, live_call_performed=False, status="PASS").to_dict()
    if packet.raw_manuscript_included or packet.credential_included:
        return normalize_response(PROVIDER_ID, model_id, packet.mode, "blocked unsafe payload", live_call_performed=False, status="BLOCK", error="unsafe_payload").to_dict()
    api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        return normalize_response(PROVIDER_ID, model_id, packet.mode, "missing GEMINI_API_KEY", live_call_performed=False, status="ERROR", error="missing_api_key").to_dict()
    base = (os.environ.get("GEMINI_BASE_URL") or "https://generativelanguage.googleapis.com/v1beta").rstrip("/")
    model = urllib.parse.quote(model_id, safe="")
    url = f"{base}/models/{model}:generateContent?key={urllib.parse.quote(api_key)}"
    payload = {"contents": [{"parts": [{"text": prompt[:config.max_prompt_chars]}]}], "generationConfig": {"maxOutputTokens": packet.max_output_tokens}}
    start = time.time()
    try:
        req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=60) as resp:
            body = json.loads(resp.read().decode("utf-8"))
        return normalize_response(PROVIDER_ID, model_id, packet.mode, _extract_text(body), live_call_performed=True, latency_ms=int((time.time()-start)*1000), status="PASS").to_dict()
    except Exception as exc:
        return normalize_response(PROVIDER_ID, model_id, packet.mode, "gemini live call error", live_call_performed=False, latency_ms=int((time.time()-start)*1000), status="ERROR", error=type(exc).__name__).to_dict()
