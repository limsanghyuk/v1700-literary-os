from __future__ import annotations

from pathlib import Path

from v1700.literary_generation_boundary import run_page18_generation_boundary_preflight


def _readiness() -> dict:
    return {
        "status": "pass",
        "decision": "ready_for_policy_review",
        "checks": {
            "provider_default_calls": 0,
            "runtime_training_enabled": False,
            "canonical_mutation_allowed": False,
            "page18_runtime_opened": False,
            "stage243_created": False,
        },
        "paths": {
            "value_proof_guidance_report": "release/current/value_proof_arm_b_guidance_pack/value_proof_arm_b_guidance_surface_report.json",
            "value_proof_preregistration_report": "release/current/value_proof_arm_b_preregistration_pack/value_proof_arm_b_preregistration_packet_report.json",
            "value_proof_blind_evaluator_report": "release/current/value_proof_blind_evaluator_pack/value_proof_blind_evaluator_packet_report.json",
        },
    }


def _policy_review() -> dict:
    return {
        "status": "pass",
        "decision": "warning_preserving_ready_for_page18_opening_gate",
        "page18_runtime_opened": False,
        "stage243_created": False,
        "provider_default_calls": 0,
        "runtime_training_enabled": False,
        "canonical_mutation_allowed": False,
    }


def _opening_gate() -> dict:
    return {
        "status": "prepared_not_executed",
        "page18_runtime_opened": False,
        "stage243_created": False,
    }


def test_page18_generation_boundary_preflight_passes_without_runtime_opening(tmp_path: Path) -> None:
    _seed_ref_files(tmp_path)

    result = run_page18_generation_boundary_preflight(
        repo_root=tmp_path,
        readiness_report=_readiness(),
        policy_review=_policy_review(),
        opening_gate=_opening_gate(),
    )

    assert result["status"] == "pass"
    assert result["allowed_promotion"] == "page18_boundary_preflight_pass"
    assert result["provider_default_calls"] == 0
    assert result["runtime_training_enabled"] is False
    assert result["canonical_mutation_allowed"] is False
    assert result["page18_runtime_opened"] is False
    assert result["stage243_created"] is False
    assert result["experiment_started"] is False
    assert result["output_capture_started"] is False

    parts = result["parts"]
    request = parts["literary_generation_request"]
    context_packet = parts["generation_context_packet"]
    provider_policy = parts["provider_execution_policy"]
    output_schema = parts["output_capture_schema"]
    mutation_blocker = parts["canonical_mutation_blocker"]
    validation = parts["page18_generation_boundary_validation_report"]

    assert request["provider_execution_policy_ref"] == provider_policy["policy_id"]
    assert request["output_capture_schema_ref"] == output_schema["schema_id"]
    assert request["canonical_mutation_blocker_ref"] == mutation_blocker["blocker_id"]
    assert "source_text_payload" in request["forbidden_context_refs"]
    assert "unregistered_prompt_mutation" in request["forbidden_context_refs"]

    assert context_packet["source_text_allowed"] is False
    assert context_packet["provider_generation_allowed"] is False
    assert context_packet["canonical_mutation_allowed"] is False
    assert context_packet["metadata_refs"]
    assert context_packet["proof_packet_refs"]
    assert all(ref["raw_text_exported"] is False for ref in context_packet["metadata_refs"])
    assert all(ref["raw_text_exported"] is False for ref in context_packet["proof_packet_refs"])
    assert {ref["ref_id"] for ref in context_packet["metadata_refs"]} >= {
        "corpus_absorption_report",
        "local_corpus_db_survey_report",
    }
    assert {ref["ref_id"] for ref in context_packet["proof_packet_refs"]} >= {
        "page18_readiness_precheck",
        "value_proof_blind_evaluator_report",
    }

    assert provider_policy["provider_generation_allowed"] is False
    assert provider_policy["provider_default_calls"] == 0
    assert output_schema["output_capture_started"] is False
    assert output_schema["capture_allowed"] is False
    assert mutation_blocker["canonical_mutation_allowed"] is False
    assert validation["status"] == "pass"

    output_dir = tmp_path / "release/current/literary_generation_boundary_pack"
    assert (output_dir / "literary_generation_request.json").exists()
    assert (output_dir / "generation_context_packet.json").exists()
    assert (output_dir / "provider_execution_policy.json").exists()
    assert (output_dir / "output_capture_schema.json").exists()
    assert (output_dir / "canonical_mutation_blocker.json").exists()
    assert (output_dir / "page18_generation_boundary_preflight_report.json").exists()


def test_page18_generation_boundary_blocks_without_readiness(tmp_path: Path) -> None:
    _seed_ref_files(tmp_path)
    readiness = _readiness()
    readiness["status"] = "blocked"

    result = run_page18_generation_boundary_preflight(
        repo_root=tmp_path,
        readiness_report=readiness,
        policy_review=_policy_review(),
        opening_gate=_opening_gate(),
    )

    assert result["status"] == "blocked"
    assert "page18_readiness_not_pass" in result["issues"]
    assert result["page18_runtime_opened"] is False
    assert result["stage243_created"] is False


def test_page18_generation_boundary_blocks_without_refs(tmp_path: Path) -> None:
    result = run_page18_generation_boundary_preflight(
        repo_root=tmp_path,
        readiness_report=_readiness(),
        policy_review=_policy_review(),
        opening_gate=_opening_gate(),
    )

    assert result["status"] == "blocked"
    assert "metadata_refs_missing" in result["issues"]
    assert "proof_packet_refs_missing" in result["issues"]
    assert result["page18_runtime_opened"] is False
    assert result["stage243_created"] is False


def _seed_ref_files(root: Path) -> None:
    paths = [
        "release/current/corpus_ko_absorption_pack/corpus_absorption_report.json",
        "release/current/corpus_formula_bridge_pack/corpus_formula_bridge_report.json",
        "release/current/formula_signal_store_pack/formula_signal_store_report.json",
        "release/current/local_corpus_db_survey_report.json",
        "docs/policies/narrative_corpus_source_policy.md",
        "docs/architecture/corpus_formula_signal_bridge_blueprint.md",
        "release/current/page18_readiness_precheck_report.json",
        "release/current/page18_policy_review_warning_decision.json",
        "release/current/page18_opening_gate_checklist.json",
        "release/current/value_proof_arm_b_guidance_pack/value_proof_arm_b_guidance_surface_report.json",
        "release/current/value_proof_arm_b_preregistration_pack/value_proof_arm_b_preregistration_packet_report.json",
        "release/current/value_proof_blind_evaluator_pack/value_proof_blind_evaluator_packet_report.json",
        "release/current/stage242_release_gate_report.json",
        "release/current/release_gate_report.json",
    ]
    for rel in paths:
        path = root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text('{"status": "pass"}\n', encoding="utf-8")
