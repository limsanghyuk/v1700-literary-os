import json
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

SCHEMA = Path("release/current/season_wiring_pack/full_season_instantiated_ledger_schema_p8_3.json")
TEMPLATE = Path("release/current/season_wiring_pack/full_season_instantiated_ledger_fixture_p8_3.json")
P8_2_RESULT = Path("release/current/season_wiring_pack/full_season_deeper_integrity_result_p8_2.json")
P8_2_SELF_CHECK = Path("release/current/season_wiring_pack/full_season_hard_rule_self_check_v2.json")
P8_1_RESULT = Path("release/current/season_wiring_pack/full_season_validation_result_p8_1.json")
FIXTURE = Path("release/current/season_wiring_pack/full_season_candidate_package_fixture_v1.json")
EPISODE_ARC = Path("release/current/data_foundry_pack/episode_arc_inventory_v5.json")
SEQUENCE_BLUEPRINT = Path("release/current/data_foundry_pack/sequence_blueprint_inventory_v5.json")
SCHEMA_REGISTRY = Path("release/current/data_foundry_pack/schema_registry.json")
PROMOTION_REGISTRY = Path("release/current/measured_learning_pack/promotion_evidence_registry.json")

RESULT = Path("release/current/season_wiring_pack/full_season_instantiated_ledger_result_p8_3.json")
VALIDATION = Path("release/current/season_wiring_pack/full_season_instantiated_ledger_validation_p8_3.json")
REPORT = Path("release/current/transition_council_pack/p8_3_local_instantiated_ledger_build_report_20260710.md")


def read_json(rel):
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


def write_json(rel, data):
    path = ROOT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_text(rel, text):
    path = ROOT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def utc_now():
    return datetime.now(timezone.utc).isoformat()


def count_ledgers(ledgers):
    return {
        "episode_nodes": len(ledgers["episode_node_ledger"]),
        "sequence_bindings": len(ledgers["sequence_binding_ledger"]),
        "scene_bindings": len(ledgers["scene_binding_ledger"]),
        "renderer_bindings": len(ledgers["renderer_packet_binding_ledger"]),
        "plant_payoff_links": len(ledgers["plant_payoff_ledger"]),
        "character_transitions": len(ledgers["character_arc_transition_ledger"]),
        "relationship_transitions": len(ledgers["relationship_arc_transition_ledger"]),
        "causal_edges": len(ledgers["causal_edge_ledger"]),
        "hook_links": len(ledgers["hook_consequence_ledger"]),
        "genre_rhythm_targets": len(ledgers["genre_rhythm_target_ledger"]),
    }


def validate_with_jsonschema(schema, instance):
    try:
        import jsonschema
    except Exception as exc:
        return False, [f"jsonschema_unavailable: {exc}"]
    validator = jsonschema.Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(instance), key=lambda e: list(e.path))
    return not errors, [
        {"path": "/".join(str(x) for x in e.path), "message": e.message}
        for e in errors
    ]


def build_result():
    required = [SCHEMA, TEMPLATE, P8_2_RESULT, P8_2_SELF_CHECK, P8_1_RESULT, FIXTURE, EPISODE_ARC, SEQUENCE_BLUEPRINT]
    input_files_present = {str(p).replace("\\", "/"): (ROOT / p).exists() for p in required}
    if not all(input_files_present.values()):
        template = {
            "document_type": "full_season_instantiated_ledger",
            "version": "1.0-stage243-p8.3-local-build",
            "authority": {
                "metadata_only": True,
                "fixture_template_only": False,
                "local_execution_required": True,
                "raw_text_exported": False,
                "provider_call_count": 0,
                "runtime_generation": False,
                "promotion_claim": False,
            },
            "source_refs": {},
            "candidate_identity": {
                "candidate_package_id": "missing_inputs",
                "series_id": "missing_inputs",
                "season_id": "missing_inputs",
                "target_episode_count": 1,
            },
            "ledger_status": {
                "overall_status": "blocked",
                "ledger_instance_level": "template_only",
                "gate_a_ready": False,
                "scorecard_preflight_allowed": False,
            },
            "ledgers": {
                "episode_node_ledger": [],
                "sequence_binding_ledger": [],
                "scene_binding_ledger": [],
                "renderer_packet_binding_ledger": [],
                "plant_payoff_ledger": [],
                "character_arc_transition_ledger": [],
                "relationship_arc_transition_ledger": [],
                "causal_edge_ledger": [],
                "hook_consequence_ledger": [],
                "genre_rhythm_target_ledger": [],
            },
            "coverage_summary": {
                "episode_nodes": 0,
                "sequence_bindings": 0,
                "scene_bindings": 0,
                "renderer_bindings": 0,
                "plant_payoff_links": 0,
                "character_transitions": 0,
                "relationship_transitions": 0,
                "causal_edges": 0,
                "hook_links": 0,
                "genre_rhythm_targets": 0,
            },
            "hard_rule_resolution_targets": [],
            "safety": {
                "metadata_only": True,
                "raw_text_exported": False,
                "raw_vectors_exported": False,
                "provider_call_count": 0,
                "runtime_generation": False,
                "training_update": False,
                "adapter_promotion": False,
                "promotion_claim": False,
                "p9_scorecard_preflight_run": False,
            },
        }
        return template, input_files_present, ["missing_required_inputs"]

    template = read_json(TEMPLATE)
    fixture = read_json(FIXTURE)
    episode_arc = read_json(EPISODE_ARC)
    sequence_blueprint = read_json(SEQUENCE_BLUEPRINT)

    ledgers = {name: [] for name in template["ledgers"].keys()}

    # The available artifacts expose aggregate counts and bundle refs, not concrete
    # episode/sequence/scene IDs. Keeping ledgers empty is intentional: a placeholder
    # would be schema-valid but would falsely imply instantiated evidence.
    coverage = count_ledgers(ledgers)

    result = {
        "document_type": "full_season_instantiated_ledger",
        "version": "1.0-stage243-p8.3-local-build",
        "authority": {
            "metadata_only": True,
            "fixture_template_only": False,
            "local_execution_required": False,
            "raw_text_exported": False,
            "provider_call_count": 0,
            "runtime_generation": False,
            "promotion_claim": False,
        },
        "source_refs": template.get("source_refs", {}),
        "candidate_identity": fixture.get("package_identity", template.get("candidate_identity", {})),
        "ledger_status": {
            "overall_status": "manual_review_required",
            "ledger_instance_level": "reference_only",
            "gate_a_ready": False,
            "scorecard_preflight_allowed": False,
        },
        "ledgers": ledgers,
        "coverage_summary": coverage,
        "hard_rule_resolution_targets": template.get("hard_rule_resolution_targets", []),
        "safety": {
            "metadata_only": True,
            "raw_text_exported": False,
            "raw_vectors_exported": False,
            "provider_call_count": 0,
            "runtime_generation": False,
            "training_update": False,
            "adapter_promotion": False,
            "promotion_claim": False,
            "p9_scorecard_preflight_run": False,
        },
    }
    # Schema only allows candidate_identity's four required keys.
    result["candidate_identity"] = {
        "candidate_package_id": result["candidate_identity"].get("candidate_package_id", "unknown"),
        "series_id": result["candidate_identity"].get("series_id", "unknown"),
        "season_id": result["candidate_identity"].get("season_id", "unknown"),
        "target_episode_count": result["candidate_identity"].get("target_episode_count", 1),
    }

    notes = [
        "No concrete episode_node_ledger entries were created because candidate episode nodes are not exported.",
        "No concrete sequence/scene/renderer bindings were created because fixture bundle refs expose counts, not per-ID mappings.",
        "No plant/payoff, character, relationship, causal, or hook ledgers were created because instantiated metadata ledgers are absent.",
        f"Available support: target_episode_count={result['candidate_identity']['target_episode_count']}, fixture_counts={fixture.get('included_artifact_inventory', {})}.",
        f"Available corpus aggregate support: episode_arc_coverage={episode_arc.get('coverage', {})}, sequence_records={sequence_blueprint.get('record_count')}.",
    ]
    return result, input_files_present, notes


def update_registries(result, validation):
    if (ROOT / SCHEMA_REGISTRY).exists():
        registry = read_json(SCHEMA_REGISTRY)
        registry["version"] = "2.5-stage243-v5-p8.3-ledger-build"
        schemas = registry.setdefault("schemas", {})
        schemas["full_season_instantiated_ledger_result_p8_3"] = {
            "path": str(RESULT).replace("\\", "/"),
            "document_type": result["document_type"],
            "overall_status": result["ledger_status"]["overall_status"],
            "ledger_instance_level": result["ledger_status"]["ledger_instance_level"],
            "schema_validation_pass": validation["schema_validation_pass"],
            "export_policy": "metadata-only; no raw prose, vectors, or generated text",
        }
        schemas["full_season_instantiated_ledger_validation_p8_3"] = {
            "path": str(VALIDATION).replace("\\", "/"),
            "document_type": validation["document_type"],
            "validation_status": validation["validation_status"],
            "export_policy": "metadata-only validation report",
        }
        write_json(SCHEMA_REGISTRY, registry)

    if (ROOT / PROMOTION_REGISTRY).exists():
        registry = read_json(PROMOTION_REGISTRY)
        structural = registry.setdefault("evidence_classes", {}).setdefault("structural_evidence", {})
        structural["status"] = "partial_seqcard_v5_p8_3_ledger_build_manual_review_required_gate_a_blocked"
        artifacts = structural.setdefault("current_artifacts", [])
        for rel in [str(RESULT).replace("\\", "/"), str(VALIDATION).replace("\\", "/")]:
            if rel not in artifacts:
                artifacts.append(rel)
        facts = structural.setdefault("current_measured_facts", {})
        facts.update({
            "p8_3_ledger_overall_status": result["ledger_status"]["overall_status"],
            "p8_3_ledger_instance_level": result["ledger_status"]["ledger_instance_level"],
            "p8_3_schema_validation_pass": validation["schema_validation_pass"],
            "p8_3_gate_a_ready": result["ledger_status"]["gate_a_ready"],
            "p8_3_scorecard_preflight_allowed": result["ledger_status"]["scorecard_preflight_allowed"],
        })
        registry.setdefault("gate_status", {})["p8_3_instantiated_ledger_build"] = {
            "status": result["ledger_status"]["overall_status"],
            "schema_validation_pass": validation["schema_validation_pass"],
            "gate_a_ready": result["ledger_status"]["gate_a_ready"],
            "scorecard_preflight_allowed": result["ledger_status"]["scorecard_preflight_allowed"],
        }
        write_json(PROMOTION_REGISTRY, registry)


def write_report(result, validation, input_files_present, notes):
    lines = [
        "# P8.3 Local Instantiated Ledger Build Report",
        "",
        "Date: 2026-07-10",
        "Status: local build completed; instantiated ledger remains manual_review_required",
        "Scope: Stage243 P8.3 / metadata-only full-season ledger build",
        "",
        "## Result",
        "",
        f"- ledger overall_status: `{result['ledger_status']['overall_status']}`",
        f"- ledger_instance_level: `{result['ledger_status']['ledger_instance_level']}`",
        f"- schema_validation_pass: `{str(validation['schema_validation_pass']).lower()}`",
        f"- validation_status: `{validation['validation_status']}`",
        f"- gate_a_ready: `{str(result['ledger_status']['gate_a_ready']).lower()}`",
        f"- scorecard_preflight_allowed: `{str(result['ledger_status']['scorecard_preflight_allowed']).lower()}`",
        "",
        "## Coverage Summary",
        "",
    ]
    for key, value in result["coverage_summary"].items():
        lines.append(f"- {key}: `{value}`")
    lines.extend([
        "",
        "## Build Notes",
        "",
    ])
    lines.extend(f"- {note}" for note in notes)
    lines.extend([
        "",
        "## Input Files Present",
        "",
    ])
    lines.extend(f"- `{path}`: `{str(present).lower()}`" for path, present in input_files_present.items())
    lines.extend([
        "",
        "## Boundary",
        "",
        "- provider_call_count: `0`",
        "- raw_text_exported: `false`",
        "- raw_vectors_exported: `false`",
        "- runtime_generation: `false`",
        "- training_update: `false`",
        "- adapter_promotion: `false`",
        "- promotion_claim: `false`",
        "- P9 Scorecard Preflight: `not run`",
        "",
        "## Final Decision",
        "",
        "P8.3 produced a schema-valid metadata-only ledger result, but no instantiated ledger entries could be safely created from the currently exported artifacts. Gate A and P9 remain blocked until concrete metadata-only episode, sequence, scene, renderer, plant/payoff, character, relationship, causal, hook, and genre-rhythm ledger entries are available.",
        "",
    ])
    write_text(REPORT, "\n".join(lines))


def main():
    schema = read_json(SCHEMA)
    result, input_files_present, notes = build_result()
    schema_ok, schema_errors = validate_with_jsonschema(schema, result)
    validation = {
        "document_type": "full_season_instantiated_ledger_validation",
        "version": "1.0-stage243-p8.3-local-build",
        "created_at": utc_now(),
        "source_schema": str(SCHEMA).replace("\\", "/"),
        "source_result": str(RESULT).replace("\\", "/"),
        "input_files_present": input_files_present,
        "json_parse_pass": True,
        "schema_validation_pass": schema_ok,
        "schema_error_count": len(schema_errors),
        "schema_errors": schema_errors,
        "validation_status": "pass_with_manual_review_required" if schema_ok else "fail_schema_validation",
        "gate_a_ready": False,
        "scorecard_preflight_allowed": False,
        "safety": result["safety"],
    }
    write_json(RESULT, result)
    write_json(VALIDATION, validation)
    update_registries(result, validation)
    write_report(result, validation, input_files_present, notes)
    print(json.dumps({
        "wrote": [
            str(RESULT).replace("\\", "/"),
            str(VALIDATION).replace("\\", "/"),
            str(REPORT).replace("\\", "/"),
        ],
        "ledger_status": result["ledger_status"],
        "coverage_summary": result["coverage_summary"],
        "schema_validation_pass": schema_ok,
        "schema_error_count": len(schema_errors),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
