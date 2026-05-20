from __future__ import annotations

from typing import Any

from .contracts import (
    ApprovalLaneContract,
    BindingRoute,
    NamespaceContract,
    StorageContractCatalog,
    StorageFieldContract,
)

LOSDB_STORAGE_CONTRACT_MODE = "LOSDB_STORAGE_CONTRACTS_READINESS_ONLY"


def build_storage_contract_catalog(stage136_report: dict[str, Any], stage137_report: dict[str, Any]) -> StorageContractCatalog:
    registry = stage136_report.get("parts", {}).get("schema_registry", {})
    schemas = registry.get("schemas", [])
    bindings = registry.get("bindings", [])
    plan = stage137_report.get("parts", {}).get("migration_plan", {})
    steps = plan.get("steps", [])

    schemas_by_id = {schema.get("schema_id"): schema for schema in schemas}
    schema_steps = {step.get("schema_id"): step for step in steps if step.get("scope") == "schema"}
    binding_steps = {step.get("case_id"): step for step in steps if step.get("scope") == "binding"}
    checkpoint_steps = [step for step in steps if step.get("scope") == "checkpoint"]

    contracts: list[NamespaceContract] = []
    routes: list[BindingRoute] = []
    approval_lanes: list[ApprovalLaneContract] = []
    issues: list[str] = []

    if not schemas:
        issues.append("missing_stage136_schemas")
    if not bindings:
        issues.append("missing_stage136_bindings")
    if not steps:
        issues.append("missing_stage137_migration_steps")

    contract_id_by_schema: dict[str, str] = {}
    namespace_by_schema: dict[str, str] = {}

    for schema in schemas:
        schema_id = str(schema.get("schema_id", "unknown"))
        schema_step = schema_steps.get(schema_id)
        if not schema_step:
            issues.append(f"missing_stage137_schema_step:{schema_id}")
            continue
        record_kind = str(schema.get("record_kind", "unknown"))
        fields = tuple(
            StorageFieldContract(
                name=str(field.get("name", "unknown")),
                field_type=str(field.get("field_type", "string")),
                required=bool(field.get("required")),
                storage_column=str(field.get("name", "unknown")),
                index_position=index + 1,
                description=str(field.get("description", "")),
            )
            for index, field in enumerate(schema.get("fields", []))
        )
        contract_id = f"STAGE138-CONTRACT-{record_kind.upper()}"
        target_namespace = str(schema_step.get("target_namespace", "")).replace("losdb.plan.", "losdb.contract.", 1)
        governance_channel = "writer_review_queue" if schema.get("review_required") else "automatic_registry"
        contracts.append(
            NamespaceContract(
                contract_id=contract_id,
                contract_version="1.0.0",
                schema_id=schema_id,
                record_kind=record_kind,
                target_namespace=target_namespace,
                target_collection=f"{record_kind}_records",
                storage_key_template=f"stage138/{record_kind}/{{case_id}}",
                governance_channel=governance_channel,
                migration_dependency=str(schema_step.get("step_id", "")),
                fields=fields,
                requires_human_approval=bool(schema.get("review_required")),
                rollback_anchor=f"rollback:stage138:{schema_id}:storage-contract",
            )
        )
        contract_id_by_schema[schema_id] = contract_id
        namespace_by_schema[schema_id] = target_namespace

    for binding in bindings:
        case_id = str(binding.get("case_id", "unknown"))
        schema_id = str(binding.get("schema_id", "unknown"))
        binding_step = binding_steps.get(case_id)
        contract_id = contract_id_by_schema.get(schema_id)
        target_namespace = namespace_by_schema.get(schema_id, "")
        if not binding_step:
            issues.append(f"missing_stage137_binding_step:{case_id}")
            continue
        if not contract_id:
            issues.append(f"missing_storage_contract:{schema_id}")
            continue
        approval_lane = "writer_review_queue" if binding_step.get("requires_human_approval") else "automatic_registry"
        record_kind = str(schemas_by_id.get(schema_id, {}).get("record_kind", "unknown"))
        routes.append(
            BindingRoute(
                route_id=f"STAGE138-ROUTE-{case_id}",
                case_id=case_id,
                contract_id=contract_id,
                target_namespace=target_namespace,
                storage_key=f"stage138/{record_kind}/{case_id}",
                depends_on_step=str(binding_step.get("step_id", "")),
                approval_lane=approval_lane,
                stage139_governance_ready=True,
                rollback_anchor=f"rollback:stage138:{case_id}:binding-route",
            )
        )

    writer_review_case_ids = tuple(route.case_id for route in routes if route.approval_lane == "writer_review_queue")
    if checkpoint_steps:
        checkpoint_ids = tuple(str(step.get("step_id", "")) for step in checkpoint_steps)
        approval_lanes.append(
            ApprovalLaneContract(
                lane_id="STAGE138-LANE-REVIEW-ONLY",
                lane_name="writer_review_queue",
                queue_namespace="losdb.contract.review_only.queue.v1",
                depends_on_steps=checkpoint_ids,
                reviewed_case_ids=writer_review_case_ids,
                rollback_anchor="rollback:stage138:review-only-lane",
            )
        )
    else:
        issues.append("missing_stage137_approval_checkpoint")

    if not writer_review_case_ids:
        issues.append("writer_review_lane_empty")

    total_items = len(contracts) + len(routes) + len(approval_lanes)
    unique_namespaces = {contract.target_namespace for contract in contracts}
    unique_contract_ids = {contract.contract_id for contract in contracts}
    dependency_preserved_count = sum(1 for contract in contracts if contract.migration_dependency) + sum(
        1 for route in routes if route.depends_on_step
    ) + sum(1 for lane in approval_lanes if lane.depends_on_steps)
    rollback_ready_count = sum(1 for contract in contracts if contract.rollback_anchor) + sum(
        1 for route in routes if route.rollback_anchor
    ) + sum(1 for lane in approval_lanes if lane.rollback_anchor)
    write_blocked_count = sum(1 for contract in contracts if contract.write_enabled is False) + sum(
        1 for route in routes if route.write_enabled is False
    ) + sum(1 for lane in approval_lanes if lane.write_enabled is False)

    if len(routes) != len(bindings):
        issues.append("binding_route_coverage_incomplete")
    if len(unique_namespaces) != len(contracts):
        issues.append("duplicate_contract_namespace")
    if len(unique_contract_ids) != len(contracts):
        issues.append("duplicate_contract_id")
    if dependency_preserved_count != total_items:
        issues.append("dependency_preservation_incomplete")
    if rollback_ready_count != total_items:
        issues.append("rollback_anchor_missing")
    if write_blocked_count != total_items:
        issues.append("storage_contract_write_enabled")
    if any(contract.provider_call_required for contract in contracts) or any(
        route.provider_call_required for route in routes
    ) or any(lane.provider_call_required for lane in approval_lanes):
        issues.append("provider_call_required")

    counters = {
        "schema_contract_count": len(contracts),
        "binding_route_count": len(routes),
        "approval_lane_count": len(approval_lanes),
        "covered_binding_count": len(routes),
        "review_lane_route_count": len(writer_review_case_ids),
        "rollback_ready_count": rollback_ready_count,
        "write_blocked_count": write_blocked_count,
        "governance_ready_count": sum(1 for route in routes if route.stage139_governance_ready),
        "dependency_preserved_count": dependency_preserved_count,
        "unique_namespace_count": len(unique_namespaces),
        "unique_contract_count": len(unique_contract_ids),
    }

    return StorageContractCatalog(
        stage="138",
        baseline_stage="137",
        status="pass" if not issues else "blocked",
        contracts=tuple(contracts),
        routes=tuple(routes),
        approval_lanes=tuple(approval_lanes),
        issues=tuple(issues),
        counters=counters,
    )
