# Stage107.5 Developer Handoff

- Provider live sandbox adapters are implemented outside release gates.
- Default execution is dry-run contract verification with zero live provider calls.
- Ollama may perform opt-in live calls only when V1700_PROVIDER_SANDBOX=1 and V1700_ALLOW_PROVIDER_CALLS=1.
- Raw manuscript payloads, credentials, and raw provider responses are blocked from release evidence.
