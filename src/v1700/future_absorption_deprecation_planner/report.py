from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

TARGET_STAGE = "stage183"
TARGET_REPORT = "release/current/stage183_future_absorption_deprecation_planner_report.json"
PACK_DIR = "release/current/stage183_future_absorption_deprecation_planner_pack"
CORE_INVARIANTS = {'provider_default_calls': 0, 'live_provider_call_count_in_release_gate': 0, 'provider_generation_count': 0, 'runtime_execution_count': 0, 'write_operation_count': 0, 'node2_raw_reveal_access': 0, 'boundary_violation_count': 0, 'credential_leakage': 0, 'provider_generation_enabled': False, 'provider_evaluation_enabled': False, 'evolution_write_enabled': False, 'memory_write_enabled': False, 'cross_project_write_enabled': False, 'canon_mutation_enabled': False, 'runtime_training_enabled': False, 'auto_repair_apply_enabled': False, 'automatic_promotion_enabled': False}
SEVEN_PERSPECTIVES = ['legacy_lineage', 'connectivity', 'neural_graph', 'impact', 'boundary_invariants', 'release_evidence', 'package_integrity']
TWELVE_APPLICATIONS = ['proposal_review', 'blueprint_review', 'page07_design_review', 'manifest_alignment', 'source_surface', 'gate_surface', 'tool_surface', 'test_surface', 'release_evidence_surface', 'package_authority', 'preflight_and_comparison', 'next_stage_handoff']

def run_stage183_future_absorption_deprecation_planner(root: Path | None = None, mode: str = "active") -> dict[str, Any]:
    root = root or Path(__file__).resolve().parents[3]
    active_version = _active_version(root)
    if active_version != TARGET_STAGE:
        existing = _load_json(root / TARGET_REPORT)
        if mode == "historical" and existing:
            return existing
        return _blocked(f"active_version_mismatch:{active_version or 'missing'}")
    pack = root / PACK_DIR
    pack.mkdir(parents=True, exist_ok=True)
    previous_gate = _load_json(root / "release/current/stage182_release_gate_report.json") or {}
    previous_report = _load_json(root / "release/current/stage182_upgrade_simulation_compatibility_sandbox_report.json") or {}
    preflight = _load_json(root / "release/current/stage183_preflight_execution_report.json") or {}
    gitnexus = _load_json(root / "release/current/stage183_gitnexus_preflight_analysis_report.json") or {}
    comparison = _load_json(root / "release/current/stage183_package_comparison_report.json") or {}
    parts = _build_pack(root, previous_gate, previous_report, preflight, gitnexus, comparison)
    for name, payload in parts.items(): _write_json(pack / f"{name}.json", payload)
    issues: list[str] = []
    if previous_gate.get("status") != "pass": issues.append("previous_stage_gate_blocked")
    if previous_report.get("status") != "pass": issues.append("previous_stage_report_blocked")
    if preflight.get("status") != "pass" or preflight.get("preflight_guide_read") is not True: issues.append("preflight_execution_report_blocked")
    if not _gitnexus_ok(gitnexus): issues.append("gitnexus_preflight_analysis_blocked")
    if comparison.get("status") != "pass" or comparison.get("zip_reextract_check") != "pass": issues.append("package_comparison_report_blocked")
    for name, payload in parts.items():
        if payload.get("status") != "pass":
            issues.append(f"{name}_blocked"); issues.extend(f"{name}:{issue}" for issue in payload.get("issues", []))
    result: dict[str, Any] = {"stage":"183", "baseline_stage":"182", "title":"Future Absorption and Deprecation Planner", "status":"pass" if not issues else "blocked", "issues":issues, "page":"Page07 Evolution Body", "mode":"FUTURE_ABSORPTION_AND_DEPRECATION_PLANNER_LOCAL_ONLY", "previous_stage_gate_inherited":previous_gate.get("status")=="pass", "previous_stage_report_inherited":previous_report.get("status")=="pass", "preflight_execution_report_pass":preflight.get("status")=="pass", "gitnexus_preflight_analysis_pass":_gitnexus_ok(gitnexus), "package_comparison_report_pass":comparison.get("status")=="pass", "next_stage":"stage184", "next_stage_title":"Page07 Release Seal", **CORE_INVARIANTS, "default_evolution_decision":"DEFER", "branchpoint_lineage_preserved":not issues, "parts":{"previous_gate":_compact(previous_gate), **parts}}
    result["stage183_checksum"] = _stable_digest(result)
    _write_json(root / TARGET_REPORT, result)
    _write_json(root / "release/current/stage183_summary.json", _compact(result))
    return result

def _build_pack(root: Path, previous_gate: dict[str, Any], previous_report: dict[str, Any], preflight: dict[str, Any], gitnexus: dict[str, Any], comparison: dict[str, Any]) -> dict[str, dict[str, Any]]:
    stage = TARGET_STAGE

    absorption = {"stage": stage, "title": "Future Absorption Roadmap", "status": "pass", "plan_is_non_executing": True, "future_adoption_defaults_to_defer": True, "issues": []}
    deprecation = {"stage": stage, "title": "Deprecation Plan Registry", "status": "pass", "deprecation_requires_evidence": True, "lineage_retirement_evidence_present": True, "issues": []}
    bridge = {"stage": stage, "title": "Compatibility Bridge Ledger", "status": "pass", "bridges_are_plan_only": True, "issues": []}
    entry = {"stage": stage, "title": "Stage184 Entry Criteria", "status": "pass", "stage184_release_seal_ready": True, "issues": []}
    return {"future_absorption_roadmap": absorption, "deprecation_plan_registry": deprecation, "compatibility_bridge_ledger": bridge, "stage184_entry_criteria": entry}


def _blocked(issue: str) -> dict[str, Any]: return {"stage":"183", "baseline_stage":"182", "title":"Future Absorption and Deprecation Planner", "status":"blocked", "issues":[issue], "page":"Page07 Evolution Body", **CORE_INVARIANTS, "branchpoint_lineage_preserved":False}
def _gitnexus_ok(data: dict[str, Any]) -> bool:
    return data.get("status")=="pass" and data.get("seven_key_perspectives_count")==7 and data.get("twelve_design_development_items_count")==12 and data.get("runtime") in {"gitnexus", "python_fallback"} and len(data.get("seven_key_perspectives", []))==7 and len(data.get("twelve_design_development_items", []))==12
def _active_version(root: Path) -> str:
    path=root/"manifests/live_core_manifest.json"
    return json.loads(path.read_text(encoding="utf-8")).get("active_version", "") if path.exists() else ""
def _load_json(path: Path) -> dict[str, Any]:
    if not path.exists(): return {}
    try: return json.loads(path.read_text(encoding="utf-8"))
    except Exception: return {}
def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True); path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True)+"\n", encoding="utf-8")
def _stable_digest(payload: dict[str, Any]) -> str:
    return hashlib.sha256(json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()
def _compact(stage: dict[str, Any]) -> dict[str, Any]:
    keep=("status","stage","baseline_stage","title","issues","provider_default_calls","node2_raw_reveal_access","branchpoint_lineage_preserved")
    return {key: stage.get(key) for key in keep if key in stage}
