import json
import subprocess
import sys
from pathlib import Path

import pytest

from tools.option_b_writer_ide_static_flow import OptionBWriterIDEStaticFlow


REPO_ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture()
def static_flow_result():
    flow = OptionBWriterIDEStaticFlow(REPO_ROOT)
    return flow.build_flow()


def test_writer_ide_static_flow_result_shape(static_flow_result):
    assert static_flow_result["flow_version"]
    assert static_flow_result["mapping_result_ref"]
    assert "writer_ide_panels" in static_flow_result
    assert "panel_count" in static_flow_result
    assert "overall_status" in static_flow_result
    assert "acceptance_status" in static_flow_result
    assert "downstream_status" in static_flow_result


def test_writer_ide_static_flow_expected_pass(static_flow_result):
    assert static_flow_result["blocking_failure_count"] == 0
    assert static_flow_result["overall_status"] in {"PASS", "PASS_WITH_WARNINGS"}
    assert static_flow_result["panel_count"] >= 5
    assert static_flow_result["downstream_status"] == "READY_FOR_MANUAL_STATIC_REVIEW"


def test_writer_ide_static_flow_preserves_boundaries(static_flow_result):
    assert static_flow_result["provider_status"] == "DISABLED"
    assert static_flow_result["generation_status"] == "DISABLED"
    assert static_flow_result["memory_write_status"] == "DISABLED"
    assert static_flow_result["canonical_mutation_status"] == "NO_CANONICAL_MUTATION"
    assert static_flow_result["value_proof_status"] == "NOT_PROOF_PREREGISTRATION_REQUIRED"
    assert static_flow_result["learnable_critic_status"] == "NO_COEFFICIENT_UPDATE_AUDIT_REQUIRED"
    assert static_flow_result["page18_status"] == "NOT_OPENED"
    assert static_flow_result["stage243_status"] == "NOT_CREATED"


def test_writer_ide_static_flow_panels_are_advisory(static_flow_result):
    for panel in static_flow_result["writer_ide_panels"]:
        assert panel["panel_type"] == "FORMULA_SIGNAL_ADVISORY_PANEL"
        assert panel["ide_action"] == "DISPLAY_ADVISORY_ONLY"
        assert panel["advisory_only"] is True
        assert panel["manual_review_required"] is True
        assert panel["value_proof_status"] == "NOT_PROOF_PREREGISTRATION_REQUIRED"
        assert panel["learnable_critic_status"] == "NO_COEFFICIENT_UPDATE_AUDIT_REQUIRED"


def test_writer_ide_static_flow_cli_outputs_json():
    script = REPO_ROOT / "tools" / "option_b_writer_ide_static_flow.py"
    completed = subprocess.run(
        [sys.executable, str(script), "--repo-root", str(REPO_ROOT)],
        check=False,
        capture_output=True,
        text=True,
    )
    assert completed.returncode in {0, 1}
    payload = json.loads(completed.stdout)
    assert payload["flow_version"]
    assert "writer_ide_panels" in payload
