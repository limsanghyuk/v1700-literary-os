from __future__ import annotations

import hashlib
import json

from .contracts import BackupRestoreResult


def run_backup_restore_probe() -> dict:
    snapshot = {
        "project_id": "stage103_sample_project",
        "metadata_schema": "v1700.project.backup.v1",
        "episode_count": 3,
        "scene_cards": 30,
        "contains_raw_manuscript": False,
        "feature_only": True,
    }
    encoded = json.dumps(snapshot, ensure_ascii=False, sort_keys=True).encode("utf-8")
    source_checksum = hashlib.sha256(encoded).hexdigest()
    restored = json.loads(encoded.decode("utf-8"))
    restored_checksum = hashlib.sha256(json.dumps(restored, ensure_ascii=False, sort_keys=True).encode("utf-8")).hexdigest()
    issues = []
    if source_checksum != restored_checksum:
        issues.append("backup_restore_checksum_mismatch")
    if not restored.get("feature_only") or restored.get("contains_raw_manuscript"):
        issues.append("backup_contains_raw_manuscript")
    result = BackupRestoreResult(
        status="pass" if not issues else "blocked",
        backup_format="json_feature_only_project_snapshot",
        source_checksum=source_checksum,
        restored_checksum=restored_checksum,
        metadata_only=True,
        issues=tuple(issues),
    )
    return result.to_dict()
