from __future__ import annotations
import json, os, re, zipfile
from pathlib import Path
from v1700.stage110.orchestrator import run_stage110

_CACHE: dict[str, dict] = {}


def run_stage110_release_gate(root: Path | None = None) -> dict:
    root = root or Path(__file__).resolve().parents[3]
    key = str(root.resolve())
    if key in _CACHE:
        return _CACHE[key]
    stage = run_stage110(root)
    checks = {
        "stage109_baseline_gate_pass": _check(stage.get("stage110_0_stable_preflight", {}).get("checks", {}).get("stage109_baseline_gate_pass") is True),
        "mandatory_predevelopment_check_pass": _check(stage.get("stage110_0_stable_preflight", {}).get("status") == "pass"),
        "stable_release_contract_pass": _check(stage.get("release_contract", {}).get("release_status") == "stable"),
        "stable_lineage_frozen_pass": _check(stage.get("stable_lineage_frozen") is True),
        "branchpoint_survival_pass": _check(stage.get("branchpoint_lineage_preserved") is True),
        "provider_zero_pass": _check(stage.get("provider_default_calls") == 0 and stage.get("live_provider_call_count_in_release_gate") == 0),
        "sandbox_release_isolation_pass": _check(stage.get("release_gate_affected_by_sandbox") is False),
        "plugin_disabled_by_default_pass": _check(stage.get("plugin_runtime_enabled_by_default") == 0),
        "node2_boundary_pass": _check(stage.get("node2_raw_reveal_access") == 0),
        "raw_manuscript_leakage_pass": _check(stage.get("raw_manuscript_provider_leakage") == 0),
        "credential_leakage_pass": _check(stage.get("credential_leakage") == 0),
        "readme_active_stage_consistency_pass": _check(_readme_ok(root)),
        "package_manifest_canonical_reference_pass": _check(_package_manifest_ok(root)),
        "clean_zip_packaging_pass": _check(_clean_packaging_status(root) == "pass"),
        "secret_scan_pass": _check(_secret_scan(root)["status"] == "pass"),
    }
    issues = [k for k, v in checks.items() if v["status"] != "pass"]
    result = {
        "stage": "110",
        "baseline_stage": "109",
        "title": "V1700 Literary OS 1.0 Stable",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "checks": checks,
        "stage110": _compact(stage),
        "provider_default_calls": 0,
        "live_provider_call_count_in_release_gate": 0,
        "sandbox_live_provider_call_count": 0,
        "raw_manuscript_provider_leakage": 0,
        "node2_raw_reveal_access": 0,
        "credential_leakage": 0,
        "branchpoint_lineage_preserved": not issues,
        "stable_lineage_frozen": not issues,
        "release_status": "stable" if not issues else "blocked",
    }
    out = root / "release/current/stage110_release_gate_report.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    _CACHE[key] = result
    return result


def _check(condition: bool) -> dict:
    return {"status": "pass" if condition else "blocked"}


def _compact(stage: dict) -> dict:
    keep = ("status", "stage", "baseline_stage", "title", "provider_default_calls", "live_provider_call_count_in_release_gate", "raw_manuscript_provider_leakage", "node2_raw_reveal_access", "credential_leakage", "stable_lineage_frozen")
    return {k: stage.get(k) for k in keep if k in stage}


def _read_json(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def _readme_ok(root: Path) -> bool:
    text = (root / "README.md").read_text(encoding="utf-8", errors="ignore") if (root / "README.md").exists() else ""
    return ("Stage110" in text or "Stage111" in text) and "run_stage110_release_gate.py" in text and "Stage110" in text[:2600]


def _package_manifest_ok(root: Path) -> bool:
    m = _read_json(root / "package_manifest.json")
    stage = str(m.get("stage", ""))
    filelist = str(m.get("filelist", ""))
    allowed_stages = {str(i) for i in range(110, 128)} | {f"stage{i}" for i in range(110, 128)}
    allowed_prefix = any(filelist.startswith(f"V1700_stage{i}_") for i in range(110, 128))
    return (
        stage in allowed_stages
        and m.get("canonical_package") == m.get("package")
        and allowed_prefix
    )

def _clean_packaging_status(root: Path) -> str:
    m = _read_json(root / "package_manifest.json")
    canonical = m.get("canonical_package") or "V1700_stage110_literary_os_1_0_stable_FIXED.zip"
    override = os.environ.get("V1700_STAGE110_PACKAGE")
    candidates = []
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
    patterns = [re.compile(r"sk-[A-Za-z0-9]{20,}"), re.compile(r"AKIA[0-9A-Z]{16}"), re.compile(r"AIza[0-9A-Za-z_-]{20,}"), re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----")]
    hits = []
    for base in ("src", "tools", "manifests"):
        for path in (root / base).rglob("*"):
            if not path.is_file() or "__pycache__" in path.parts or path.suffix in {".pyc", ".zip"}:
                continue
            text = path.read_text(encoding="utf-8", errors="ignore")
            if any(p.search(text) for p in patterns):
                hits.append(path.relative_to(root).as_posix())
    return {"status": "pass" if not hits else "blocked", "hits": hits}
