from __future__ import annotations

import json
from pathlib import Path


def analyze_concept_impact(root: Path, target: str) -> dict:
    manifest_path = root / "manifests" / "pre_stage40_lineage_manifest.json"
    if not manifest_path.exists():
        return {"status": "blocked", "reason": "pre_stage40_lineage_manifest_missing", "target": target}

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    needle = target.lower()
    matches = []
    for concept in manifest.get("concepts", []):
        haystack = " ".join(
            [
                concept["concept_id"],
                concept["title"],
                " ".join(concept["stage_origins"]),
                " ".join(concept.get("current_runtime_anchor", [])),
                " ".join(concept.get("current_test_anchor", [])),
                " ".join(concept.get("current_gate_anchor", [])),
                " ".join(concept.get("current_doc_anchor", [])),
            ]
        ).lower()
        if needle in haystack:
            matches.append(concept)

    risk = "high" if any(c["promotion_priority"] == "HIGH" for c in matches) else "medium" if matches else "low"
    return {
        "status": "pass",
        "target": target,
        "risk": risk,
        "affected_concepts": [
            {
                "concept_id": concept["concept_id"],
                "stage_origins": concept["stage_origins"],
                "survival_status": concept["survival_status"],
                "promotion_priority": concept["promotion_priority"],
            }
            for concept in matches
        ],
    }
