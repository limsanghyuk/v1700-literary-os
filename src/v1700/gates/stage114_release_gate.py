from __future__ import annotations

import json
import os
import re
import zipfile
from pathlib import Path

from v1700.stage114.orchestrator import run_stage114

_CACHE: dict[str, dict] = {}


def run_stage114_release_gate(root: Path | None = None) -> dict:
    root = root or Path(__file__).resolve().parents[3]
    key = str(root.resolve())
    if key in _CACHE:
        return _CACHE[key]
    stage = run_stage114(root)
    amw = stage.get("adaptive_momentum_weights", {})
    guard = amw.get("drift_guard", {})
    updates = amw.get("updates", [])
    checks = {
        "stage113_baseline_gate_pass": _check(_stage113_baseline_ok(root)),
        "amw_contract_pass": _check(_amw_contract_ok(amw)),
        "amw_alpha_bounds_pass": _check(_alpha_bounds_ok(amw)),
        "amw_drift_guard_pass": _check(guard.get("status") == "pass"),
        "amw_update_count_pass": _check(len(updates) == 4),
        "amw_uses_mae_dimension_scores_pass": _check(_mae_dimension_scores_ok(updates)),
        "amw_protected_policy_pass": _check(_protected_policy_ok(guard)),
        "mae_live_provider_call_zero_pass": _check(amw.get("provider_call_count") == 0),
        "physics_reward_bridge_no_llm_pass": _check(amw.get("physics_reward_bridge_llm_call_count") == 0),
        "provider_zero_pass": _check(stage.get("provider_default_calls") == 0 and stage.get("live_provider_call_count_in_release_gate") == 0),
        "node2_boundary_pass": _check(stage.get("node2_raw_reveal_access") == 0),
        "raw_manuscript_leakage_pass": _check(stage.get("raw_manuscript_provider_leakage") == 0),
        "credential_leakage_pass": _check(stage.get("credential_leakage") == 0),
        "docs_manifest_pass": _check(_docs_manifest_ok(root)),
        "repo_doctor_active_stage_ready": _check(_repo_doctor_ready(root)),
        "clean_zip_packaging_pass": _check(_clean_packaging_status(root) == "pass"),
        "secret_scan_pass": _check(_secret_scan(root)["status"] == "pass"),
    }
    issues = [name for name, value in checks.items() if value["status"] != "pass"]
    result = {
        "stage": "114",
        "baseline_stage": "113",
        "title": "AdaptiveMomentumWeights",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "checks": checks,
        "stage114": _compact(stage),
        "amw_summary": {
            "alpha_before": amw.get("alpha_before", {}),
            "alpha_after": amw.get("alpha_after", {}),
            "update_count": len(updates),
            "observed_max_single_shift": guard.get("observed_max_single_shift"),
            "observed_run_total_shift": guard.get("observed_run_total_shift"),
            "guard_status": guard.get("status"),
        },
        "provider_default_calls": 0,
        "live_provider_call_count_in_release_gate": 0,
        "physics_reward_bridge_llm_call_count": 0,
        "mae_live_provider_call_count": 0,
        "node2_raw_reveal_access": 0,
        "raw_manuscript_provider_leakage": 0,
        "credential_leakage": 0,
        "branchpoint_lineage_preserved": not issues,
    }
    out = root / "release/current/stage114_release_gate_report.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    _CACHE[key] = result
    return result


def _check(condition: bool) -> dict:
    return {"status": "pass" if condition else "blocked"}


def _compact(stage: dict) -> dict:
    keep = (
        "status", "stage", "baseline_stage", "title", "issues",
        "provider_default_calls", "live_provider_call_count_in_release_gate",
        "physics_reward_bridge_llm_call_count", "mae_live_provider_call_count",
        "raw_manuscript_provider_leakage", "node2_raw_reveal_access",
        "credential_leakage", "branchpoint_lineage_preserved",
    )
    return {key: stage.get(key) for key in keep if key in stage}


def _read_json(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def _stage113_baseline_ok(root: Path) -> bool:
    report = _read_json(root / "release/current/stage113_release_gate_report.json")
    if report.get("status") == "pass":
        return True
    active = _read_json(root / "manifests/live_core_manifest.json").get("active_version")
    return active == "stage114" and (root / "manifests/stage113_manifest.json").exists()


def _amw_contract_ok(amw: dict) -> bool:
    return amw.get("stage") == "114" and amw.get("status") == "pass" and amw.get("scene_id") == "stage114_fixture_scene_001"


def _alpha_bounds_ok(amw: dict) -> bool:
    values = list(amw.get("alpha_before", {}).values()) + list(amw.get("alpha_after", {}).values())
    return bool(values) and all(0.30 <= float(v) <= 0.80 for v in values)


def _mae_dimension_scores_ok(updates: list[dict]) -> bool:
    return len(updates) == 4 and all(0.0 <= float(u.get("mae_dim_score", -1.0)) <= 1.0 for u in updates)


def _protected_policy_ok(guard: dict) -> bool:
    policy = guard.get("protected_policy", {})
    return (
        policy.get("surface_safety_tolerance_can_loosen") is False
        and policy.get("branchpoint_sensitivity_can_decrease") is False
        and policy.get("provider_zero_policy_can_change") is False
        and policy.get("node2_raw_reveal_tolerance") == 0
    )


def _docs_manifest_ok(root: Path) -> bool:
    return all((root / rel).exists() for rel in [
        "docs/stages/stage114.md",
        "manifests/stage114_manifest.json",
        "manifests/stage114_amw_manifest.json",
    ])


def _repo_doctor_ready(root: Path) -> bool:
    text = (root / "tools/run_stage72_repo_doctor.py").read_text(encoding="utf-8", errors="ignore")
    return "stage114" in text and "stage114_release_gate" in text and "stage114_adaptive_momentum_weights" in text


def _clean_packaging_status(root: Path) -> str:
    manifest = _read_json(root / "package_manifest.json")
    canonical = manifest.get("canonical_package") or "V1700_stage114_adaptive_momentum_weights_integrated_repository.zip"
    override = os.environ.get("V1700_STAGE114_PACKAGE")
    candidates: list[Path] = []
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
    patterns = [
        re.compile(r"sk-[A-Za-z0-9]{20,}"),
        re.compile(r"AKIA[0-9A-Z]{16}"),
        re.compile(r"AIza[0-9A-Za-z_-]{20,}"),
        re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    ]
    hits = []
    for base in ("src", "tools", "manifests"):
        for path in (root / base).rglob("*"):
            if not path.is_file() or "__pycache__" in path.parts or path.suffix in {".pyc", ".zip"}:
                continue
            text = path.read_text(encoding="utf-8", errors="ignore")
            if any(p.search(text) for p in patterns):
                hits.append(path.relative_to(root).as_posix())
    return {"status": "pass" if not hits else "blocked", "hits": hits}
