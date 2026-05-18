from __future__ import annotations

from v1700.studio_workflow.contracts import EpisodeBoard, EpisodeCard, StudioProject


def build_episode_board(project: StudioProject) -> EpisodeBoard:
    episodes = [
        EpisodeCard(
            episode_id=f"ep-{idx:02d}",
            episode_idx=idx,
            title=f"Episode {idx:02d}",
            function=_episode_function(idx, project.episode_count),
            microplot_count=5,
            structural_scene_count=6,
            production_scene_count_estimate=10,
            payoff_debt_status="tracked",
            agency_status="conserved",
            attention_status="balanced",
        )
        for idx in range(1, project.episode_count + 1)
    ]
    return EpisodeBoard(project_id=project.project_id, episodes=episodes, board_status="READY")


def episode_board_report(board: EpisodeBoard) -> dict:
    return {
        "status": "pass" if board.board_status == "READY" and board.episodes else "blocked",
        "board": board.to_dict(),
        "episode_count": len(board.episodes),
        "microplot_total": sum(episode.microplot_count for episode in board.episodes),
        "production_scene_count_estimate": sum(episode.production_scene_count_estimate for episode in board.episodes),
    }


def _episode_function(idx: int, total: int) -> str:
    if idx == 1:
        return "inciting_contract"
    if idx == total:
        return "payoff_convergence"
    if idx in {total // 2, total // 2 + 1}:
        return "midpoint_reversal"
    return "escalation"
