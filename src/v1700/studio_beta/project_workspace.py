from __future__ import annotations

from .contracts import SceneCard, StudioBetaProject, WorkspaceState


def build_sample_project() -> StudioBetaProject:
    return StudioBetaProject(
        project_id="stage104_sample_project",
        title="Rain Station Studio Beta Sample",
        project_type="series",
        privacy_mode="FEATURE_ONLY",
        active_mode="PROSE",
        baseline_stage="stage103",
        feature_only=True,
        metadata={"source": "stage104_beta_fixture", "writer_control": "approval_required"},
    )


def build_sample_workspace() -> dict:
    project = build_sample_project()
    cards = (
        SceneCard("scene-001", "ep-001", "폐역 도착", "PROSE", "guilt_sensory_anchor", 3),
        SceneCard("scene-002", "ep-001", "전광판 점등", "SCENARIO", "prop_led_reveal", 4),
        SceneCard("scene-003", "ep-001", "수정 검토", "REVIEW", "writer_decision_checkpoint", 2),
    )
    state = WorkspaceState(
        project_id=project.project_id,
        episodes=("ep-001", "ep-002", "ep-003"),
        scene_cards=cards,
        revision_queue_size=2,
        unresolved_block_count=0,
        export_ready=True,
    )
    return {"project": project.to_dict(), "workspace_state": state.to_dict()}
