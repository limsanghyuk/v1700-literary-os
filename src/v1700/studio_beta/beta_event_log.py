from __future__ import annotations


def build_beta_event_log() -> dict:
    events = [
        {"event": "open_project", "project_id": "stage104_sample_project", "raw_text": False},
        {"event": "switch_mode", "mode": "SCENARIO", "raw_text": False},
        {"event": "approve_revision", "revision_id": "rev-001", "raw_text": False},
        {"event": "export_feature_only", "export_id": "stage104-beta-export-001", "raw_text": False},
    ]
    return {"status": "pass", "events": events, "event_count": len(events), "raw_manuscript_included": False}
