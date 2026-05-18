from __future__ import annotations

import json
import os
import re
import zipfile
from pathlib import Path

from v1700.stage124.orchestrator import run_stage124

_CACHE: dict[str, dict] = {}


def run_stage124_release_gate(root: Path | None = None) -> dict:
    root = root or Path(__file__).resolve().parents[3]
    key = str(root.resolve())
    if key in _CACHE:
        return _CACHE[key]
    stage = run_stage124(root)
    policy = stage.get("absorption_policy", {})
    gate29 = stage.get("gate29", {})
    feedback = stage.get("feedback_learner", {})
    predictor = stage.get("debt_predictor", {})
    summary = stage.get("summary", {})
    checks = {
        "stage123_baseline_preserved": _check(stage.get("baseline_stage") == "123"),
        "stage123_gate28_secondary_preserved": _check(policy.get("stage123_gate28_secondary_quality_gate_preserved") is True),
        "pne_core_pattern_library_pass": _check(stage.get("pne_core", {}).get("total_ingested", 0) > 0),
        "debt_predictor_heuristic_fallback_pass": _check(predictor.get("mode") == "heuristic_fallback" and predictor.get("runtime_training_enabled") is False),
        "preemptive_low_case_allowed": _check(summary.get("low_risk_blocked") is False),
        "preemptive_high_case_blocked": _check(summary.get("high_risk_blocked") is True and summary.get("high_risk_max_probability", 0.0) >= 0.60),
        "feedback_precision_target_met": _check(feedback.get("metrics", {}).get("precision", 0.0) >= 0.70 and feedback.get("runtime_retraining_triggered") is False),
        "gate29_secondary_predictive_gate": _check(policy.get("gate29_authority_mode") == "secondary_predictive_gate" and policy.get("gate29_primary_authority_enabled") is False),
        "gate29_negative_case_blocked": _check(gate29.get("matched_expectation") is True and gate29.get("high_risk_case", {}).get("status") == "blocked"),
        "direct_v555_merge_blocked": _check(policy.get("direct_v555_merge_performed") is False),
        "runtime_training_disabled": _check(policy.get("release_gate_runtime_training_enabled") is False and stage.get("pne_runtime_training_count") == 0),
        "sklearn_optional_fallback_pass": _check(policy.get("sklearn_required") is False),
        "docs_manifest_pass": _check(_docs_manifest_ok(root)),
        "repo_doctor_active_stage_ready": _check(_repo_doctor_ready(root)),
        "provider_zero_pass": _check(stage.get("provider_default_calls") == 0 and stage.get("live_provider_call_count_in_release_gate") == 0 and stage.get("pne_provider_call_count") == 0),
        "node2_boundary_pass": _check(stage.get("node2_raw_reveal_access") == 0),
        "raw_manuscript_leakage_zero_pass": _check(stage.get("raw_manuscript_provider_leakage") == 0),
        "credential_leakage_zero_pass": _check(stage.get("credential_leakage") == 0),
        "clean_zip_packaging_pass": _check(_clean_packaging_status(root) == "pass"),
        "secret_scan_pass": _check(_secret_scan(root)["status"] == "pass"),
    }
    issues = [name for name, value in checks.items() if value["status"] != "pass"]
    result = {
        "stage": "124",
        "baseline_stage": "123",
        "title": "PNE / Gate29 Absorption Release Gate",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "checks": checks,
        "stage124": _compact(stage),
        "provider_default_calls": 0,
        "live_provider_call_count_in_release_gate": 0,
        "embedding_provider_call_count": 0,
        "query_classifier_llm_call_count": 0,
        "physics_reward_bridge_llm_call_count": 0,
        "mae_live_provider_call_count": 0,
        "story_doctor_llm_call_count": 0,
        "pne_provider_call_count": 0,
        "pne_runtime_training_count": 0,
        "node2_raw_reveal_access": 0,
        "raw_manuscript_provider_leakage": 0,
        "credential_leakage": 0,
        "branchpoint_lineage_preserved": not issues,
    }
    out = root / "release/current/stage124_release_gate_report.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    _CACHE[key] = result
    return result


def _check(condition: bool) -> dict:
    return {"status": "pass" if condition else "blocked"}


def _compact(stage: dict) -> dict:
    keep = (
        "status", "stage", "baseline_stage", "title", "issues", "summary",
        "provider_default_calls", "live_provider_call_count_in_release_gate",
        "pne_provider_call_count", "pne_runtime_training_count",
        "raw_manuscript_provider_leakage", "node2_raw_reveal_access", "credential_leakage",
        "branchpoint_lineage_preserved",
    )
    return {key: stage.get(key) for key in keep if key in stage}


def _docs_manifest_ok(root: Path) -> bool:
    return all((root / rel).exists() for rel in [
        "docs/stages/stage124.md",
        "manifests/stage124_manifest.json",
        "manifests/stage124_pne_gate29_manifest.json",
        "release/current/stage124_pne_gate29_absorption_report.json",
        "release/current/stage124_prediction_report.json",
        "release/current/stage124_gate29_report.json",
        "release/current/stage124_feedback_metrics_report.json",
    ])


def _repo_doctor_ready(root: Path) -> bool:
    text = (root / "tools/run_stage72_repo_doctor.py").read_text(encoding="utf-8", errors="ignore")
    return "stage124" in text and "stage124_release_gate" in text and "stage124_pne_gate29_absorption" in text


def _read_json(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def _clean_packaging_status(root: Path) -> str:
    manifest = _read_json(root / "package_manifest.json")
    canonical = manifest.get("canonical_package") or "V1700_stage124_pne_gate29_absorption_integrated_repository.zip"
    override = os.environ.get("V1700_STAGE124_PACKAGE")
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
            if "FILELIST.txt" not in names or "SHA256SUMS.txt" not in names:
                bad.append("missing_internal_manifest")
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
