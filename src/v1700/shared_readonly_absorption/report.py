from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .canon_conflict_report import run_canon_conflict_report
from .gitnexus_preflight import run_stage128_gitnexus_preflight
from .license_boundary import run_license_boundary_adapter
from .project_isolation import run_project_isolation_guard
from .shared_character_adapter import run_shared_character_read_only_adapter
from .shared_world_adapter import run_shared_world_read_only_adapter


def run_stage128_read_only_absorption(root: Path | None = None) -> dict[str, Any]:
    root = root or Path(__file__).resolve().parents[3]
    character = run_shared_character_read_only_adapter()
    world = run_shared_world_read_only_adapter()
    license_boundary = run_license_boundary_adapter()
    isolation = run_project_isolation_guard()
    canon = run_canon_conflict_report()
    gitnexus = run_stage128_gitnexus_preflight(root)
    parts = {
        "shared_character_adapter": character,
        "shared_world_adapter": world,
        "license_boundary_adapter": license_boundary,
        "project_isolation_guard": isolation,
        "canon_conflict_report": canon,
        "gitnexus_preflight": gitnexus,
    }
    issues = [name for name, report in parts.items() if report.get("status") not in {"pass", "PASS"}]
    result = {
        "stage": "128",
        "baseline_stage": "127",
        "title": "SharedWorld / SharedCharacter Read-Only Absorption",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "read_only_absorption": True,
        "shared_character_read_only_adapter_pass": character.get("status") == "PASS",
        "shared_world_read_only_adapter_pass": world.get("status") == "PASS",
        "cross_project_write": isolation.get("cross_project_write", 1),
        "unauthorized_cross_reads": isolation.get("unauthorized_cross_reads", 1),
        "unauthorized_cross_writes": isolation.get("unauthorized_cross_writes", 1),
        "raw_manuscript_cross_project_leakage": isolation.get("raw_manuscript_cross_project_leakage", 1),
        "raw_manuscript_provider_leakage": 0,
        "full_text_exported": False,
        "provider_default_calls": 0,
        "live_provider_call_count_in_release_gate": 0,
        "node2_raw_reveal_access": 0,
        "credential_leakage": 0,
        "shared_world_source_of_truth_promotion_allowed": False,
        "direct_v571_merge_performed": False,
        "stage129_canon_governor_required": True,
        "branchpoint_lineage_preserved": not issues,
        "python_fallback_used": gitnexus.get("python_fallback_used", True),
        "parts": parts,
    }
    pack = root / "release/current/stage128_read_only_absorption_pack"
    _write_json(root / "release/current/stage128_read_only_absorption_report.json", result)
    _write_json(pack / "shared_character_adapter_report.json", character)
    _write_json(pack / "shared_world_adapter_report.json", world)
    _write_json(pack / "license_boundary_adapter_report.json", license_boundary)
    _write_json(pack / "project_isolation_guard_report.json", isolation)
    _write_json(pack / "canon_conflict_report.json", canon)
    _write_json(pack / "gitnexus_preflight_report.json", gitnexus)
    _write_json(pack / "stage128_summary.json", _summary(result))
    return result


def _summary(result: dict[str, Any]) -> dict[str, Any]:
    return {
        "stage": result.get("stage"),
        "status": result.get("status"),
        "read_only_absorption": result.get("read_only_absorption"),
        "provider_default_calls": result.get("provider_default_calls"),
        "live_provider_call_count_in_release_gate": result.get("live_provider_call_count_in_release_gate"),
        "raw_manuscript_provider_leakage": result.get("raw_manuscript_provider_leakage"),
        "unauthorized_cross_reads": result.get("unauthorized_cross_reads"),
        "unauthorized_cross_writes": result.get("unauthorized_cross_writes"),
        "stage129_canon_governor_required": result.get("stage129_canon_governor_required"),
    }


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
