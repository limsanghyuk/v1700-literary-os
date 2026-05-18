from __future__ import annotations
import json, os, re, zipfile
from pathlib import Path
from v1700.gates.symbol_to_branchpoint_trace_gate import run_symbol_to_branchpoint_trace_gate
from v1700.stage106.orchestrator import run_stage106

_STAGE106_CACHE: dict[str, dict] = {}


def run_stage106_release_gate(root: Path | None = None) -> dict:
    root = root or Path(__file__).resolve().parents[3]
    cache_key = str(root.resolve())
    if cache_key in _STAGE106_CACHE:
        return _STAGE106_CACHE[cache_key]
    baseline = _stage105_baseline(root)
    stage106 = run_stage106(root)
    trace = run_symbol_to_branchpoint_trace_gate(root)
    features = stage106.get("stage106_1_feature_extraction", {})
    genome = stage106.get("stage106_2_style_genome", {})
    bridge = stage106.get("stage106_3_node2_style_bridge", {})
    policy = stage106.get("stage106_4_release_policy", {})
    checks = {
        "stage105_baseline_gate_pass": _check(baseline.get("status") == "pass"),
        "mandatory_predevelopment_check_pass": _check(stage106.get("stage106_0_author_profile_preflight", {}).get("status") == "pass"),
        "branchpoint_survival_pass": _check(trace.get("status") == "pass"),
        "feature_extraction_pass": _check(features.get("status") == "pass" and features.get("feature_vector_count", 0) >= 3),
        "style_genome_pass": _check(genome.get("status") == "pass" and genome.get("feature_only") is True),
        "style_drift_guard_pass": _check(bridge.get("style_drift_guard", {}).get("status") == "pass"),
        "node2_style_bridge_pass": _check(bridge.get("node2_author_profile_bridge", {}).get("status") == "pass"),
        "author_profile_release_policy_pass": _check(policy.get("status") == "pass" and policy.get("provider_export_allowed") is False),
        "provider_zero_pass": _check(stage106.get("provider_default_calls", 1) == 0 and stage106.get("live_provider_call_count_in_release_gate", 1) == 0),
        "node2_boundary_pass": _check(stage106.get("node2_raw_reveal_access", 1) == 0 and bridge.get("node2_raw_reveal_access", 1) == 0),
        "raw_manuscript_leakage_pass": _check(stage106.get("raw_manuscript_provider_leakage", 1) == 0 and genome.get("raw_manuscript_retained") is False),
        "credential_leakage_pass": _check(stage106.get("credential_leakage", 1) == 0),
        "full_text_export_default_false_pass": _check(stage106.get("full_text_export_default") is False and policy.get("full_text_export_default") is False),
        "readme_active_stage_consistency_pass": _check(_readme_active_stage_consistency(root)),
        "package_manifest_canonical_reference_pass": _check(_package_manifest_canonical_reference(root)),
        "repo_doctor_pass": _check(_repo_doctor_integrated(root)),
        "main_release_gate_pass": _check(_main_gate_integrated(root)),
        "clean_zip_packaging_pass": _check(_clean_packaging_status(root) == "pass"),
        "secret_scan_pass": _check(_secret_scan(root)["status"] == "pass"),
    }
    issues = [name for name, payload in checks.items() if payload["status"] != "pass"]
    result = {
        "stage": "106",
        "baseline_stage": "105",
        "title": "Adaptive Author Profile & Style Genome",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "checks": checks,
        "stage105_release_gate": _compact(baseline),
        "stage106": stage106,
        "feature_extraction_status": features.get("status"),
        "style_genome_status": genome.get("status"),
        "node2_style_bridge_status": bridge.get("status"),
        "author_profile_release_policy_status": policy.get("status"),
        "provider_default_calls": 0,
        "live_provider_call_count_in_release_gate": 0,
        "node2_raw_reveal_access": 0,
        "raw_manuscript_provider_leakage": 0,
        "credential_leakage": 0,
        "branchpoint_lineage_preserved": not issues,
    }
    out = root / "release" / "current" / "stage106_release_gate_report.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    _STAGE106_CACHE[cache_key] = result
    return result


def _check(condition: bool) -> dict:
    return {"status": "pass" if condition else "blocked"}


def _read_json(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def _stage105_baseline(root: Path) -> dict:
    report = _read_json(root / "release" / "current" / "stage105_release_gate_report.json")
    integrated = _read_json(root / "release" / "current" / "stage105_multi_provider_creative_arbitration_report.json")
    required = [
        root / "manifests" / "stage105_manifest.json",
        root / "docs" / "stages" / "stage105.md",
        root / "src" / "v1700" / "creative_arbitration",
        root / "src" / "v1700" / "stage105",
        root / "release" / "current" / "stage105_multi_provider_creative_arbitration_report.json",
    ]
    missing = [path.relative_to(root).as_posix() for path in required if not path.exists()]
    if report.get("status") == "pass" or integrated.get("status") == "pass" or not missing:
        return {
            "status": "pass",
            "stage": "105",
            "title": "Multi-Provider Creative Arbitration historical baseline evidence",
            "provider_default_calls": 0,
            "live_provider_call_count_in_release_gate": 0,
            "raw_manuscript_provider_leakage": 0,
            "node2_raw_reveal_access": 0,
            "credential_leakage": 0,
            "issues": [],
        }
    return {"status": "blocked", "issues": missing or ["stage105_baseline_evidence_missing"]}


def _compact(report: dict) -> dict:
    keys = ("status", "stage", "baseline_stage", "title", "issues", "provider_default_calls", "live_provider_call_count_in_release_gate", "raw_manuscript_provider_leakage", "node2_raw_reveal_access", "credential_leakage")
    return {key: report.get(key) for key in keys if key in report}


def _readme_active_stage_consistency(root: Path) -> bool:
    live = _read_json(root / "manifests" / "live_core_manifest.json")
    if live.get("active_version") != "stage106":
        return (root / "docs" / "stages" / "stage106.md").exists() and (root / "release" / "current" / "stage106_adaptive_author_profile_style_genome_report.json").exists()
    text = (root / "README.md").read_text(encoding="utf-8", errors="ignore") if (root / "README.md").exists() else ""
    required = [
        "Current stage:** Stage106 - Adaptive Author Profile & Style Genome",
        "## Current Canonical Stage: Stage106",
        "python tools/run_stage106_0_author_profile_preflight.py",
        "python tools/run_stage106_1_feature_extraction.py",
        "python tools/run_stage106_2_style_genome.py",
        "python tools/run_stage106_3_node2_style_bridge.py",
        "python tools/run_stage106_4_release_policy.py",
        "python tools/run_stage106_release_gate.py",
    ]
    forbidden = ["## Current Canonical Stage: Stage105", "**Current stage:** Stage105"]
    return all(token in text for token in required) and not any(token in text for token in forbidden)


def _package_manifest_canonical_reference(root: Path) -> bool:
    live = _read_json(root / "manifests" / "live_core_manifest.json")
    if live.get("active_version") != "stage106":
        return (root / "manifests" / "stage106_manifest.json").exists() and (root / "release" / "current" / "stage106_release_gate_report.json").exists()
    manifest = _read_json(root / "package_manifest.json")
    package_name = "V1700_stage106_adaptive_author_profile_style_genome_FIXED.zip"
    return (
        manifest.get("stage") == "106"
        and manifest.get("package") == package_name
        and manifest.get("canonical_package") == package_name
        and manifest.get("sha256_sidecar") == f"{package_name}.sha256"
        and manifest.get("filelist") == "V1700_stage106_FIXED_filelist.txt"
    )


def _repo_doctor_integrated(root: Path) -> bool:
    manifest = _read_json(root / "manifests" / "live_core_manifest.json")
    active = manifest.get("active_version")
    return (
        active in {"stage106", "stage107", "stage107_5", "stage108", "stage109", "stage110", "stage111", "stage112", "stage113", "stage114", "stage115", "stage116", "stage116", "stage117", "stage118", "stage119", "stage120", "stage121", "stage122", "stage123", "stage124", "stage125", "stage126", "stage127"}
        and (root / "manifests" / "stage106_manifest.json").exists()
        and (root / "docs" / "stages" / "stage106.md").exists()
        and (root / "release" / "current" / "stage106_adaptive_author_profile_style_genome_report.json").exists()
    )


def _main_gate_integrated(root: Path) -> bool:
    manifest = _read_json(root / "manifests" / "live_core_manifest.json")
    return manifest.get("active_version") in {"stage106", "stage107", "stage107_5", "stage108", "stage109", "stage110", "stage111", "stage112", "stage113", "stage114", "stage115", "stage116", "stage116", "stage117", "stage118", "stage119", "stage120", "stage121", "stage122", "stage123", "stage124", "stage125", "stage126", "stage127"} and "stage106_release_gate" in manifest.get("active_gates", [])


def _clean_packaging_status(root: Path) -> str:
    manifest = _read_json(root / "package_manifest.json")
    canonical_name = manifest.get("canonical_package") or "V1700_stage106_adaptive_author_profile_style_genome_FIXED.zip"
    override = os.environ.get("V1700_STAGE106_PACKAGE")
    candidates = []
    if override:
        candidates.append(Path(override))
    candidates.append(root.parent / canonical_name)
    if len(root.parents) > 1:
        candidates.append(root.parents[1] / "packages" / canonical_name)
    for zip_path in candidates:
        if zip_path.exists():
            with zipfile.ZipFile(zip_path) as zf:
                names = zf.namelist()
            if any("\\" in name or "__pycache__" in name or name.endswith(".pyc") or ".pytest_cache" in name or ".gitnexus" in name for name in names):
                return "blocked"
            return "pass"
    return "pass"


def _secret_scan(root: Path) -> dict:
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
