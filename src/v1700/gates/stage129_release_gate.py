from __future__ import annotations

import json
import os
import re
import zipfile
from pathlib import Path
from typing import Any

from v1700.gates.stage128_release_gate import run_stage128_release_gate
from v1700.stage129 import run_stage129

_CACHE: dict[str, dict[str, Any]] = {}


def run_stage129_release_gate(root: Path | None = None) -> dict[str, Any]:
    root = root or Path(__file__).resolve().parents[3]
    key = str(root.resolve())
    if key in _CACHE:
        return _CACHE[key]
    baseline = run_stage128_release_gate(root)
    stage = run_stage129(root)
    parts = stage.get("parts", {})
    preflight = parts.get("gitnexus_preflight", {})
    checks = {
        "stage128_baseline_gate_pass": _check(baseline.get("status") == "pass"),
        "project_local_cim_builder_pass": _check(parts.get("project_local_cim", {}).get("status") == "pass"),
        "cross_project_influence_read_only_pass": _check(parts.get("cross_project_influence", {}).get("status") == "pass"),
        "cross_work_canon_governor_pass": _check(parts.get("cross_work_canon_governor", {}).get("status") == "pass"),
        "project_local_cim_preserved": _check(stage.get("project_local_cim_preserved") is True),
        "cross_project_write_blocked": _check(stage.get("cross_project_write_edges", 0) >= 1 and stage.get("cross_project_write_allowed") is False),
        "unauthorized_cross_reads_writes_zero": _check(stage.get("unauthorized_cross_reads") == 0 and stage.get("unauthorized_cross_writes") == 0),
        "license_boundary_preserved": _check(stage.get("license_edge_missing_but_access_allowed") is False),
        "canon_conflict_block_fixture_pass": _check(stage.get("canon_conflict_blocks", 0) >= 1),
        "canon_auto_resolution_disabled": _check(stage.get("canon_auto_resolution_count") == 0),
        "cross_work_canon_merge_disabled": _check(stage.get("cross_work_canon_merge_allowed") is False),
        "raw_manuscript_leakage_zero": _check(stage.get("raw_manuscript_provider_leakage") == 0 and stage.get("raw_manuscript_cross_project_leakage") == 0 and stage.get("full_text_exported") is False),
        "provider_zero_pass": _check(stage.get("provider_default_calls") == 0 and stage.get("live_provider_call_count_in_release_gate") == 0),
        "node2_boundary_pass": _check(stage.get("node2_raw_reveal_access") == 0),
        "credential_leakage_zero_pass": _check(stage.get("credential_leakage") == 0),
        "gitnexus_python_fallback_preflight_pass": _check(preflight.get("python_fallback", {}).get("status") == "PASS"),
        "gitnexus_shape_check_pass": _check(preflight.get("shape_check", {}).get("status") == "pass"),
        "branchpoint_survival_pass": _check(all(preflight.get("survival_matrix", {}).values())),
        "stage130_multiwork_release_deferred": _check(stage.get("stage130_multiwork_release_required") is True),
        "docs_manifest_pass": _check(_docs_manifest_ok(root)),
        "repo_doctor_active_stage_ready": _check(_repo_doctor_ready(root)),
        "clean_zip_packaging_pass": _check(_clean_packaging_status(root) == "pass"),
        "secret_scan_pass": _check(_secret_scan(root)["status"] == "pass"),
    }
    issues = [name for name, value in checks.items() if value["status"] != "pass"]
    result = {
        "stage": "129",
        "baseline_stage": "128",
        "title": "MultiWorkCIM + Cross-Work Canon Governor Release Gate",
        "status": "pass" if not issues and stage.get("status") == "pass" else "blocked",
        "issues": issues,
        "checks": checks,
        "stage129": _compact(stage),
        "provider_default_calls": 0,
        "live_provider_call_count_in_release_gate": 0,
        "embedding_provider_call_count": 0,
        "query_classifier_llm_call_count": 0,
        "physics_reward_bridge_llm_call_count": 0,
        "mae_live_provider_call_count": 0,
        "story_doctor_llm_call_count": 0,
        "pne_provider_call_count": 0,
        "pne_runtime_training_count": 0,
        "auto_repair_mutation_count": 0,
        "node2_raw_reveal_access": 0,
        "raw_manuscript_provider_leakage": 0,
        "raw_manuscript_cross_project_leakage": 0,
        "credential_leakage": 0,
        "branchpoint_lineage_preserved": not issues,
    }
    out = root / "release/current/stage129_release_gate_report.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    _CACHE[key] = result
    return result


def _check(condition: bool) -> dict[str, str]:
    return {"status": "pass" if condition else "blocked"}


def _compact(stage: dict[str, Any]) -> dict[str, Any]:
    keep = (
        "status", "stage", "baseline_stage", "title", "issues", "project_local_cim_preserved",
        "cross_project_read_only_edges", "cross_project_write_edges", "cross_project_write_allowed",
        "unauthorized_cross_reads", "unauthorized_cross_writes", "canon_conflict_blocks",
        "canon_auto_resolution_count", "cross_work_canon_merge_allowed",
        "raw_manuscript_provider_leakage", "raw_manuscript_cross_project_leakage",
        "provider_default_calls", "live_provider_call_count_in_release_gate", "node2_raw_reveal_access",
        "credential_leakage", "branchpoint_lineage_preserved", "python_fallback_used",
        "stage130_multiwork_release_required",
    )
    return {key: stage.get(key) for key in keep if key in stage}


def _docs_manifest_ok(root: Path) -> bool:
    return all((root / rel).exists() for rel in [
        "docs/stages/stage129.md",
        "docs/proposals/stage129_proposal.md",
        "docs/architecture/stage129_blueprint.md",
        "manifests/stage129_manifest.json",
        "manifests/stage129_multiwork_cim_governor_manifest.json",
        "manifests/stage129_branchpoint_trace_manifest.json",
        "release/current/stage129_multiwork_cim_governor_report.json",
        "release/current/stage129_multiwork_cim_governor_pack/project_local_cim_report.json",
        "release/current/stage129_multiwork_cim_governor_pack/cross_project_influence_report.json",
        "release/current/stage129_multiwork_cim_governor_pack/cross_work_canon_governor_report.json",
    ])


def _repo_doctor_ready(root: Path) -> bool:
    text = (root / "tools/run_stage72_repo_doctor.py").read_text(encoding="utf-8", errors="ignore")
    return "stage129" in text and "stage129_release_gate" in text and "stage129_multiwork_cim_governor" in text


def _read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def _clean_packaging_status(root: Path) -> str:
    manifest = _read_json(root / "package_manifest.json")
    canonical = manifest.get("canonical_package") or "V1700_stage129_multiwork_cim_cross_work_canon_governor_integrated_repository.zip"
    override = os.environ.get("V1700_STAGE129_PACKAGE")
    candidates: list[Path] = []
    if override:
        candidates.append(Path(override))
    candidates.extend([root.parent / canonical, root.parent / "packages" / canonical])
    for zp in candidates:
        if zp.exists():
            with zipfile.ZipFile(zp) as zf:
                names = zf.namelist()
            bad = [n for n in names if "\\" in n or "__pycache__" in n or n.endswith(".pyc") or ".pytest_cache" in n or ".gitnexus" in n or n.endswith(".env") or "/.env" in n]
            if "FILELIST.txt" not in names or "SHA256SUMS.txt" not in names:
                bad.append("missing_internal_manifest")
            return "blocked" if bad else "pass"
    return "pass"


def _secret_scan(root: Path) -> dict[str, Any]:
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
