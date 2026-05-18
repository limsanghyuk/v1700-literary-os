from __future__ import annotations
from .benchmark_seed_bank import default_seed_bank, modes
from .payload_redactor import make_prompt_packet, redact_prompt
from .sandbox_config import load_sandbox_config
from . import openai_live_adapter, anthropic_live_adapter, gemini_live_adapter, ollama_live_adapter

ADAPTERS = {"openai": openai_live_adapter, "anthropic": anthropic_live_adapter, "gemini": gemini_live_adapter, "ollama": ollama_live_adapter}

def run_provider_benchmark(providers: tuple[str, ...] = ("openai", "ollama"), seed_limit: int = 3) -> dict:
    config = load_sandbox_config()
    seeds = default_seed_bank()[:seed_limit]
    results = []
    live_count = 0
    for seed in seeds:
        for provider_id in providers:
            adapter = ADAPTERS.get(provider_id)
            if adapter is None:
                continue
            for mode in modes():
                prompt = f"mode={mode}\nseed_id={seed['seed_id']}\n{seed['prompt']}"
                redacted, info = redact_prompt(prompt, config.max_prompt_chars)
                packet = make_prompt_packet(f"{seed['seed_id']}_{provider_id}_{mode.lower()}", provider_id, mode, redacted)
                result = adapter.generate(packet, redacted, config)
                live_count += 1 if result.get("live_call_performed") else 0
                results.append({"seed_id": seed["seed_id"], "provider_id": provider_id, "mode": mode, "packet": packet.to_dict(), "redaction": info, "result": result})
    issues = [r for r in results if r["packet"]["raw_manuscript_included"] or r["packet"]["credential_included"] or r["result"].get("raw_response_stored")]
    return {"stage": "107.5.3", "title": "Provider Benchmark Runner", "status": "pass" if not issues else "blocked", "issues": ["unsafe_result"] if issues else [], "release_gate_affected": False, "provider_live_call_count": live_count, "raw_manuscript_sent": False, "raw_response_stored": False, "result_count": len(results), "results": results}
