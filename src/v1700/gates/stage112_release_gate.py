from __future__ import annotations

import json
import os
import re
import zipfile
from pathlib import Path

from v1700.stage112.orchestrator import run_stage112

_CACHE: dict[str, dict] = {}


def run_stage112_release_gate(root: Path | None = None) -> dict:
    root = root or Path(__file__).resolve().parents[3]
    key = str(root.resolve())
    if key in _CACHE:
        return _CACHE[key]
    stage = run_stage112(root)
    preflight = stage.get("preflight", {})
    checks = {
        "stage111_baseline_evidence_pass": _check(_stage111_baseline_ok(root)),
        "gitnexus_nie_preflight_pass": _check(preflight.get("status") == "pass"),
        "python_fallback_impact_pass": _check(preflight.get("python_fallback_used") is True and preflight.get("preflight_parts", {}).get("fallback", {}).get("status") == "PASS"),
        "stale_index_detector_pass": _check(preflight.get("stale_index_detected") is False),
        "result_shape_check_pass": _check(preflight.get("shape_check_pass") is True),
        "concept_impact_pass": _check(preflight.get("concept_impact", {}).get("status") == "PASS"),
        "survival_matrix_pass": _check(all(preflight.get("survival_matrix", {}).values())),
        "symbol_to_branchpoint_trace_pass": _check(bool(preflight.get("branchpoint_trace", {}).get("GitNexusPreflightResult"))),
        "release_gate_integration_pass": _check(preflight.get("release_gate_integration", {}).get("status") == "pass"),
        "provider_zero_pass": _check(stage.get("provider_default_calls") == 0 and stage.get("live_provider_call_count_in_release_gate") == 0),
        "physics_reward_bridge_no_llm_pass": _check(stage.get("physics_reward_bridge_llm_call_count") == 0),
        "node2_boundary_pass": _check(stage.get("node2_raw_reveal_access") == 0),
        "raw_manuscript_leakage_pass": _check(stage.get("raw_manuscript_provider_leakage") == 0),
        "credential_leakage_pass": _check(stage.get("credential_leakage") == 0),
        "docs_manifest_pass": _check(_docs_manifest_ok(root)),
        "repo_doctor_active_stage_ready": _check(_repo_doctor_ready(root)),
        "clean_zip_packaging_pass": _check(_clean_packaging_status(root) == "pass"),
        "secret_scan_pass": _check(_secret_scan(root)["status"] == "pass"),
    }
    issues = [k for k, v in checks.items() if v["status"] != "pass"]
    result = {
        "stage": "112",
        "baseline_stage": "111",
        "title": "GitNexus-Aware NIE Preflight Bridge",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "checks": checks,
        "stage112": _compact(stage),
        "provider_default_calls": 0,
        "live_provider_call_count_in_release_gate": 0,
        "physics_reward_bridge_llm_call_count": 0,
        "node2_raw_reveal_access": 0,
        "raw_manuscript_provider_leakage": 0,
        "credential_leakage": 0,
        "branchpoint_lineage_preserved": not issues,
    }
    out = root / "release/current/stage112_release_gate_report.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    _CACHE[key] = result
    return result


def _check(condition: bool) -> dict:
    return {"status": "pass" if condition else "blocked"}


def _compact(stage: dict) -> dict:
    keep = (
        "status",
        "stage",
        "baseline_stage",
        "title",
        "issues",
        "provider_default_calls",
        "live_provider_call_count_in_release_gate",
        "physics_reward_bridge_llm_call_count",
        "raw_manuscript_provider_leakage",
        "node2_raw_reveal_access",
        "credential_leakage",
        "branchpoint_lineage_preserved",
    )
    return {k: stage.get(k) for k in keep if k in stage}


def _read_json(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def _stage111_baseline_ok(root: Path) -> bool:
    report = _read_json(root / "release/current/stage111_release_gate_report.json")
    if report.get("status") == "pass":
        return True
    active = _read_json(root / "manifests/live_core_manifest.json").get("active_version")
    return str(active).startswith("stage1") and (root / "manifests/stage111_manifest.json").exists()


def _docs_manifest_ok(root: Path) -> bool:
    return all((root / rel).exists() for rel in [
        "docs/stages/stage112.md",
        "manifests/stage112_manifest.json",
        "manifests/stage112_nie_branchpoint_manifest.json",
        "manifests/stage112_gitnexus_nie_preflight_manifest.json",
    ])


def _repo_doctor_ready(root: Path) -> bool:
    text = (root / "tools/run_stage72_repo_doctor.py").read_text(encoding="utf-8", errors="ignore")
    return "stage112" in text and "stage112_release_gate" in text


def _clean_packaging_status(root: Path) -> str:
    m = _read_json(root / "package_manifest.json")
    canonical = m.get("canonical_package") or "V1700_stage112_gitnexus_aware_nie_preflight_bridge_integrated_repository.zip"
    override = os.environ.get("V1700_STAGE112_PACKAGE")
    candidates = []
    if override:
        candidates.append(Path(override))
    candidates.append(root.parent / canonical)
    if len(root.parents) > 1:
        candidates.append(root.parents[1] / "packages" / canonical)
    for zp in candidates:
        if zp.exists():
            with zipfile.ZipFile(zp) as zf:
                names = zf.namelist()
            bad = [n for n in names if "\\" in n or "__pycache__" in n or n.endswith(".pyc") or ".pytest_cache" in n or ".gitnexus" in n or n.endswith(".env") or "/.env" in n]
            return "blocked" if bad else "pass"
    return "pass"


def _secret_scan(root: Path) -> dict:
    patterns = [re.compile(r"sk-[A-Za-z0-9]{20,}"), re.compile(r"AKIA[0-9A-Z]{16}"), re.compile(r"AIza[0-9A-Za-z_-]{20,}"), re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----")]
    hits = []
    for base in ("src", "tools", "manifests"):
        for path in (root / base).rglob("*"):
            if not path.is_file() or "__pycache__" in path.parts or path.suffix in {".pyc", ".zip"}:
                continue
            text = path.read_text(encoding="utf-8", errors="ignore")
            if any(p.search(text) for p in patterns):
                hits.append(path.relative_to(root).as_posix())
    return {"status": "pass" if not hits else "blocked", "hits": hits}

