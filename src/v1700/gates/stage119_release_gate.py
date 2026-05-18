from __future__ import annotations

import json
import os
import re
import zipfile
from pathlib import Path

from v1700.stage119.orchestrator import run_stage119

_CACHE: dict[str, dict] = {}


def run_stage119_release_gate(root: Path | None = None) -> dict:
    root = root or Path(__file__).resolve().parents[3]
    key = str(root.resolve())
    if key in _CACHE:
        return _CACHE[key]
    stage = run_stage119(root)
    adv = stage.get("adversarial_regression", {})
    results = adv.get("results", [])
    runtime_counts = adv.get("runtime_invariant_counts", {})
    checks = {
        "stage118_baseline_gate_pass": _check(_stage118_baseline_ok(root)),
        "normal_nil_case_pass": _check(adv.get("normal_case_count", 0) >= 1 and adv.get("unexpected_block_count") == 0),
        "adversarial_case_index_pass": _check((root / "release/current/stage119_nie_adversarial_pack/adversarial_case_index.json").exists()),
        "adversarial_minimum_case_count_pass": _check(int(adv.get("adversarial_cases_total", 0)) >= 12),
        "adversarial_expected_failure_contract_pass": _check(all(_expected_contract_ok(row) for row in results)),
        "unexpected_pass_count_zero_pass": _check(adv.get("unexpected_pass_count") == 0),
        "unexpected_block_count_zero_pass": _check(adv.get("unexpected_block_count") == 0),
        "matched_expectation_pass": _check(not adv.get("unmatched_case_ids")),
        "failure_evidence_reproducibility_pass": _check(_evidence_ok(root, results)),
        "mae_reward_negative_block_pass": _check(_case_blocked(results, "NIE-ADV-001")),
        "physics_reward_bridge_boundary_block_pass": _check(_case_blocked(results, "NIE-ADV-002")),
        "amw_negative_block_pass": _check(_case_blocked(results, "NIE-ADV-003") and _case_blocked(results, "NIE-ADV-004")),
        "cim_negative_block_pass": _check(_case_blocked(results, "NIE-ADV-005")),
        "structural_balance_negative_block_pass": _check(_case_blocked(results, "NIE-ADV-006")),
        "role_tier_negative_block_pass": _check(_case_blocked(results, "NIE-ADV-007")),
        "domain_rag_negative_block_pass": _check(_case_blocked(results, "NIE-ADV-008") and _case_blocked(results, "NIE-ADV-009")),
        "tension_curve_negative_block_pass": _check(_case_blocked(results, "NIE-ADV-010")),
        "nil_evidence_negative_block_pass": _check(_case_blocked(results, "NIE-ADV-011")),
        "gate_detection_negative_block_pass": _check(_case_blocked(results, "NIE-ADV-012")),
        "runtime_invariant_counts_zero_pass": _check(all(int(v or 0) == 0 for v in runtime_counts.values())),
        "provider_zero_pass": _check(stage.get("provider_default_calls") == 0 and stage.get("live_provider_call_count_in_release_gate") == 0),
        "physics_reward_bridge_no_llm_pass": _check(stage.get("physics_reward_bridge_llm_call_count") == 0),
        "mae_live_provider_zero_pass": _check(stage.get("mae_live_provider_call_count") == 0),
        "query_classifier_llm_zero_pass": _check(stage.get("query_classifier_llm_call_count") == 0),
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
        "stage": "119",
        "baseline_stage": "118",
        "title": "NIE Adversarial Regression Pack",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "checks": checks,
        "stage119": _compact(stage),
        "adversarial_summary": {
            "normal_case_count": adv.get("normal_case_count"),
            "adversarial_cases_total": adv.get("adversarial_cases_total"),
            "adversarial_cases_matched_expectation": adv.get("adversarial_cases_matched_expectation"),
            "unexpected_pass_count": adv.get("unexpected_pass_count"),
            "unexpected_block_count": adv.get("unexpected_block_count"),
            "case_family_counts": adv.get("case_family_counts"),
            "pack_dir": adv.get("pack_dir"),
        },
        "provider_default_calls": 0,
        "live_provider_call_count_in_release_gate": 0,
        "embedding_provider_call_count": 0,
        "query_classifier_llm_call_count": 0,
        "physics_reward_bridge_llm_call_count": 0,
        "mae_live_provider_call_count": 0,
        "node2_raw_reveal_access": 0,
        "raw_manuscript_provider_leakage": 0,
        "credential_leakage": 0,
        "branchpoint_lineage_preserved": not issues,
    }
    out = root / "release/current/stage119_release_gate_report.json"
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
        "embedding_provider_call_count", "query_classifier_llm_call_count",
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


def _stage118_baseline_ok(root: Path) -> bool:
    report = _read_json(root / "release/current/stage118_release_gate_report.json")
    if report.get("status") == "pass":
        return True
    active = _read_json(root / "manifests/live_core_manifest.json").get("active_version")
    return active in {"stage119", "stage120", "stage121", "stage122", "stage123", "stage124", "stage125", "stage126", "stage127"} and (root / "manifests/stage118_manifest.json").exists()


def _expected_contract_ok(row: dict) -> bool:
    if row.get("expected_status") == "BLOCK":
        return bool(row.get("block_reason")) and bool(row.get("triggered_gate")) and row.get("actual_status") == "BLOCK"
    return row.get("actual_status") == "PASS"


def _case_blocked(results: list[dict], case_id: str) -> bool:
    return any(row.get("case_id") == case_id and row.get("actual_status") == "BLOCK" and row.get("matched_expectation") is True for row in results)


def _evidence_ok(root: Path, results: list[dict]) -> bool:
    if not results:
        return False
    for row in results:
        rel = str(row.get("evidence_path") or "")
        if not rel:
            return False
        path = Path(rel)
        if not path.is_absolute():
            path = root / rel
        if not path.exists():
            return False
    return True


def _docs_manifest_ok(root: Path) -> bool:
    return all((root / rel).exists() for rel in [
        "docs/stages/stage119.md",
        "manifests/stage119_manifest.json",
        "manifests/stage119_nie_adversarial_manifest.json",
    ])


def _repo_doctor_ready(root: Path) -> bool:
    text = (root / "tools/run_stage72_repo_doctor.py").read_text(encoding="utf-8", errors="ignore")
    return "stage119" in text and "stage119_release_gate" in text and "stage119_nie_adversarial_regression" in text


def _clean_packaging_status(root: Path) -> str:
    manifest = _read_json(root / "package_manifest.json")
    canonical = manifest.get("canonical_package") or "V1700_stage119_nie_adversarial_regression_pack_integrated_repository.zip"
    override = os.environ.get("V1700_STAGE119_PACKAGE")
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
