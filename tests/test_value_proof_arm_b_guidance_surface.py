from __future__ import annotations

from pathlib import Path

from v1700.value_proof_arm_b_guidance_surface import run_value_proof_arm_b_guidance_surface


def _mock_writer_ide_report() -> dict:
    return {
        "status": "pass",
        "counters": {"focus_work_id": "10부"},
        "parts": {
            "writer_ide_surface_cards": {
                "cards": [
                    {
                        "card_id": "writer-card:center:10부",
                        "panel_ref": "writer_ide:center_panel:approval_boundary",
                        "zone": "center",
                        "work_id": "10부",
                        "headline": "10부 approval boundary review",
                        "summary": "approval=PENDING_REVIEW",
                        "confidence": 0.78,
                        "review_status": "PENDING_REVIEW",
                        "signal_refs": ["formula-signal:emotion:10부"],
                        "advisory_only": True,
                        "canonical_mutation_allowed": False,
                    },
                    {
                        "card_id": "writer-card:right:tensor:10부",
                        "panel_ref": "writer_ide:right_panel:narrative_state_tensor",
                        "zone": "right",
                        "work_id": "10부",
                        "headline": "10부 narrative tensor advisory",
                        "summary": "REVIEW_REQUIRED",
                        "confidence": 0.78,
                        "review_status": "VALID_FOR_VALUE_PROOF_PREREGISTRATION",
                        "signal_refs": ["formula-signal:tensor:10부"],
                        "advisory_only": True,
                        "canonical_mutation_allowed": False,
                    },
                ]
            }
        },
    }


def test_value_proof_arm_b_guidance_surface_passes_with_mock_report(tmp_path: Path) -> None:
    result = run_value_proof_arm_b_guidance_surface(repo_root=tmp_path, writer_ide_advisory_report=_mock_writer_ide_report())

    assert result["status"] == "pass"
    assert result["provider_default_calls"] == 0
    assert result["canonical_mutation_allowed"] is False
    assert result["page18_runtime_opened"] is False
    assert result["counters"]["focus_work_id"] == "10부"
    assert result["counters"]["arm_b_guidance_card_count"] == 2

    board = result["parts"]["value_proof_arm_b_guidance_board"]
    assert board["visible_to_evaluator"] is False
    assert board["provider_generation_allowed"] is False
    assert "value_proof_preregistration_required" in board["promotion_blockers"]


def test_value_proof_arm_b_guidance_surface_rejects_empty_cards(tmp_path: Path) -> None:
    report = {"status": "pass", "counters": {"focus_work_id": "10부"}, "parts": {"writer_ide_surface_cards": {"cards": []}}}
    result = run_value_proof_arm_b_guidance_surface(repo_root=tmp_path, writer_ide_advisory_report=report)

    assert result["status"] == "blocked"
    assert "arm_b_guidance_cards_empty" in result["issues"]
