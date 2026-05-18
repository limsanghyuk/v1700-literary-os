from __future__ import annotations

from .contracts import BoardReport


def build_prose_board() -> dict:
    cards = (
        {"card_id": "prose-001", "scene_id": "scene-001", "voice_note": "restrained guilt", "sensory_anchor": "rain_on_platform", "node2_surface_safety": "pass"},
        {"card_id": "prose-002", "scene_id": "scene-002", "rhythm_note": "short beats before reveal", "emotion_movement": "avoidance_to_confrontation", "node2_surface_safety": "pass"},
    )
    return BoardReport(status="pass", board_id="stage104-prose-board", mode="PROSE", cards=cards).to_dict()
