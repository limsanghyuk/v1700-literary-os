# Stage92 Developer Handoff Report

Stage92 adds a local multi-provider adapter runtime for a personal developer workstation.

## Providers

- Ollama: `local_ollama`
- GPT/OpenAI: `gpt_openai` using `OPENAI_API_KEY` only when live calls are explicitly enabled
- Claude/Anthropic: `claude_anthropic` using `ANTHROPIC_API_KEY` only when live calls are explicitly enabled
- Gemini/Google: `gemini_google` using `GOOGLE_API_KEY` only when live calls are explicitly enabled

## Safety rule

Release gates never perform live provider calls. Runtime remains provider-default-calls 0 until a developer intentionally enables live calls outside release verification.

- Configured providers: `4`
- Route order: `local_ollama, gpt_openai, claude_anthropic, gemini_google`
- Live call count during gate: `0`
- Provider default calls: `0`
- Node2 raw reveal access: `0`
