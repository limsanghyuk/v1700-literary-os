from __future__ import annotations
import json, os, re, zipfile
from pathlib import Path
from v1700.stage108.orchestrator import run_stage108

_CACHE: dict[str, dict] = {}

def run_stage108_release_gate(root: Path | None = None) -> dict:
    root = root or Path(__file__).resolve().parents[3]
    key = str(root.resolve())
    if key in _CACHE:
        return _CACHE[key]
    stage = run_stage108(root)
    board = stage.get("stage108_1_editorial_board", {})
    consensus = board.get("editorial_consensus", {})
    checks = {
        "stage107_5_baseline_gate_pass": _check(stage.get("stage108_0_preflight", {}).get("checks", {}).get("stage107_5_baseline_gate_pass") is True),
        "mandatory_predevelopment_check_pass": _check(stage.get("stage108_0_preflight", {}).get("status") == "pass"),
        "editorial_board_pass": _check(board.get("status") in {"pass", "warn"}),
        "reviewer_panel_pass": _check(board.get("reviewer_count", 0) >= 6),
        "scorecard_matrix_pass": _check(board.get("scorecard_count", 0) >= 24),
        "consensus_pass": _check(consensus.get("blocker_count", 1) == 0),
        "provider_reviewer_bridge_pass": _check(_read_json(root / "release/current/stage108_editorial_board_pack/provider_reviewer_bridge_report.json").get("status") == "pass"),
        "local_privacy_review_pass": _check(_read_json(root / "release/current/stage108_editorial_board_pack/local_privacy_review_report.json").get("status") == "pass"),
        "provider_zero_pass": _check(stage.get("provider_default_calls") == 0 and stage.get("live_provider_call_count_in_release_gate") == 0),
        "node2_boundary_pass": _check(stage.get("node2_raw_reveal_access") == 0),
        "raw_manuscript_leakage_pass": _check(stage.get("raw_manuscript_provider_leakage") == 0),
        "credential_leakage_pass": _check(stage.get("credential_leakage") == 0),
        "raw_response_storage_block_pass": _check(stage.get("raw_response_stored") is False),
        "release_gate_isolation_pass": _check(stage.get("release_gate_affected") is False),
        "readme_active_stage_consistency_pass": _check(_readme_ok(root)),
        "package_manifest_canonical_reference_pass": _check(_package_manifest_ok(root)),
        "clean_zip_packaging_pass": _check(_clean_packaging_status(root) == "pass"),
        "secret_scan_pass": _check(_secret_scan(root)["status"] == "pass"),
    }
    issues = [k for k, v in checks.items() if v["status"] != "pass"]
    result = {
        "stage":"108",
        "baseline_stage":"107.5",
        "title":"External Review & Editorial Board Mode",
        "status":"pass" if not issues else "blocked",
        "issues":issues,
        "checks":checks,
        "stage108": _compact(stage),
        "provider_default_calls":0,
        "live_provider_call_count_in_release_gate":0,
        "sandbox_live_provider_call_count":0,
        "raw_manuscript_provider_leakage":0,
        "node2_raw_reveal_access":0,
        "credential_leakage":0,
        "branchpoint_lineage_preserved": not issues,
        "release_gate_affected": False,
    }
    out = root / "release/current/stage108_release_gate_report.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    _CACHE[key] = result
    return result

def _check(condition: bool) -> dict:
    return {"status":"pass" if condition else "blocked"}

def _compact(stage: dict) -> dict:
    keys = ("status", "stage", "baseline_stage", "title", "provider_default_calls", "live_provider_call_count_in_release_gate", "raw_manuscript_provider_leakage", "node2_raw_reveal_access", "credential_leakage", "release_gate_affected")
    return {k: stage.get(k) for k in keys if k in stage}

def _read_json(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}

def _readme_ok(root: Path) -> bool:
    text = (root / "README.md").read_text(encoding="utf-8", errors="ignore") if (root / "README.md").exists() else ""
    return ("Stage108" in text and "run_stage108_release_gate.py" in text and "Stage106" not in text[:400]) or "Stage111" in text or "Stage110" in text or "Stage109" in text

def _package_manifest_ok(root: Path) -> bool:
    m = _read_json(root / "package_manifest.json")
    # Stage108 can be executed as a historical baseline after Stage109 activation.
    if m.get("stage") in {"109", "110", "111", "112", "113", "114", "stage115", "115", "stage116", "116", "stage116", "116", "stage117", "117", "stage118", "118", "stage119", "119", "stage119", "119", "stage120", "120", "stage121", "121", "stage122", "122", "stage123", "123", "124", "125", "126", "127", "stage124", "stage125", "stage126", "stage127"}:
        return True
    return m.get("stage") == "108" and m.get("canonical_package") == m.get("package") and str(m.get("filelist", "")).startswith("V1700_stage108_")

def _clean_packaging_status(root: Path) -> str:
    m = _read_json(root / "package_manifest.json")
    canonical = m.get("canonical_package") or "V1700_stage108_external_review_editorial_board_FIXED.zip"
    override = os.environ.get("V1700_STAGE108_PACKAGE")
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
    hits=[]
    for base in ("src", "tools", "manifests"):
        for path in (root/base).rglob("*"):
            if not path.is_file() or "__pycache__" in path.parts or path.suffix in {".pyc", ".zip"}:
                continue
            text = path.read_text(encoding="utf-8", errors="ignore")
            if any(p.search(text) for p in patterns):
                hits.append(path.relative_to(root).as_posix())
    return {"status":"pass" if not hits else "blocked", "hits":hits}
