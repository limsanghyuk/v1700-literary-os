from __future__ import annotations

from pathlib import Path

from v1700.manuscript_learning.coefficient_memory import build_coefficient_memory
from v1700.manuscript_learning.corpus_loader import load_synthetic_corpus
from v1700.manuscript_learning.pattern_miner import mine_scene_patterns
from v1700.manuscript_learning.privacy_guard import audit_feature_privacy
from v1700.manuscript_learning.scene_feature_extractor import extract_scene_features
from v1700.narrative_optimization.optimizer import run_narrative_physics_optimization


def run_manuscript_learning(root: Path | None = None, optimization: dict | None = None) -> dict:
    root = root or Path.cwd()
    optimization = optimization or run_narrative_physics_optimization()
    corpus = load_synthetic_corpus(root)
    features = extract_scene_features(corpus)
    privacy = audit_feature_privacy(features)
    patterns = mine_scene_patterns(features)
    memory = build_coefficient_memory(optimization, features, privacy)
    issues = []
    if not features:
        issues.append("scene_feature_extraction_empty")
    if privacy["status"] != "pass":
        issues.append("privacy_guard_blocked")
    if optimization.get("status") != "pass":
        issues.append("optimization_blocked")
    return {
        "stage": "96B",
        "status": "pass" if not issues else "blocked",
        "corpus_source": corpus[0]["source"] if corpus else "",
        "scene_feature_count": len(features),
        "feature_preview": [feature.to_dict() for feature in features[:5]],
        "patterns": patterns,
        "coefficient_memory": memory,
        "privacy_report": privacy,
        "provider_default_calls": 0,
        "live_provider_call_count": 0,
        "issues": issues,
    }


def build_stage96_manuscript_learning_manifest() -> dict:
    return {
        "stage": "96B",
        "title": "Manuscript Learning",
        "status": "pass_pending_export",
        "source_policy": "local_feature_only",
        "raw_manuscript_provider_transmission_allowed": False,
    }
