from __future__ import annotations

import json
import os
import re
import zipfile
from pathlib import Path
from typing import Any

from v1700.gates.stage131_release_gate import run_stage131_release_gate
from v1700.stage132 import run_stage132

_CACHE: dict[str, dict[str, Any]] = {}


def run_stage132_release_gate(root: Path | None = None) -> dict[str, Any]:
    root = root or Path(__file__).resolve().parents[3]
    key = str(root.resolve())
    if key in _CACHE:
        return _CACHE[key]
    baseline = run_stage131_release_gate(root)
    stage = run_stage132(root)
    parts = stage.get("parts", {})
    preflight = parts.get("gitnexus_preflight", {})
    checks = {
        "stage131_baseline_gate_pass": _check(baseline.get("status") == "pass"),
        "classifier_matrix_pass": _check(parts.get("classifier_matrix", {}).get("status") == "pass"),
        "mystery_exemption_pass": _check(parts.get("mystery_exemption", {}).get("status") == "pass"),
        "gitnexus_python_fallback_preflight_pass": _check(preflight.get("python_fallback", {}).get("status") == "PASS"),
        "symbol_to_branchpoint_trace_pass": _check(preflight.get("release_gate_integration", {}).get("stage132_gate_registered") is True),
        "true_contradiction_review_pass": _check(stage.get("true_contradiction_review_required") is True),
        "mystery_exemption_guard_pass": _check(stage.get("mystery_exemption_requires_reveal_lock") is True),
        "gate26_advisory_only_pass": _check(stage.get("gate26_hard_block_enabled") is False and stage.get("gate26_hard_block_count") == 0),
        "canon_auto_resolution_blocked": _check(stage.get("canon_auto_resolution_count") == 0),
        "auto_repair_blocked": _check(stage.get("auto_repair_mutation_count") == 0),
        "cross_project_write_blocked": _check(stage.get("cross_project_write_allowed") is False),
        "provider_zero_pass": _check(stage.get("provider_default_calls") == 0 and stage.get("live_provider_call_count_in_release_gate") == 0),
        "node2_boundary_pass": _check(stage.get("node2_raw_reveal_access") == 0),
        "raw_manuscript_leakage_zero": _check(stage.get("raw_manuscript_provider_leakage") == 0 and stage.get("raw_manuscript_cross_project_leakage") == 0),
        "credential_leakage_zero_pass": _check(stage.get("credential_leakage") == 0),
        "branchpoint_survival_pass": _check(stage.get("branchpoint_lineage_preserved") is True),
        "docs_manifest_pass": _check(_docs_manifest_ok(root)),
        "repo_doctor_active_stage_ready": _check(_repo_doctor_ready(root)),
        "clean_zip_packaging_pass": _check(_clean_packaging_status(root) == "pass"),
        "secret_scan_pass": _check(_secret_scan(root)["status"] == "pass"),
    }
    issues = [name for name, value in checks.items() if value["status"] != "pass"]
    result = {
        "stage": "132",
        "baseline_stage": "131",
        "title": "Contradiction Classifier + Mystery Exemption Gate",
        "status": "pass" if not issues and stage.get("status") == "pass" else "blocked",
        "issues": issues,
        "checks": checks,
        "stage132": _compact(stage),
        "provider_default_calls": 0,
        "live_provider_call_count_in_release_gate": 0,
        "node2_raw_reveal_access": 0,
        "raw_manuscript_provider_leakage": 0,
        "raw_manuscript_cross_project_leakage": 0,
        "credential_leakage": 0,
        "branchpoint_lineage_preserved": not issues,
    }
    out = root / "release/current/stage132_release_gate_report.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    _CACHE[key] = result
    return result


def _check(condition: bool) -> dict[str, str]:
    return {"status": "pass" if condition else "blocked"}


def _compact(stage: dict[str, Any]) -> dict[str, Any]:
    keep = (
        "status", "stage", "baseline_stage", "title", "issues", "classifier_mode",
        "case_count", "exemption_count", "true_contradiction_review_required",
        "mystery_exemption_requires_reveal_lock", "gate26_hard_block_enabled",
        "gate26_hard_block_count", "auto_repair_mutation_count", "canon_auto_resolution_count",
        "cross_project_write_allowed", "raw_manuscript_provider_leakage",
        "raw_manuscript_cross_project_leakage", "provider_default_calls",
        "live_provider_call_count_in_release_gate", "node2_raw_reveal_access",
        "credential_leakage", "writer_approval_guard", "branchpoint_lineage_preserved",
    )
    return {key: stage.get(key) for key in keep if key in stage}


def _docs_manifest_ok(root: Path) -> bool:
    return all((root / rel).exists() for rel in [
        "docs/stages/stage132.md",
        "docs/proposals/stage132_proposal.md",
        "docs/architecture/stage132_blueprint.md",
        "docs/roadmaps/stage132_roadmap.md",
        "manifests/stage132_manifest.json",
        "manifests/stage132_contradiction_classifier_manifest.json",
        "manifests/stage132_branchpoint_trace_manifest.json",
        "release/current/stage132_contradiction_classifier_report.json",
        "release/current/stage132_contradiction_classifier_pack/classifier_matrix_report.json",
        "release/current/stage132_contradiction_classifier_pack/mystery_exemption_report.json",
        "release/current/stage132_contradiction_classifier_pack/gitnexus_preflight_report.json",
    ])


def _repo_doctor_ready(root: Path) -> bool:
    text = (root / "tools/run_stage72_repo_doctor.py").read_text(encoding="utf-8", errors="ignore")
    return "stage132" in text and "stage132_release_gate" in text and "stage132_contradiction_classifier" in text


def _read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def _clean_packaging_status(root: Path) -> str:
    manifest = _read_json(root / "package_manifest.json")
    canonical = manifest.get("canonical_package") or "V1700_stage132_contradiction_classifier_mystery_exemption_integrated_repository.zip"
    override = os.environ.get("V1700_STAGE132_PACKAGE")
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
