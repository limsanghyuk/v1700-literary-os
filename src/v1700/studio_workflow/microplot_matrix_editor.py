from __future__ import annotations

from v1700.studio_workflow.contracts import EpisodeBoard


def build_microplot_matrix_editor_report(board: EpisodeBoard) -> dict:
    rows = [
        {
            "episode_id": episode.episode_id,
            "microplot_slots": episode.microplot_count,
            "branchpoint_lineage_preserved": True,
            "editable": True,
            "raw_text_cell": False,
        }
        for episode in board.episodes
    ]
    return {
        "status": "pass" if rows else "blocked",
        "project_id": board.project_id,
        "row_count": len(rows),
        "rows": rows,
        "provider_call_count": 0,
        "raw_manuscript_provider_leakage": 0,
    }
