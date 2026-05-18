from __future__ import annotations

import json
from pathlib import Path

from v1700.longform_adversarial.contracts import CoefficientBridgeConfig


def load_stage96_coefficient_bridge(root: Path | None = None) -> dict:
    root = root or Path.cwd()
    memory_path = root / "release" / "current" / "stage96_coefficient_memory.json"
    if not memory_path.exists():
        config = _fallback_config(memory_path)
        return {
            "status": "pass",
            "source": "fallback_defaults",
            "config": config.to_dict(),
            "issues": [],
        }

    memory = json.loads(memory_path.read_text(encoding="utf-8"))
    learned = memory.get("learned_coefficients", {})
    fatigue_weight = float(learned.get("fatigue_penalty_weight", 0.6))
    branch_weight = float(learned.get("branchpoint_survival_weight", 1.35))
    surface_weight = float(learned.get("surface_safety_weight", 1.25))
    config = CoefficientBridgeConfig(
        source_stage=str(memory.get("version", "stage96")),
        coefficient_memory_path=str(memory_path.relative_to(root)),
        load_weight_overrides={key: float(value) for key, value in learned.items()},
        fatigue_threshold=round(max(0.38, 0.52 - fatigue_weight * 0.08), 3),
        agency_floor=round(min(0.68, 0.52 + branch_weight * 0.03), 3),
        payoff_default_threshold=0.0,
        style_drift_tolerance=round(max(0.14, 0.22 - surface_weight * 0.025), 3),
        privacy_mode="LOCAL_ONLY",
    )
    privacy = memory.get("privacy_report", {})
    issues = []
    if memory.get("source_policy") != "local_feature_only":
        issues.append("coefficient_memory_source_policy_not_local_feature_only")
    if privacy.get("raw_manuscript_sent_to_provider") is not False:
        issues.append("raw_manuscript_provider_leakage")
    if memory.get("drift_guard", {}).get("status") != "pass":
        issues.append("coefficient_drift_guard_blocked")
    return {
        "status": "pass" if not issues else "blocked",
        "source": "stage96_coefficient_memory",
        "config": config.to_dict(),
        "feature_summary": memory.get("feature_summary", {}),
        "privacy_report": privacy,
        "issues": issues,
    }


def _fallback_config(memory_path: Path) -> CoefficientBridgeConfig:
    return CoefficientBridgeConfig(
        source_stage="stage96",
        coefficient_memory_path=str(memory_path),
        load_weight_overrides={},
        fatigue_threshold=0.47,
        agency_floor=0.56,
        payoff_default_threshold=0.0,
        style_drift_tolerance=0.18,
        privacy_mode="LOCAL_ONLY",
    )
