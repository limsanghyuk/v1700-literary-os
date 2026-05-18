from __future__ import annotations

from datetime import datetime, timezone

from .contracts import StudioSession


def open_studio_session(project_id: str = "stage104_sample_project") -> dict:
    session = StudioSession(
        session_id="stage104-session-001",
        project_id=project_id,
        opened_at=datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        active_episode_id="ep-001",
        active_scene_id="scene-001",
        unsaved_changes=False,
        provider_call_count=0,
        live_provider_call_count_in_release_gate=0,
    )
    return session.to_dict()
