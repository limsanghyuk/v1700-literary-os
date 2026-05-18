# Stage001-039 Foundation Lineage

This document maps the early V1650 foundation concepts into the current V1700 runtime.

| Concept | Stage origin | Evidence | Survival | Current anchor | Missing work |
|---|---|---|---|---|---|
| Multi-Provider Creative Comparison | STAGE10 | E4_TESTED | PARTIAL | src/v1700/runtime/provider_boundary.py | provider quality score normalization |
| Provider Execution Trace | STAGE11 | E4_TESTED | PARTIAL | src/v1700/runtime/cost_ledger.py<br>src/v1700/runtime/provider_boundary.py | full provider trace persistence |
| End-to-End Authoring Scenario Runner | STAGE12 | E3_EXECUTABLE | DOCUMENTED_ONLY | docs/stages/stage_001_039_foundation.md | modern authoring scenario runner |
| Memory Conflict Resolver | STAGE13 | E3_EXECUTABLE | PARTIAL | src/v1700/ledgers/character_event_time.py<br>src/v1700/ledgers/reveal_budget.py | explicit conflict resolver gate |
| Node2 Literary Quality Engine | STAGE14 | E5_LIVE_CURRENT | LIVE_RUNTIME | src/v1700/nodes/node2_prose_renderer/compiler.py<br>src/v1700/nodes/node2_prose_renderer/scorer.py | none |
| Literary Depth Calibration | STAGE15 | E4_TESTED | PARTIAL | src/v1700/nodes/node2_prose_renderer/scorer.py<br>src/v1700/ir/style_profile.py | dedicated literary depth benchmark |
| Long-Horizon Memory Drift Stress | STAGE16 | E4_TESTED | PARTIAL | src/v1700/ledgers/reveal_budget.py<br>src/v1700/ledgers/character_event_time.py | long horizon regression fixture |
| Authoring Review Workflow | STAGE17 | E3_EXECUTABLE | DOCUMENTED_ONLY | docs/runbooks/organic_impact_review_protocol.md | modern review workflow runtime |
| Human/Agent Review Console | STAGE18 | E3_EXECUTABLE | DOCUMENTED_ONLY | docs/reviews/stage72_3_principal_engineer_validation.md | agent review console adapter |
| Episode Draft Export Harness | STAGE21 | E4_TESTED | PARTIAL | docs/stages/stage_050_052_longform_state_guards.md | episode draft export command |
| Series Arc Control | STAGE22 | E4_TESTED | PARTIAL | src/v1700/ir/scene_intent.py<br>src/v1700/nodes/node1_architect/__init__.py | season arc planner<br>episode arc planner |
| Node2 Style Evolution Memory | STAGE23 | E5_LIVE_CURRENT | LIVE_RUNTIME | src/v1700/ledgers/style_memory.py<br>src/v1700/nodes/node2_prose_renderer/authorial_profile.py | none |
| Boundary Registry | STAGE24 | E4_TESTED | PARTIAL | src/v1700/graph_nexus/projection.py<br>src/v1700/graph_nexus/graph_nexus_packet.py | central boundary registry manifest |
| Release Candidate Gate | STAGE25 | E5_LIVE_CURRENT | LIVE_RUNTIME | src/v1700/gates/release_gate.py<br>src/v1700/gates/stage72_2_release_gate.py | none |
| Stage26-28 Regression Stream | STAGE26, STAGE27, STAGE28 | E4_TESTED | PARTIAL | src/v1700/gates/release_gate.py | cross-stage regression matrix |
| Concept Validation Workbench | STAGE33 | E4_TESTED | PARTIAL | src/v1700/gates/pre_stage40_survival_gate.py | interactive concept workbench revival |
| Evidence Intake Foundation | STAGE39 | E3_EXECUTABLE | PARTIAL | src/v1700/graph_nexus/tools/context.py | evidence intake queue integration |
| Analyzer/Librarian Integration | STAGE39 | E3_EXECUTABLE | PARTIAL | src/v1700/graph_nexus/tools/query.py<br>src/v1700/graph_nexus/tools/context.py | librarian role runtime adapter |
| Graph Retrieval Bridge | STAGE39 | E3_EXECUTABLE | PARTIAL | src/v1700/graph_nexus/registry.py<br>src/v1700/graph_nexus/tools/query.py | narrative GraphRAG retriever |
| Temporal Continuity | STAGE39 | E4_TESTED | PARTIAL | src/v1700/ledgers/character_event_time.py<br>src/v1700/ir/scene_intent.py | temporal delta controller in Node1 planning route |
| Longform Scene-Sequence Planner | STAGE39 | E4_TESTED | PARTIAL | src/v1700/ir/scene_intent.py | runtime sequence planner<br>scene count estimator |
| Branch Commit/Rollback | STAGE39 | E4_TESTED | DOCUMENTED_ONLY | docs/proposals/stage72_3_pre_stage40_lineage_recovery_proposal.md | branch isolation runtime<br>what-if archive policy |
| Emotional Pressure Valve | STAGE39 | E4_TESTED | PARTIAL | src/v1700/ir/scene_intent.py<br>src/v1700/nodes/node2_prose_renderer/emotion_renderer.py | series-level emotional wave controller |
| Node2 Candidate Rendering | STAGE39 | E5_LIVE_CURRENT | LIVE_RUNTIME | src/v1700/nodes/node2_prose_renderer/candidates.py<br>src/v1700/nodes/node2_prose_renderer/compiler.py | none |
| Actual Replay Reconvergence | STAGE39 | E4_TESTED | PARTIAL | src/v1700/gates/release_gate.py | deterministic replay ledger |

## Operating Rule

Pre-Stage40 material is not restored by blind file copy. It is restored by concept survival mapping, source evidence, current anchors, and release gates.
