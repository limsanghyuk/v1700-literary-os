from __future__ import annotations

from .project_workspace import build_sample_workspace


def scene_card_index() -> dict:
    workspace = build_sample_workspace()["workspace_state"]
    return {
        "status": "pass",
        "scene_count": len(workspace["scene_cards"]),
        "scene_cards": workspace["scene_cards"],
        "raw_manuscript_included": False,
    }
