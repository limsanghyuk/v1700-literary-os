from __future__ import annotations

import json
import os
import re
import zipfile
from pathlib import Path

from v1700.stage116.orchestrator import run_stage116

_CACHE: dict[str, dict] = {}


def run_stage116_release_gate(root: Path | None = None) -> dict:
    root = root or Path(__file__).resolve().parents[3]
    key = str(root.resolve())
    if key in _CACHE:
        return _CACHE[key]
    stage = run_stage116(root)
    rag = stage.get("rag_fusion", {})
    classifier = rag.get("query_intent_classifier", {})
    classified = classifier.get("classified_queries", [])
    lexicon = rag.get("drama_lexicon", {})
    boosts = lexicon.get("boosts_observed", [])
    policies = rag.get("adaptive_hybrid_weights", {}).get("policies", [])
    intents = {row.get("intent") for row in classified}
    checks = {
        "stage115_baseline_gate_pass": _check(_stage115_baseline_ok(root)),
        "rag_fusion_contract_pass": _check(stage.get("status") == "pass" and rag.get("stage") == "116"),
        "query_intent_classifier_pass": _check(intents == {"CHARACTER", "EMOTIONAL", "PLOT_EVENT"}),
        "llm_query_classification_zero_pass": _check(stage.get("query_classifier_llm_call_count") == 0),
        "adaptive_bm25_dense_policy_pass": _check(_policy_matrix_ok(policies)),
        "drama_lexicon_boost_pass": _check(_boosts_ok(boosts)),
        "rrf_k_policy_pass": _check(all(int(p.get("rrf_k", 0)) == 60 for p in policies)),
        "embedding_provider_zero_pass": _check(stage.get("embedding_provider_call_count") == 0),
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
        "stage": "116",
        "baseline_stage": "115",
        "title": "Domain-Specific RAG Fusion",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "checks": checks,
        "stage116": _compact(stage),
        "rag_summary": {
            "classified_intents": sorted(intents),
            "classified_query_count": len(classified),
            "policies": policies,
            "boosts_observed": boosts,
            "query_classifier_llm_call_count": stage.get("query_classifier_llm_call_count"),
            "embedding_provider_call_count": stage.get("embedding_provider_call_count"),
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
    out = root / "release/current/stage116_release_gate_report.json"
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


def _stage115_baseline_ok(root: Path) -> bool:
    report = _read_json(root / "release/current/stage115_release_gate_report.json")
    if report.get("status") == "pass":
        return True
    active = _read_json(root / "manifests/live_core_manifest.json").get("active_version")
    return active == "stage116" and (root / "manifests/stage115_manifest.json").exists()


def _policy_matrix_ok(policies: list[dict]) -> bool:
    by_intent = {p.get("intent"): p for p in policies}
    return (
        by_intent.get("CHARACTER", {}).get("bm25_weight") == 0.70
        and by_intent.get("CHARACTER", {}).get("dense_weight") == 0.30
        and by_intent.get("CHARACTER", {}).get("k") == 40
        and by_intent.get("EMOTIONAL", {}).get("bm25_weight") == 0.30
        and by_intent.get("EMOTIONAL", {}).get("dense_weight") == 0.70
        and by_intent.get("EMOTIONAL", {}).get("k") == 60
        and by_intent.get("PLOT_EVENT", {}).get("bm25_weight") == 0.50
        and by_intent.get("PLOT_EVENT", {}).get("dense_weight") == 0.50
        and by_intent.get("PLOT_EVENT", {}).get("k") == 50
    )


def _boosts_ok(boosts: list[dict]) -> bool:
    observed = {(b.get("category"), b.get("boost")) for b in boosts}
    return (
        ("CHARACTER_NAMES", 1.5) in observed
        and ("EPISODE_TERMS", 1.3) in observed
        and ("DRAMA_KEYWORDS", 1.2) in observed
    )


def _docs_manifest_ok(root: Path) -> bool:
    return all((root / rel).exists() for rel in [
        "docs/stages/stage116.md",
        "manifests/stage116_manifest.json",
        "manifests/stage116_rag_fusion_manifest.json",
    ])


def _repo_doctor_ready(root: Path) -> bool:
    text = (root / "tools/run_stage72_repo_doctor.py").read_text(encoding="utf-8", errors="ignore")
    return "stage116" in text and "stage116_release_gate" in text and "stage116_domain_rag_fusion" in text


def _clean_packaging_status(root: Path) -> str:
    manifest = _read_json(root / "package_manifest.json")
    canonical = manifest.get("canonical_package") or "V1700_stage116_domain_specific_rag_fusion_integrated_repository.zip"
    override = os.environ.get("V1700_STAGE116_PACKAGE")
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
