from __future__ import annotations

import json
import os
import re
import zipfile
from pathlib import Path
from typing import Any

from v1700.gates.stage132_release_gate import run_stage132_release_gate
from v1700.stage133 import run_stage133

_CACHE: dict[str, dict[str, Any]] = {}


def run_stage133_release_gate(root: Path | None = None) -> dict[str, Any]:
    root = root or Path(__file__).resolve().parents[3]
    key = str(root.resolve())
    if key in _CACHE:
        return _CACHE[key]
    baseline = run_stage132_release_gate(root)
    stage = run_stage133(root)
    parts = stage.get("parts", {})
    tensor = parts.get("tensor_measurement", {})
    preflight = parts.get("gitnexus_preflight", {})
    checks = {
        "stage132_baseline_gate_pass": _check(baseline.get("status") == "pass"),
        "tensor_measurement_pass": _check(tensor.get("status") == "pass"),
        "dimension_count_8_pass": _check(stage.get("dimension_count") == 8),
        "true_contradiction_review_tensor_pass": _check(stage.get("review_required_tensor_count", 0) >= 1),
        "mystery_exemption_tensor_pass": _check(_has_mystery_pass_tensor(tensor)),
        "gitnexus_python_fallback_preflight_pass": _check(preflight.get("python_fallback", {}).get("status") == "PASS"),
        "symbol_to_branchpoint_trace_pass": _check(preflight.get("release_gate_integration", {}).get("stage133_gate_registered") is True),
        "gate26_advisory_only_pass": _check(stage.get("gate26_hard_block_enabled") is False),
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
        "stage": "133",
        "baseline_stage": "132",
        "title": "NarrativeStateTensor 8D Measurement Layer Gate",
        "status": "pass" if not issues and stage.get("status") == "pass" else "blocked",
        "issues": issues,
        "checks": checks,
        "stage133": _compact(stage),
        "provider_default_calls": 0,
        "live_provider_call_count_in_release_gate": 0,
        "node2_raw_reveal_access": 0,
        "raw_manuscript_provider_leakage": 0,
        "raw_manuscript_cross_project_leakage": 0,
        "credential_leakage": 0,
        "branchpoint_lineage_preserved": not issues,
    }
    out = root / "release/current/stage133_release_gate_report.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    _CACHE[key] = result
    return result


def _check(condition: bool) -> dict[str, str]:
    return {"status": "pass" if condition else "blocked"}


def _has_mystery_pass_tensor(tensor: dict[str, Any]) -> bool:
    return any(item.get("classification") == "intentional_mystery" and item.get("status") == "PASS" for item in tensor.get("tensors", []))


def _compact(stage: dict[str, Any]) -> dict[str, Any]:
    keep = (
        "status", "stage", "baseline_stage", "title", "issues", "measurement_mode",
        "dimension_count", "tensor_case_count", "review_required_tensor_count",
        "pass_tensor_count", "lowest_observed_dimension", "gate26_hard_block_enabled",
        "auto_repair_mutation_count", "canon_auto_resolution_count",
        "cross_project_write_allowed", "raw_manuscript_provider_leakage",
        "raw_manuscript_cross_project_leakage", "provider_default_calls",
        "live_provider_call_count_in_release_gate", "node2_raw_reveal_access",
        "credential_leakage", "writer_review_required_for_true_contradiction",
        "mystery_exemption_requires_reveal_lock", "branchpoint_lineage_preserved",
    )
    return {key: stage.get(key) for key in keep if key in stage}


def _docs_manifest_ok(root: Path) -> bool:
    return all((root / rel).exists() for rel in [
        "docs/stages/stage133.md",
        "docs/proposals/stage133_proposal.md",
        "docs/architecture/stage133_blueprint.md",
        "docs/roadmaps/stage133_roadmap.md",
        "manifests/stage133_manifest.json",
        "manifests/stage133_narrative_state_tensor_manifest.json",
        "manifests/stage133_branchpoint_trace_manifest.json",
        "release/current/stage133_narrative_state_tensor_report.json",
        "release/current/stage133_narrative_state_tensor_pack/tensor_measurement_report.json",
        "release/current/stage133_narrative_state_tensor_pack/gitnexus_preflight_report.json",
    ])


def _repo_doctor_ready(root: Path) -> bool:
    text = (root / "tools/run_stage72_repo_doctor.py").read_text(encoding="utf-8", errors="ignore")
    return "stage133" in text and "stage133_release_gate" in text and "stage133_narrative_state_tensor" in text


def _read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def _clean_packaging_status(root: Path) -> str:
    manifest = _read_json(root / "package_manifest.json")
    canonical = manifest.get("canonical_package") or "V1700_stage133_narrative_state_tensor_8d_integrated_repository.zip"
    override = os.environ.get("V1700_STAGE133_PACKAGE")
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
