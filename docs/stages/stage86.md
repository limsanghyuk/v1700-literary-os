# Stage86: V380 Arc-Reveal-Knowledge Absorption

Stage86 promotes the V380 longform ideas into the active V1700 Branchpoint OS.

It does not replace V1700 with the Claude/V380 repository. The absorption rule is:

```text
V380 concept -> V1700 code symbol -> test -> release gate -> trace matrix
```

## Runtime Additions

| Concept | Live symbol | Runtime role |
| --- | --- | --- |
| SeriesArcPlanner | `v1700.arc_reveal_knowledge.series_arc_planner.SeriesArcPlanner` | Builds a four-act 16-episode season arc. |
| CausalPlotGraph | `v1700.arc_reveal_knowledge.causal_plot_graph.CausalPlotGraph` | Tracks causal, foreshadow, callback, and emotional escalation edges. |
| EpisodeRevealBudget | `v1700.arc_reveal_knowledge.reveal_budget.EpisodeRevealBudget` | Blocks direct premature reveal while allowing foreshadowing. |
| CharacterKnowledgeProseBridge | `v1700.arc_reveal_knowledge.character_knowledge_bridge.CharacterKnowledgeProseBridge` | Converts character knowledge asymmetry into prose constraints. |
| ProseRenderContract bridge | `v1700.arc_reveal_knowledge.prose_contract_bridge.build_prose_render_contract` | Feeds reveal and knowledge constraints into Node2 surface-only rendering. |

## Preserved Boundaries

- Provider default calls remain `0`.
- Node2 raw reveal access remains `0`.
- GitNexus remains optional sidecar evidence.
- GraphNexus remains the internal authority graph.
- Python fallback remains required.
- Stage85 symbol-to-branchpoint traceability remains active.

## Developer Commands

```bash
python tools/run_stage86_release_gate.py
python tools/run_symbol_to_branchpoint_trace_gate.py
python tools/run_release_gate.py
python -m pytest -q tests
```

## Long-Term Direction

Stage86 is the first step after the Stage85 safety layer. The next staged direction is:

```text
Stage87: 8-16 episode scale-up evidence
Stage88: external editorial benchmark protocol
Stage89: Writer Studio UI and export pipeline
```
