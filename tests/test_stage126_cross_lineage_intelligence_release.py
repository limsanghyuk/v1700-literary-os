from __future__ import annotations

from pathlib import Path

from v1700.stage126.orchestrator import run_stage126
from v1700.gates.stage126_release_gate import run_stage126_release_gate


def test_stage126_cross_lineage_release_seals_governed_lineage():
    root = Path(__file__).resolve().parents[1]
    result = run_stage126(root)
    assert result["status"] == "pass"
    assert result["release_policy"]["stage125_governor_preserved"] is True
    assert result["release_policy"]["gate25_primary_authority_preserved"] is True
    assert result["release_policy"]["gate28_secondary_quality_preserved"] is True
    assert result["release_policy"]["gate29_secondary_predictive_preserved"] is True
    assert result["release_policy"]["direct_v545_v555_merge_performed"] is False
    assert result["pne_runtime_training_count"] == 0
    assert result["auto_repair_mutation_count"] == 0
    assert result["provider_default_calls"] == 0


def test_stage126_release_gate_passes_and_preserves_authority_stack():
    root = Path(__file__).resolve().parents[1]
    result = run_stage126_release_gate(root)
    assert result["status"] == "pass"
    checks = result["checks"]
    assert checks["gate25_primary_authority_preserved"]["status"] == "pass"
    assert checks["gate28_secondary_quality_preserved"]["status"] == "pass"
    assert checks["gate29_secondary_predictive_preserved"]["status"] == "pass"
    assert checks["runtime_training_disabled"]["status"] == "pass"
    assert checks["provider_zero_pass"]["status"] == "pass"
