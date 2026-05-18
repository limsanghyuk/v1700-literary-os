from __future__ import annotations
import json, os, time, urllib.request
from .contracts import ProviderSandboxConfig, ProviderPromptPacket
from .live_call_guard import sandbox_live_calls_allowed
from .response_normalizer import normalize_response

PROVIDER_ID = "openai"

def contract_status(config: ProviderSandboxConfig) -> dict:
    return {"provider_id": PROVIDER_ID, "status": "pass", "live_adapter_present": True, "release_safe_default": True, "raw_manuscript_allowed": False, "endpoint_family": "openai_responses_or_compatible"}

def _extract_text(body: dict) -> str:
    if isinstance(body.get("output_text"), str):
        return body["output_text"]
    chunks: list[str] = []
    for item in body.get("output", []) if isinstance(body.get("output"), list) else []:
        for content in item.get("content", []) if isinstance(item, dict) else []:
            if isinstance(content, dict) and content.get("type") in {"output_text", "text"}:
                chunks.append(str(content.get("text", "")))
    if chunks:
        return "\n".join(chunks)
    choices = body.get("choices") if isinstance(body.get("choices"), list) else []
    if choices:
        msg = choices[0].get("message", {})
        if isinstance(msg, dict) and msg.get("content"):
            return str(msg["content"])
    return str(body)[:1000]

def generate(packet: ProviderPromptPacket, prompt: str, config: ProviderSandboxConfig) -> dict:
    allowed, _ = sandbox_live_calls_allowed(config)
    model_id = config.model_aliases.get(PROVIDER_ID) or os.environ.get("OPENAI_MODEL_ID") or "env:OPENAI_MODEL_ID"
    if not allowed:
        text = f"openai contract-ready dry-run response for {packet.mode}. No live provider call was executed."
        return normalize_response(PROVIDER_ID, model_id, packet.mode, text, live_call_performed=False, status="PASS").to_dict()
    if packet.raw_manuscript_included or packet.credential_included:
        return normalize_response(PROVIDER_ID, model_id, packet.mode, "blocked unsafe payload", live_call_performed=False, status="BLOCK", error="unsafe_payload").to_dict()
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        return normalize_response(PROVIDER_ID, model_id, packet.mode, "missing OPENAI_API_KEY", live_call_performed=False, status="ERROR", error="missing_api_key").to_dict()
    base = (os.environ.get("OPENAI_BASE_URL") or "https://api.openai.com/v1").rstrip("/")
    payload = {"model": model_id, "input": prompt[:config.max_prompt_chars], "max_output_tokens": packet.max_output_tokens}
    start = time.time()
    try:
        req = urllib.request.Request(base + "/responses", data=json.dumps(payload).encode("utf-8"), headers={"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"})
        with urllib.request.urlopen(req, timeout=60) as resp:
            body = json.loads(resp.read().decode("utf-8"))
        return normalize_response(PROVIDER_ID, model_id, packet.mode, _extract_text(body), live_call_performed=True, latency_ms=int((time.time()-start)*1000), status="PASS").to_dict()
    except Exception as exc:
        return normalize_response(PROVIDER_ID, model_id, packet.mode, "openai live call error", live_call_performed=False, latency_ms=int((time.time()-start)*1000), status="ERROR", error=type(exc).__name__).to_dict()
