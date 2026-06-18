from __future__ import annotations

import json
from pathlib import Path

from v1700.value_proof_blind_evaluator_packet_builder import run_value_proof_blind_evaluator_packet_builder


def _mock_preregistration_report() -> dict:
    return {
        "status": "pass",
        "counters": {"focus_work_id": "10부"},
        "parts": {
            "arm_a_prompt_packet": {
                "prompt_packet_id": "value-proof-arm-a-prompt:10부:preregistered",
                "arm": "A",
                "packet_hash": "hash-a",
                "raw_script_text_allowed": False,
                "provider_generation_allowed": False,
                "canonical_mutation_allowed": False,
            },
            "arm_b_prompt_packet": {
                "prompt_packet_id": "value-proof-arm-b-prompt:10부:preregistered",
                "arm": "B",
                "packet_hash": "hash-b",
                "raw_script_text_allowed": False,
                "provider_generation_allowed": False,
                "canonical_mutation_allowed": False,
            },
            "value_proof_preregistration_lock_record": {
                "work_id": "10부",
                "experiment_started": False,
                "page18_runtime_opened": False,
            },
        },
    }


def test_blind_evaluator_packet_builder_hides_arm_labels(tmp_path: Path) -> None:
    result = run_value_proof_blind_evaluator_packet_builder(
        repo_root=tmp_path,
        preregistration_report=_mock_preregistration_report(),
    )

    assert result["status"] == "pass"
    assert result["provider_default_calls"] == 0
    assert result["experiment_started"] is False
    assert result["output_capture_started"] is False
    assert result["page18_runtime_opened"] is False
    assert result["canonical_mutation_allowed"] is False

    parts = result["parts"]
    packet_01 = parts["evaluator_packet_01"]
    packet_02 = parts["evaluator_packet_02"]
    private_mapping = parts["private_arm_mapping"]

    assert packet_01["label_visible_to_evaluator"] is False
    assert packet_02["label_visible_to_evaluator"] is False
    assert "arm" not in packet_01
    assert "arm" not in packet_02
    assert "source_prompt_packet_id" not in packet_01
    assert "source_prompt_packet_id" not in packet_02
    assert "source_prompt_packet_ref_hash" in packet_01
    assert "source_prompt_packet_ref_hash" in packet_02
    assert private_mapping["visible_to_evaluator"] is False
    assert private_mapping["records"][0]["arm"] == "A"
    assert private_mapping["records"][1]["arm"] == "B"

    public_packet_json = json.dumps(
        {
            "evaluator_packet_01": packet_01,
            "evaluator_packet_02": packet_02,
            "blind_packet_registry": parts["blind_packet_registry"],
        },
        ensure_ascii=False,
    ).lower()
    assert '"arm"' not in public_packet_json
    assert "arm-a" not in public_packet_json
    assert "arm-b" not in public_packet_json
    assert "value-proof-arm" not in public_packet_json
    assert "source_prompt_packet_id" not in public_packet_json


def test_blind_evaluator_packet_builder_blocks_failed_preregistration(tmp_path: Path) -> None:
    bad_report = {"status": "blocked", "counters": {"focus_work_id": "10부"}, "parts": {}}
    result = run_value_proof_blind_evaluator_packet_builder(repo_root=tmp_path, preregistration_report=bad_report)

    assert result["status"] == "blocked"
    assert "preregistration_report_not_pass" in result["issues"]
    assert "source_prompt_packet_ref_hash_missing" in result["issues"]
