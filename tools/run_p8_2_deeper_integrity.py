import json
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

P8_1_RESULT = Path("release/current/season_wiring_pack/full_season_validation_result_p8_1.json")
P8_2_CONTRACT = Path("release/current/season_wiring_pack/full_season_hard_rule_gate_rerun_p8_2.json")
FIXTURE = Path("release/current/season_wiring_pack/full_season_candidate_package_fixture_v1.json")
EPISODE_ARC = Path("release/current/data_foundry_pack/episode_arc_inventory_v5.json")
SEQUENCE_BLUEPRINT = Path("release/current/data_foundry_pack/sequence_blueprint_inventory_v5.json")
SCENE_TAXONOMY = Path("release/current/data_foundry_pack/scene_function_taxonomy_16_v5.json")
PAIR_DISTRIBUTION = Path("release/current/data_foundry_pack/scene_function_pair_distribution_v5.json")
SCHEMA_REGISTRY = Path("release/current/data_foundry_pack/schema_registry.json")
PROMOTION_REGISTRY = Path("release/current/measured_learning_pack/promotion_evidence_registry.json")

DEEPER_RESULT = Path("release/current/season_wiring_pack/full_season_deeper_integrity_result_p8_2.json")
SELF_CHECK_V2 = Path("release/current/season_wiring_pack/full_season_hard_rule_self_check_v2.json")
REPORT = Path("release/current/transition_council_pack/p8_2_local_deeper_integrity_execution_report_20260705.md")


def read_json(rel):
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


def write_json(rel, data):
    path = ROOT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def now():
    return datetime.now(timezone.utc).isoformat()


def check(status, check_id, evidence, limitations=None, required_next_action=None):
    return {
        "check_id": check_id,
        "status": status,
        "evidence": evidence,
        "limitations": limitations or [],
        "required_next_action": required_next_action,
    }


def run_checks(fixture, p8_1, episode_arc, sequence_blueprint, scene_taxonomy, pair_distribution):
    package = fixture.get("package_identity", {})
    inventory = fixture.get("included_artifact_inventory", {})
    safety = fixture.get("safety_boundary", {})
    target_episode_count = package.get("target_episode_count")

    episode_coverage = episode_arc.get("coverage", {})
    episode_aggregate = episode_arc.get("aggregate", {})
    sequence_records = sequence_blueprint.get("records_per_episode", {})
    taxonomy_summary = scene_taxonomy.get("summary", {})
    pair_summary = pair_distribution.get("summary", {})
    p8_1_warning_ids = {
        item.split(":", 1)[-1]
        for item in p8_1.get("integrity_warnings", [])
    }

    checks = []

    series_refs_present = all(
        fixture.get(k, {}).get("status") == "present"
        for k in ("full_series_arc_spec_ref", "season_plan_ref")
    )
    checks.append(check(
        "manual_review_required",
        "series_to_season_integrity",
        {
            "series_id_present": bool(package.get("series_id")),
            "season_id_present": bool(package.get("season_id")),
            "target_episode_count": target_episode_count,
            "full_series_arc_spec_ref_present": series_refs_present,
            "season_plan_ref_present": series_refs_present,
        },
        [
            "Fixture exposes references and package identity, but not instantiated season goal, central conflict axis, entry state, or exit state values.",
            "Metadata-only references cannot prove series-to-season narrative alignment.",
        ],
        "Inspect instantiated FullSeriesArcSpec and SeasonPlan fields before hard-rule pass.",
    ))

    checks.append(check(
        "manual_review_required",
        "season_to_episode_integrity",
        {
            "target_episode_count": target_episode_count,
            "episode_arc_chain_ref_status": fixture.get("episode_arc_chain_ref", {}).get("status"),
            "seqcard_episode_ids": episode_coverage.get("seqcard_episode_ids"),
            "episode_arc_files": episode_coverage.get("episode_arc_files"),
            "seqcard_without_episode_arc": episode_coverage.get("seqcard_without_episode_arc"),
            "episode_arc_without_seqcard": episode_coverage.get("episode_arc_without_seqcard"),
        },
        [
            "V5 corpus-level EpisodeArc coverage is complete, but the fixture does not expose the actual 16 ordered episode nodes.",
            "Midpoint, crisis, climax, resolution, and episode transition continuity cannot be proven from counts alone.",
        ],
        "Provide or inspect instantiated EpisodeArcChain nodes for the 16-episode candidate.",
    ))

    seq_count_min = episode_aggregate.get("sequence_count_min")
    seq_count_max = episode_aggregate.get("sequence_count_max")
    seq_missing = episode_coverage.get("seqcard_without_seqblueprint", [])
    checks.append(check(
        "pass_with_warning" if seq_missing == [] and seq_count_min is not None and seq_count_max is not None else "manual_review_required",
        "episode_to_sequence_integrity",
        {
            "fixture_target_episode_count": target_episode_count,
            "fixture_sequence_blueprint_count": inventory.get("sequence_blueprint_count"),
            "v5_sequence_count_min": seq_count_min,
            "v5_sequence_count_max": seq_count_max,
            "v5_sequence_count_mean": episode_aggregate.get("sequence_count_mean"),
            "seqcard_without_seqblueprint": seq_missing,
            "seqblueprint_without_seqcard": episode_coverage.get("seqblueprint_without_seqcard"),
        },
        [
            "Corpus-level episode-to-sequence coverage is complete, but fixture-specific episode-to-sequence IDs are not enumerated.",
        ],
        "Bind fixture episode nodes to concrete sequence blueprint IDs before hard-rule pass.",
    ))

    member_scene_warning_count = sequence_blueprint.get("member_scene_warning_count")
    checks.append(check(
        "pass_with_warning" if member_scene_warning_count == 0 else "manual_review_required",
        "sequence_to_scene_integrity",
        {
            "sequence_blueprint_record_count": sequence_blueprint.get("record_count"),
            "records_per_episode": sequence_records,
            "member_scene_warning_count": member_scene_warning_count,
            "member_scene_warning_samples": sequence_blueprint.get("member_scene_warning_samples"),
            "fixture_scene_blueprint_count": inventory.get("scene_blueprint_count"),
        },
        [
            "Member-scene metadata has no warning samples, but required transition support is not available as exported fixture instances.",
        ],
        "Bind fixture sequence spans to concrete scene blueprint IDs before hard-rule pass.",
    ))

    scene_count = inventory.get("scene_blueprint_count")
    renderer_count = inventory.get("renderer_prompt_packet_count")
    renderer_refs_present = all(
        ref.get("status") == "present"
        for ref in fixture.get("llm_renderer_prompt_packet_refs", [])
    )
    renderer_authority_safe = not any([
        safety.get("actual_provider_call_allowed"),
        safety.get("actual_prose_generation_allowed"),
        safety.get("canonical_mutation_allowed"),
    ])
    checks.append(check(
        "pass_with_warning" if scene_count == renderer_count and renderer_refs_present and renderer_authority_safe else "manual_review_required",
        "scene_to_renderer_packet_integrity",
        {
            "fixture_scene_blueprint_count": scene_count,
            "fixture_renderer_prompt_packet_count": renderer_count,
            "renderer_refs_present": renderer_refs_present,
            "provider_call_allowed": safety.get("actual_provider_call_allowed"),
            "prose_generation_allowed": safety.get("actual_prose_generation_allowed"),
            "canonical_mutation_allowed": safety.get("canonical_mutation_allowed"),
        },
        [
            "Counts and safety boundary align, but packet-by-scene bijection is not instantiated in exported metadata.",
        ],
        "Expose metadata-only scene_id to renderer_packet_id mapping for hard-rule pass.",
    ))

    manual_checks = [
        (
            "plant_payoff_integrity",
            "Plant/payoff ledgers are not exported as instantiated metadata, so orphan plant, payoff-without-plant, timing, and unresolved setup risks cannot be cleared.",
            "Provide metadata-only plant/payoff ledger IDs and timing links.",
        ),
        (
            "character_arc_integrity",
            "Character state, belief, motivation, and agency transitions are not exported as instantiated metadata.",
            "Provide metadata-only character arc transition graph with causal supports.",
        ),
        (
            "relationship_arc_integrity",
            "Relationship state transitions and reversal causes are not exported as instantiated metadata.",
            "Provide metadata-only relationship transition graph with supporting event IDs.",
        ),
        (
            "causal_spine_integrity",
            "Causal dependency edges across episodes and sequences are not exported as instantiated metadata.",
            "Provide metadata-only causal edge graph linking episode, sequence, and scene IDs.",
        ),
        (
            "hook_chain_integrity",
            "Hook-to-consequence links are not exported as instantiated metadata.",
            "Provide metadata-only hook ledger with downstream consequence IDs.",
        ),
    ]
    for check_id, limitation, action in manual_checks:
        checks.append(check(
            "manual_review_required",
            check_id,
            {
                "fixture_declared_status": fixture.get("cross_level_integrity_checks", {}).get(check_id, {}).get("status"),
                "p8_1_warning_present": check_id in p8_1_warning_ids,
            },
            [limitation],
            action,
        ))

    taxonomy_ok = (
        taxonomy_summary.get("records_total", 0) > 0
        and taxonomy_summary.get("core_missing") == 0
        and taxonomy_summary.get("all_16_present_in_core") is True
        and pair_summary.get("unique_pairs", 0) > 0
    )
    checks.append(check(
        "pass_with_warning" if taxonomy_ok else "manual_review_required",
        "genre_rhythm_integrity",
        {
            "scene_function_records_total": taxonomy_summary.get("records_total"),
            "core_missing": taxonomy_summary.get("core_missing"),
            "all_16_present_in_core": taxonomy_summary.get("all_16_present_in_core"),
            "unique_scene_function_pairs": pair_summary.get("unique_pairs"),
            "core2_none_treated_as_missing": pair_summary.get("core2_NONE_treated_as_missing"),
        },
        [
            "Scene-function distribution is strong corpus-level rhythm evidence, but candidate-specific genre mode and rhythm target are not instantiated.",
        ],
        "Bind candidate season genre mode and per-episode rhythm targets to scene-function metadata.",
    ))

    return checks


def summarize(checks):
    counts = {
        "pass_count": sum(1 for c in checks if c["status"] == "pass"),
        "pass_with_warning_count": sum(1 for c in checks if c["status"] == "pass_with_warning"),
        "manual_review_required_count": sum(1 for c in checks if c["status"] == "manual_review_required"),
        "fail_hard_rule_count": sum(1 for c in checks if c["status"] == "fail_hard_rule"),
        "blocked_count": sum(1 for c in checks if c["status"] == "blocked"),
    }
    if counts["blocked_count"]:
        overall = "blocked"
    elif counts["fail_hard_rule_count"]:
        overall = "fail_hard_rule"
    elif counts["manual_review_required_count"]:
        overall = "manual_review_required"
    elif counts["pass_with_warning_count"]:
        overall = "pass_with_warning"
    else:
        overall = "pass"
    return counts, overall


def update_schema_registry(result, self_check):
    path = ROOT / SCHEMA_REGISTRY
    if not path.exists():
        return
    registry = read_json(SCHEMA_REGISTRY)
    registry["version"] = "2.4-stage243-v5-p8.2-deeper-integrity"
    registry["purpose"] = (
        registry.get("purpose", "")
        + " Includes P8.2 local deeper integrity result and hard-rule self-check v2."
    ).strip()
    schemas = registry.setdefault("schemas", {})
    schemas["full_season_deeper_integrity_result_p8_2"] = {
        "path": str(DEEPER_RESULT).replace("\\", "/"),
        "document_type": result["document_type"],
        "status": result["overall_deeper_integrity_status"],
        "check_count": len(result["check_results"]),
        "manual_review_required_count": result["manual_review_required_count"],
        "export_policy": "metadata-only integrity findings; no raw prose exported",
    }
    schemas["full_season_hard_rule_self_check_v2"] = {
        "path": str(SELF_CHECK_V2).replace("\\", "/"),
        "document_type": self_check["document_type"],
        "hard_rule_pass": self_check["hard_rule_pass"],
        "final_verdict": self_check["final_verdict"],
        "export_policy": "metadata-only hard-rule gate result; no promotion claim",
    }
    write_json(SCHEMA_REGISTRY, registry)


def update_promotion_registry(result, self_check):
    path = ROOT / PROMOTION_REGISTRY
    if not path.exists():
        return
    registry = read_json(PROMOTION_REGISTRY)
    structural = registry.setdefault("evidence_classes", {}).setdefault("structural_evidence", {})
    structural["status"] = "partial_seqcard_v5_p8_2_deeper_integrity_manual_review_required_gate_a_blocked"
    artifacts = structural.setdefault("current_artifacts", [])
    for rel in (str(DEEPER_RESULT).replace("\\", "/"), str(SELF_CHECK_V2).replace("\\", "/")):
        if rel not in artifacts:
            artifacts.append(rel)
    facts = structural.setdefault("current_measured_facts", {})
    facts.update({
        "p8_2_deeper_integrity_status": result["overall_deeper_integrity_status"],
        "p8_2_pass_with_warning_count": result["pass_with_warning_count"],
        "p8_2_manual_review_required_count": result["manual_review_required_count"],
        "p8_2_fail_hard_rule_count": result["fail_hard_rule_count"],
        "p8_2_blocked_count": result["blocked_count"],
        "p8_2_hard_rule_pass": self_check["hard_rule_pass"],
        "p8_2_gate_a_ready": self_check["gate_a_ready"],
        "p8_2_scorecard_preflight_allowed": self_check["scorecard_preflight_allowed"],
    })
    gate_status = registry.setdefault("gate_status", {})
    gate_status["p8_2_hard_rule_gate"] = {
        "status": self_check["final_verdict"],
        "hard_rule_pass": self_check["hard_rule_pass"],
        "gate_a_ready": self_check["gate_a_ready"],
        "scorecard_preflight_allowed": self_check["scorecard_preflight_allowed"],
    }
    write_json(PROMOTION_REGISTRY, registry)


def write_report(result, self_check):
    lines = [
        "# P8.2 Local Deeper Integrity Execution Report",
        "",
        "Date: 2026-07-05",
        "Status: local execution completed; hard-rule remains blocked",
        "Scope: Stage243 P8.2 / 11 deeper integrity checks / metadata-only execution",
        "",
        "## Summary",
        "",
        f"- Overall deeper integrity status: `{result['overall_deeper_integrity_status']}`",
        f"- pass: `{result['pass_count']}`",
        f"- pass_with_warning: `{result['pass_with_warning_count']}`",
        f"- manual_review_required: `{result['manual_review_required_count']}`",
        f"- fail_hard_rule: `{result['fail_hard_rule_count']}`",
        f"- blocked: `{result['blocked_count']}`",
        f"- hard_rule_pass: `{str(self_check['hard_rule_pass']).lower()}`",
        f"- gate_a_ready: `{str(self_check['gate_a_ready']).lower()}`",
        f"- scorecard_preflight_allowed: `{str(self_check['scorecard_preflight_allowed']).lower()}`",
        "",
        "## Boundary",
        "",
        "- provider_call_count: `0`",
        "- live prose generation: `false`",
        "- canonical mutation: `false`",
        "- training update: `false`",
        "- adapter promotion: `false`",
        "- promotion claim: `false`",
        "- P9 Scorecard Preflight: `not run`",
        "",
        "## Check Results",
        "",
    ]
    for c in result["check_results"]:
        lines.extend([
            f"### {c['check_id']}",
            "",
            f"- status: `{c['status']}`",
            f"- required_next_action: {c.get('required_next_action')}",
            f"- evidence: `{json.dumps(c['evidence'], ensure_ascii=False)}`",
            f"- limitations: `{json.dumps(c['limitations'], ensure_ascii=False)}`",
            "",
        ])
    lines.extend([
        "## Final Decision",
        "",
        "P8.2 did execute the 11 deeper integrity checks at the available metadata level. The result does not permit Gate A or P9 because seven checks still require instantiated narrative ledgers or human review before hard-rule pass can be claimed.",
        "",
        "Next local requirement: provide metadata-only instantiated ledgers for episode nodes, sequence/scene IDs, plant-payoff links, character/relationship transitions, causal edges, and hook consequences. Until then, P9 remains blocked.",
        "",
    ])
    path = ROOT / REPORT
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def main():
    required_inputs = [
        P8_1_RESULT,
        P8_2_CONTRACT,
        FIXTURE,
        EPISODE_ARC,
        SEQUENCE_BLUEPRINT,
        SCENE_TAXONOMY,
        PAIR_DISTRIBUTION,
        SCHEMA_REGISTRY,
        PROMOTION_REGISTRY,
    ]
    input_files_present = {
        str(rel).replace("\\", "/"): (ROOT / rel).exists()
        for rel in required_inputs
    }
    if not all(input_files_present.values()):
        checks = []
        counts = {
            "pass_count": 0,
            "pass_with_warning_count": 0,
            "manual_review_required_count": 0,
            "fail_hard_rule_count": 0,
            "blocked_count": 1,
        }
        overall = "blocked"
    else:
        p8_1 = read_json(P8_1_RESULT)
        p8_2 = read_json(P8_2_CONTRACT)
        fixture = read_json(FIXTURE)
        episode_arc = read_json(EPISODE_ARC)
        sequence_blueprint = read_json(SEQUENCE_BLUEPRINT)
        scene_taxonomy = read_json(SCENE_TAXONOMY)
        pair_distribution = read_json(PAIR_DISTRIBUTION)
        checks = run_checks(fixture, p8_1, episode_arc, sequence_blueprint, scene_taxonomy, pair_distribution)
        counts, overall = summarize(checks)

    hard_rule_pass = overall in {"pass", "pass_with_warning"} and counts["manual_review_required_count"] == 0
    gate_a_ready = hard_rule_pass
    scorecard_preflight_allowed = hard_rule_pass and gate_a_ready

    result = {
        "document_type": "full_season_deeper_integrity_result",
        "version": "1.0-stage243-p8.2-local-execution",
        "created_at": now(),
        "source_validation_result": str(P8_1_RESULT).replace("\\", "/"),
        "source_p8_2_contract": str(P8_2_CONTRACT).replace("\\", "/"),
        "input_files_present": input_files_present,
        "check_results": checks,
        **counts,
        "overall_deeper_integrity_status": overall,
        "hard_rule_recommendation": "pass" if hard_rule_pass else "do_not_pass",
        "gate_a_recommendation": "ready" if gate_a_ready else "blocked",
        "scorecard_preflight_recommendation": "allowed" if scorecard_preflight_allowed else "blocked",
        "safety": {
            "metadata_only": True,
            "provider_call_count": 0,
            "runtime_generation": False,
            "live_prose_generation": False,
            "canonical_mutation": False,
            "training_update": False,
            "adapter_promotion": False,
            "promotion_claim": False,
            "p9_scorecard_preflight_run": False,
            "raw_text_exported": False,
            "raw_vectors_exported": False,
        },
    }

    blocking_findings = [
        {
            "check_id": c["check_id"],
            "status": c["status"],
            "required_next_action": c["required_next_action"],
        }
        for c in checks
        if c["status"] in {"manual_review_required", "fail_hard_rule", "blocked"}
    ]
    warning_findings = [
        {
            "check_id": c["check_id"],
            "status": c["status"],
            "limitations": c["limitations"],
        }
        for c in checks
        if c["status"] == "pass_with_warning"
    ]
    self_check = {
        "document_type": "full_season_hard_rule_self_check",
        "version": "2.0-stage243-p8.2-local-execution",
        "created_at": now(),
        "source_p8_1_result": str(P8_1_RESULT).replace("\\", "/"),
        "source_deeper_integrity_result": str(DEEPER_RESULT).replace("\\", "/"),
        "hard_rule_pass": hard_rule_pass,
        "final_verdict": "pass" if hard_rule_pass else "manual_review_required",
        "gate_a_ready": gate_a_ready,
        "scorecard_preflight_allowed": scorecard_preflight_allowed,
        "blocking_findings": blocking_findings,
        "warning_findings": warning_findings,
        "required_next_actions": [
            "do_not_run_P9_until_hard_rule_pass_and_gate_a_ready",
            "provide_metadata_only_instantiated_episode_sequence_scene_ledgers",
            "provide_metadata_only_plant_payoff_character_relationship_causal_hook_ledgers",
            "rerun_P8_2_deeper_integrity_after_ledgers_are_available",
        ],
        "promotion_status": {
            "macro_planner_promotion": "blocked",
            "full_author_promotion": "blocked",
            "live_generation_readiness": "blocked",
        },
        "safety": result["safety"],
    }

    write_json(DEEPER_RESULT, result)
    write_json(SELF_CHECK_V2, self_check)
    update_schema_registry(result, self_check)
    update_promotion_registry(result, self_check)
    write_report(result, self_check)
    print(json.dumps({
        "wrote": [
            str(DEEPER_RESULT).replace("\\", "/"),
            str(SELF_CHECK_V2).replace("\\", "/"),
            str(REPORT).replace("\\", "/"),
        ],
        "overall_deeper_integrity_status": overall,
        "pass_with_warning_count": counts["pass_with_warning_count"],
        "manual_review_required_count": counts["manual_review_required_count"],
        "hard_rule_pass": hard_rule_pass,
        "gate_a_ready": gate_a_ready,
        "scorecard_preflight_allowed": scorecard_preflight_allowed,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
