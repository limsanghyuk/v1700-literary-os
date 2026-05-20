from __future__ import annotations

from typing import Any

from .contracts import CandidateSchemaBinding, SchemaDefinition, SchemaField, SchemaRegistry

SCHEMA_REGISTRY_MODE = "SCHEMA_REGISTRY_DRY_RUN"

_DECISION_TO_SCHEMA_ID = {
    "ACCEPT_CANDIDATE": "stage136.accepted_candidate.v1",
    "REJECT_CANDIDATE": "stage136.rejected_candidate.v1",
    "REVIEW_ONLY": "stage136.review_only_candidate.v1",
}


def build_schema_registry(stage135_report: dict[str, Any]) -> SchemaRegistry:
    registry = stage135_report.get("parts", {}).get("candidate_registry", {})
    candidates = registry.get("candidates", [])
    schemas = _default_schema_catalog()
    schema_lookup = {schema.schema_id: schema for schema in schemas}
    bindings = tuple(_bind_candidate(candidate, schema_lookup) for candidate in candidates)
    issues: list[str] = []
    if not candidates:
        issues.append("missing_stage135_candidates")
    if len(schemas) < 3:
        issues.append("schema_catalog_incomplete")
    if any(binding.status != "pass" for binding in bindings):
        issues.append("candidate_binding_failed")
    if any(binding.losdb_write_enabled for binding in bindings):
        issues.append("losdb_write_enabled")
    if any(binding.migration_execution_enabled for binding in bindings):
        issues.append("migration_execution_enabled")
    if any(binding.provider_call_required for binding in bindings):
        issues.append("provider_call_required")
    if any(not binding.schema_valid for binding in bindings):
        issues.append("schema_validation_failed")
    if not any(binding.decision == "REVIEW_ONLY" for binding in bindings):
        issues.append("review_only_schema_route_missing")
    counters = {
        "schema_count": len(schemas),
        "binding_count": len(bindings),
        "validated_candidate_count": sum(1 for binding in bindings if binding.schema_valid),
        "accepted_binding_count": sum(1 for binding in bindings if binding.decision == "ACCEPT_CANDIDATE"),
        "rejected_binding_count": sum(1 for binding in bindings if binding.decision == "REJECT_CANDIDATE"),
        "review_only_binding_count": sum(1 for binding in bindings if binding.decision == "REVIEW_ONLY"),
        "migration_ready_count": sum(1 for binding in bindings if binding.migration_ready),
        "storage_contract_ready_count": sum(1 for binding in bindings if binding.storage_contract_ready),
    }
    return SchemaRegistry(
        stage="136",
        baseline_stage="135",
        status="pass" if not issues else "blocked",
        schemas=schemas,
        bindings=bindings,
        issues=tuple(issues),
        counters=counters,
    )


def _default_schema_catalog() -> tuple[SchemaDefinition, ...]:
    common_fields = (
        SchemaField("case_id", "string", True, "Deterministic case identifier from Stage135 candidate registry."),
        SchemaField("source_stage", "string", True, "Origin stage for the candidate record."),
        SchemaField("source_recommendation", "string", True, "Original recommendation emitted by the predecessor stage."),
        SchemaField("decision", "string", True, "Candidate disposition after Stage135 gate evaluation."),
        SchemaField("gate_verified", "boolean", True, "Whether the predecessor gate verified the source case."),
        SchemaField("writer_review_required", "boolean", True, "Whether a human writer review must happen before promotion."),
        SchemaField("reason", "string", True, "Human-readable rationale preserved for later migration planning."),
    )
    return (
        SchemaDefinition(
            schema_id="stage136.accepted_candidate.v1",
            title="Stage136 Accepted Candidate Schema",
            stage="136",
            version="1.0.0",
            record_kind="accepted_candidate",
            fields=common_fields,
            review_required=False,
            migration_ready=True,
            storage_contract_ready=True,
        ),
        SchemaDefinition(
            schema_id="stage136.rejected_candidate.v1",
            title="Stage136 Rejected Candidate Schema",
            stage="136",
            version="1.0.0",
            record_kind="rejected_candidate",
            fields=common_fields,
            review_required=False,
            migration_ready=True,
            storage_contract_ready=True,
        ),
        SchemaDefinition(
            schema_id="stage136.review_only_candidate.v1",
            title="Stage136 Review-Only Candidate Schema",
            stage="136",
            version="1.0.0",
            record_kind="review_only_candidate",
            fields=common_fields,
            review_required=True,
            migration_ready=True,
            storage_contract_ready=True,
        ),
    )


def _bind_candidate(candidate: dict[str, Any], schema_lookup: dict[str, SchemaDefinition]) -> CandidateSchemaBinding:
    decision = str(candidate.get("decision", ""))
    issues: list[str] = []
    schema_id = _DECISION_TO_SCHEMA_ID.get(decision, "")
    if not schema_id:
        issues.append("unknown_decision")
    schema = schema_lookup.get(schema_id)
    if schema is None:
        issues.append("missing_schema_definition")
    required_fields = {"case_id", "source_stage", "source_recommendation", "decision", "gate_verified", "writer_review_required", "reason"}
    if not required_fields.issubset(candidate):
        issues.append("missing_required_candidate_fields")
    writer_review_required = bool(candidate.get("writer_review_required"))
    schema_valid = not issues and schema is not None
    return CandidateSchemaBinding(
        case_id=str(candidate.get("case_id", "unknown")),
        decision=decision,
        schema_id=schema_id or "unbound",
        status="pass" if schema_valid else "blocked",
        schema_valid=schema_valid,
        migration_ready=bool(schema and schema.migration_ready),
        storage_contract_ready=bool(schema and schema.storage_contract_ready),
        writer_review_required=writer_review_required,
        losdb_write_enabled=False,
        migration_execution_enabled=False,
        provider_call_required=False,
        issues=tuple(issues),
    )
