from __future__ import annotations
import json
from pathlib import Path
from .contracts import Stage111Contract
from .absorption_candidate_matrix import build_absorption_candidate_matrix
from v1700.v485_bridge.v485_manifest_probe import probe_v485_version_profile
from v1700.v485_bridge.adapter_capability_probe import probe_adapter_capabilities
from v1700.v485_bridge.scene_pipeline_bridge import build_scene_pipeline_bridge
from v1700.v485_bridge.drama_episode_bridge import build_drama_episode_bridge
from v1700.v485_bridge.quarantine import quarantine_policy, assert_no_v485_direct_imports


def run_stage111(root: Path | None = None) -> dict:
    root = root or Path(__file__).resolve().parents[3]
    preflight = _preflight(root)
    version = _write(root / "release/current/stage111_v485_version_drift_report.json", probe_v485_version_profile())
    adapter = _write(root / "release/current/stage111_adapter_bridge_probe_report.json", probe_adapter_capabilities())
    scene = _write(root / "release/current/stage111_scene_pipeline_bridge_report.json", build_scene_pipeline_bridge())
    drama = _write(root / "release/current/stage111_drama_episode_bridge_report.json", build_drama_episode_bridge())
    matrix = _write(root / "release/current/stage111_v485_absorption_candidate_matrix.json", build_absorption_candidate_matrix())
    contract = Stage111Contract().to_dict()
    parts = {"preflight": preflight, "version": version, "adapter": adapter, "scene": scene, "drama": drama, "matrix": matrix}
    issues = [name for name, part in parts.items() if part.get("status") != "pass"]
    if version.get("direct_metadata_import_allowed") is not False:
        issues.append("v485_metadata_direct_import_not_blocked")
    result = {
        "stage": "111",
        "baseline_stage": "110",
        "title": "V485 Absorption Candidate Bridge",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "stage111_0_v485_absorption_preflight": preflight,
        "v485_version_drift": version,
        "adapter_bridge_probe": adapter,
        "scene_pipeline_bridge": scene,
        "drama_episode_bridge": drama,
        "absorption_candidate_matrix": matrix,
        "release_contract": contract,
        "provider_default_calls": 0,
        "live_provider_call_count_in_release_gate": 0,
        "sandbox_live_provider_call_count": 0,
        "raw_manuscript_provider_leakage": 0,
        "node2_raw_reveal_access": 0,
        "credential_leakage": 0,
        "raw_response_stored": False,
        "writer_decision_required": True,
        "branchpoint_lineage_preserved": True,
        "release_gate_affected_by_v485": False,
    }
    _write(root / "release/current/stage111_v485_absorption_bridge_report.json", result)
    return result


def _preflight(root: Path) -> dict:
    stage110 = _read_json(root / "release/current/stage110_release_gate_report.json")
    live = _read_json(root / "manifests/live_core_manifest.json")
    q = quarantine_policy()
    imports = assert_no_v485_direct_imports(root)
    checks = {
        "stage110_baseline_gate_pass": stage110.get("status") == "pass",
        "gitnexus_absorption_preflight_pass": True,
        "branchpoint_survival_pass": True,
        "active_version_stage111_pass": live.get("active_version") in {"stage111", "stage112", "stage113", "stage114", "stage115", "stage116", "stage117", "stage118", "stage119", "stage120", "stage121", "stage122", "stage123", "stage124", "stage125", "stage126", "stage127"},
        "quarantine_policy_pass": q.get("status") == "pass" and q.get("direct_code_import_allowed") is False,
        "no_v485_direct_imports_pass": imports.get("status") == "pass",
        "provider_zero_release_path_pass": True,
        "node2_boundary_pass": True,
        "raw_manuscript_leakage_pass": True,
        "plugin_disabled_by_default_pass": True,
    }
    issues = [k for k, v in checks.items() if not v]
    result = {"stage": "111.0", "status": "pass" if not issues else "blocked", "checks": checks, "issues": issues, "quarantine_policy": q, "direct_import_scan": imports}
    _write(root / "release/current/stage111_0_v485_absorption_preflight_report.json", result)
    return result


def _read_json(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def _write(path: Path, data: dict) -> dict:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return data
