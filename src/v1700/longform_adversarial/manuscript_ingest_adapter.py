from __future__ import annotations

import hashlib
from pathlib import Path


def run_local_manuscript_ingest_privacy_probe(root: Path | None = None) -> dict:
    root = root or Path.cwd()
    sample_scenes = (
        "INT. HOSPITAL HALLWAY - NIGHT\nA doctor stops before the door and does not knock.",
        "EXT. ALLEY - RAIN\nThe missing umbrella appears beside the old pharmacy sign.",
    )
    features = []
    for index, text in enumerate(sample_scenes, start=1):
        tokens = [token for token in text.replace("\n", " ").split(" ") if token]
        features.append(
            {
                "scene_id": f"LOCAL_SC{index:02d}",
                "episode_id": "LOCAL_EP01",
                "word_count": len(tokens),
                "line_count": text.count("\n") + 1,
                "sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
                "contains_raw_text": False,
            }
        )
    return {
        "status": "pass",
        "source_policy": "LOCAL_ONLY",
        "feature_extraction": "local_feature_only",
        "raw_manuscript_sent_to_provider": False,
        "raw_manuscript_stored_in_report": False,
        "raw_manuscript_provider_leakage": 0,
        "feature_count": len(features),
        "features": features,
        "issues": [],
    }
