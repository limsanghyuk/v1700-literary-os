from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List


ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "release/current/season_wiring_pack/full_season_candidate_package_fixture_v1.json"
SCHEMA = ROOT / "release/current/season_wiring_pack/full_season_candidate_package_schema_v1.json"
SELF_CHECK = ROOT / "release/current/season_wiring_pack/full_season_hard_rule_self_check_v1.json"
PROTOCOL = ROOT / "release/current/season_wiring_pack/full_season_validation_protocol_p8_1.json"
OUT = ROOT / "release/current/season_wiring_pack/full_season_validation_result_p8_1.json"


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8-sig") as f:
        return json.load(f)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def main() -> None:
    result: Dict[str, Any] = {
        "document_type": "full_season_validation_result",
        "version": "1.0-stage243-p8.1-local-rerun",
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "source_fixture": rel(FIXTURE),
        "source_schema": rel(SCHEMA),
        "source_self_check": rel(SELF_CHECK),
        "source_protocol": rel(PROTOCOL),
        "input_file_fingerprints": {},
        "json_parse_pass": False,
        "json_parse_error_count": 0,
        "parsed_file_count": 0,
        "schema_validation_pass": False,
        "schema_error_count": 0,
        "schema_error_paths": [],
        "cross_level_integrity_pass": False,
        "integrity_error_count": 0,
        "integrity_warning_count": 0,
        "blocking_integrity_findings": [],
        "boundary_invariants_pass": False,
        "boundary_error_count": 0,
        "boundary_warning_count": 0,
        "overall_validation_status": "blocked",
        "gate_a_ready_after_validation": False,
        "scorecard_preflight_allowed": False,
        "required_next_actions": [],
        "promotion_status": {
            "macro_planner_promotion": "blocked",
            "full_author_promotion": "blocked",
            "live_generation_readiness": "blocked",
        },
        "safety": {
            "provider_call_count": 0,
            "runtime_generation": False,
            "raw_text_exported": False,
            "raw_vectors_exported": False,
            "draft_text_exported": False,
            "training_update_started": False,
            "adapter_promotion": False,
            "promotion_claim": False,
        },
    }

    inputs = [
        ("fixture", FIXTURE),
        ("schema", SCHEMA),
        ("self_check", SELF_CHECK),
        ("protocol", PROTOCOL),
    ]
    missing = [rel(path) for _, path in inputs if not path.exists()]
    result["missing_required_inputs"] = missing
    if missing:
        result["overall_validation_status"] = "blocked_missing_required_inputs"
        result["required_next_actions"] = ["load_missing_required_inputs"]
        OUT.write_text(json.dumps(result, ensure_ascii=True, indent=2), encoding="utf-8")
        print(f"Wrote {OUT}")
        return

    parsed: Dict[str, Any] = {}
    for name, path in inputs:
        try:
            parsed[name] = load_json(path)
            result["parsed_file_count"] += 1
            result["input_file_fingerprints"][name] = {
                "path": rel(path),
                "bytes": path.stat().st_size,
                "sha256": sha256_file(path),
            }
        except Exception as exc:
            result["json_parse_error_count"] += 1
            result.setdefault("json_parse_errors", []).append(
                {"file": rel(path), "error": str(exc)}
            )

    result["json_parse_pass"] = result["json_parse_error_count"] == 0

    if not result["json_parse_pass"]:
        result["overall_validation_status"] = "fail_validation"
        result["required_next_actions"] = ["fix_json_parse_errors"]
        OUT.write_text(json.dumps(result, ensure_ascii=True, indent=2), encoding="utf-8")
        print(f"Wrote {OUT}")
        return

    fixture = parsed["fixture"]
    schema = parsed["schema"]
    self_check = parsed["self_check"]
    protocol = parsed["protocol"]
    result["protocol_document_type"] = protocol.get("document_type")
    result["protocol_roadmap_position"] = protocol.get("roadmap_position")

    try:
        import jsonschema

        validator = jsonschema.Draft202012Validator(schema)
        errors = sorted(validator.iter_errors(fixture), key=lambda e: list(e.path))
        result["schema_error_count"] = len(errors)
        result["schema_error_paths"] = [
            "/" + "/".join(map(str, e.path)) + ": " + e.message for e in errors
        ]
        result["schema_validation_pass"] = len(errors) == 0
    except Exception as exc:
        result["schema_validation_pass"] = False
        result["schema_error_count"] = 1
        result["schema_error_paths"] = ["schema_validation_blocked: " + str(exc)]

    integrity_findings: List[str] = []

    expected_counts = fixture.get("included_artifact_inventory", {})
    if expected_counts.get("full_series_arc_spec_count", 0) < 1:
        integrity_findings.append("missing_full_series_arc_spec_ref")
    if expected_counts.get("season_plan_count", 0) < 1:
        integrity_findings.append("missing_season_plan_ref")
    if expected_counts.get("episode_arc_chain_count", 0) < 1:
        integrity_findings.append("missing_episode_arc_chain_ref")
    if expected_counts.get("sequence_blueprint_count", 0) < 1:
        integrity_findings.append("missing_sequence_blueprint_refs")
    if expected_counts.get("scene_blueprint_count", 0) < 1:
        integrity_findings.append("missing_scene_blueprint_refs")
    if expected_counts.get("renderer_prompt_packet_count", 0) < 1:
        integrity_findings.append("missing_renderer_prompt_packet_refs")

    if fixture.get("package_identity", {}).get("target_episode_count") not in (16, 24):
        integrity_findings.append("invalid_target_episode_count")

    checks = fixture.get("cross_level_integrity_checks", {})
    not_run_checks = [
        key
        for key, value in checks.items()
        if isinstance(value, dict) and value.get("status") == "not_run"
    ]
    if not_run_checks:
        result["integrity_warning_count"] += len(not_run_checks)
        result.setdefault("integrity_warnings", []).extend(
            ["not_run:" + x for x in not_run_checks]
        )

    result["blocking_integrity_findings"] = integrity_findings
    result["integrity_error_count"] = len(integrity_findings)
    result["cross_level_integrity_pass"] = len(integrity_findings) == 0

    boundary_errors: List[str] = []
    authority = fixture.get("authority", {})
    safety = fixture.get("safety_boundary", {})
    if authority.get("provider_call_count") != 0:
        boundary_errors.append("provider_call_count_not_zero")
    if authority.get("runtime_generation") is not False:
        boundary_errors.append("runtime_generation_not_false")
    if authority.get("draft_text_exported") is not False:
        boundary_errors.append("draft_text_exported_not_false")
    if authority.get("promotion_claim") is not False:
        boundary_errors.append("promotion_claim_not_false")
    if safety.get("actual_provider_call_allowed") is not False:
        boundary_errors.append("actual_provider_call_allowed_not_false")
    if safety.get("actual_prose_generation_allowed") is not False:
        boundary_errors.append("actual_prose_generation_allowed_not_false")

    result["boundary_error_count"] = len(boundary_errors)
    result["boundary_errors"] = boundary_errors
    result["boundary_invariants_pass"] = len(boundary_errors) == 0

    if not result["schema_validation_pass"]:
        result["overall_validation_status"] = "fail_validation"
        result["required_next_actions"] = ["fix_schema_validation_errors"]
    elif not result["boundary_invariants_pass"]:
        result["overall_validation_status"] = "blocked"
        result["required_next_actions"] = ["fix_boundary_invariant_errors"]
    elif not result["cross_level_integrity_pass"]:
        result["overall_validation_status"] = "manual_review_required"
        result["required_next_actions"] = ["fix_cross_level_integrity_findings"]
    elif result["integrity_warning_count"] > 0:
        result["overall_validation_status"] = "pass_with_warning"
        result["required_next_actions"] = [
            "run_deeper_instantiated_integrity_checks",
            "rerun_hard_rule_gate",
        ]
    else:
        result["overall_validation_status"] = "pass"
        result["required_next_actions"] = [
            "rerun_hard_rule_gate",
            "consider_scorecard_preflight_if_allowed",
        ]

    hard_rule_pass = self_check.get("self_check_summary", {}).get("hard_rule_pass") is True
    result["hard_rule_pass_from_self_check"] = hard_rule_pass
    result["gate_a_ready_after_validation"] = (
        result["overall_validation_status"] in {"pass", "pass_with_warning"}
        and hard_rule_pass
    )
    result["scorecard_preflight_allowed"] = result["gate_a_ready_after_validation"]
    result["next_required_step"] = (
        "rerun_hard_rule_gate_before_scorecard"
        if result["overall_validation_status"] in {"pass", "pass_with_warning"}
        else "resolve_validation_findings"
    )

    OUT.write_text(json.dumps(result, ensure_ascii=True, indent=2), encoding="utf-8")
    print(f"Wrote {OUT}")
    print(
        json.dumps(
            {
                "json_parse_pass": result["json_parse_pass"],
                "schema_validation_pass": result["schema_validation_pass"],
                "schema_error_count": result["schema_error_count"],
                "cross_level_integrity_pass": result["cross_level_integrity_pass"],
                "integrity_error_count": result["integrity_error_count"],
                "integrity_warning_count": result["integrity_warning_count"],
                "boundary_invariants_pass": result["boundary_invariants_pass"],
                "overall_validation_status": result["overall_validation_status"],
                "hard_rule_pass_from_self_check": result["hard_rule_pass_from_self_check"],
                "gate_a_ready_after_validation": result["gate_a_ready_after_validation"],
                "scorecard_preflight_allowed": result["scorecard_preflight_allowed"],
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
