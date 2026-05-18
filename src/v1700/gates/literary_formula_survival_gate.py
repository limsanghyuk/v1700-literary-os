from __future__ import annotations

import json
from pathlib import Path

REQUIRED_FORMULAS = (
    "DRSE",
    "EmotionalMomentum4D",
    "MiseEnSceneCompiler",
    "SceneGraphQueryEngine",
    "LiteraryRefinementLoop",
)


def run_literary_formula_survival_gate(root: Path | None = None) -> dict:
    root = root or Path(__file__).resolve().parents[3]
    manifest_path = root / "manifests" / "literary_formula_manifest.json"
    issues: list[str] = []
    if not manifest_path.exists():
        return {"stage": "73.1", "status": "blocked", "issues": ["literary_formula_manifest_missing"]}
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    formulas = {item.get("formula_id"): item for item in manifest.get("formulas", [])}
    for formula_id in REQUIRED_FORMULAS:
        item = formulas.get(formula_id)
        if not item:
            issues.append(f"formula_missing:{formula_id}")
            continue
        for rel in item.get("source_paths", []):
            if not (root / rel).exists():
                issues.append(f"source_missing:{formula_id}:{rel}")
        for rel in item.get("test_paths", []):
            if not (root / rel).exists():
                issues.append(f"test_missing:{formula_id}:{rel}")
        if item.get("survival_status") not in {"LIVE_RUNTIME", "PARTIAL_RUNTIME"}:
            issues.append(f"formula_not_runtime:{formula_id}")
    return {
        "stage": "73.1",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "formula_count": len(formulas),
        "required_formulas": list(REQUIRED_FORMULAS),
        "provider_default_calls": 0,
        "node2_raw_reveal_access_count": 0,
    }
