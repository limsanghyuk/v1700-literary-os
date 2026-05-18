from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class BranchpointModel:
    branchpoint_id: str
    source: str
    priority: str
    why_it_branches: str
    core_logic_ids: tuple[str, ...]
    required_in_current_model: bool = True

    def to_dict(self) -> dict:
        return {
            "branchpoint_id": self.branchpoint_id,
            "source": self.source,
            "priority": self.priority,
            "why_it_branches": self.why_it_branches,
            "core_logic_ids": list(self.core_logic_ids),
            "required_in_current_model": self.required_in_current_model,
        }


def build_branchpoint_registry() -> tuple[BranchpointModel, ...]:
    """Canonical Stage75 branchpoint registry.

    The registry intentionally separates branchpoint models from ordinary stage
    increments. A branchpoint is a model/stage that changed the system's
    operating logic, literary math, or release boundary.
    """
    return (
        BranchpointModel(
            "BP_STAGE25_NODE2_REWRITE_ENGINE",
            "Stage25 / Node2 Generative Rewrite Engine",
            "P0",
            "Node2 changed from evaluator/surface helper into a candidate-generating rewrite orchestrator.",
            ("node2_candidate_generation", "node2_authority_guard", "node2_selection_layer"),
        ),
        BranchpointModel(
            "BP_STAGE39_DRAMA_EXECUTION_ENGINE",
            "Stage39 Drama Execution Engine",
            "P0",
            "The project moved from literary scaffolding into drama execution: temporal continuity, pressure, branch rollback, and reconvergence.",
            ("temporal_continuity", "emotional_pressure_valve", "branch_commit_rollback", "replay_reconvergence"),
        ),
        BranchpointModel(
            "BP_STAGE50_THREE_EPISODE_ENGINE",
            "Stage50 Prompt-to-Three-Episode Engine",
            "P0",
            "Prompt-to-longform became a three-episode, sequence, and scene scale engine.",
            ("three_episode_structure", "sequence_scale_planning", "scene_scale_planning"),
        ),
        BranchpointModel(
            "BP_STAGE56_QUALITY_GATE",
            "Stage56 Literary Quality Evaluation Gate",
            "P0",
            "Literary generation gained multi-axis quality scoring rather than ad-hoc acceptance.",
            ("ten_axis_literary_quality", "quality_blocker_detection"),
        ),
        BranchpointModel(
            "BP_STAGE57_REFINEMENT_LOOP",
            "Stage57 Literary Refinement Loop",
            "P0",
            "Drafts gained a measured critic -> revise -> rescore loop with score delta.",
            ("score_improving_refinement", "blocker_axis_reduction"),
        ),
        BranchpointModel(
            "BP_STAGE60_FINAL_USER_RC",
            "Stage60 Final User Release Candidate",
            "P0",
            "The literary engine reached a user-facing release candidate with Stage50/56/57 evidence.",
            ("stage60_release_contract", "stage60_literary_engine_bundle"),
        ),
        BranchpointModel(
            "BP_V328_DRSE_STACK",
            "V328 / DRSE, EmotionalMomentum, Mise-en-scene",
            "P0",
            "The user's mathematical literary theory became a relational scoring and mise-en-scene stack.",
            ("drse_weighted_relation_scoring", "emotional_momentum_vector", "mise_en_scene_directive"),
        ),
        BranchpointModel(
            "BP_STAGE12_E2E_AUTHORING",
            "Stage12 End-to-End Authoring Scenario Runner",
            "P1",
            "Early isolated loops became an end-to-end authoring scenario.",
            ("e2e_authoring_scenario",),
        ),
        BranchpointModel(
            "BP_STAGE29_GRAPHRAG_MEMORY",
            "Stage29~31 Canon Memory Index / GraphRAG / Controlled Weight Mutation",
            "P1",
            "Memory became indexed, graph-queryable, and weight-adjustable.",
            ("canon_memory_index", "scene_graph_query", "controlled_weight_mutation"),
        ),
        BranchpointModel(
            "BP_STAGE33_35_VALIDATION_AND_CRITIC",
            "Stage33~35 Concept Validation / Authoring Console / Critic Comparison Gate",
            "P1",
            "Generation became a validated, author-facing, critic-comparable process.",
            ("concept_validation_workbench", "authoring_console", "critic_comparison_gate"),
        ),
        BranchpointModel(
            "BP_STAGE65_GRAPH_INTELLIGENCE",
            "Stage65~66 Graph Intelligence Consolidation",
            "P1",
            "Graph sidecar thinking became consolidated and authority-bounded.",
            ("graph_intelligence_sidecar", "authority_boundary"),
        ),
        BranchpointModel(
            "BP_STAGE70_FINAL_VERIFIED_RUNTIME",
            "Stage70 Final Verified Runtime Release",
            "P1",
            "The system gained local-first runtime verification and provider default call zero.",
            ("local_first_runtime", "provider_zero_gate", "verified_release_gate"),
        ),
        BranchpointModel(
            "BP_STAGE71_READER_SURFACE",
            "Stage71 Node2 Reader-Facing Prose Renderer",
            "P1",
            "The project re-centered reader-facing prose surface and anti-LLM naturalness.",
            ("reader_surface_renderer", "anti_llm_surface"),
        ),
        BranchpointModel(
            "BP_STAGE72_GRAPHNEXUS",
            "Stage72.1~72.3 GraphNexus / GitNexus / Foundation Lineage",
            "P1",
            "The system built code/narrative/stage lineage graphs and pre-Stage40 survival gates.",
            ("graph_nexus_three_graphs", "foundation_lineage_survival"),
        ),
        BranchpointModel(
            "BP_STAGE73_74_BASELINE_AND_FORMULA",
            "Stage73~74 Full Workspace Baseline / Formula Restoration",
            "P1",
            "Full workspace reproducibility and smoke-level literary formula restoration became canonical.",
            ("full_workspace_reproducibility", "longform_smoke_engine"),
        ),
    )
