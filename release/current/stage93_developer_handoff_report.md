# Stage93 Developer Handoff

Stage93 adds a live-provider opt-in sandbox, credential redaction audit, and response normalization layer for Ollama, GPT, Claude, and Gemini. Release gates remain provider-zero.

## Local live opt-in

```bash
export V1700_ALLOW_PROVIDER_CALLS=1
export V1700_STAGE93_EXECUTE_LIVE_PROVIDER=1
export OPENAI_API_KEY=...
export ANTHROPIC_API_KEY=...
export GOOGLE_API_KEY=...
python tools/run_stage93_live_provider_sandbox.py
```

The release gate intentionally runs with live execution disabled and validates redaction, normalization, and zero default calls.
