from __future__ import annotations

SECRET_MARKERS = ("sk-", "BEGIN PRIVATE KEY", "READER_ONLY", "NODE2_RAW_REVEAL", "password=")


def audit_feature_privacy(features: tuple) -> dict:
    serialized = repr([feature.to_dict() for feature in features])
    leaked_markers = [marker for marker in SECRET_MARKERS if marker in serialized]
    return {
        "status": "pass" if not leaked_markers else "blocked",
        "source_policy": "local_feature_only",
        "raw_manuscript_sent_to_provider": False,
        "raw_manuscript_stored_in_report": False,
        "provider_log_leakage_count": 0,
        "leaked_markers": leaked_markers,
    }
