from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from v1700.surface_draft_dry_run_renderer.renderer import build_surface_draft_dry_run

FORBIDDEN_TOKENS = (
    "hidden_reveal_payload",
    "hidden_render_payload",
    "private_note",
    "provider handle",
    "provider_handle",
    "provider_payload",
    "provider_generation_payload",
    "write_handle",
    "canon_mutation_command",
    "learning_payload",
    "raw_manuscript_payload",
    "credential",
    "internal_trace_payload",
)


def analyze_render_quality_boundary(root: Path | None = None) -> dict[str, Any]:
    root = root or Path(__file__).resolve().parents[3]
    stage164 = build_surface_draft_dry_run(root)
    units = list(stage164.get("units", []))
    trace = list(stage164.get("trace_steps", []))
    issues: list[str] = []
    if stage164.get("status") != "pass":
        issues.extend(f"stage164:{issue}" for issue in stage164.get("issues", []))

    unit_count = len(units)
    trace_count = len(trace)
    draft_texts = [str(unit.get("draft_text", "")) for unit in units]
    words = [len(text.split()) for text in draft_texts]
    avg_words = sum(words) / unit_count if unit_count else 0.0
    min_words = min(words) if words else 0
    unique_checksums = len({str(unit.get("checksum", "")) for unit in units})
    render_types = {str(unit.get("render_type", "")) for unit in units}
    channels = {str(unit.get("surface_channel", "")) for unit in units}

    if unit_count == 0:
        issues.append("no_surface_draft_units")
    if trace_count != unit_count:
        issues.append("trace_unit_count_mismatch")
    if min_words < 3:
        issues.append("surface_draft_unit_too_short")
    if unique_checksums != unit_count:
        issues.append("surface_draft_checksum_not_unique")
    if len(render_types) < 3:
        issues.append("render_type_coverage_too_low")
    if not channels:
        issues.append("surface_channel_missing")

    order_values = [unit.get("order_index") for unit in units]
    if order_values != list(range(unit_count)):
        issues.append("surface_draft_order_not_stable")

    for unit in units:
        draft_unit_id = unit.get("draft_unit_id")
        if unit.get("boundary_level") != "NODE2_SURFACE_SAFE":
            issues.append(f"boundary_level_not_surface_safe:{draft_unit_id}")
        if unit.get("visibility") not in {"NODE2_SAFE", "SURFACE_ONLY", "surface_safe"}:
            issues.append(f"visibility_not_surface_only:{draft_unit_id}")
        surface = json.dumps({"draft_text": unit.get("draft_text", ""), "summary": unit.get("node2_projection_summary", "")}, ensure_ascii=False).lower()
        for token in FORBIDDEN_TOKENS:
            if token in surface:
                issues.append(f"forbidden_surface_token:{draft_unit_id}:{token}")

    for step in trace:
        if step.get("provider_call_allowed") is not False:
            issues.append(f"trace_provider_call_allowed:{step.get('step_id')}")
        if step.get("write_allowed") is not False:
            issues.append(f"trace_write_allowed:{step.get('step_id')}")
        if step.get("deterministic") is not True:
            issues.append(f"trace_not_deterministic:{step.get('step_id')}")

    quality_score = _quality_score(unit_count, trace_count, min_words, avg_words, unique_checksums, render_types, issues)
    canonical = {
        "unit_count": unit_count,
        "trace_count": trace_count,
        "avg_words": round(avg_words, 6),
        "min_words": min_words,
        "unique_checksums": unique_checksums,
        "render_types": sorted(render_types),
        "channels": sorted(channels),
        "source_surface_draft_checksum": stage164.get("surface_draft_checksum", ""),
        "quality_score": quality_score,
    }
    return {
        "status": "pass" if not issues and quality_score >= 0.92 else "blocked",
        "issues": issues if quality_score >= 0.92 else [*issues, "quality_score_below_threshold"],
        "unit_count": unit_count,
        "trace_count": trace_count,
        "avg_words_per_unit": round(avg_words, 6),
        "min_words_per_unit": min_words,
        "unique_draft_checksum_count": unique_checksums,
        "render_type_count": len(render_types),
        "surface_channel_count": len(channels),
        "quality_score": quality_score,
        "quality_threshold": 0.92,
        "render_types": sorted(render_types),
        "surface_channels": sorted(channels),
        "source_surface_draft_checksum": stage164.get("surface_draft_checksum", ""),
        "quality_boundary_checksum": _stable_checksum(canonical),
        "provider_default_calls": 0,
        "provider_generation_count": 0,
        "runtime_execution_count": 0,
        "write_operation_count": 0,
        "node2_raw_reveal_access": 0,
        "boundary_violation_count": 0,
    }


def _quality_score(unit_count: int, trace_count: int, min_words: int, avg_words: float, unique_checksums: int, render_types: set[str], issues: list[str]) -> float:
    score = 1.0
    if unit_count <= 0:
        score -= 0.4
    if trace_count != unit_count:
        score -= 0.2
    if min_words < 3:
        score -= 0.12
    if avg_words < 5:
        score -= 0.08
    if unique_checksums != unit_count:
        score -= 0.12
    if len(render_types) < 3:
        score -= 0.08
    score -= min(0.4, 0.03 * len(issues))
    return round(max(0.0, score), 6)


def _stable_checksum(payload: dict[str, Any]) -> str:
    body = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(body.encode("utf-8")).hexdigest()
