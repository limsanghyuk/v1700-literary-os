from __future__ import annotations

from pathlib import Path

from v1700.manuscript_learning.learning_report import run_manuscript_learning
from v1700.narrative_optimization.optimizer import run_narrative_physics_optimization
from v1700.narrative_physics.engine import run_stage95_narrative_physics_smoke
from v1700.provider_ensemble.arbiter import run_provider_ensemble_arbitration


def run_stage96_pipeline(root: Path | None = None) -> dict:
    root = root or Path.cwd()
    stage95 = run_stage95_narrative_physics_smoke()
    optimization = run_narrative_physics_optimization(stage95)
    learning = run_manuscript_learning(root, optimization)
    ensemble = run_provider_ensemble_arbitration(root, stage95, optimization)
    checks = {
        "stage95_baseline": stage95,
        "narrative_optimization": optimization,
        "manuscript_learning": learning,
        "provider_ensemble": ensemble,
    }
    issues = [name for name, report in checks.items() if report.get("status") != "pass"]
    if ensemble.get("live_provider_call_count") != 0 or learning.get("live_provider_call_count") != 0:
        issues.append("live_provider_call_count_not_zero")
    if ensemble.get("provider_default_calls") != 0 or learning.get("provider_default_calls") != 0:
        issues.append("provider_default_calls_not_zero")
    if stage95.get("node2_raw_reveal_access_count") != 0 or ensemble.get("node2_raw_reveal_access_count") != 0:
        issues.append("node2_raw_reveal_access_not_zero")
    return {
        "stage": "96",
        "status": "pass" if not issues else "blocked",
        "title": "Narrative Physics Optimization, Manuscript Learning, and Provider Ensemble Arbitration",
        "checks": checks,
        "provider_default_calls": 0,
        "live_provider_call_count": 0,
        "node2_raw_reveal_access_count": 0,
        "issues": issues,
    }
