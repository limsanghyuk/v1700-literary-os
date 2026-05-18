from __future__ import annotations

from v1700.studio_workflow.contracts import StudioProject


def build_story_bible_report(project: StudioProject) -> dict:
    return {
        "status": "pass",
        "project_id": project.project_id,
        "baseline_stage": project.baseline_stage,
        "bible_mode": "feature_only",
        "tracks": ["branchpoints", "payoff_debt", "agency", "attention", "voice"],
        "raw_text_included": False,
        "node2_raw_reveal_access": 0,
    }
