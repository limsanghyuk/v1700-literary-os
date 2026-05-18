from __future__ import annotations

from .unified_board import build_unified_board


def render_board_summary() -> dict:
    board = build_unified_board()
    return {
        "status": board.get("status"),
        "render_target": "local_beta_console_or_static_html",
        "raw_manuscript_rendered": False,
        "cards_rendered": len(board["prose_board"]["cards"]) + len(board["scenario_board"]["cards"]),
    }
