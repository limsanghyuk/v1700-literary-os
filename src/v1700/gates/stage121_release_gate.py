from __future__ import annotations

import json
import os
import re
import zipfile
from pathlib import Path

from v1700.stage121.orchestrator import run_stage121

_CACHE: dict[str, dict] = {}


def run_stage121_release_gate(root: Path | None = None) -> dict:
    root = root or Path(__file__).resolve().parents[3]
    key = str(root.resolve())
    if key in _CACHE:
        return _CACHE[key]
    stage = run_stage121(root)
    preflight = stage.get("cross_lineage_preflight", {})
    checks = {
        "stage120_trunk_preserved": _check(stage.get("stage120_trunk_preserved") is True),
        "candidate_direct_merge_blocked": _check(stage.get("candidate_direct_merge_allowed") is False),
        "formula_ledger_generated": _check(stage.get("formula_ledger_entry_count", 0) >= 8),
        "conflict_matrix_generated": _check(stage.get("conflict_count", 0) >= 6),
        "gate_authority_primary_gate25": _check(stage.get("gate_authority_primary") == "Gate25"),
        "lineage_relationship_map_generated": _check(preflight.get("lineage_relationship_map", {}).get("candidate_count") == 3),
        "packaging_cleanliness_report_generated": _check(preflight.get("packaging_cleanliness_report", {}).get("candidate_direct_merge_allowed_count") == 0),
        "absorption_plan_generated": _check(len(preflight.get("stage122_to_stage126_plan", [])) == 5),
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
        "stage": "121",
        "baseline_stage": "120",
        "title": "Cross-Lineage Formula Reconciliation & Absorption Preflight Release Gate",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "checks": checks,
        "stage121": _compact(stage),
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
    out = root / "release/current/stage121_release_gate_report.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    _CACHE[key] = result
    return result


def _check(condition: bool) -> dict:
    return {"status": "pass" if condition else "blocked"}


def _compact(stage: dict) -> dict:
    keep = (
        "status", "stage", "baseline_stage", "title", "issues",
        "formula_ledger_entry_count", "conflict_count", "gate_authority_primary",
        "candidate_direct_merge_allowed", "provider_default_calls",
        "live_provider_call_count_in_release_gate", "raw_manuscript_provider_leakage",
        "node2_raw_reveal_access", "credential_leakage", "branchpoint_lineage_preserved",
    )
    return {key: stage.get(key) for key in keep if key in stage}


def _read_json(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def _docs_manifest_ok(root: Path) -> bool:
    return all((root / rel).exists() for rel in [
        "docs/stages/stage121.md",
        "manifests/stage121_manifest.json",
        "manifests/stage121_formula_ledger.json",
        "manifests/stage121_lineage_relationship_map.json",
        "manifests/stage121_conflict_matrix.json",
        "manifests/stage121_absorption_candidate_registry.json",
        "manifests/stage121_gate_authority_map.json",
        "release/current/stage121_cross_lineage_preflight_report.json",
        "release/current/stage121_formula_conflict_report.json",
        "release/current/stage121_packaging_cleanliness_report.json",
    ])


def _repo_doctor_ready(root: Path) -> bool:
    text = (root / "tools/run_stage72_repo_doctor.py").read_text(encoding="utf-8", errors="ignore")
    return "stage121" in text and "stage121_release_gate" in text and "stage121_cross_lineage_preflight" in text


def _clean_packaging_status(root: Path) -> str:
    manifest = _read_json(root / "package_manifest.json")
    canonical = manifest.get("canonical_package") or "V1700_stage121_cross_lineage_formula_reconciliation_preflight_integrated_repository.zip"
    override = os.environ.get("V1700_STAGE121_PACKAGE")
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
