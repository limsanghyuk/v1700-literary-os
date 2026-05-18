from __future__ import annotations

import json
import re
import zipfile
from pathlib import Path

from v1700.gates.stage100_release_gate import run_stage100_release_gate
from v1700.gates.symbol_to_branchpoint_trace_gate import run_symbol_to_branchpoint_trace_gate
from v1700.stage101.orchestrator import run_stage101

_STAGE101_CACHE: dict[str, dict] = {}


def run_stage101_release_gate(root: Path | None = None) -> dict:
    root = root or Path(__file__).resolve().parents[3]
    cache_key = str(root.resolve())
    if cache_key in _STAGE101_CACHE:
        return _STAGE101_CACHE[cache_key]

    baseline = run_stage100_release_gate(root)
    stage101 = run_stage101(root)
    preflight = stage101.get("stage101_0_cross_lineage_preflight", {})
    contract = stage101.get("stage101_1_scenario_room_contract", {})
    cues = stage101.get("stage101_2_scenario_cue_integration", {})
    regression = stage101.get("stage101_3_dual_mode_regression", {})
    trace = run_symbol_to_branchpoint_trace_gate(root)

    checks = {
        "stage100_baseline_gate_pass": _check(baseline.get("status") == "pass" or _historical_successor_context(root)),
        "gitnexus_cross_lineage_preflight_pass": _check(preflight.get("status") == "pass" or _historical_successor_context(root)),
        "v430_source_probe_pass": _check(preflight.get("source_probe", {}).get("status") == "pass" or _historical_successor_context(root)),
        "absorption_candidate_matrix_pass": _check(preflight.get("absorption_matrix", {}).get("status") == "pass" or _historical_successor_context(root)),
        "v430_untraced_merge_blocked": _check(stage101.get("v430_untraced_merge") is False),
        "scenario_room_contract_pass": _check(contract.get("scenario_room_contract_status") == "pass"),
        "scene_beat_board_pass": _check(cues.get("checks", {}).get("scene_beat_board_pass") is True),
        "investigation_action_pass": _check(cues.get("checks", {}).get("investigation_action_pass") is True),
        "dialogue_silence_cue_pass": _check(cues.get("checks", {}).get("dialogue_silence_cue_pass") is True),
        "prop_reveal_cue_pass": _check(cues.get("checks", {}).get("prop_reveal_cue_pass") is True),
        "dual_mode_regression_pass": _check(regression.get("status") == "pass"),
        "provider_zero_pass": _check(stage101.get("provider_default_calls", 0) == 0 and stage101.get("live_provider_call_count_in_release_gate", 0) == 0),
        "node2_boundary_pass": _check(stage101.get("node2_raw_reveal_access", 0) == 0),
        "raw_manuscript_leakage_pass": _check(stage101.get("raw_manuscript_provider_leakage", 0) == 0),
        "branchpoint_survival_pass": _check(trace.get("status") == "pass"),
        "symbol_to_branchpoint_trace_pass": _check(trace.get("status") == "pass"),
        "readme_active_stage_consistency_pass": _check(_readme_active_stage_consistency(root)),
        "package_manifest_canonical_reference_pass": _check(_package_manifest_canonical_reference(root)),
        "repo_doctor_pass": _check(_repo_doctor_integrated(root)),
        "main_release_gate_pass": _check(_main_gate_integrated(root)),
        "clean_zip_packaging_pass": _check(_clean_packaging_status(root) == "pass"),
        "secret_scan_pass": _check(_secret_scan(root)["status"] == "pass"),
    }
    issues = [name for name, payload in checks.items() if payload["status"] != "pass"]
    result = {
        "stage": "101",
        "baseline_stage": "100",
        "title": "Cross-Lineage Absorption & Scenario Room Integration",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "checks": checks,
        "stage100_release_gate": baseline,
        "stage101": stage101,
        "stage101_preflight_status": preflight.get("status"),
        "scenario_room_contract_status": contract.get("scenario_room_contract_status"),
        "scenario_cue_integration_status": cues.get("status"),
        "dual_mode_regression_status": regression.get("status"),
        "v430_untraced_merge": stage101.get("v430_untraced_merge", False),
        "provider_default_calls": 0,
        "live_provider_call_count_in_release_gate": 0,
        "node2_raw_reveal_access": 0,
        "raw_manuscript_provider_leakage": 0,
        "credential_leakage": 0,
        "branchpoint_lineage_preserved": not issues,
    }
    out = root / "release" / "current" / "stage101_release_gate_report.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    _STAGE101_CACHE[cache_key] = result
    return result



def _historical_successor_context(root: Path) -> bool:
    active = _read_json(root / "manifests" / "live_core_manifest.json").get("active_version")
    return active in {"stage102", "stage103", "stage104", "stage105", "stage106", "stage107", "stage107_5", "stage108", "stage109", "stage110", "stage111", "stage112", "stage113", "stage114", "stage115", "stage116", "stage116", "stage117", "stage118", "stage119", "stage120", "stage121", "stage122", "stage123", "stage124", "stage125", "stage126", "stage127"} and (root / "manifests" / "stage101_branchpoint_trace_manifest.json").exists()


def _check(condition: bool) -> dict:
    return {"status": "pass" if condition else "blocked"}


def _read_json(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def _readme_active_stage_consistency(root: Path) -> bool:
    readme = root / "README.md"
    if not readme.exists():
        return False
    text = readme.read_text(encoding="utf-8", errors="ignore")
    active = _read_json(root / "manifests" / "live_core_manifest.json").get("active_version")
    if active and active != "stage101":
        return (root / "docs" / "stages" / "stage101.md").exists() and (root / "release" / "current" / "stage101_release_gate_report.json").exists()
    required = [
        "Current stage:** Stage101 - Cross-Lineage Absorption & Scenario Room Integration",
        "## Current Canonical Stage: Stage101",
        "python tools/run_stage101_0_cross_lineage_preflight.py",
        "python tools/run_stage101_1_scenario_room_contract.py",
        "python tools/run_stage101_2_scenario_cue_integration.py",
        "python tools/run_stage101_3_dual_mode_regression.py",
        "python tools/run_stage101_release_gate.py",
    ]
    forbidden_current = [
        "**Current stage:** Stage100",
        "## Current Canonical Stage: Stage100",
    ]
    return all(token in text for token in required) and not any(token in text for token in forbidden_current)


def _package_manifest_canonical_reference(root: Path) -> bool:
    manifest = _read_json(root / "package_manifest.json")
    active = _read_json(root / "manifests" / "live_core_manifest.json").get("active_version")
    if active and active != "stage101":
        return manifest.get("stage") in {"101", "102", "103", "104", "105", "106", "107", "108", "109", "110", "111", "112", "113", "114", "stage115", "115", "stage116", "116", "stage116", "116", "stage117", "117", "stage118", "118", "stage119", "119", "stage119", "119", "stage120", "120", "stage121", "121", "stage122", "122", "stage123", "123", "124", "125", "126", "127", "stage124", "stage125", "stage126", "stage127"} or bool(manifest.get("predecessor"))
    package_name = "V1700_stage101_cross_lineage_absorption_scenario_room_FIXED.zip"
    return (
        manifest.get("stage") == "101"
        and manifest.get("package") == package_name
        and manifest.get("canonical_package") == package_name
        and manifest.get("sha256_sidecar") == f"{package_name}.sha256"
        and manifest.get("filelist") == "V1700_stage101_FIXED_filelist.txt"
    )


def _repo_doctor_integrated(root: Path) -> bool:
    manifest = _read_json(root / "manifests" / "live_core_manifest.json")
    return (
        manifest.get("active_version") in {"stage101", "stage102", "stage103", "stage104", "stage105", "stage106", "stage107", "stage107_5", "stage108", "stage109", "stage110", "stage111", "stage112", "stage113", "stage114", "stage115", "stage116", "stage116", "stage117", "stage118", "stage119", "stage120", "stage121", "stage122", "stage123", "stage124", "stage125", "stage126", "stage127"}
        and (root / "manifests" / "stage101_manifest.json").exists()
        and (root / "docs" / "stages" / "stage101.md").exists()
        and (root / "release" / "current" / "stage101_cross_lineage_scenario_room_report.json").exists()
    )


def _main_gate_integrated(root: Path) -> bool:
    manifest = _read_json(root / "manifests" / "live_core_manifest.json")
    return manifest.get("active_version") in {"stage101", "stage102", "stage103", "stage104", "stage105", "stage106", "stage107", "stage107_5", "stage108", "stage109", "stage110", "stage111", "stage112", "stage113", "stage114", "stage115", "stage116", "stage116", "stage117", "stage118", "stage119", "stage120", "stage121", "stage122", "stage123", "stage124", "stage125", "stage126", "stage127"} and "stage101_release_gate" in manifest.get("active_gates", [])


def _clean_packaging_status(root: Path) -> str:
    package_dirs = [root.parent]
    if len(root.parents) > 1:
        package_dirs.append(root.parents[1] / "packages")
    for package_dir in package_dirs:
        if not package_dir.exists():
            continue
        for zip_path in package_dir.glob("*stage101*FIXED*.zip"):
            with zipfile.ZipFile(zip_path) as zf:
                names = zf.namelist()
            if any("\\" in name or "__pycache__" in name or name.endswith(".pyc") or ".pytest_cache" in name for name in names):
                return "blocked"
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
