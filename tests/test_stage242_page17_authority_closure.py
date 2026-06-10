from __future__ import annotations

import json
from pathlib import Path

from v1700.gates.stage242_release_gate import run_stage242_release_gate

ROOT = Path(__file__).resolve().parents[1]


def test_stage242_release_gate_passes() -> None:
    result = run_stage242_release_gate(ROOT)
    assert result["status"] == "pass"
    assert result["checks"]["stage242_gitnexus_evidence_pass"]["status"] == "pass"
    assert result["checks"]["warning_visibility_pass"]["status"] == "pass"


def test_stage242_active_version_mismatch_blocks(tmp_path: Path) -> None:
    sandbox = tmp_path / "repo"
    (sandbox / "manifests").mkdir(parents=True, exist_ok=True)
    manifest = json.loads((ROOT / "manifests/live_core_manifest.json").read_text(encoding="utf-8"))
    manifest["active_version"] = "stage184"
    (sandbox / "manifests/live_core_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    result = run_stage242_release_gate(sandbox)
    assert result["status"] == "blocked"
    assert "active_version_pass" in result["issues"]
