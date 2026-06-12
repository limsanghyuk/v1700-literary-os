import json
import subprocess
import sys
from pathlib import Path

import pytest

from tools.writer_ide_render_packet_review import WriterIDERenderPacketReview


REPO_ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture()
def review_result():
    review = WriterIDERenderPacketReview(REPO_ROOT)
    return review.review()


def test_render_packet_review_shape(review_result):
    assert review_result["review_version"]
    assert review_result["packet_ref"]
    assert "overall_status" in review_result
    assert "acceptance_status" in review_result
    assert "blocking_failures" in review_result


def test_render_packet_review_expected_pass(review_result):
    assert review_result["overall_status"] == "PASS"
    assert review_result["acceptance_status"] == "READY_FOR_FRONTEND_RENDERER_BLUEPRINT"
    assert review_result["blocking_failure_count"] == 0
    assert review_result["panel_card_count"] >= 5


def test_render_packet_review_preserves_boundaries(review_result):
    assert review_result["page18_status"] == "NOT_OPENED"
    assert review_result["stage243_status"] == "NOT_CREATED"
    assert review_result["provider_status"] == "DISABLED"
    assert review_result["generation_status"] == "DISABLED"
    assert review_result["memory_write_status"] == "DISABLED"
    assert review_result["canonical_mutation_status"] == "NO_CANONICAL_MUTATION"


def test_render_packet_review_cli_outputs_json():
    script = REPO_ROOT / "tools" / "writer_ide_render_packet_review.py"
    completed = subprocess.run(
        [sys.executable, str(script), "--repo-root", str(REPO_ROOT)],
        check=False,
        capture_output=True,
        text=True,
    )
    assert completed.returncode in {0, 1}
    payload = json.loads(completed.stdout)
    assert payload["review_version"]
    assert "blocking_failures" in payload
