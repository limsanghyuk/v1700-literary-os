from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from v1700.render_plan_builder import build_deterministic_render_plan

from .contracts import DryRunRenderTraceStep, SurfaceDraftUnit

FORBIDDEN_SURFACE_TOKENS = (
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

STORE_PATH = Path("samples/stage162_render_packet_store/render_packets.jsonl")


def build_surface_draft_dry_run(root: Path | None = None) -> dict[str, Any]:
    root = root or Path(__file__).resolve().parents[3]
    plan = build_deterministic_render_plan(root / STORE_PATH)
    issues: list[str] = []
    if plan.get("status") != "pass":
        issues.extend(f"render_plan:{issue}" for issue in plan.get("issues", []))
        return _blocked(issues, plan)

    units: list[SurfaceDraftUnit] = []
    for index, node in enumerate(plan.get("nodes", [])):
        draft_text = _deterministic_surface_text(node, index)
        checksum = _stable_checksum({"draft_text": draft_text, "node": node, "order_index": index})
        unit = SurfaceDraftUnit(
            draft_unit_id=f"surface_draft_unit_{node.get('render_packet_id')}",
            render_plan_node_id=str(node.get("node_id", "")),
            render_packet_id=str(node.get("render_packet_id", "")),
            render_type=str(node.get("render_type", "")),
            surface_channel=str(node.get("surface_channel", "")),
            project_id=str(node.get("project_id", "")),
            boundary_level=str(node.get("boundary_level", "")),
            visibility=str(node.get("visibility", "")),
            draft_text=draft_text,
            checksum=checksum,
            order_index=index,
            node2_projection_summary=_node2_summary(node, draft_text),
        )
        units.append(unit)

    traces = [
        DryRunRenderTraceStep(
            step_id=f"dry_run_render_step_{index:03d}",
            draft_unit_id=unit.draft_unit_id,
            action="compose_surface_draft_unit_without_provider_or_write",
            deterministic=True,
            provider_call_allowed=False,
            write_allowed=False,
            evidence="release/current/stage164_surface_draft_dry_run_renderer_report.json",
        )
        for index, unit in enumerate(units)
    ]

    unit_dicts = [unit.to_dict() for unit in units]
    trace_dicts = [step.to_dict() for step in traces]
    issues.extend(_surface_boundary_issues(unit_dicts))
    issues.extend(_trace_policy_issues(trace_dicts))
    canonical = {"units": unit_dicts, "trace": trace_dicts, "source_plan_checksum": plan.get("render_plan_checksum", "")}
    checksum = _stable_checksum(canonical)
    return {
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "source_render_plan_status": plan.get("status"),
        "source_render_plan_checksum": plan.get("render_plan_checksum", ""),
        "draft_unit_count": len(unit_dicts),
        "trace_step_count": len(trace_dicts),
        "surface_draft_checksum": checksum,
        "units": unit_dicts,
        "trace_steps": trace_dicts,
        "source_render_order": plan.get("render_order", []),
    }


def _deterministic_surface_text(node: dict[str, Any], index: int) -> str:
    render_type = str(node.get("render_type", "surface"))
    channel = str(node.get("surface_channel", "surface"))
    packet = str(node.get("render_packet_id", "packet"))
    summary = str(node.get("node2_projection_summary", "surface-safe draft"))
    return f"[{index:02d}|{channel}|{render_type}] {packet}: {summary}"


def _node2_summary(node: dict[str, Any], draft_text: str) -> str:
    return f"surface_draft_summary:{node.get('render_packet_id')}:{draft_text[:96]}"


def _surface_boundary_issues(units: list[dict[str, Any]]) -> list[str]:
    issues: list[str] = []
    for unit in units:
        if unit.get("boundary_level") != "NODE2_SURFACE_SAFE":
            issues.append(f"boundary_level_not_surface_safe:{unit.get('draft_unit_id')}")
        if unit.get("visibility") not in {"NODE2_SAFE", "SURFACE_ONLY", "surface_safe"}:
            issues.append(f"visibility_not_surface_only:{unit.get('draft_unit_id')}")
        surface = json.dumps({"draft_text": unit.get("draft_text", ""), "summary": unit.get("node2_projection_summary", "")}, ensure_ascii=False).lower()
        for token in FORBIDDEN_SURFACE_TOKENS:
            if token in surface:
                issues.append(f"forbidden_surface_token:{unit.get('draft_unit_id')}:{token}")
    return issues


def _trace_policy_issues(trace_steps: list[dict[str, Any]]) -> list[str]:
    issues: list[str] = []
    for step in trace_steps:
        if step.get("deterministic") is not True:
            issues.append(f"trace_not_deterministic:{step.get('step_id')}")
        if step.get("provider_call_allowed") is not False:
            issues.append(f"trace_provider_call_allowed:{step.get('step_id')}")
        if step.get("write_allowed") is not False:
            issues.append(f"trace_write_allowed:{step.get('step_id')}")
    return issues


def _stable_checksum(payload: dict[str, Any]) -> str:
    body = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(body.encode("utf-8")).hexdigest()


def _blocked(issues: list[str], plan: dict[str, Any]) -> dict[str, Any]:
    return {
        "status": "blocked",
        "issues": issues,
        "source_render_plan_status": plan.get("status"),
        "source_render_plan_checksum": plan.get("render_plan_checksum", ""),
        "draft_unit_count": 0,
        "trace_step_count": 0,
        "surface_draft_checksum": "",
        "units": [],
        "trace_steps": [],
        "source_render_order": [],
    }
