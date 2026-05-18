from __future__ import annotations
from dataclasses import dataclass
from .branchpoint_registry import build_branchpoint_registry

LIVE_RUNTIME = "LIVE_RUNTIME"
PARTIAL_RUNTIME = "PARTIAL_RUNTIME"
DOCUMENTED_ONLY = "DOCUMENTED_ONLY"
MISSING_BUT_REQUIRED = "MISSING_BUT_REQUIRED"
DEPRECATED_BY_DESIGN = "DEPRECATED_BY_DESIGN"
UNKNOWN_NEEDS_REVIEW = "UNKNOWN_NEEDS_REVIEW"

@dataclass(frozen=True)
class CoreLogicEntry:
    logic_id: str
    source_branchpoint: str
    expected_behavior: str
    current_location: str
    evidence_files: tuple[str, ...]
    test_coverage: tuple[str, ...]
    gate_coverage: tuple[str, ...]
    survival_status: str
    reabsorption_priority: str

    def to_dict(self) -> dict:
        return {
            "logic_id": self.logic_id,
            "source_branchpoint": self.source_branchpoint,
            "expected_behavior": self.expected_behavior,
            "current_location": self.current_location,
            "evidence_files": list(self.evidence_files),
            "test_coverage": list(self.test_coverage),
            "gate_coverage": list(self.gate_coverage),
            "survival_status": self.survival_status,
            "reabsorption_priority": self.reabsorption_priority,
        }


def build_core_logic_survival_matrix() -> tuple[CoreLogicEntry, ...]:
    """Truthful Stage75 matrix before Stage76~79 reabsorption.

    Stage75 does not pretend that every P0 logic is already fully reabsorbed.
    It identifies what is live, partial, documented, or missing, and hands P0
    reabsorption targets to later stages.
    """
    return (
        CoreLogicEntry("node2_candidate_generation", "BP_STAGE25_NODE2_REWRITE_ENGINE", "Generate multiple prose candidates and select by authority/surface rules.", "src/v1700/nodes/node2_prose_renderer/candidates.py + planned Stage77 rewrite_orchestrator", ("docs/concepts/reader_surface_evaluation.md",), ("tests/test_stage77_node2_rewrite_restoration.py",), ("stage77_release_gate",), PARTIAL_RUNTIME, "P0"),
        CoreLogicEntry("node2_authority_guard", "BP_STAGE25_NODE2_REWRITE_ENGINE", "Prevent Node2 from overriding canon, reveal, or raw graph authority.", "src/v1700/nodes/node2_prose_renderer/validators.py", ("docs/architecture/node_authority_boundaries.md",), ("tests/test_stage72_1_node_projection_gate.py",), ("node_projection_gate", "stage77_release_gate"), LIVE_RUNTIME, "P0"),
        CoreLogicEntry("temporal_continuity", "BP_STAGE39_DRAMA_EXECUTION_ENGINE", "Maintain ordered dramatic timeline and detect discontinuity.", "planned src/v1700/drama_execution/temporal_continuity.py", (), ("tests/test_stage78_drama_execution_engine.py",), ("stage78_release_gate",), MISSING_BUT_REQUIRED, "P0"),
        CoreLogicEntry("emotional_pressure_valve", "BP_STAGE39_DRAMA_EXECUTION_ENGINE", "Escalate/release scene pressure deterministically.", "planned src/v1700/drama_execution/pressure.py", (), ("tests/test_stage78_drama_execution_engine.py",), ("stage78_release_gate",), MISSING_BUT_REQUIRED, "P0"),
        CoreLogicEntry("branch_commit_rollback", "BP_STAGE39_DRAMA_EXECUTION_ENGINE", "Commit, rollback, and reconverge narrative branch choices.", "planned src/v1700/drama_execution/branching.py", (), ("tests/test_stage78_drama_execution_engine.py",), ("stage78_release_gate",), MISSING_BUT_REQUIRED, "P0"),
        CoreLogicEntry("three_episode_structure", "BP_STAGE50_THREE_EPISODE_ENGINE", "Build a three-episode macro proof from a user prompt.", "src/v1700/longform/planners.py", ("docs/runbooks/stage74_longform_execution.md",), ("tests/test_stage74_longform_execution_engine.py",), ("longform_execution_gate", "stage76_release_gate"), PARTIAL_RUNTIME, "P0"),
        CoreLogicEntry("sequence_scale_planning", "BP_STAGE50_THREE_EPISODE_ENGINE", "Recover Stage60-scale sequence planning, target >= 29 sequences.", "planned src/v1700/reabsorption/stage60_literary_engine.py", (), ("tests/test_stage76_stage60_literary_engine_reabsorption.py",), ("stage76_release_gate",), MISSING_BUT_REQUIRED, "P0"),
        CoreLogicEntry("scene_scale_planning", "BP_STAGE50_THREE_EPISODE_ENGINE", "Recover Stage60-scale scene planning, target >= 532 planned scenes.", "planned src/v1700/reabsorption/stage60_literary_engine.py", (), ("tests/test_stage76_stage60_literary_engine_reabsorption.py",), ("stage76_release_gate",), MISSING_BUT_REQUIRED, "P0"),
        CoreLogicEntry("ten_axis_literary_quality", "BP_STAGE56_QUALITY_GATE", "Score prose using a multi-axis literary quality gate.", "planned src/v1700/reabsorption/stage60_literary_engine.py", (), ("tests/test_stage76_stage60_literary_engine_reabsorption.py",), ("stage76_release_gate",), MISSING_BUT_REQUIRED, "P0"),
        CoreLogicEntry("score_improving_refinement", "BP_STAGE57_REFINEMENT_LOOP", "Show measured before/after improvement with blockers reduced.", "src/v1700/longform/refinement.py + planned Stage76 Stage60 loop", ("docs/concepts/literary_formula_stack.md",), ("tests/test_stage76_stage60_literary_engine_reabsorption.py",), ("stage76_release_gate",), PARTIAL_RUNTIME, "P0"),
        CoreLogicEntry("drse_weighted_relation_scoring", "BP_V328_DRSE_STACK", "Compute relation, causality, emotion, residue, and legacy weights outside the LLM.", "src/v1700/literary_formulas/drse.py", ("docs/concepts/drse_formula.md",), ("tests/test_stage73_1_literary_formula_restoration.py",), ("stage73_1_release_gate",), LIVE_RUNTIME, "P0"),
        CoreLogicEntry("emotional_momentum_vector", "BP_V328_DRSE_STACK", "Track tension, sympathy, dread, catharsis as a 4D vector.", "src/v1700/literary_formulas/emotional_momentum.py", ("docs/concepts/emotional_momentum_vector.md",), ("tests/test_stage73_1_literary_formula_restoration.py",), ("stage73_1_release_gate",), LIVE_RUNTIME, "P0"),
        CoreLogicEntry("mise_en_scene_directive", "BP_V328_DRSE_STACK", "Compile DRSE and momentum into sensory/directorial directives.", "src/v1700/literary_formulas/mise_en_scene_compiler.py", ("docs/concepts/mise_en_scene_compiler.md",), ("tests/test_stage73_1_literary_formula_restoration.py",), ("stage73_1_release_gate",), LIVE_RUNTIME, "P0"),
        CoreLogicEntry("graph_nexus_three_graphs", "BP_STAGE72_GRAPHNEXUS", "Maintain CodeGraph, NarrativeGraph, StageLineageGraph.", "src/v1700/graph_nexus", ("docs/concepts/graph_nexus_3graph_model.md",), ("tests/test_stage72_1_graph_nexus_three_graphs.py",), ("graph_nexus_release_gate",), LIVE_RUNTIME, "P1"),
        CoreLogicEntry("full_workspace_reproducibility", "BP_STAGE73_74_BASELINE_AND_FORMULA", "Package active repo and knowledge base for cross-local reproduction.", "package/release manifests", ("release/current/STAGE74_FULL_WORKSPACE_RELEASE_REPORT.md",), ("tests/test_stage74_longform_execution_engine.py",), ("stage74_release_gate",), LIVE_RUNTIME, "P1"),
    )


def build_missing_required_logic_manifest() -> dict:
    entries = [entry for entry in build_core_logic_survival_matrix() if entry.survival_status in {MISSING_BUT_REQUIRED, PARTIAL_RUNTIME} and entry.reabsorption_priority == "P0"]
    return {
        "stage": "75",
        "status": "known_blockers_registered",
        "meaning": "Stage75 identifies required missing or partial branchpoint logics; Stage76+ must reabsorb them.",
        "missing_or_partial_count": len(entries),
        "items": [entry.to_dict() for entry in entries],
    }


def stage75_truthful_status() -> dict:
    registry = build_branchpoint_registry()
    matrix = build_core_logic_survival_matrix()
    missing = build_missing_required_logic_manifest()
    issues = []
    required_bp = {"BP_STAGE25_NODE2_REWRITE_ENGINE", "BP_STAGE39_DRAMA_EXECUTION_ENGINE", "BP_STAGE50_THREE_EPISODE_ENGINE", "BP_STAGE56_QUALITY_GATE", "BP_STAGE57_REFINEMENT_LOOP", "BP_STAGE60_FINAL_USER_RC", "BP_V328_DRSE_STACK"}
    present = {bp.branchpoint_id for bp in registry}
    if not required_bp.issubset(present):
        issues.append("p0_branchpoints_missing_from_registry")
    if not matrix:
        issues.append("core_logic_matrix_empty")
    if missing["missing_or_partial_count"] < 1:
        issues.append("missing_logic_manifest_not_truthful")
    return {
        "stage": "75",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "branchpoint_count": len(registry),
        "core_logic_count": len(matrix),
        "known_p0_missing_or_partial_count": missing["missing_or_partial_count"],
        "pass_meaning": "All critical branchpoints are registered and missing/partial P0 logic is truthfully recorded for Stage76+ reabsorption.",
    }
