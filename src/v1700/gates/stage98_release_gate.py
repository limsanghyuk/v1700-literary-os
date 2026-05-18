from __future__ import annotations

import json
import re
import zipfile
from pathlib import Path

from v1700.gates.stage97_2_release_gate import run_stage97_2_release_gate
from v1700.stage98.orchestrator import run_stage98

_STAGE98_CACHE: dict[str, dict] = {}


def run_stage98_release_gate(root: Path | None = None) -> dict:
    root = root or Path(__file__).resolve().parents[3]
    cache_key = str(root.resolve())
    if cache_key in _STAGE98_CACHE:
        return _STAGE98_CACHE[cache_key]

    baseline = run_stage97_2_release_gate(root)
    workflow = run_stage98(root)
    pack = root / "release" / "current" / "stage98_studio_pack"
    stage98_0 = _read_json(root / "release" / "current" / "stage98_0_studio_workflow_core_report.json")
    stage98_1 = _read_json(root / "release" / "current" / "stage98_1_review_queue_report.json")
    stage98_2 = _read_json(root / "release" / "current" / "stage98_2_publishing_package_report.json")
    publishing_manifest = _read_json(pack / "publishing_package_manifest.json")
    branchpoint_summary = _branchpoint_survival_summary(root)
    checks = {
        "stage97_baseline_gate_pass": _check(baseline.get("checks", {}).get("stage97_1_baseline_gate", {}).get("checks", {}).get("stage97_baseline_gate", {}).get("status") == "pass" or baseline.get("status") == "pass"),
        "stage97_1_adversarial_gate_pass": _check(baseline.get("checks", {}).get("stage97_1_baseline_gate", {}).get("status") == "pass"),
        "stage97_2_provider_runtime_gate_pass": _check(baseline.get("status") == "pass"),
        "stage98_0_step_pass": _check(stage98_0.get("stage") == "98.0" and stage98_0.get("status") == "pass"),
        "stage98_1_step_pass": _check(stage98_1.get("baseline_stage") == "98.0" and stage98_1.get("status") == "pass"),
        "stage98_2_step_pass": _check(stage98_2.get("baseline_stage") == "98.1" and stage98_2.get("status") == "pass"),
        "stage98_step_sequence_pass": _check(workflow.get("stage_sequence") == ["98.0", "98.1", "98.2"]),
        "studio_project_contract_pass": _check(workflow.get("studio_project_status") == "pass"),
        "project_ingest_privacy_pass": _check(workflow.get("raw_manuscript_provider_leakage") == 0 and workflow.get("full_text_exported") is False),
        "episode_board_pass": _check(workflow.get("episode_board_status") == "pass"),
        "microplot_matrix_editor_pass": _check(workflow.get("microplot_matrix_editor_status") == "pass"),
        "payoff_dashboard_pass": _file_status(pack / "payoff_dashboard_report.json"),
        "agency_dashboard_pass": _file_status(pack / "agency_dashboard_report.json"),
        "dialogue_warning_panel_pass": _file_status(pack / "dialogue_warning_panel_report.json"),
        "voice_drift_monitor_pass": _file_status(pack / "voice_drift_monitor_report.json"),
        "attention_heatmap_pass": _file_status(pack / "attention_heatmap_report.json"),
        "revision_queue_pass": _check(workflow.get("revision_queue_status") == "pass"),
        "writer_approval_guard_pass": _check(workflow.get("writer_approval_guard_status") == "pass"),
        "publishing_package_manifest_pass": _check(publishing_manifest.get("status") == "pass"),
        "provider_zero_pass": _check(workflow.get("provider_call_count") == 0 and workflow.get("live_provider_call_count") == 0),
        "node2_boundary_pass": _check(workflow.get("node2_raw_reveal_access") == 0),
        "raw_manuscript_leakage_pass": _check(workflow.get("raw_manuscript_provider_leakage") == 0 and workflow.get("full_text_exported") is False),
        "branchpoint_survival_pass": _check(branchpoint_summary.get("status") == "pass"),
        "zip_path_separator_pass": _check(_zip_path_separator_status(root) == "pass"),
        "secret_scan_pass": _check(_secret_scan(root)["status"] == "pass"),
        "main_release_gate_integration_pass": _check(_main_gate_integrated(root)),
    }
    issues = [name for name, payload in checks.items() if payload["status"] != "pass"]
    if workflow.get("unresolved_block_items", 0) > 0 and publishing_manifest:
        issues.append("unresolved_block_items_with_publishing_package")

    result = {
        "status": "pass" if not issues else "blocked",
        "stage": "98",
        "baseline_stage": "97.2",
        "title": "Commercial Studio Workflow + Publishing Package",
        "checks": checks,
        "issues": issues,
        "stage97_2_release_gate": baseline,
        "stage98_0_studio_workflow_core": stage98_0,
        "stage98_1_review_queue": stage98_1,
        "stage98_2_publishing_package": stage98_2,
        "stage98_studio_workflow": workflow,
        "studio_project_status": workflow.get("studio_project_status"),
        "episode_board_status": workflow.get("episode_board_status"),
        "revision_queue_status": workflow.get("revision_queue_status"),
        "publishing_package_status": workflow.get("publishing_package_status"),
        "unresolved_block_items": workflow.get("unresolved_block_items", 0),
        "writer_approval_guard_status": workflow.get("writer_approval_guard_status"),
        "raw_manuscript_provider_leakage": workflow.get("raw_manuscript_provider_leakage", 0),
        "full_text_exported": workflow.get("full_text_exported", False),
        "provider_call_count": workflow.get("provider_call_count", 0),
        "live_provider_call_count": workflow.get("live_provider_call_count", 0),
        "provider_default_calls": workflow.get("provider_default_calls", 0),
        "node2_raw_reveal_access": workflow.get("node2_raw_reveal_access", 0),
        "reader_only_leakage": workflow.get("reader_only_leakage", 0),
        "internal_marker_leakage": workflow.get("internal_marker_leakage", 0),
        "branchpoint_survival_summary": branchpoint_summary,
        "main_release_gate_integration_status": checks["main_release_gate_integration_pass"]["status"],
        "zip_path_separator_status": checks["zip_path_separator_pass"]["status"],
        "secret_scan_status": checks["secret_scan_pass"]["status"],
    }
    _STAGE98_CACHE[cache_key] = result
    return result


def _check(condition: bool) -> dict:
    return {"status": "pass" if condition else "blocked"}


def _read_json(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def _file_status(path: Path) -> dict:
    payload = _read_json(path)
    return _check(payload.get("status") == "pass")


def _branchpoint_survival_summary(root: Path) -> dict:
    required = [
        root / "manifests" / "stage97_2_branchpoint_trace_manifest.json",
        root / "manifests" / "stage98_branchpoint_trace_manifest.json",
    ]
    return {
        "status": "pass" if all(path.exists() for path in required) else "blocked",
        "required_manifests": [str(path.relative_to(root)) for path in required],
    }


def _zip_path_separator_status(root: Path) -> str:
    package_dirs = [root.parent]
    if len(root.parents) > 1:
        package_dirs.append(root.parents[1] / "packages")
    for package_dir in package_dirs:
        if not package_dir.exists():
            continue
        for zip_path in package_dir.glob("*stage98*.zip"):
            with zipfile.ZipFile(zip_path) as zf:
                if any("\\" in name for name in zf.namelist()):
                    return "blocked"
    return "pass"


def _secret_scan(root: Path) -> dict:
    patterns = [
        re.compile(r"sk-[A-Za-z0-9]{20,}"),
        re.compile(r"AKIA[0-9A-Z]{16}"),
        re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    ]
    hits: list[str] = []
    for path in list((root / "src").rglob("*.py")) + list((root / "tools").rglob("*.py")) + list((root / "manifests").rglob("*.json")):
        text = path.read_text(encoding="utf-8", errors="ignore")
        if any(pattern.search(text) for pattern in patterns):
            hits.append(str(path.relative_to(root)))
    return {"status": "pass" if not hits else "blocked", "hits": hits}


def _main_gate_integrated(root: Path) -> bool:
    manifest = _read_json(root / "manifests" / "live_core_manifest.json")
    return manifest.get("active_version") in {"stage98", "stage99", "stage100", "stage101", "stage102", "stage103", "stage104", "stage105", "stage106", "stage107", "stage107_5", "stage108", "stage109", "stage110", "stage111", "stage112", "stage113", "stage114", "stage115", "stage116", "stage116", "stage117", "stage118", "stage119", "stage120", "stage121", "stage122", "stage123", "stage124", "stage125", "stage126", "stage127"} and "stage98_release_gate" in manifest.get("active_gates", [])
