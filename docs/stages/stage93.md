# Stage93 - Live Provider Opt-in Sandbox / Credential Audit / Response Normalization

Stage93 hardens the Stage92 multi-provider adapter runtime before any real local live-provider usage.

## Purpose

- Keep Ollama / GPT / Claude / Gemini configured.
- Add a local live-provider opt-in sandbox boundary.
- Audit credentials with redaction only; never serialize raw API keys.
- Normalize provider responses into one canonical V1700 response contract.
- Preserve provider default calls = 0 during all release gates.

## Developer opt-in

```bash
export V1700_ALLOW_PROVIDER_CALLS=1
export V1700_STAGE93_EXECUTE_LIVE_PROVIDER=1
export OPENAI_API_KEY=...
export ANTHROPIC_API_KEY=...
export GOOGLE_API_KEY=...
python tools/run_stage93_live_provider_sandbox.py
```

Release gates intentionally run with live execution disabled.
