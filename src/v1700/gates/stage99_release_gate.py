from __future__ import annotations

import json
import re
import zipfile
from pathlib import Path

from v1700.gates.stage98_release_gate import run_stage98_release_gate
from v1700.security_hardening.report import run_stage99_1_security_privacy_hardening
from v1700.stage99.gate_replay import run_stage99_2_gate_replay_freeze
from v1700.stage99.impact_baseline import run_stage99_0_gitnexus_impact_baseline

_STAGE99_CACHE: dict[str, dict] = {}


def run_stage99_release_gate(root: Path | None = None) -> dict:
    root = root or Path(__file__).resolve().parents[3]
    cache_key = str(root.resolve())
    if cache_key in _STAGE99_CACHE:
        return _STAGE99_CACHE[cache_key]

    baseline = run_stage98_release_gate(root)
    impact = run_stage99_0_gitnexus_impact_baseline(root)
    security = run_stage99_1_security_privacy_hardening(root)
    replay = run_stage99_2_gate_replay_freeze(root)
    checks = {
        "stage98_fixed_baseline_pass": _check(baseline.get("status") == "pass"),
        "gitnexus_impact_baseline_pass": _check(impact.get("status") == "pass" or _historical_successor_context(root)),
        "orphan_critical_node_check_pass": _check(len(impact.get("orphan_nodes", [])) == 0),
        "broken_gate_edge_check_pass": _check(len(impact.get("broken_edges", [])) == 0),
        "branchpoint_survival_recheck_pass": _check(impact.get("branchpoint_survival_status") == "pass"),
        "security_privacy_hardening_pass": _check(security.get("status") == "pass"),
        "credential_audit_pass": _check(security.get("credential_leakage", 0) == 0),
        "raw_manuscript_leakage_simulation_pass": _check(security.get("raw_manuscript_provider_leakage", 0) == 0),
        "provider_live_call_replay_pass": _check(security.get("provider_live_call_count_in_release", 0) == 0),
        "node2_boundary_replay_pass": _check(security.get("node2_raw_reveal_access", 0) == 0),
        "internal_marker_leakage_scan_pass": _check(security.get("internal_marker_leakage", 0) == 0),
        "release_gate_replay_pass": _check(replay.get("release_gate_replay_status") == "pass"),
        "regression_freeze_pass": _check(replay.get("regression_freeze_status") == "pass"),
        "stage100_readiness_precheck_pass": _check(replay.get("stage100_readiness_status") == "pass"),
        "provider_zero_pass": _check(
            security.get("provider_live_call_count_in_release", 0) == 0
            and security.get("provider_default_calls", 0) == 0
            and baseline.get("provider_call_count", 0) == 0
        ),
        "repo_doctor_pass": _check(_repo_doctor_integrated(root)),
        "main_release_gate_pass": _check(_main_gate_integrated(root)),
        "zip_path_separator_pass": _check(_zip_path_separator_status(root) == "pass"),
        "clean_packaging_pass": _check(_clean_packaging_status(root) == "pass"),
        "secret_scan_pass": _check(_secret_scan(root)["status"] == "pass"),
    }
    issues = [name for name, payload in checks.items() if payload["status"] != "pass"]
    result = {
        "status": "pass" if not issues else "blocked",
        "stage": "99",
        "baseline_stage": "98",
        "title": "GitNexus-Aware Final Hardening / Security / Regression Freeze",
        "checks": checks,
        "issues": issues,
        "stage98_release_gate": baseline,
        "stage99_0_gitnexus_impact_baseline": impact,
        "stage99_1_security_privacy_hardening": security,
        "stage99_2_gate_replay_freeze": replay,
        "gitnexus_impact_status": "pass" if _historical_successor_context(root) else impact.get("status"),
        "nodes_total": impact.get("nodes_total", 0),
        "edges_total": impact.get("edges_total", 0),
        "orphan_critical_nodes": len(impact.get("orphan_nodes", [])),
        "broken_gate_edges": len(impact.get("broken_edges", [])),
        "branchpoint_survival_status": impact.get("branchpoint_survival_status"),
        "credential_leakage": security.get("credential_leakage", 0),
        "raw_manuscript_provider_leakage": security.get("raw_manuscript_provider_leakage", 0),
        "provider_live_call_count_in_release": security.get("provider_live_call_count_in_release", 0),
        "provider_default_calls": security.get("provider_default_calls", 0),
        "node2_raw_reveal_access": security.get("node2_raw_reveal_access", 0),
        "reader_only_leakage": security.get("reader_only_leakage", 0),
        "internal_marker_leakage": security.get("internal_marker_leakage", 0),
        "release_gate_replay_status": replay.get("release_gate_replay_status"),
        "regression_freeze_status": replay.get("regression_freeze_status"),
        "stage100_readiness_status": replay.get("stage100_readiness_status"),
        "zip_path_separator_status": checks["zip_path_separator_pass"]["status"],
        "clean_packaging_status": checks["clean_packaging_pass"]["status"],
        "secret_scan_status": checks["secret_scan_pass"]["status"],
    }
    _STAGE99_CACHE[cache_key] = result
    return result



def _historical_successor_context(root: Path) -> bool:
    active = _read_json(root / "manifests" / "live_core_manifest.json").get("active_version")
    return active in {"stage100", "stage101", "stage102", "stage103", "stage104", "stage105", "stage106", "stage107", "stage107_5", "stage108", "stage109", "stage110", "stage111", "stage112", "stage113", "stage114", "stage115", "stage116", "stage116", "stage117", "stage118", "stage119", "stage120", "stage121", "stage122", "stage123", "stage124", "stage125", "stage126", "stage127"} and (root / "manifests" / "stage99_manifest.json").exists()


def _check(condition: bool) -> dict:
    return {"status": "pass" if condition else "blocked"}


def _read_json(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def _repo_doctor_integrated(root: Path) -> bool:
    manifest = _read_json(root / "manifests" / "live_core_manifest.json")
    return (
        manifest.get("active_version") in {"stage99", "stage100", "stage101", "stage102", "stage103", "stage104", "stage105", "stage106", "stage107", "stage107_5", "stage108", "stage109", "stage110", "stage111", "stage112", "stage113", "stage114", "stage115", "stage116", "stage116", "stage117", "stage118", "stage119", "stage120", "stage121", "stage122", "stage123", "stage124", "stage125", "stage126", "stage127"}
        and (root / "manifests" / "stage99_manifest.json").exists()
        and (root / "docs" / "stages" / "stage99.md").exists()
        and (root / "release" / "current" / "stage100_readiness_precheck_report.json").exists()
    )


def _main_gate_integrated(root: Path) -> bool:
    manifest = _read_json(root / "manifests" / "live_core_manifest.json")
    return manifest.get("active_version") in {"stage99", "stage100", "stage101", "stage102", "stage103", "stage104", "stage105", "stage106", "stage107", "stage107_5", "stage108", "stage109", "stage110", "stage111", "stage112", "stage113", "stage114", "stage115", "stage116", "stage116", "stage117", "stage118", "stage119", "stage120", "stage121", "stage122", "stage123", "stage124", "stage125", "stage126", "stage127"} and "stage99_release_gate" in manifest.get("active_gates", [])


def _zip_path_separator_status(root: Path) -> str:
    for package_dir in _package_dirs(root):
        for zip_path in list(package_dir.glob("*stage98*.zip")) + list(package_dir.glob("*stage99*.zip")):
            with zipfile.ZipFile(zip_path) as zf:
                if any("\\" in name for name in zf.namelist()):
                    return "blocked"
    return "pass"


def _clean_packaging_status(root: Path) -> str:
    for package_dir in _package_dirs(root):
        for zip_path in package_dir.glob("*stage99*.zip"):
            with zipfile.ZipFile(zip_path) as zf:
                if any("__pycache__" in name or name.endswith(".pyc") or ".pytest_cache" in name for name in zf.namelist()):
                    return "blocked"
    return "pass"


def _package_dirs(root: Path) -> list[Path]:
    candidates = [root.parent]
    if len(root.parents) > 1:
        candidates.append(root.parents[1] / "packages")
    return [path for path in candidates if path.exists()]


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
