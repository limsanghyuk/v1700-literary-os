from __future__ import annotations

from pathlib import Path

from v1700.value_proof_arm_b_preregistration_packet_builder import run_value_proof_arm_b_preregistration_packet_builder


def _mock_guidance_surface_report() -> dict:
    return {
        "status": "pass",
        "counters": {"focus_work_id": "10부"},
        "parts": {
            "value_proof_arm_b_guidance_cards": {
                "cards": [
                    {
                        "guidance_card_id": "value-proof-arm-b:right:1:10부",
                        "work_id": "10부",
                        "signal_refs": ["formula-signal:tensor:10부"],
                    }
                ]
            },
            "value_proof_arm_b_guidance_board": {
                "arm_b_allowed_context": ["metadata_only_corpus_refs", "formula_signal_refs"],
                "arm_b_forbidden_context": ["raw_script_text", "canonical_mutation"],
                "preregistered_formula_signal_refs": ["formula-signal:tensor:10부"],
            },
        },
    }


def test_preregistration_packet_builder_creates_locked_hashes(tmp_path: Path) -> None:
    result = run_value_proof_arm_b_preregistration_packet_builder(
        repo_root=tmp_path,
        guidance_surface_report=_mock_guidance_surface_report(),
    )

    assert result["status"] == "pass"
    assert result["provider_default_calls"] == 0
    assert result["experiment_started"] is False
    assert result["page18_runtime_opened"] is False
    assert result["canonical_mutation_allowed"] is False

    parts = result["parts"]
    arm_a = parts["arm_a_prompt_packet"]
    arm_b = parts["arm_b_prompt_packet"]
    lock_record = parts["value_proof_preregistration_lock_record"]

    assert arm_a["arm"] == "A"
    assert arm_b["arm"] == "B"
    assert arm_a["packet_hash"] != arm_b["packet_hash"]
    assert arm_b["raw_script_text_allowed"] is False
    assert lock_record["experiment_started"] is False
    assert "A" in lock_record["locked_prompt_packet_hashes"]
    assert "B" in lock_record["locked_prompt_packet_hashes"]


def test_preregistration_packet_builder_blocks_failed_guidance_surface(tmp_path: Path) -> None:
    bad_report = {"status": "blocked", "counters": {"focus_work_id": "10부"}, "parts": {}}
    result = run_value_proof_arm_b_preregistration_packet_builder(repo_root=tmp_path, guidance_surface_report=bad_report)

    assert result["status"] == "blocked"
    assert "guidance_surface_not_pass" in result["issues"]
