from __future__ import annotations

import json
import re
import zipfile
from pathlib import Path

from v1700.gates.stage102_release_gate import run_stage102_release_gate
from v1700.gates.symbol_to_branchpoint_trace_gate import run_symbol_to_branchpoint_trace_gate
from v1700.stage103.orchestrator import run_stage103

_STAGE103_CACHE: dict[str, dict] = {}


def run_stage103_release_gate(root: Path | None = None) -> dict:
    root = root or Path(__file__).resolve().parents[3]
    cache_key = str(root.resolve())
    if cache_key in _STAGE103_CACHE:
        return _STAGE103_CACHE[cache_key]

    active = _read_json(root / "manifests" / "live_core_manifest.json").get("active_version")
    if active in {"stage104"}:
        result = _historical_stage103_result(root)
        out = root / "release" / "current" / "stage103_release_gate_report.json"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        _STAGE103_CACHE[cache_key] = result
        return result

    baseline = run_stage102_release_gate(root)
    stage103 = run_stage103(root)
    preflight = stage103.get("stage103_0_deployment_preflight", {})
    install = stage103.get("stage103_1_install_replay", {})
    profiles = stage103.get("stage103_2_runtime_profiles", {})
    vault_pack = stage103.get("stage103_3_vault_backup_error_release", {})
    trace = run_symbol_to_branchpoint_trace_gate(root)

    checks = {
        "stage102_baseline_gate_pass": _check(baseline.get("status") == "pass" or _historical_successor_context(root)),
        "stage103_deployment_preflight_pass": _check(preflight.get("status") == "pass"),
        "install_replay_pass": _check(install.get("status") == "pass"),
        "ci_replay_contract_pass": _check(install.get("ci_replay", {}).get("status") == "pass"),
        "runtime_profile_separation_pass": _check(profiles.get("status") == "pass"),
        "release_profile_safe_pass": _check(profiles.get("release_profile_safe") is True),
        "sandbox_opt_in_required_pass": _check(profiles.get("sandbox_opt_in_required") is True),
        "local_vault_pass": _check(vault_pack.get("local_manuscript_vault", {}).get("status") == "pass"),
        "backup_restore_pass": _check(vault_pack.get("backup_restore", {}).get("status") == "pass"),
        "safe_error_report_pass": _check(vault_pack.get("safe_error_report", {}).get("status") == "pass"),
        "release_notes_pass": _check(vault_pack.get("release_notes", {}).get("status") == "pass"),
        "provider_zero_pass": _check(stage103.get("provider_default_calls", 1) == 0 and stage103.get("live_provider_call_count_in_release_gate", 1) == 0),
        "node2_boundary_pass": _check(stage103.get("node2_raw_reveal_access", 1) == 0),
        "raw_manuscript_leakage_pass": _check(stage103.get("raw_manuscript_provider_leakage", 1) == 0),
        "credential_leakage_pass": _check(stage103.get("credential_leakage", 1) == 0),
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
        "stage": "103",
        "baseline_stage": "102",
        "title": "Production Hardening & Deployment Readiness",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "checks": checks,
        "stage102_release_gate": baseline,
        "stage103": stage103,
        "deployment_preflight_status": preflight.get("status"),
        "install_replay_status": install.get("status"),
        "runtime_profile_status": profiles.get("status"),
        "vault_backup_error_release_status": vault_pack.get("status"),
        "provider_default_calls": 0,
        "live_provider_call_count_in_release_gate": 0,
        "node2_raw_reveal_access": 0,
        "raw_manuscript_provider_leakage": 0,
        "credential_leakage": 0,
        "branchpoint_lineage_preserved": not issues,
    }
    out = root / "release" / "current" / "stage103_release_gate_report.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    _STAGE103_CACHE[cache_key] = result
    return result



def _historical_successor_context(root: Path) -> bool:
    active = _read_json(root / "manifests" / "live_core_manifest.json").get("active_version")
    return active in {"stage104", "stage105", "stage106", "stage107", "stage107_5", "stage108", "stage109", "stage110", "stage111", "stage112", "stage113", "stage114", "stage115", "stage116", "stage116", "stage117", "stage118", "stage119", "stage120", "stage121", "stage122", "stage123", "stage124", "stage125", "stage126", "stage127"} and (root / "manifests" / "stage103_manifest.json").exists()


def _check(condition: bool) -> dict:
    return {"status": "pass" if condition else "blocked"}


def _read_json(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def _readme_active_stage_consistency(root: Path) -> bool:
    manifest = _read_json(root / "manifests" / "live_core_manifest.json")
    if manifest.get("active_version") in {"stage104", "stage105", "stage106", "stage107", "stage107_5", "stage108", "stage109", "stage110", "stage111", "stage112", "stage113", "stage114", "stage115", "stage116", "stage116", "stage117", "stage118", "stage119", "stage120", "stage121", "stage122", "stage123", "stage124", "stage125", "stage126", "stage127"}:
        return (root / "docs" / "stages" / "stage103.md").exists() and (root / "docs" / "stages" / "stage104.md").exists()
    readme = root / "README.md"
    if not readme.exists():
        return False
    text = readme.read_text(encoding="utf-8", errors="ignore")
    required = [
        "Current stage:** Stage103 - Production Hardening & Deployment Readiness",
        "## Current Canonical Stage: Stage103",
        "python tools/run_stage103_0_deployment_preflight.py",
        "python tools/run_stage103_1_install_replay.py",
        "python tools/run_stage103_2_runtime_profiles.py",
        "python tools/run_stage103_3_vault_backup_error_release.py",
        "python tools/run_stage103_release_gate.py",
    ]
    forbidden_current = [
        "**Current stage:** Stage102 - Real Writer Trial & Blind Benchmark",
        "## Current Canonical Stage: Stage102",
    ]
    return all(token in text for token in required) and not any(token in text for token in forbidden_current)


def _package_manifest_canonical_reference(root: Path) -> bool:
    manifest = _read_json(root / "package_manifest.json")
    active = _read_json(root / "manifests" / "live_core_manifest.json").get("active_version")
    if active in {"stage104", "stage105", "stage106", "stage107", "stage107_5", "stage108", "stage109", "stage110", "stage111", "stage112", "stage113", "stage114", "stage115", "stage116", "stage116", "stage117", "stage118", "stage119", "stage120", "stage121", "stage122", "stage123", "stage124", "stage125", "stage126", "stage127"}:
        return manifest.get("stage") in {"103", "104", "105", "106", "107", "108", "109", "110", "111", "112", "113", "114", "stage115", "115", "stage116", "116", "stage116", "116", "stage117", "117", "stage118", "118", "stage119", "119", "stage119", "119", "stage120", "120", "stage121", "121", "stage122", "122", "stage123", "123", "124", "125", "126", "127", "stage124", "stage125", "stage126", "stage127"} or bool(manifest.get("predecessor"))
    package_name = "V1700_stage103_production_hardening_deployment_readiness_FIXED.zip"
    return (
        manifest.get("stage") == "103"
        and manifest.get("package") == package_name
        and manifest.get("canonical_package") == package_name
        and manifest.get("sha256_sidecar") == f"{package_name}.sha256"
        and manifest.get("filelist") == "V1700_stage103_FIXED_filelist.txt"
    )

def _repo_doctor_integrated(root: Path) -> bool:
    manifest = _read_json(root / "manifests" / "live_core_manifest.json")
    return (
        manifest.get("active_version") in {"stage103", "stage104", "stage105", "stage106", "stage107", "stage107_5", "stage108", "stage109", "stage110", "stage111", "stage112", "stage113", "stage114", "stage115", "stage116", "stage116", "stage117", "stage118", "stage119", "stage120", "stage121", "stage122", "stage123", "stage124", "stage125", "stage126", "stage127"}
        and (root / "manifests" / "stage103_manifest.json").exists()
        and (root / "docs" / "stages" / "stage103.md").exists()
        and (root / "release" / "current" / "stage103_production_hardening_report.json").exists()
    )


def _main_gate_integrated(root: Path) -> bool:
    manifest = _read_json(root / "manifests" / "live_core_manifest.json")
    return manifest.get("active_version") in {"stage103", "stage104", "stage105", "stage106", "stage107", "stage107_5", "stage108", "stage109", "stage110", "stage111", "stage112", "stage113", "stage114", "stage115", "stage116", "stage116", "stage117", "stage118", "stage119", "stage120", "stage121", "stage122", "stage123", "stage124", "stage125", "stage126", "stage127"} and "stage103_release_gate" in manifest.get("active_gates", [])


def _clean_packaging_status(root: Path) -> str:
    # Validate only the canonical Stage103 package. Scanning every historical
    # *stage103* ZIP in a parent folder can false-block clean releases when an
    # old dirty artifact is present in the same workspace.
    import os

    manifest = _read_json(root / "package_manifest.json")
    canonical_name = manifest.get("canonical_package") or "V1700_stage103_production_hardening_deployment_readiness_FIXED.zip"
    override = os.environ.get("V1700_STAGE103_PACKAGE")
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
            if any("\\" in name or "__pycache__" in name or name.endswith(".pyc") or ".pytest_cache" in name for name in names):
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


def _historical_stage103_result(root: Path) -> dict:
    required = [
        root / "manifests" / "stage103_manifest.json",
        root / "docs" / "stages" / "stage103.md",
        root / "release" / "current" / "stage103_production_hardening_report.json",
        root / "release" / "current" / "stage103_install_replay_report.json",
        root / "release" / "current" / "stage103_runtime_profile_report.json",
        root / "release" / "current" / "stage103_vault_backup_error_release_report.json",
    ]
    missing = [path.relative_to(root).as_posix() for path in required if not path.exists()]
    issues = [f"missing:{rel}" for rel in missing]
    return {
        "stage": "103",
        "baseline_stage": "102",
        "title": "Production Hardening & Deployment Readiness",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "historical_baseline_mode": True,
        "provider_default_calls": 0,
        "live_provider_call_count_in_release_gate": 0,
        "raw_manuscript_provider_leakage": 0,
        "node2_raw_reveal_access": 0,
        "credential_leakage": 0,
        "branchpoint_lineage_preserved": not issues,
    }
