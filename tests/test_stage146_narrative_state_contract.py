from __future__ import annotations

import json
from pathlib import Path

from v1700.gates.release_gate import run_release_gate
from v1700.gates.stage146_release_gate import run_stage146_release_gate
from v1700.stage146 import run_stage146

ROOT = Path(__file__).resolve().parents[1]


def test_stage146_report_passes() -> None:
    result = run_stage146(ROOT)
    assert result["status"] == "pass"
    assert result["narrative_state_contract_only"] is True
    assert result["canonical_state_object_count"] >= 7
    assert result["hierarchy_edge_count"] >= 6
    assert result["continuity_rule_count"] >= 6
    assert result["reveal_boundary_complete"] is True


def test_stage146_preserves_provider_zero_and_boundaries() -> None:
    result = run_stage146(ROOT)
    assert result["runtime_training_enabled"] is False
    assert result["active_meta_learning_enabled"] is False
    assert result["model_weight_update_count"] == 0
    assert result["losdb_write_enabled"] is False
    assert result["migration_execution_enabled"] is False
    assert result["provider_default_calls"] == 0
    assert result["node2_raw_reveal_access"] == 0


def test_stage146_reuses_stage145_baseline_and_passes_gate() -> None:
    result = run_stage146(ROOT)
    baseline = result["parts"]["stage145_baseline"]
    assert baseline["status"] == "pass"
    assert baseline["branchpoint_lineage_preserved"] is True
    gate = run_stage146_release_gate(ROOT)
    assert gate["status"] == "pass"
    assert gate["checks"]["state_shape_catalog_pass"]["status"] == "pass"
    assert gate["checks"]["reveal_boundary_matrix_pass"]["status"] == "pass"


def test_stage146_is_the_active_release_baseline() -> None:
    manifest = (ROOT / "manifests" / "live_core_manifest.json").read_text(encoding="utf-8")
    active_version = json.loads(manifest)["active_version"]
    assert active_version.startswith("stage")
    assert int(active_version.removeprefix("stage")) >= 146
    assert '"stage146_narrative_state_contract"' in manifest
    assert '"stage146_release_gate"' in manifest

    result = run_release_gate()
    assert result["status"] == "pass"
    assert result["stage146_release_gate"]["status"] == "pass"
