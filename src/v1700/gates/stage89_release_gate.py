from __future__ import annotations

from pathlib import Path

from v1700.gates.stage88_release_gate import run_stage88_release_gate
from v1700.gates.symbol_to_branchpoint_trace_gate import run_symbol_to_branchpoint_trace_gate
from v1700.writer_studio.export_pipeline import run_stage89_export_pipeline_smoke
from v1700.writer_studio.workspace import run_writer_studio_smoke


def _project_root() -> Path:
    return Path(__file__).resolve().parents[3]


_STAGE89_CACHE: dict[str, dict] = {}


def run_stage89_release_gate(root: Path | None = None) -> dict:
    root = root or _project_root()
    cache_key = str(root.resolve())
    if cache_key in _STAGE89_CACHE:
        return _STAGE89_CACHE[cache_key]
    stage88 = run_stage88_release_gate(root)
    studio = run_writer_studio_smoke()
    export_pipeline = run_stage89_export_pipeline_smoke()
    trace_gate = run_symbol_to_branchpoint_trace_gate(root)
    checks = {
        "stage88_release_gate": stage88,
        "writer_studio_smoke": studio,
        "export_pipeline_smoke": export_pipeline,
        "symbol_to_branchpoint_trace_gate": trace_gate,
    }
    issues = [name for name, report in checks.items() if report.get("status") != "pass"]
    required_panels = {
        "story_bible",
        "episode_board",
        "scene_card_board",
        "character_knowledge_board",
        "reveal_budget_board",
        "agent_benchmark_panel",
        "branchpoint_impact_panel",
        "export_pipeline_panel",
    }
    if not required_panels.issubset(set(studio.get("panel_ids", []))):
        issues.append("writer_studio_required_panels_missing")
    if export_pipeline.get("artifact_count", 0) < 5:
        issues.append("stage89_export_artifact_count_below_5")
    required_formats = {"markdown", "json", "html", "platform_serialization_pack", "scene_csv"}
    if not required_formats.issubset(set(export_pipeline.get("formats", []))):
        issues.append("stage89_required_export_formats_missing")
    if studio.get("provider_default_calls") != 0 or export_pipeline.get("provider_default_calls") != 0:
        issues.append("provider_default_calls_not_zero")
    if studio.get("node2_raw_reveal_access_count") != 0 or export_pipeline.get("node2_raw_reveal_access_count") != 0:
        issues.append("node2_raw_reveal_access_not_zero")
    result = {
        "stage": "89",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "claim": "Stage89 adds a writer-facing Studio UI data model and deterministic export pipeline on top of the Stage88 AI-agent benchmark.",
        "checks": checks,
        "provider_default_calls": 0,
        "node2_raw_reveal_access_count": 0,
    }
    _STAGE89_CACHE[cache_key] = result
    return result
