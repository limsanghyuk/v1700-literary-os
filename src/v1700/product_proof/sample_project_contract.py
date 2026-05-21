from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .contracts import ProductProofCheck, ProductProofReport

SAMPLE_ROOT = "samples/korean_drama_family_secret"


def validate_sample_project_contract(root: Path | None = None) -> dict[str, Any]:
    root = root or Path(__file__).resolve().parents[3]
    sample = root / SAMPLE_ROOT
    project_path = sample / "project.json"
    characters_path = sample / "characters.json"
    world_path = sample / "world.json"
    outline_path = sample / "plot_outline.md"
    scene_path = sample / "scene_requests/scene_001.json"
    project = _read_json(project_path)
    characters = _read_json(characters_path)
    world = _read_json(world_path)
    scene = _read_json(scene_path)
    outline = outline_path.read_text(encoding="utf-8") if outline_path.exists() else ""
    checks = [
        _check("project_file_present", project_path.exists(), "exists", "exists" if project_path.exists() else "missing", project_path),
        _check("project_is_synthetic", project.get("synthetic_only") is True, "synthetic_only=true", str(project.get("synthetic_only")), project_path),
        _check("project_provider_calls_disabled", project.get("provider_calls_allowed") is False, "provider_calls_allowed=false", str(project.get("provider_calls_allowed")), project_path),
        _check("characters_present", isinstance(characters.get("characters"), list) and len(characters.get("characters", [])) >= 3, "at least 3 characters", str(len(characters.get("characters", [])) if isinstance(characters.get("characters"), list) else 0), characters_path),
        _check("world_contract_present", bool(world.get("world_id")) and world.get("synthetic_only") is True, "synthetic synthetic world contract", json.dumps({"world_id": world.get("world_id"), "synthetic_only": world.get("synthetic_only")}, sort_keys=True), world_path),
        _check("plot_outline_public_safe", "synthetic" in outline.lower() and "private manuscript" not in outline.lower(), "synthetic public-safe outline", outline[:160], outline_path),
        _check("scene_request_present", bool(scene.get("scene_id")) and bool(scene.get("objective")), "scene_id and objective", json.dumps({"scene_id": scene.get("scene_id"), "objective": scene.get("objective")}, ensure_ascii=False, sort_keys=True), scene_path),
        _check("scene_request_provider_zero", scene.get("provider_calls_allowed") is False, "provider_calls_allowed=false", str(scene.get("provider_calls_allowed")), scene_path),
    ]
    issues = tuple(c.name for c in checks if c.status != "pass")
    return ProductProofReport(
        stage="stage140",
        title="Synthetic Sample Project Contract",
        status="pass" if not issues else "blocked",
        checks=tuple(checks),
        issues=issues,
        counters={"check_count": len(checks), "pass_count": sum(1 for c in checks if c.status == "pass"), "blocked_count": len(issues)},
    ).to_dict()


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}


def _check(name: str, condition: bool, expected: str, actual: str, path: Path) -> ProductProofCheck:
    return ProductProofCheck(name=name, status="pass" if condition else "blocked", expected=expected, actual=actual, path=path.as_posix())
