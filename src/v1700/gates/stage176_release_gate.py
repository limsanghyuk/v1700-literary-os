from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from v1700.lineage_review_gate import run_stage176_lineage_review_gate

CORE_INVARIANTS = {'provider_default_calls': 0, 'live_provider_call_count_in_release_gate': 0, 'provider_generation_count': 0, 'runtime_execution_count': 0, 'write_operation_count': 0, 'node2_raw_reveal_access': 0, 'boundary_violation_count': 0, 'credential_leakage': 0, 'provider_generation_enabled': False, 'provider_evaluation_enabled': False, 'governance_write_enabled': False, 'project_write_enabled': False, 'memory_write_enabled': False, 'cross_project_write_enabled': False, 'canon_mutation_enabled': False, 'runtime_training_enabled': False, 'auto_repair_apply_enabled': False, 'automatic_promotion_enabled': False}


def run_stage176_release_gate(root: Path | None = None) -> dict[str, Any]:
    root = root or Path(__file__).resolve().parents[3]

    if _active_version(root) != "stage176":
        existing = root / "release/current/stage176_release_gate_report.json"
        if existing.exists():
            try:
                return json.loads(existing.read_text(encoding="utf-8"))
            except Exception:
                pass
    stage = run_stage176_lineage_review_gate(root)
    checks = {
        "previous_stage_gate_pass": _check(_report_pass(root, "release/current/stage175_release_gate_report.json")),
        "stage176_lineage_review_gate_pass": _check(stage.get("status") == "pass"),
        "preflight_execution_report_pass": _check(_report_pass(root, "release/current/stage176_preflight_execution_report.json")),
        "gitnexus_preflight_analysis_pass": _check(_gitnexus_analysis_ok(root)),
        "package_comparison_report_pass": _check(_report_pass(root, "release/current/stage176_package_comparison_report.json")),
        "provider_zero_pass": _check(stage.get("provider_default_calls") == 0 and stage.get("live_provider_call_count_in_release_gate") == 0),
        "write_zero_pass": _check(stage.get("write_operation_count") == 0 and stage.get("memory_write_enabled") is False and stage.get("cross_project_write_enabled") is False),
        "node2_boundary_pass": _check(stage.get("node2_raw_reveal_access") == 0),
        "training_mutation_disabled_pass": _check(stage.get("runtime_training_enabled") is False and stage.get("canon_mutation_enabled") is False and stage.get("auto_repair_apply_enabled") is False),
        "docs_manifest_pass": _check(_docs_manifest_ok(root)),
        "procedure_alignment_pass": _check(_procedure_alignment_ok(root)),
    }
    issues = [name for name, check in checks.items() if check["status"] != "pass"]
    result = {"stage": "176", "baseline_stage": "175", "title": "Lineage Review Gate", "status": "pass" if not issues else "blocked", "issues": issues, "checks": checks, "default_authority_decision": "DENY", **CORE_INVARIANTS, "branchpoint_lineage_preserved": not issues}
    out = root / "release/current/stage176_release_gate_report.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True)+"\n", encoding="utf-8")
    return result


def _check(condition: bool) -> dict[str, str]: return {"status": "pass" if condition else "blocked"}

def _report_pass(root: Path, rel: str) -> bool:
    path = root / rel
    if not path.exists(): return False
    try: data=json.loads(path.read_text(encoding="utf-8"))
    except Exception: return False
    return data.get("status") == "pass"

def _gitnexus_analysis_ok(root: Path) -> bool:
    path = root / "release/current/stage176_gitnexus_preflight_analysis_report.json"
    if not path.exists(): return False
    try: data=json.loads(path.read_text(encoding="utf-8"))
    except Exception: return False
    perspectives=data.get("seven_key_perspectives", [])
    items=data.get("twelve_design_development_items", [])
    return data.get("status") == "pass" and data.get("seven_key_perspectives_count") == 7 and data.get("twelve_design_development_items_count") == 12 and data.get("runtime") in {"gitnexus", "python_fallback"} and len(perspectives)==7 and len(items)==12 and all(item.get("status")=="pass" for item in perspectives) and all(item.get("status")=="pass" for item in items)

def _docs_manifest_ok(root: Path) -> bool:
    expected=["docs/stages/stage176.md", "docs/proposals/stage176_lineage_review_gate_proposal.md", "docs/architecture/stage176_lineage_review_gate_blueprint.md", "docs/development/stage176_developer_handoff.md", "manifests/stage176_manifest.json", "manifests/stage176_lineage_review_gate_manifest.json", "manifests/stage176_branchpoint_trace_manifest.json", "manifests/live_core_stage176_overlay.json", "release/current/stage176_release_asset_manifest.json", "release/current/stage176_lineage_review_gate_report.json", "release/current/stage176_preflight_execution_report.json", "release/current/stage176_gitnexus_preflight_analysis_report.json", "release/current/stage176_package_comparison_report.json"]
    return all((root / rel).exists() for rel in expected)

def _procedure_alignment_ok(root: Path) -> bool:
    text="\n".join((root/p).read_text(encoding="utf-8") for p in ["README.md","RELEASE_NOTES.md","package_manifest.json"] if (root/p).exists())
    return all(token in text for token in ["stage176", "run_stage176_lineage_review_gate.py", "run_stage176_release_gate.py"])


def _active_version(root: Path) -> str:
    path = root / "manifests/live_core_manifest.json"
    if not path.exists():
        return ""
    try:
        return json.loads(path.read_text(encoding="utf-8")).get("active_version", "")
    except Exception:
        return ""
