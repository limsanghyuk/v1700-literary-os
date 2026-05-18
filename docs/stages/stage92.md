# Stage92 — Local Multi-Provider Adapter Runtime

Stage92 configures a personal developer workstation for four provider families: Ollama, GPT, Claude, and Gemini.

The adapter layer is intentionally provider-zero during release gates. It registers provider configs, request payload builders, route order, and Writer Studio visibility, but does not perform live network calls unless a developer explicitly opts in outside release verification.

## Providers

- `local_ollama` — local Ollama adapter, no API key required.
- `gpt_openai` — GPT adapter, reads `OPENAI_API_KEY` only after explicit live-call opt-in.
- `claude_anthropic` — Claude adapter, reads `ANTHROPIC_API_KEY` only after explicit live-call opt-in.
- `gemini_google` — Gemini adapter, reads `GOOGLE_API_KEY` only after explicit live-call opt-in.

## Invariants

- provider default calls: `0`
- live call count in release gate: `0`
- Node2 raw reveal access: `0`
- GraphNexus and GitNexus traceability preserved
- Stage91 Studio persistence, review queue, and UI event replay preserved

## Gates

- `python tools/run_stage92_multi_adapter_smoke.py`
- `python tools/run_stage92_release_gate.py`
- `python tools/run_release_gate.py`
