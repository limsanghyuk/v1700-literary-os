from __future__ import annotations

from pathlib import Path

from v1700.stage125.orchestrator import run_stage125
from v1700.gates.stage125_release_gate import run_stage125_release_gate


def test_stage125_governor_passes_and_preserves_authority():
    root = Path(__file__).resolve().parents[1]
    result = run_stage125(root)
    assert result["status"] == "pass"
    assert result["summary"]["primary_gate"] == "Gate25"
    assert "Gate28" in result["summary"]["secondary_gates"]
    assert "Gate29" in result["summary"]["secondary_gates"]
    assert result["absorption_policy"]["gate28_primary_authority_enabled"] is False
    assert result["absorption_policy"]["gate29_primary_authority_enabled"] is False
    assert result["pne_runtime_training_count"] == 0
    assert result["auto_repair_mutation_count"] == 0


def test_stage125_release_gate_passes():
    root = Path(__file__).resolve().parents[1]
    result = run_stage125_release_gate(root)
    assert result["status"] == "pass"
    checks = result["checks"]
    assert checks["gate25_primary_authority_preserved"]["status"] == "pass"
    assert checks["gate28_secondary_quality_preserved"]["status"] == "pass"
    assert checks["gate29_secondary_predictive_preserved"]["status"] == "pass"
    assert checks["provider_zero_pass"]["status"] == "pass"
