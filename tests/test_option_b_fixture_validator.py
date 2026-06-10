import json
import subprocess
import sys
from pathlib import Path

import pytest

from tools.option_b_fixture_validator import OptionBFixtureValidator


REPO_ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture()
def validator_result():
    validator = OptionBFixtureValidator(REPO_ROOT)
    return validator.validate()


def test_option_b_fixture_validator_returns_result_shape(validator_result):
    assert validator_result["validator_version"]
    assert validator_result["fixture_bundle_refs"]
    assert "module_results" in validator_result
    assert "warning_count" in validator_result
    assert "blocking_failure_count" in validator_result
    assert "overall_status" in validator_result
    assert "acceptance_status" in validator_result
    assert "downstream_readiness" in validator_result


def test_option_b_fixture_validator_has_expected_modules(validator_result):
    module_names = {module["module_name"] for module in validator_result["module_results"]}
    assert "JSON Parse Validator" in module_names
    assert "Mapping Table Validator" in module_names
    assert "Source Policy Validator" in module_names
    assert "Schema Validator" in module_names
    assert "Formula Catalog Validator" in module_names
    assert "Formula Signal Validator" in module_names
    assert "Rejected Records Validator" in module_names


def test_option_b_fixture_validator_is_fail_closed_contract_compatible(validator_result):
    if validator_result["blocking_failure_count"] > 0:
        assert validator_result["overall_status"] == "BLOCKED"
        assert validator_result["acceptance_status"] == "BLOCKED"
        assert validator_result["downstream_readiness"] == "NOT_READY"
    elif validator_result["warning_count"] > 0:
        assert validator_result["overall_status"] == "PASS_WITH_WARNINGS"
        assert validator_result["acceptance_status"] == "ACCEPTED_WITH_WARNINGS"
    else:
        assert validator_result["overall_status"] == "PASS"


def test_option_b_fixture_validator_expected_current_fixture_result(validator_result):
    # The current synthetic fixture bundle is designed to be metadata-only and internally linked.
    assert validator_result["blocking_failure_count"] == 0
    assert validator_result["overall_status"] in {"PASS", "PASS_WITH_WARNINGS"}
    assert validator_result["downstream_readiness"] in {
        "READY_FOR_SCHEMA_WIRING",
        "READY_FOR_FORMULA_SIGNAL_MAPPING",
    }


def test_option_b_fixture_validator_cli_outputs_json():
    script = REPO_ROOT / "tools" / "option_b_fixture_validator.py"
    completed = subprocess.run(
        [sys.executable, str(script), "--repo-root", str(REPO_ROOT)],
        check=False,
        capture_output=True,
        text=True,
    )
    assert completed.returncode in {0, 1}
    payload = json.loads(completed.stdout)
    assert payload["validator_version"]
    assert "overall_status" in payload
