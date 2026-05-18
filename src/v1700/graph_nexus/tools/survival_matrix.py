from __future__ import annotations

import json
from pathlib import Path


def build_survival_matrix(root: Path) -> dict:
    manifest_path = root / "manifests" / "pre_stage40_lineage_manifest.json"
    if not manifest_path.exists():
        return {"status": "blocked", "reason": "pre_stage40_lineage_manifest_missing"}

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    buckets: dict[str, list[str]] = {}
    for concept in manifest.get("concepts", []):
        buckets.setdefault(concept["survival_status"], []).append(concept["concept_id"])

    return {
        "status": "pass",
        "concept_count": manifest.get("concept_count", 0),
        "buckets": {key: sorted(value) for key, value in sorted(buckets.items())},
    }
