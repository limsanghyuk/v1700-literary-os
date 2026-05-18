# Stage94: Live Provider Evaluation Harness

Stage94 adds a provider comparison layer for Ollama, GPT, Claude, and Gemini.

The stage does not make live provider calls during release verification. It sends the same dry-run prompt suite through all four configured adapters, normalizes the responses using the Stage93 response contract, and scores each provider on deterministic release-safe axes.

## Runtime Additions

| Concept | Live symbol | Purpose |
| --- | --- | --- |
| Prompt suite | `v1700.provider_evaluation.prompt_suite.build_stage94_prompt_suite` | Keeps provider comparison prompt-equivalent. |
| Evaluation harness | `v1700.provider_evaluation.harness.ProviderEvaluationHarness` | Routes dry-run requests across all providers. |
| Response scoring | `v1700.provider_evaluation.scoring.score_normalized_response` | Scores latency, cost, tokens, safety, literary quality, and branchpoint compliance. |
| Provider profiles | `v1700.provider_evaluation.scoring.build_provider_profiles` | Reports provider strengths and weaknesses. |
| Release gate | `v1700.gates.stage94_release_gate.run_stage94_release_gate` | Blocks promotion if provider-zero or schema safety regresses. |

## Guarantees

- Provider default calls remain `0`.
- Release gate live provider calls remain `0`.
- Node2 raw reveal access remains `0`.
- Credential values are not written to reports.
- Stage93 sandbox and normalization are inherited.
- GitNexus remains optional developer evidence.

## Commands

```bash
python tools/run_stage94_provider_evaluation.py
python tools/run_stage94_release_gate.py
python tools/run_release_gate.py
python -m pytest -q tests/test_stage94_provider_evaluation.py
```
