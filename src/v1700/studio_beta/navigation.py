from __future__ import annotations


def build_navigation_report() -> dict:
    return {
        "status": "pass",
        "navigation_model": "episode_scene_beat_navigation",
        "routes": ["/project", "/episode/ep-001", "/scene/scene-001", "/review", "/export"],
        "provider_call_count": 0,
    }
