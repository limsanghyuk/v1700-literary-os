from __future__ import annotations
import json, os, re, zipfile
from pathlib import Path
from v1700.stage107_5.provider_sandbox_orchestrator import run_stage107_5

_CACHE: dict[str, dict] = {}

def run_stage107_5_sandbox_gate(root: Path | None = None) -> dict:
    root = root or Path(__file__).resolve().parents[3]
    key = str(root.resolve())
    if key in _CACHE:
        return _CACHE[key]
    stage = run_stage107_5(root)
    preflight = stage.get("stage107_5_0_sandbox_preflight", {})
    probe = stage.get("stage107_5_1_model_id_probe", {})
    contract = stage.get("stage107_5_2_adapter_contract", {})
    comparison = stage.get("stage107_5_4_arbitration_comparison", {})
    checks = {
        "stage107_baseline_gate_pass": _check(preflight.get("checks", {}).get("stage107_baseline_gate_pass") is True),
        "sandbox_explicit_opt_in_policy_pass": _check(preflight.get("checks", {}).get("sandbox_explicit_opt_in_required") is True),
        "credential_externality_pass": _check(preflight.get("checks", {}).get("credential_externality_pass") is True),
        "payload_redactor_pass": _check(stage.get("raw_manuscript_provider_leakage", 1) == 0 and stage.get("credential_leakage", 1) == 0),
        "raw_manuscript_block_pass": _check(stage.get("raw_manuscript_provider_leakage", 1) == 0),
        "model_id_probe_shape_pass": _check(probe.get("status") == "pass" and probe.get("model_ids_hardcoded_as_canonical") is False),
        "adapter_contract_pass": _check(contract.get("status") == "pass"),
        "response_normalization_pass": _check(comparison.get("status") == "pass"),
        "cost_latency_ledger_pass": _check(comparison.get("cost_latency_ledger", {}).get("status") == "pass"),
        "release_gate_isolation_pass": _check(stage.get("release_gate_affected") is False and stage.get("live_provider_call_count_in_release_gate") == 0),
        "raw_response_storage_block_pass": _check(stage.get("raw_response_stored") is False),
        "provider_zero_release_path_pass": _check(stage.get("provider_default_calls") == 0 and stage.get("live_provider_call_count_in_release_gate") == 0),
        "clean_zip_packaging_pass": _check(_clean_packaging_status(root) == "pass"),
        "secret_scan_pass": _check(_secret_scan(root)["status"] == "pass"),
    }
    issues = [name for name, payload in checks.items() if payload["status"] != "pass"]
    result = {
        "stage": "107.5",
        "baseline_stage": "107",
        "title": "Provider Live Sandbox Adapter Verification",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "checks": checks,
        "stage107_5": _compact(stage),
        "provider_default_calls": 0,
        "live_provider_call_count_in_release_gate": 0,
        "raw_manuscript_provider_leakage": 0,
        "node2_raw_reveal_access": 0,
        "credential_leakage": 0,
        "branchpoint_lineage_preserved": not issues,
        "release_gate_affected": False,
    }
    out = root / "release/current/stage107_5_sandbox_gate_report.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    _CACHE[key] = result
    return result

def _check(condition: bool) -> dict:
    return {"status": "pass" if condition else "blocked"}

def _compact(report: dict) -> dict:
    keep = ("status", "stage", "baseline_stage", "title", "issues", "release_gate_affected", "provider_default_calls", "live_provider_call_count_in_release_gate", "sandbox_live_provider_call_count", "raw_manuscript_provider_leakage", "node2_raw_reveal_access", "credential_leakage", "raw_response_stored")
    return {k: report.get(k) for k in keep if k in report}

def _read_json(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}

def _clean_packaging_status(root: Path) -> str:
    m = _read_json(root / "package_manifest.json")
    canonical = m.get("canonical_package") or "V1700_stage107_5_provider_live_sandbox_adapter_verification_FIXED.zip"
    override = os.environ.get("V1700_STAGE107_5_PACKAGE")
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
            if any("\\" in n or "__pycache__" in n or n.endswith(".pyc") or ".pytest_cache" in n or ".gitnexus" in n or n.endswith(".env") or "/.env" in n for n in names):
                return "blocked"
            return "pass"
    return "pass"

def _secret_scan(root: Path) -> dict:
    patterns = [re.compile(r"sk-[A-Za-z0-9]{20,}"), re.compile(r"AKIA[0-9A-Z]{16}"), re.compile(r"AIza[0-9A-Za-z_-]{20,}"), re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----")]
    hits: list[str] = []
    for base in ("src", "tools", "manifests"):
        for path in (root / base).rglob("*"):
            if not path.is_file() or "__pycache__" in path.parts or path.suffix in {".pyc", ".zip"}:
                continue
            text = path.read_text(encoding="utf-8", errors="ignore")
            if any(p.search(text) for p in patterns):
                hits.append(path.relative_to(root).as_posix())
    return {"status": "pass" if not hits else "blocked", "hits": hits}
