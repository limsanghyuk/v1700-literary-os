# Foundation Lineage Skill

Use this skill when a change may affect pre-Stage40 literary generator logic.

## Required Checks

- Identify related `concept_id` entries in `manifests/pre_stage40_lineage_manifest.json`.
- Verify source evidence exists in the knowledge base.
- Verify LIVE/PARTIAL concepts still have runtime, gate, test, or doc anchors.
- Run `python tools/run_pre_stage40_survival_gate.py` before promotion.

## High-Priority Concepts

- `foundation.memory.conflict_resolver`: PARTIAL
- `foundation.node2.literary_quality_engine`: LIVE_RUNTIME
- `foundation.node2.literary_depth_calibration`: PARTIAL
- `foundation.memory.long_horizon_drift_stress`: PARTIAL
- `foundation.longform.episode_draft_export`: PARTIAL
- `foundation.longform.series_arc_control`: PARTIAL
- `foundation.node2.style_evolution_memory`: LIVE_RUNTIME
- `foundation.governance.boundary_registry`: PARTIAL
- `foundation.governance.release_candidate_gate`: LIVE_RUNTIME
- `foundation.governance.stage26_28_regression_stream`: PARTIAL
- `foundation.governance.concept_validation_workbench`: PARTIAL
- `foundation.stage39.evidence_intake_foundation`: PARTIAL
- `foundation.stage39.analyzer_librarian_integration`: PARTIAL
- `foundation.stage39.graph_retrieval_bridge`: PARTIAL
- `foundation.stage39.temporal_continuity`: PARTIAL
- `foundation.stage39.longform_scene_sequence_planner`: PARTIAL
- `foundation.stage39.branch_commit_rollback`: DOCUMENTED_ONLY
- `foundation.stage39.emotional_pressure_valve`: PARTIAL
- `foundation.stage39.node2_candidate_rendering`: LIVE_RUNTIME
- `foundation.stage39.actual_replay_reconvergence`: PARTIAL
