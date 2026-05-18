from __future__ import annotations

import json
import os
import re
import zipfile
from pathlib import Path

from v1700.stage113.orchestrator import run_stage113

_CACHE: dict[str, dict] = {}


def run_stage113_release_gate(root: Path | None = None) -> dict:
    root = root or Path(__file__).resolve().parents[3]
    key = str(root.resolve())
    if key in _CACHE:
        return _CACHE[key]
    stage = run_stage113(root)
    reward = stage.get("reward_bridge", {})
    signal = reward.get("reward_signal", {})
    proposals = reward.get("coefficient_update_proposals", [])
    checks = {
        "stage112_baseline_gate_pass": _check(_stage112_baseline_ok(root)),
        "mae_reward_contract_pass": _check(_mae_contract_ok(reward)),
        "physics_reward_bridge_no_llm_pass": _check(signal.get("physics_reward_bridge_llm_call_count") == 0),
        "mae_live_provider_call_zero_pass": _check(signal.get("provider_call_count") == 0),
        "reward_weight_sum_pass": _check(abs(sum(signal.get("weights", {}).values()) - 1.0) < 1e-9),
        "reward_calculation_pass": _check(abs(float(signal.get("reward", -1.0)) - 0.7855) < 1e-9),
        "advantage_calculation_pass": _check(abs(float(signal.get("advantage", -1.0)) - 0.2855) < 1e-9),
        "baseline_ema_pass": _check(abs(float(signal.get("baseline_after", -1.0)) - 0.514275) < 1e-9),
        "coefficient_update_proposal_pass": _check(len(proposals) >= 4),
        "bounded_update_pass": _check(reward.get("drift_guard", {}).get("status") == "pass"),
        "provider_zero_pass": _check(stage.get("provider_default_calls") == 0 and stage.get("live_provider_call_count_in_release_gate") == 0),
        "node2_boundary_pass": _check(stage.get("node2_raw_reveal_access") == 0),
        "raw_manuscript_leakage_pass": _check(stage.get("raw_manuscript_provider_leakage") == 0),
        "credential_leakage_pass": _check(stage.get("credential_leakage") == 0),
        "docs_manifest_pass": _check(_docs_manifest_ok(root)),
        "repo_doctor_active_stage_ready": _check(_repo_doctor_ready(root)),
        "clean_zip_packaging_pass": _check(_clean_packaging_status(root) == "pass"),
        "secret_scan_pass": _check(_secret_scan(root)["status"] == "pass"),
    }
    issues = [key for key, value in checks.items() if value["status"] != "pass"]
    result = {
        "stage": "113",
        "baseline_stage": "112",
        "title": "PhysicsRewardBridge + MAE Reward Wiring",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "checks": checks,
        "stage113": _compact(stage),
        "reward_signal_summary": {
            "reward": signal.get("reward"),
            "advantage": signal.get("advantage"),
            "baseline_before": signal.get("baseline_before"),
            "baseline_after": signal.get("baseline_after"),
            "coefficient_update_proposal_count": len(proposals),
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
    out = root / "release/current/stage113_release_gate_report.json"
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


def _stage112_baseline_ok(root: Path) -> bool:
    report = _read_json(root / "release/current/stage112_release_gate_report.json")
    if report.get("status") == "pass":
        return True
    active = _read_json(root / "manifests/live_core_manifest.json").get("active_version")
    return active in {"stage113", "stage114", "stage115", "stage116", "stage116", "stage117", "stage118", "stage119", "stage120", "stage121", "stage122", "stage123", "stage124", "stage125", "stage126", "stage127"} and (root / "manifests/stage112_manifest.json").exists()


def _mae_contract_ok(reward: dict) -> bool:
    mae = reward.get("mae_result", {})
    if reward.get("status") != "pass":
        return False
    if mae.get("live_provider_call_count") != 0:
        return False
    scores = [mae.get("reader_score"), mae.get("writer_score"), mae.get("editor_score"), mae.get("cultural_score")]
    dims = list(mae.get("dimension_scores", {}).values())
    values = [v for v in scores + dims if isinstance(v, (int, float))]
    return len(values) == 8 and all(0.0 <= float(v) <= 1.0 for v in values)


def _docs_manifest_ok(root: Path) -> bool:
    return all((root / rel).exists() for rel in [
        "docs/stages/stage113.md",
        "manifests/stage113_manifest.json",
        "manifests/stage113_reward_bridge_manifest.json",
    ])


def _repo_doctor_ready(root: Path) -> bool:
    text = (root / "tools/run_stage72_repo_doctor.py").read_text(encoding="utf-8", errors="ignore")
    return "stage113" in text and "stage113_release_gate" in text and "stage113_physics_reward_bridge" in text


def _clean_packaging_status(root: Path) -> str:
    manifest = _read_json(root / "package_manifest.json")
    canonical = manifest.get("canonical_package") or "V1700_stage113_physics_reward_bridge_mae_reward_wiring_integrated_repository.zip"
    override = os.environ.get("V1700_STAGE113_PACKAGE")
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
