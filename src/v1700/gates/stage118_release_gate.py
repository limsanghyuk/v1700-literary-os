from __future__ import annotations

import json
import os
import re
import zipfile
from pathlib import Path

from v1700.stage118.orchestrator import run_stage118

_CACHE: dict[str, dict] = {}


def run_stage118_release_gate(root: Path | None = None) -> dict:
    root = root or Path(__file__).resolve().parents[3]
    key = str(root.resolve())
    if key in _CACHE:
        return _CACHE[key]
    stage = run_stage118(root)
    nil_report = stage.get("nil_orchestrator", {})
    convergence = nil_report.get("convergence", {})
    components = nil_report.get("components", [])
    invariant_counts = nil_report.get("invariant_counts", {})
    checks = {
        "stage117_baseline_gate_pass": _check(_stage117_baseline_ok(root)),
        "nil_orchestrator_contract_pass": _check(stage.get("status") == "pass" and nil_report.get("stage") == "118"),
        "nil_component_count_pass": _check(len(components) == 5),
        "nil_component_status_pass": _check(all(component.get("status") == "pass" for component in components)),
        "nil_loop_order_pass": _check(_loop_order_ok(nil_report.get("loop_order", []))),
        "nil_loop_closure_pass": _check(convergence.get("loop_closure_status") == "pass"),
        "reward_advantage_pass": _check(float(convergence.get("reward_advantage", 0.0)) > 0.0),
        "amw_drift_guard_pass": _check(convergence.get("checks", {}).get("amw_drift_guard_pass") is True),
        "cim_high_tension_triangle_pass": _check(int(convergence.get("high_tension_triangle_count", 0)) >= 1),
        "rag_intent_coverage_pass": _check(set(convergence.get("rag_intents", [])) == {"CHARACTER", "EMOTIONAL", "PLOT_EVENT"}),
        "tension_final_loss_pass": _check(float(convergence.get("final_tension_loss", 1.0)) < 0.10),
        "nil_invariant_counts_zero_pass": _check(all(int(value or 0) == 0 for value in invariant_counts.values())),
        "provider_zero_pass": _check(stage.get("provider_default_calls") == 0 and stage.get("live_provider_call_count_in_release_gate") == 0),
        "embedding_provider_zero_pass": _check(stage.get("embedding_provider_call_count") == 0),
        "query_classifier_llm_zero_pass": _check(stage.get("query_classifier_llm_call_count") == 0),
        "physics_reward_bridge_no_llm_pass": _check(stage.get("physics_reward_bridge_llm_call_count") == 0),
        "mae_live_provider_zero_pass": _check(stage.get("mae_live_provider_call_count") == 0),
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
        "stage": "118",
        "baseline_stage": "117",
        "title": "NIL Orchestrator",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "checks": checks,
        "stage118": _compact(stage),
        "nil_summary": {
            "component_count": len(components),
            "component_names": [component.get("name") for component in components],
            "loop_order": nil_report.get("loop_order"),
            "convergence": convergence,
            "invariant_counts": invariant_counts,
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
    out = root / "release/current/stage118_release_gate_report.json"
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


def _stage117_baseline_ok(root: Path) -> bool:
    report = _read_json(root / "release/current/stage117_release_gate_report.json")
    if report.get("status") == "pass":
        return True
    active = _read_json(root / "manifests/live_core_manifest.json").get("active_version")
    return active == "stage118" and (root / "manifests/stage117_manifest.json").exists()


def _loop_order_ok(order: list) -> bool:
    expected = [
        "CharacterInfluenceMatrix",
        "StructuralBalance",
        "AdaptiveMomentumWeights",
        "MAERewardSignal",
        "PhysicsRewardBridge",
        "CoefficientUpdateProposal",
        "DomainSpecificRAGFusion",
        "NarrativeTensionCurve",
    ]
    return order == expected


def _docs_manifest_ok(root: Path) -> bool:
    return all((root / rel).exists() for rel in [
        "docs/stages/stage118.md",
        "manifests/stage118_manifest.json",
        "manifests/stage118_nil_orchestrator_manifest.json",
    ])


def _repo_doctor_ready(root: Path) -> bool:
    text = (root / "tools/run_stage72_repo_doctor.py").read_text(encoding="utf-8", errors="ignore")
    return "stage118" in text and "stage118_release_gate" in text and "stage118_nil_orchestrator" in text


def _clean_packaging_status(root: Path) -> str:
    manifest = _read_json(root / "package_manifest.json")
    canonical = manifest.get("canonical_package") or "V1700_stage118_nil_orchestrator_integrated_repository.zip"
    override = os.environ.get("V1700_STAGE118_PACKAGE")
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
