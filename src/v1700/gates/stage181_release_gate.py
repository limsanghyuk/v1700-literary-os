from __future__ import annotations
import json
from pathlib import Path
from typing import Any
from v1700.migration_plan_compiler import run_stage181_migration_plan_compiler
CORE_INVARIANTS={'provider_default_calls': 0, 'live_provider_call_count_in_release_gate': 0, 'provider_generation_count': 0, 'runtime_execution_count': 0, 'write_operation_count': 0, 'node2_raw_reveal_access': 0, 'boundary_violation_count': 0, 'credential_leakage': 0, 'provider_generation_enabled': False, 'provider_evaluation_enabled': False, 'evolution_write_enabled': False, 'memory_write_enabled': False, 'cross_project_write_enabled': False, 'canon_mutation_enabled': False, 'runtime_training_enabled': False, 'auto_repair_apply_enabled': False, 'automatic_promotion_enabled': False}

def run_stage181_release_gate(root: Path | None = None) -> dict[str, Any]:
    root = root or Path(__file__).resolve().parents[3]
    if _active_version(root) != "stage181":
        existing = root / "release/current/stage181_release_gate_report.json"
        if existing.exists():
            try: return json.loads(existing.read_text(encoding="utf-8"))
            except Exception: pass
    stage = run_stage181_migration_plan_compiler(root)
    checks = {
        "previous_stage_gate_pass": _check(_report_pass(root, "release/current/stage180_release_gate_report.json")),
        "stage181_migration_plan_compiler_pass": _check(stage.get("status") == "pass"),
        "preflight_execution_report_pass": _check(_report_pass(root, "release/current/stage181_preflight_execution_report.json")),
        "gitnexus_preflight_analysis_pass": _check(_gitnexus_analysis_ok(root)),
        "package_comparison_report_pass": _check(_report_pass(root, "release/current/stage181_package_comparison_report.json")),
        "provider_zero_pass": _check(stage.get("provider_default_calls") == 0 and stage.get("live_provider_call_count_in_release_gate") == 0),
        "write_zero_pass": _check(stage.get("write_operation_count") == 0 and stage.get("memory_write_enabled") is False and stage.get("cross_project_write_enabled") is False),
        "node2_boundary_pass": _check(stage.get("node2_raw_reveal_access") == 0),
        "training_mutation_disabled_pass": _check(stage.get("runtime_training_enabled") is False and stage.get("canon_mutation_enabled") is False and stage.get("auto_repair_apply_enabled") is False),
        "docs_manifest_pass": _check(_docs_manifest_ok(root)),
        "procedure_alignment_pass": _check(_procedure_alignment_ok(root)),
    }
    issues=[name for name, check in checks.items() if check["status"] != "pass"]
    result={"stage":"181","baseline_stage":"180","title":"Migration Plan Compiler","status":"pass" if not issues else "blocked","issues":issues,"checks":checks,"default_evolution_decision":"DEFER", **CORE_INVARIANTS, "branchpoint_lineage_preserved": not issues}
    out=root/"release/current/stage181_release_gate_report.json"; out.parent.mkdir(parents=True, exist_ok=True); out.write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True)+"\n", encoding="utf-8")
    return result

def _check(condition: bool) -> dict[str,str]: return {"status":"pass" if condition else "blocked"}
def _report_pass(root: Path, rel: str) -> bool:
    path=root/rel
    if not path.exists(): return False
    try: data=json.loads(path.read_text(encoding="utf-8"))
    except Exception: return False
    return data.get("status") == "pass"
def _gitnexus_analysis_ok(root: Path) -> bool:
    path=root/"release/current/stage181_gitnexus_preflight_analysis_report.json"
    if not path.exists(): return False
    try: data=json.loads(path.read_text(encoding="utf-8"))
    except Exception: return False
    return data.get("status")=="pass" and data.get("seven_key_perspectives_count")==7 and data.get("twelve_design_development_items_count")==12 and data.get("runtime") in {"gitnexus","python_fallback"} and all(x.get("status")=="pass" for x in data.get("seven_key_perspectives", [])) and all(x.get("status")=="pass" for x in data.get("twelve_design_development_items", []))
def _docs_manifest_ok(root: Path) -> bool:
    expected=["docs/stages/stage181.md","docs/proposals/stage181_migration_plan_compiler_proposal.md","docs/architecture/stage181_migration_plan_compiler_blueprint.md","docs/development/stage181_developer_handoff.md","manifests/stage181_manifest.json","manifests/stage181_migration_plan_compiler_manifest.json","manifests/stage181_branchpoint_trace_manifest.json","manifests/live_core_stage181_overlay.json","release/current/stage181_release_asset_manifest.json","release/current/stage181_migration_plan_compiler_report.json","release/current/stage181_release_gate_report.json","release/current/stage181_preflight_execution_report.json","release/current/stage181_gitnexus_preflight_analysis_report.json","release/current/stage181_package_comparison_report.json"]
    return all((root/rel).exists() for rel in expected)
def _procedure_alignment_ok(root: Path) -> bool:
    text="\n".join((root/p).read_text(encoding="utf-8") for p in ["README.md","RELEASE_NOTES.md","package_manifest.json","docs/stages/stage181.md","docs/development/stage181_developer_handoff.md"] if (root/p).exists())
    return all(token in text for token in ["stage181", "run_stage181_migration_plan_compiler.py", "run_stage181_release_gate.py"])
def _active_version(root: Path) -> str:
    path=root/"manifests/live_core_manifest.json"
    if not path.exists(): return ""
    try: return json.loads(path.read_text(encoding="utf-8")).get("active_version", "")
    except Exception: return ""
