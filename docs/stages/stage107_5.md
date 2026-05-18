# Stage107.5 — Provider Live Sandbox Adapter Verification

Stage107.5 verifies GPT / Claude / Gemini / Ollama adapter contracts in an opt-in sandbox outside the deterministic release path.

## Invariants

- Release gate live provider calls remain 0.
- Sandbox live calls require explicit opt-in.
- Raw manuscript payloads are blocked.
- Credentials and raw provider responses are not written to release evidence or ZIP packages.
- Model IDs are probe targets, not hardcoded release constants.
- Python fallback remains required because GitNexus is an optional sidecar.
