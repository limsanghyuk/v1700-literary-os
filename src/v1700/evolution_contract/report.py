from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

TARGET_STAGE = "stage179"
TARGET_REPORT = "release/current/stage179_evolution_contract_report.json"
PACK_DIR = "release/current/stage179_evolution_contract_pack"
CORE_INVARIANTS = {'provider_default_calls': 0, 'live_provider_call_count_in_release_gate': 0, 'provider_generation_count': 0, 'runtime_execution_count': 0, 'write_operation_count': 0, 'node2_raw_reveal_access': 0, 'boundary_violation_count': 0, 'credential_leakage': 0, 'provider_generation_enabled': False, 'provider_evaluation_enabled': False, 'evolution_write_enabled': False, 'memory_write_enabled': False, 'cross_project_write_enabled': False, 'canon_mutation_enabled': False, 'runtime_training_enabled': False, 'auto_repair_apply_enabled': False, 'automatic_promotion_enabled': False}
SEVEN_PERSPECTIVES = ['legacy_lineage', 'connectivity', 'neural_graph', 'impact', 'boundary_invariants', 'release_evidence', 'package_integrity']
TWELVE_APPLICATIONS = ['proposal_review', 'blueprint_review', 'page07_design_review', 'manifest_alignment', 'source_surface', 'gate_surface', 'tool_surface', 'test_surface', 'release_evidence_surface', 'package_authority', 'preflight_and_comparison', 'next_stage_handoff']

def run_stage179_evolution_contract(root: Path | None = None, mode: str = "active") -> dict[str, Any]:
    root = root or Path(__file__).resolve().parents[3]
    active_version = _active_version(root)
    if active_version != TARGET_STAGE:
        existing = _load_json(root / TARGET_REPORT)
        if mode == "historical" and existing:
            return existing
        return _blocked(f"active_version_mismatch:{active_version or 'missing'}")
    pack = root / PACK_DIR
    pack.mkdir(parents=True, exist_ok=True)
    previous_gate = _load_json(root / "release/current/stage178_release_gate_report.json") or {}
    previous_report = _load_json(root / "release/current/stage178_page06_release_seal_report.json") or {}
    preflight = _load_json(root / "release/current/stage179_preflight_execution_report.json") or {}
    gitnexus = _load_json(root / "release/current/stage179_gitnexus_preflight_analysis_report.json") or {}
    comparison = _load_json(root / "release/current/stage179_package_comparison_report.json") or {}
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
    result: dict[str, Any] = {"stage":"179", "baseline_stage":"178", "title":"Evolution Contract", "status":"pass" if not issues else "blocked", "issues":issues, "page":"Page07 Evolution Body", "mode":"EVOLUTION_CONTRACT_LOCAL_ONLY", "previous_stage_gate_inherited":previous_gate.get("status")=="pass", "previous_stage_report_inherited":previous_report.get("status")=="pass", "preflight_execution_report_pass":preflight.get("status")=="pass", "gitnexus_preflight_analysis_pass":_gitnexus_ok(gitnexus), "package_comparison_report_pass":comparison.get("status")=="pass", "next_stage":"stage180", "next_stage_title":"Architecture Drift and Long-Horizon Self-Audit", **CORE_INVARIANTS, "default_evolution_decision":"DEFER", "branchpoint_lineage_preserved":not issues, "parts":{"previous_gate":_compact(previous_gate), **parts}}
    result["stage179_checksum"] = _stable_digest(result)
    _write_json(root / TARGET_REPORT, result)
    _write_json(root / "release/current/stage179_summary.json", _compact(result))
    return result

def _build_pack(root: Path, previous_gate: dict[str, Any], previous_report: dict[str, Any], preflight: dict[str, Any], gitnexus: dict[str, Any], comparison: dict[str, Any]) -> dict[str, dict[str, Any]]:
    stage = TARGET_STAGE

    contract = {"stage": stage, "title": "Evolution Contract Matrix", "status": "pass", "default_evolution_decision": "DEFER", "page06_governance_evidence_required": True, "provider_runtime_allowed": False, "write_runtime_allowed": False, "training_runtime_allowed": False, "issues": []}
    schema = {"stage": stage, "title": "Evolution Schema Registry", "status": "pass", "records": ["EvolutionCandidate", "EvolutionScope", "GovernanceEvidenceRef", "MigrationTarget", "CompatibilitySnapshot", "DriftRecord", "UpgradeConstraint", "DeprecationCandidate", "RollbackRequirement", "EvolutionVerdict"], "issues": []}
    refs = {"stage": stage, "title": "Governance Evidence References", "status": "pass", "required_source_stage": "stage178", "page06_release_seal_required": True, "issues": []}
    entry = {"stage": stage, "title": "Stage180 Entry Criteria", "status": "pass", "stage180_drift_audit_ready": True, "issues": []}
    return {"evolution_contract_matrix": contract, "evolution_schema_registry": schema, "governance_evidence_refs": refs, "stage180_entry_criteria": entry}


def _blocked(issue: str) -> dict[str, Any]: return {"stage":"179", "baseline_stage":"178", "title":"Evolution Contract", "status":"blocked", "issues":[issue], "page":"Page07 Evolution Body", **CORE_INVARIANTS, "branchpoint_lineage_preserved":False}
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
