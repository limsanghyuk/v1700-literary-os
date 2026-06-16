# Corpus Formula Signal Bridge Blueprint

## Purpose

Map metadata-only corpus absorption outputs into V1700 advisory formula signals and tensor summaries.

## Inputs

- `release/current/corpus_ko_absorption_pack/canonical_work_registry.json`
- `release/current/corpus_ko_absorption_pack/rag_index_registry.json`
- `release/current/corpus_ko_absorption_pack/learning_signal_registry.json`
- `docs/contracts/formula_signal_record_contract.md`

## Outputs

- `release/current/corpus_formula_bridge_pack/formula_signal_registry.json`
- `release/current/corpus_formula_bridge_pack/narrative_state_tensor_registry.json`
- `release/current/corpus_formula_bridge_pack/bridge_summary.json`

## Bridge Rules

- metadata-only inputs only
- formula outputs remain advisory
- writer authority remains upstream
- no raw scene text emitted
- no raw vectors emitted

## Initial Signal Families

- Narrative State Tensor
- Emotional Momentum
- Retrieval Grounding / RAG readiness

## Next Intended Consumers

- Writer IDE advisory panels
- LearnableCritic audit wiring
- Value Proof Arm B preregistration
- future Formula Signal Store
