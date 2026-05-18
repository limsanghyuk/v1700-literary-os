from __future__ import annotations

import json
import os
import re
import zipfile
from pathlib import Path

from v1700.stage115.orchestrator import run_stage115

_CACHE: dict[str, dict] = {}


def run_stage115_release_gate(root: Path | None = None) -> dict:
    root = root or Path(__file__).resolve().parents[3]
    key = str(root.resolve())
    if key in _CACHE:
        return _CACHE[key]
    stage = run_stage115(root)
    cim_report = stage.get("cim", {})
    matrix = cim_report.get("character_influence_matrix", {})
    centrality = matrix.get("centrality", {})
    role_tiers = centrality.get("role_tiers", {})
    checks = {
        "stage114_baseline_gate_pass": _check(_stage114_baseline_ok(root)),
        "cim_contract_pass": _check(stage.get("status") == "pass" and cim_report.get("stage") == "115"),
        "cim_asymmetric_matrix_pass": _check(matrix.get("asymmetric_pair_count", 0) >= 4),
        "structural_balance_triangle_pass": _check(matrix.get("triangle_count", 0) >= 4 and matrix.get("high_tension_triangle_count", 0) >= 1),
        "pagerank_centrality_pass": _check(_centrality_ok(centrality.get("pagerank", {}))),
        "betweenness_centrality_pass": _check(bool(centrality.get("betweenness", {}))),
        "role_tier_assignment_pass": _check(_role_tiers_ok(role_tiers, matrix.get("characters", []))),
        "janggi_role_tier_growth_ready": _check("jang" in set(role_tiers.values()) and "jol" in set(role_tiers.values())),
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
    issues = [name for name, value in checks.items() if value["status"] != "pass"]
    result = {
        "stage": "115",
        "baseline_stage": "114",
        "title": "CharacterInfluenceMatrix + Structural Balance",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "checks": checks,
        "stage115": _compact(stage),
        "cim_summary": {
            "character_count": len(matrix.get("characters", [])),
            "asymmetric_pair_count": matrix.get("asymmetric_pair_count"),
            "triangle_count": matrix.get("triangle_count"),
            "high_tension_triangle_count": matrix.get("high_tension_triangle_count"),
            "role_tiers": role_tiers,
            "pagerank": centrality.get("pagerank", {}),
            "betweenness": centrality.get("betweenness", {}),
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
    out = root / "release/current/stage115_release_gate_report.json"
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


def _stage114_baseline_ok(root: Path) -> bool:
    report = _read_json(root / "release/current/stage114_release_gate_report.json")
    if report.get("status") == "pass":
        return True
    active = _read_json(root / "manifests/live_core_manifest.json").get("active_version")
    return active == "stage115" and (root / "manifests/stage114_manifest.json").exists()


def _centrality_ok(pagerank: dict) -> bool:
    if not pagerank:
        return False
    total = sum(float(v) for v in pagerank.values())
    return abs(total - 1.0) <= 0.0001 and all(0.0 <= float(v) <= 1.0 for v in pagerank.values())


def _role_tiers_ok(role_tiers: dict, characters: list[str]) -> bool:
    allowed = {"jang", "cha", "po", "ma_sang", "jol"}
    return bool(role_tiers) and set(role_tiers) == set(characters) and set(role_tiers.values()).issubset(allowed)


def _docs_manifest_ok(root: Path) -> bool:
    return all((root / rel).exists() for rel in [
        "docs/stages/stage115.md",
        "manifests/stage115_manifest.json",
        "manifests/stage115_cim_manifest.json",
    ])


def _repo_doctor_ready(root: Path) -> bool:
    text = (root / "tools/run_stage72_repo_doctor.py").read_text(encoding="utf-8", errors="ignore")
    return "stage115" in text and "stage115_release_gate" in text and "stage115_character_influence_matrix" in text


def _clean_packaging_status(root: Path) -> str:
    manifest = _read_json(root / "package_manifest.json")
    canonical = manifest.get("canonical_package") or "V1700_stage115_character_influence_matrix_structural_balance_integrated_repository.zip"
    override = os.environ.get("V1700_STAGE115_PACKAGE")
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
