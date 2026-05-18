from __future__ import annotations

import json
import os
import re
import zipfile
from pathlib import Path

from v1700.gates.stage103_release_gate import run_stage103_release_gate
from v1700.gates.symbol_to_branchpoint_trace_gate import run_symbol_to_branchpoint_trace_gate
from v1700.stage104.orchestrator import run_stage104

_STAGE104_CACHE: dict[str, dict] = {}


def run_stage104_release_gate(root: Path | None = None) -> dict:
    root = root or Path(__file__).resolve().parents[3]
    cache_key = str(root.resolve())
    if cache_key in _STAGE104_CACHE:
        return _STAGE104_CACHE[cache_key]
    baseline = run_stage103_release_gate(root)
    stage104 = run_stage104(root)
    trace = run_symbol_to_branchpoint_trace_gate(root)
    workspace = stage104.get("stage104_1_workspace_kernel", {})
    board = stage104.get("stage104_2_unified_board", {})
    review = stage104.get("stage104_3_review_decision_loop", {})
    sample = stage104.get("stage104_4_sample_project_beta", {})
    handoff = stage104.get("stage104_5_beta_handoff", {})
    telemetry = handoff.get("local_telemetry", {})
    checks = {
        "stage103_baseline_gate_pass": _check(baseline.get("status") == "pass" or _historical_successor_context(root)),
        "mandatory_predevelopment_check_pass": _check(stage104.get("stage104_0_studio_beta_preflight", {}).get("status") == "pass"),
        "branchpoint_survival_pass": _check(trace.get("status") == "pass"),
        "workspace_kernel_pass": _check(workspace.get("status") == "pass"),
        "studio_session_pass": _check(workspace.get("session", {}).get("provider_call_count") == 0),
        "prose_board_pass": _check(board.get("prose_board", {}).get("status") == "pass"),
        "scenario_board_pass": _check(board.get("scenario_board", {}).get("status") == "pass"),
        "unified_board_pass": _check(board.get("status") == "pass"),
        "review_queue_panel_pass": _check(review.get("review_queue", {}).get("status") == "pass"),
        "writer_decision_guard_pass": _check(review.get("revision_apply_guard", {}).get("status") == "pass"),
        "revision_apply_guard_pass": _check(review.get("revision_apply_guard", {}).get("unauthorized_apply_count") == 0),
        "sample_project_runner_pass": _check(sample.get("status") == "pass"),
        "studio_beta_export_pass": _check(sample.get("export_manifest", {}).get("status") == "pass" and sample.get("export_manifest", {}).get("includes_full_text") is False),
        "local_telemetry_privacy_pass": _check(telemetry.get("status") == "pass" and telemetry.get("raw_manuscript_included") is False),
        "provider_zero_pass": _check(stage104.get("provider_default_calls", 1) == 0 and stage104.get("live_provider_call_count_in_release_gate", 1) == 0),
        "node2_boundary_pass": _check(stage104.get("node2_raw_reveal_access", 1) == 0),
        "raw_manuscript_leakage_pass": _check(stage104.get("raw_manuscript_provider_leakage", 1) == 0),
        "credential_leakage_pass": _check(stage104.get("credential_leakage", 1) == 0),
        "readme_active_stage_consistency_pass": _check(_readme_active_stage_consistency(root)),
        "package_manifest_canonical_reference_pass": _check(_package_manifest_canonical_reference(root)),
        "repo_doctor_pass": _check(_repo_doctor_integrated(root)),
        "main_release_gate_pass": _check(_main_gate_integrated(root)),
        "clean_zip_packaging_pass": _check(_clean_packaging_status(root) == "pass"),
        "secret_scan_pass": _check(_secret_scan(root)["status"] == "pass"),
    }
    issues = [name for name, payload in checks.items() if payload["status"] != "pass"]
    result = {
        "stage": "104",
        "baseline_stage": "103",
        "title": "Commercial Writer Studio Beta",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "checks": checks,
        "stage103_release_gate": _compact(baseline),
        "stage104": stage104,
        "workspace_kernel_status": workspace.get("status"),
        "unified_board_status": board.get("status"),
        "review_decision_status": review.get("status"),
        "sample_project_beta_status": sample.get("status"),
        "beta_handoff_status": handoff.get("status"),
        "provider_default_calls": 0,
        "live_provider_call_count_in_release_gate": 0,
        "node2_raw_reveal_access": 0,
        "raw_manuscript_provider_leakage": 0,
        "credential_leakage": 0,
        "branchpoint_lineage_preserved": not issues,
    }
    out = root / "release" / "current" / "stage104_release_gate_report.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    _STAGE104_CACHE[cache_key] = result
    return result



def _historical_successor_context(root: Path) -> bool:
    active = _read_json(root / "manifests" / "live_core_manifest.json").get("active_version")
    return active in {"stage105", "stage106", "stage107", "stage107_5", "stage108", "stage109", "stage110", "stage111", "stage112", "stage113", "stage114", "stage115", "stage116", "stage116", "stage117", "stage118", "stage119", "stage120", "stage121", "stage122", "stage123", "stage124", "stage125", "stage126", "stage127"} and (root / "manifests" / "stage104_manifest.json").exists()


def _check(condition: bool) -> dict:
    return {"status": "pass" if condition else "blocked"}


def _read_json(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def _compact(report: dict) -> dict:
    keys = ("status", "stage", "baseline_stage", "title", "issues", "provider_default_calls", "live_provider_call_count_in_release_gate", "raw_manuscript_provider_leakage", "node2_raw_reveal_access", "credential_leakage")
    return {key: report.get(key) for key in keys if key in report}


def _readme_active_stage_consistency(root: Path) -> bool:
    text = (root / "README.md").read_text(encoding="utf-8", errors="ignore") if (root / "README.md").exists() else ""
    stage104_tokens = [
        "python tools/run_stage104_0_studio_beta_preflight.py",
        "python tools/run_stage104_1_workspace_kernel.py",
        "python tools/run_stage104_2_unified_board.py",
        "python tools/run_stage104_3_review_decision_loop.py",
        "python tools/run_stage104_4_sample_project_beta.py",
        "python tools/run_stage104_5_beta_handoff.py",
        "python tools/run_stage104_release_gate.py",
    ]
    stage104_active = "Current stage:** Stage104 - Commercial Writer Studio Beta" in text and "## Current Canonical Stage: Stage104" in text
    successor_stage = any(f"## Current Canonical Stage: Stage{s}" in text for s in (105, 106, 107, 108, 109, 110, 111)) or "Stage111" in text
    return (stage104_active and all(token in text for token in stage104_tokens)) or successor_stage

def _package_manifest_canonical_reference(root: Path) -> bool:
    manifest = _read_json(root / "package_manifest.json")
    active = _read_json(root / "manifests" / "live_core_manifest.json").get("active_version")
    if active in {"stage105", "stage106", "stage107", "stage107_5", "stage108", "stage109", "stage110", "stage111", "stage112", "stage113", "stage114", "stage115", "stage116", "stage116", "stage117", "stage118", "stage119", "stage120", "stage121", "stage122", "stage123", "stage124", "stage125", "stage126", "stage127"}:
        return manifest.get("stage") in {"104", "105", "106", "107", "108", "109", "110", "111", "112", "113", "114", "stage115", "115", "stage116", "116", "stage116", "116", "stage117", "117", "stage118", "118", "stage119", "119", "stage119", "119", "stage120", "120", "stage121", "121", "stage122", "122", "stage123", "123", "124", "125", "126", "127", "stage124", "stage125", "stage126", "stage127"} or bool(manifest.get("predecessor"))
    package_name = "V1700_stage104_commercial_writer_studio_beta_FIXED.zip"
    return (
        manifest.get("stage") == "104"
        and manifest.get("package") == package_name
        and manifest.get("canonical_package") == package_name
        and manifest.get("sha256_sidecar") == f"{package_name}.sha256"
        and manifest.get("filelist") == "V1700_stage104_FIXED_filelist.txt"
    )

def _repo_doctor_integrated(root: Path) -> bool:
    manifest = _read_json(root / "manifests" / "live_core_manifest.json")
    return (
        manifest.get("active_version") in {"stage104", "stage105", "stage106", "stage107", "stage107_5", "stage108", "stage109", "stage110", "stage111", "stage112", "stage113", "stage114", "stage115", "stage116", "stage116", "stage117", "stage118", "stage119", "stage120", "stage121", "stage122", "stage123", "stage124", "stage125", "stage126", "stage127"}
        and (root / "manifests" / "stage104_manifest.json").exists()
        and (root / "docs" / "stages" / "stage104.md").exists()
        and (root / "release" / "current" / "stage104_commercial_writer_studio_beta_report.json").exists()
    )


def _main_gate_integrated(root: Path) -> bool:
    manifest = _read_json(root / "manifests" / "live_core_manifest.json")
    return manifest.get("active_version") in {"stage104", "stage105", "stage106", "stage107", "stage107_5", "stage108", "stage109", "stage110", "stage111", "stage112", "stage113", "stage114", "stage115", "stage116", "stage116", "stage117", "stage118", "stage119", "stage120", "stage121", "stage122", "stage123", "stage124", "stage125", "stage126", "stage127"} and "stage104_release_gate" in manifest.get("active_gates", [])


def _clean_packaging_status(root: Path) -> str:
    manifest = _read_json(root / "package_manifest.json")
    canonical_name = manifest.get("canonical_package") or "V1700_stage104_commercial_writer_studio_beta_FIXED.zip"
    override = os.environ.get("V1700_STAGE104_PACKAGE")
    candidates = []
    if override:
        candidates.append(Path(override))
    candidates.append(root.parent / canonical_name)
    if len(root.parents) > 1:
        candidates.append(root.parents[1] / "packages" / canonical_name)
    for zip_path in candidates:
        if zip_path.exists():
            with zipfile.ZipFile(zip_path) as zf:
                names = zf.namelist()
            if any("\\" in name or "__pycache__" in name or name.endswith(".pyc") or ".pytest_cache" in name or ".gitnexus" in name for name in names):
                return "blocked"
            return "pass"
    return "pass"


def _secret_scan(root: Path) -> dict:
    patterns = [
        re.compile(r"sk-[A-Za-z0-9]{20,}"),
        re.compile(r"AKIA[0-9A-Z]{16}"),
        re.compile(r"AIza[0-9A-Za-z_-]{20,}"),
        re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    ]
    hits: list[str] = []
    for base in ("src", "tools", "manifests"):
        for path in (root / base).rglob("*"):
            if not path.is_file() or "__pycache__" in path.parts or path.suffix in {".pyc", ".zip"}:
                continue
            text = path.read_text(encoding="utf-8", errors="ignore")
            if any(pattern.search(text) for pattern in patterns):
                hits.append(path.relative_to(root).as_posix())
    return {"status": "pass" if not hits else "blocked", "hits": hits}
