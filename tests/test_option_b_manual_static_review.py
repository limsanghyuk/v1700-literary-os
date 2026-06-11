import json
import subprocess
import sys
from pathlib import Path

import pytest

from tools.option_b_manual_static_review import OptionBManualStaticReview


REPO_ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture()
def review_result():
    review = OptionBManualStaticReview(REPO_ROOT)
    return review.build_review()


def test_manual_static_review_result_shape(review_result):
    assert review_result["review_version"]
    assert review_result["input_ref"]
    assert "manual_review_objects" in review_result
    assert "review_object_count" in review_result
    assert "overall_status" in review_result
    assert "acceptance_status" in review_result


def test_manual_static_review_expected_pass(review_result):
    assert review_result["overall_status"] == "PASS"
    assert review_result["blocking_failure_count"] == 0
    assert review_result["review_object_count"] >= 5
    assert review_result["acceptance_status"] == "READY_FOR_HUMAN_REVIEW"


def test_manual_static_review_preserves_boundaries(review_result):
    assert review_result["page18_status"] == "NOT_OPENED"
    assert review_result["stage243_status"] == "NOT_CREATED"
    assert review_result["generation_status"] == "DISABLED"
    assert review_result["memory_write_status"] == "DISABLED"
    assert review_result["canonical_mutation_status"] == "NO_CANONICAL_MUTATION"


def test_manual_static_review_objects_are_pending(review_result):
    for obj in review_result["manual_review_objects"]:
        assert obj["review_type"] == "HUMAN_STATIC_ADVISORY_REVIEW"
        assert obj["default_decision"] == "PENDING_REVIEW"
        assert obj["manual_review_required"] is True
        assert obj["advisory_only"] is True


def test_manual_static_review_cli_outputs_json():
    script = REPO_ROOT / "tools" / "option_b_manual_static_review.py"
    completed = subprocess.run(
        [sys.executable, str(script), "--repo-root", str(REPO_ROOT)],
        check=False,
        capture_output=True,
        text=True,
    )
    assert completed.returncode in {0, 1}
    payload = json.loads(completed.stdout)
    assert payload["review_version"]
    assert "manual_review_objects" in payload
