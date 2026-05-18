from __future__ import annotations

from pathlib import Path

from .report import write_json
from .unified_board import build_unified_board


def export_board(path: Path) -> dict:
    board = build_unified_board()
    write_json(path, board)
    return {"status": board.get("status"), "path": path.as_posix(), "includes_full_text": False}
