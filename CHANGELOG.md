# Changelog

## v1.53.0-stage153

- Added Stage153 Memory Health & Leakage Boundary.
- Implemented local memory health and record verification rules (inspecting duplicate keys, null values, malformed JSONL, invalid continuity, private reveal leakage, planner private notes, write handles, canon mutations, learning payloads, and credential tokens).
- Implemented Node2 leakage boundaries enforcing surface-safe access rules for hidden reveals and planner private notes.
- Added query boundary probes (hidden reveal probe, planner private probe, reader surface probe).
- Kept external RAG, vector DB runtime dependency, canon mutation, memory write, auto-repair, and training disabled (Provider-Zero).
- Added Stage153 proposal, blueprint, manifests, release evidence, tests, repo doctor wiring, and main release gate integration.

## v1.52.0-stage152

- Added Stage152 Deterministic Local Query / Ranking over the read-only JSONL memory store.
- Implemented core memory query interface APIs (`find_project_memory`, `find_characters`, `find_episodes`, `find_scenes`, `find_events`, `find_reveals`, `find_payoffs`, `query_by_intent`, `rank_memory_candidates`, `project_for_node2`).
- Added local deterministic ranking algorithms: lexical term overlap, field priority, temporal metadata, simple rank fusion, boundary-safe penalty.
- Kept live provider RAG, vector DB runtime dependencies, memory write, canon mutation, runtime training, and auto-repair apply disabled.
- Added Stage152 proposal, blueprint, manifests, release evidence, tests, repo doctor wiring, and main release gate integration.

## v1.51.0-stage151

- Added Stage151 Local Read-Only Memory Store.
- Implemented the read-only memory store loader and JSONL schema validation mechanism.
- Added Stage151 manifests, live core overlay, lineage traces, release evidence, and local store tests.

## v1.50.0-stage150

- Added Stage150 Memory Contract representing the core memory structure definitions and dataclasses.
- Defined memory records, project boundary policy, memory write policies, and Node2 projection policies.

## v1.33.0-stage133

- Added Stage133 NarrativeStateTensor 8D Measurement Layer.
- Added deterministic local-only tensor measurement for causality, time, reveal budget, agency, emotion, voice, attention, and canon isolation.
- Routed true contradictions to measured review state instead of auto-repair.
- Preserved Stage132 mystery exemption semantics when reveal lock and payoff budget exist.
- Kept Gate26 hard block, canon auto-resolution, AutoRepair mutation, cross-project write, provider calls, raw manuscript leakage, and Node2 raw reveal access disabled.
- Added Stage133 proposal, blueprint, roadmap, stage note, manifests, release evidence, tests, repo doctor wiring, and main release gate integration.

## v1.32.0-stage132

- Added Stage132 Contradiction Classifier + Mystery Exemption.
- Added deterministic evidence classification for true contradiction, intentional mystery, character misunderstanding, reveal delay, and no-conflict cases.
- Added mystery exemption audit requiring reveal lock and payoff budget.
- Preserved writer approval for true contradictions.
- Kept Gate26 hard block, canon auto-resolution, AutoRepair mutation, cross-project write, provider calls, raw manuscript leakage, and Node2 raw reveal access disabled.
- Added Stage132 proposal, blueprint, roadmap, stage note, manifests, release evidence, tests, repo doctor wiring, and main release gate integration.

## v1.31.0-stage131

- Added Stage131 GIG / Gate26 advisory-only absorption.
- Added deterministic classification for true contradiction, intentional mystery, character misunderstanding, and reveal delay.
- Preserved writer approval for true contradictions.
- Kept Gate26 hard block, canon auto-resolution, AutoRepair mutation, cross-project write, provider calls, raw manuscript leakage, and Node2 raw reveal access disabled.
- Added Stage131 proposal, blueprint, roadmap, stage note, manifests, release evidence, tests, repo doctor wiring, and main release gate integration.
- Documented GitNexus native indexing attempt and Python fallback preflight path.

## v1.30.0-stage130

- Sealed Stage127-129 MultiWork work into the first clean MultiWork release authority.
- Preserved read-only shared world and shared character absorption.
- Kept direct V571 merge, cross-project write, raw manuscript sharing, canon auto-resolution, Gate26 hard block, active learning, and AutoRepair mutation blocked.
