from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .contracts import ProductProofCheck, ProductProofReport

BENCHMARK_ROOT = "benchmarks/longform_output"


def validate_longform_benchmark_contract(root: Path | None = None) -> dict[str, Any]:
    root = root or Path(__file__).resolve().parents[3]
    benchmark = root / BENCHMARK_ROOT
    readme_path = benchmark / "README.md"
    metrics_path = benchmark / "expected_metrics.json"
    results_keep = benchmark / "results/.gitkeep"
    readme = readme_path.read_text(encoding="utf-8") if readme_path.exists() else ""
    metrics = _read_json(metrics_path)
    checks = [
        _check("benchmark_readme_present", readme_path.exists(), "exists", "exists" if readme_path.exists() else "missing", readme_path),
        _check("benchmark_declares_stage141_path", "Stage141" in readme and "prose-generation E2E" in readme, "README declares Stage141 prose-generation E2E path", readme[:160], readme_path),
        _check("expected_metrics_present", metrics_path.exists(), "exists", "exists" if metrics_path.exists() else "missing", metrics_path),
        _check("expected_metrics_synthetic_only", metrics.get("synthetic_only") is True, "synthetic_only=true", str(metrics.get("synthetic_only")), metrics_path),
        _check("expected_metrics_provider_zero", metrics.get("provider_calls_allowed") is False, "provider_calls_allowed=false", str(metrics.get("provider_calls_allowed")), metrics_path),
        _check("expected_metrics_min_scene_count", int(metrics.get("min_scene_count", 0)) >= 1, "min_scene_count >= 1", str(metrics.get("min_scene_count", 0)), metrics_path),
        _check("results_directory_tracked", results_keep.exists(), "results/.gitkeep exists", "exists" if results_keep.exists() else "missing", results_keep),
    ]
    issues = tuple(c.name for c in checks if c.status != "pass")
    return ProductProofReport(
        stage="stage140",
        title="Longform Benchmark Skeleton Contract",
        status="pass" if not issues else "blocked",
        checks=tuple(checks),
        issues=issues,
        counters={"check_count": len(checks), "pass_count": sum(1 for c in checks if c.status == "pass"), "blocked_count": len(issues)},
    ).to_dict()


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}


def _check(name: str, condition: bool, expected: str, actual: str, path: Path) -> ProductProofCheck:
    return ProductProofCheck(name=name, status="pass" if condition else "blocked", expected=expected, actual=actual, path=path.as_posix())
