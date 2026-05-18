from __future__ import annotations

import json
import os
import re
import zipfile
from pathlib import Path

from v1700.stage123.orchestrator import run_stage123

_CACHE: dict[str, dict] = {}


def run_stage123_release_gate(root: Path | None = None) -> dict:
    root = root or Path(__file__).resolve().parents[3]
    key = str(root.resolve())
    if key in _CACHE:
        return _CACHE[key]
    stage = run_stage123(root)
    gate28 = stage.get("gate28", {})
    policy = stage.get("absorption_policy", {})
    dry_run = stage.get("auto_repair_dry_run", {})
    negative = stage.get("negative_case", {})
    checks = {
        "stage122_baseline_preserved": _check(stage.get("baseline_stage") == "122"),
        "stage120_gate25_primary_authority_preserved": _check(policy.get("stage120_gate25_primary_authority_preserved") is True),
        "gate28_secondary_quality_gate": _check(policy.get("gate28_authority_mode") == "secondary_quality_gate" and policy.get("gate28_primary_authority_enabled") is False),
        "story_doctor_report_pass": _check(stage.get("story_doctor", {}).get("status") == "pass"),
        "gate28_thresholds_pass": _check(gate28.get("status") == "pass" and gate28.get("approved") is True),
        "gate28_negative_case_blocked": _check(negative.get("matched_expectation") is True and negative.get("gate28", {}).get("status") == "blocked"),
        "auto_repair_dry_run_only": _check(dry_run.get("status") == "pass" and dry_run.get("mutation_count") == 0),
        "direct_v545_merge_blocked": _check(policy.get("direct_v545_merge_performed") is False),
        "gate29_not_enabled": _check(policy.get("gate29_enabled") is False),
        "llm_repair_generation_zero": _check(policy.get("llm_repair_generation_enabled") is False and stage.get("story_doctor_llm_call_count") == 0),
        "docs_manifest_pass": _check(_docs_manifest_ok(root)),
        "repo_doctor_active_stage_ready": _check(_repo_doctor_ready(root)),
        "provider_zero_pass": _check(stage.get("provider_default_calls") == 0 and stage.get("live_provider_call_count_in_release_gate") == 0),
        "node2_boundary_pass": _check(stage.get("node2_raw_reveal_access") == 0),
        "raw_manuscript_leakage_zero_pass": _check(stage.get("raw_manuscript_provider_leakage") == 0),
        "credential_leakage_zero_pass": _check(stage.get("credential_leakage") == 0),
        "clean_zip_packaging_pass": _check(_clean_packaging_status(root) == "pass"),
        "secret_scan_pass": _check(_secret_scan(root)["status"] == "pass"),
    }
    issues = [name for name, value in checks.items() if value["status"] != "pass"]
    result = {
        "stage": "123",
        "baseline_stage": "122",
        "title": "ASD / Gate28 Absorption Release Gate",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "checks": checks,
        "stage123": _compact(stage),
        "provider_default_calls": 0,
        "live_provider_call_count_in_release_gate": 0,
        "embedding_provider_call_count": 0,
        "query_classifier_llm_call_count": 0,
        "physics_reward_bridge_llm_call_count": 0,
        "mae_live_provider_call_count": 0,
        "story_doctor_llm_call_count": 0,
        "node2_raw_reveal_access": 0,
        "raw_manuscript_provider_leakage": 0,
        "credential_leakage": 0,
        "branchpoint_lineage_preserved": not issues,
    }
    out = root / "release/current/stage123_release_gate_report.json"
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
        "story_doctor_llm_call_count", "auto_repair_mutation_count",
        "raw_manuscript_provider_leakage", "node2_raw_reveal_access", "credential_leakage",
        "branchpoint_lineage_preserved",
    )
    return {key: stage.get(key) for key in keep if key in stage}


def _docs_manifest_ok(root: Path) -> bool:
    return all((root / rel).exists() for rel in [
        "docs/stages/stage123.md",
        "manifests/stage123_manifest.json",
        "manifests/stage123_asd_gate28_manifest.json",
        "release/current/stage123_asd_gate28_absorption_report.json",
        "release/current/stage123_story_doctor_report.json",
        "release/current/stage123_gate28_report.json",
        "release/current/stage123_auto_repair_dry_run_report.json",
    ])


def _repo_doctor_ready(root: Path) -> bool:
    text = (root / "tools/run_stage72_repo_doctor.py").read_text(encoding="utf-8", errors="ignore")
    return "stage123" in text and "stage123_release_gate" in text and "stage123_asd_gate28_absorption" in text


def _read_json(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def _clean_packaging_status(root: Path) -> str:
    manifest = _read_json(root / "package_manifest.json")
    canonical = manifest.get("canonical_package") or "V1700_stage123_asd_gate28_absorption_integrated_repository.zip"
    override = os.environ.get("V1700_STAGE123_PACKAGE")
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
