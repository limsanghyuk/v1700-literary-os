from __future__ import annotations

import json
import shutil
from pathlib import Path

from v1700.page06_release_seal import run_stage178_page06_release_seal
from v1700.gates.stage178_release_gate import run_stage178_release_gate

ROOT = Path(__file__).resolve().parents[1]

def test_stage178_page06_release_seal_passes() -> None:
    result = run_stage178_page06_release_seal(ROOT, mode="historical")
    assert result["status"] == "pass"
    assert result["provider_default_calls"] == 0
    assert result["node2_raw_reveal_access"] == 0
    assert result["memory_write_enabled"] is False
    assert result["runtime_training_enabled"] is False

def test_stage178_release_gate_requires_gitnexus_7x12() -> None:
    result = run_stage178_release_gate(ROOT)
    assert result["status"] == "pass"
    assert result["checks"]["gitnexus_preflight_analysis_pass"]["status"] == "pass"
    assert result["checks"]["package_comparison_report_pass"]["status"] == "pass"

def test_stage178_active_version_mismatch_blocks(tmp_path: Path) -> None:
    sandbox = tmp_path / "repo"
    _copy_minimal_repo(ROOT, sandbox)
    manifest_path = sandbox / "manifests/live_core_manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["active_version"] = "stage177"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    result = run_stage178_page06_release_seal(sandbox)
    assert result["status"] == "blocked"
    assert any(issue.startswith("active_version_mismatch") for issue in result["issues"])

def _copy_minimal_repo(src: Path, dst: Path) -> None:
    (dst / "manifests").mkdir(parents=True, exist_ok=True)
    source = src / "manifests/live_core_manifest.json"
    (dst / "manifests/live_core_manifest.json").write_text(source.read_text(encoding="utf-8"), encoding="utf-8")
