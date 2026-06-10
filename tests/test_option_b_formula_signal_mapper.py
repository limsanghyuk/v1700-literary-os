import json
import subprocess
import sys
from pathlib import Path

import pytest

from tools.option_b_formula_signal_mapper import OptionBFormulaSignalMapper


REPO_ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture()
def mapping_result():
    mapper = OptionBFormulaSignalMapper(REPO_ROOT)
    return mapper.map_signals()


def test_formula_signal_mapper_result_shape(mapping_result):
    assert mapping_result["mapper_version"]
    assert mapping_result["validator_result_ref"]
    assert mapping_result["input_refs"]
    assert "formula_signal_mappings" in mapping_result
    assert "mapping_count" in mapping_result
    assert "overall_status" in mapping_result
    assert "acceptance_status" in mapping_result
    assert "downstream_status" in mapping_result


def test_formula_signal_mapper_expected_pass(mapping_result):
    assert mapping_result["blocking_failure_count"] == 0
    assert mapping_result["overall_status"] in {"PASS", "PASS_WITH_WARNINGS"}
    assert mapping_result["mapping_count"] >= 5


def test_formula_signal_mapper_preserves_boundaries(mapping_result):
    assert mapping_result["value_proof_status"] == "NOT_PROOF_PREREGISTRATION_REQUIRED"
    assert mapping_result["learnable_critic_status"] == "NO_COEFFICIENT_UPDATE_AUDIT_REQUIRED"
    assert mapping_result["canonical_mutation_status"] == "NO_CANONICAL_MUTATION"
    assert mapping_result["page18_status"] == "NOT_OPENED"
    assert mapping_result["stage243_status"] == "NOT_CREATED"


def test_formula_signal_mapper_mappings_are_advisory(mapping_result):
    for mapping in mapping_result["formula_signal_mappings"]:
        assert mapping["advisory_only"] is True
        assert mapping["signal_type_label"] in {
            "PLACEHOLDER_SIGNAL",
            "MANUAL_REVIEW_SIGNAL",
            "FIXTURE_SIGNAL",
        }
        assert mapping["value_proof_status"] == "PREREGISTRATION_REQUIRED_NOT_PROOF"
        assert mapping["learnable_critic_status"] == "AUDIT_REQUIRED_NO_COEFFICIENT_UPDATE"
        assert mapping["writer_ide_status"] == "ADVISORY_PANEL_ONLY"


def test_formula_signal_mapper_cli_outputs_json():
    script = REPO_ROOT / "tools" / "option_b_formula_signal_mapper.py"
    completed = subprocess.run(
        [sys.executable, str(script), "--repo-root", str(REPO_ROOT)],
        check=False,
        capture_output=True,
        text=True,
    )
    assert completed.returncode in {0, 1}
    payload = json.loads(completed.stdout)
    assert payload["mapper_version"]
    assert "formula_signal_mappings" in payload
