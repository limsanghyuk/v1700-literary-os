import json
import subprocess
import sys
from pathlib import Path

import pytest

from tools.writer_ide_advisory_panel_renderer import WriterIDEAdvisoryPanelRenderer


REPO_ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture()
def render_packet():
    renderer = WriterIDEAdvisoryPanelRenderer(REPO_ROOT)
    return renderer.build_packet()


def test_renderer_result_shape(render_packet):
    assert render_packet["renderer_version"]
    assert render_packet["source_result_refs"]
    assert "panel_cards" in render_packet
    assert "panel_card_count" in render_packet
    assert "overall_status" in render_packet
    assert "acceptance_status" in render_packet


def test_renderer_expected_pass(render_packet):
    assert render_packet["overall_status"] == "PASS"
    assert render_packet["blocking_failure_count"] == 0
    assert render_packet["panel_card_count"] >= 5
    assert render_packet["acceptance_status"] == "READY_FOR_UI_RENDER_PACKET_REVIEW"


def test_renderer_preserves_boundaries(render_packet):
    assert render_packet["page18_status"] == "NOT_OPENED"
    assert render_packet["stage243_status"] == "NOT_CREATED"
    assert render_packet["provider_status"] == "DISABLED"
    assert render_packet["generation_status"] == "DISABLED"
    assert render_packet["memory_write_status"] == "DISABLED"
    assert render_packet["canonical_mutation_status"] == "NO_CANONICAL_MUTATION"


def test_renderer_cards_link_review_objects(render_packet):
    for card in render_packet["panel_cards"]:
        assert card["panel_id"]
        assert card["review_object_id"]
        assert card["manual_review_status"] == "PENDING_REVIEW"
        assert card["ide_region"] == "advisory_panel"
        assert card["display_mode"] == "read_only_advisory"
        assert len(card["evidence_refs"]) == 2


def test_renderer_cli_outputs_json():
    script = REPO_ROOT / "tools" / "writer_ide_advisory_panel_renderer.py"
    completed = subprocess.run(
        [sys.executable, str(script), "--repo-root", str(REPO_ROOT)],
        check=False,
        capture_output=True,
        text=True,
    )
    assert completed.returncode in {0, 1}
    payload = json.loads(completed.stdout)
    assert payload["renderer_version"]
    assert "panel_cards" in payload
