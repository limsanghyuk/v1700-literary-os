from __future__ import annotations

from typing import Any

from .contracts import MigrationPlan, MigrationStep

MIGRATION_MANAGER_MODE = "MIGRATION_MANAGER_PLAN_ONLY"


def build_migration_plan(stage136_report: dict[str, Any]) -> MigrationPlan:
    registry = stage136_report.get("parts", {}).get("schema_registry", {})
    schemas = registry.get("schemas", [])
    bindings = registry.get("bindings", [])
    schema_by_id = {schema.get("schema_id"): schema for schema in schemas}
    steps: list[MigrationStep] = []
    issues: list[str] = []
    order = 1
    schema_step_ids: dict[str, str] = {}
    binding_step_ids: dict[str, str] = {}

    if not schemas:
        issues.append("missing_stage136_schemas")
    if not bindings:
        issues.append("missing_stage136_bindings")

    for schema in schemas:
        schema_id = str(schema.get("schema_id", "unknown"))
        record_kind = str(schema.get("record_kind", "unknown"))
        step_id = f"STAGE137-SCHEMA-{record_kind.upper()}"
        schema_step_ids[schema_id] = step_id
        steps.append(
            MigrationStep(
                step_id=step_id,
                order=order,
                scope="schema",
                action="FREEZE_SCHEMA_CATALOG",
                schema_id=schema_id,
                target_namespace=f"losdb.plan.{record_kind}.v1",
                rollback_anchor=f"rollback:{schema_id}:catalog-freeze",
            )
        )
        order += 1

    for binding in bindings:
        case_id = str(binding.get("case_id", "unknown"))
        schema_id = str(binding.get("schema_id", "unbound"))
        record_kind = str(schema_by_id.get(schema_id, {}).get("record_kind", "unknown"))
        if schema_id not in schema_step_ids:
            issues.append(f"missing_schema_step:{schema_id}")
        step_id = f"STAGE137-BINDING-{case_id}"
        binding_step_ids[case_id] = step_id
        steps.append(
            MigrationStep(
                step_id=step_id,
                order=order,
                scope="binding",
                action="PLAN_NAMESPACE_MIGRATION",
                schema_id=schema_id,
                case_id=case_id,
                target_namespace=f"losdb.plan.{record_kind}.records.v1",
                depends_on=(schema_step_ids.get(schema_id, ""),),
                requires_human_approval=bool(binding.get("writer_review_required")),
                rollback_anchor=f"rollback:{case_id}:binding-plan",
            )
        )
        order += 1

    review_only_case_ids = [str(binding.get("case_id")) for binding in bindings if binding.get("decision") == "REVIEW_ONLY"]
    if review_only_case_ids:
        steps.append(
            MigrationStep(
                step_id="STAGE137-CHECKPOINT-REVIEW-ONLY",
                order=order,
                scope="checkpoint",
                action="PLAN_APPROVAL_CHECKPOINT",
                target_namespace="human.review.queue.stage137",
                depends_on=tuple(binding_step_ids.get(case_id, "") for case_id in review_only_case_ids),
                requires_human_approval=True,
                rollback_anchor="rollback:stage137:review-only-checkpoint",
            )
        )
        order += 1
    else:
        issues.append("review_only_checkpoint_missing")

    if any(step.execution_enabled for step in steps):
        issues.append("migration_execution_enabled")
    if any(step.losdb_write_enabled for step in steps):
        issues.append("losdb_write_enabled")
    if any(step.provider_call_required for step in steps):
        issues.append("provider_call_required")
    if any(not step.rollback_anchor for step in steps):
        issues.append("rollback_anchor_missing")
    if any(not step.target_namespace for step in steps):
        issues.append("target_namespace_missing")
    orders = [step.order for step in steps]
    if orders != sorted(orders):
        issues.append("unordered_migration_steps")
    if len(set(orders)) != len(orders):
        issues.append("duplicate_migration_step_order")

    covered_binding_count = sum(1 for step in steps if step.scope == "binding" and step.case_id)
    counters = {
        "migration_step_count": len(steps),
        "schema_step_count": sum(1 for step in steps if step.scope == "schema"),
        "binding_step_count": sum(1 for step in steps if step.scope == "binding"),
        "approval_checkpoint_count": sum(1 for step in steps if step.scope == "checkpoint"),
        "review_only_checkpoint_count": sum(1 for step in steps if step.scope == "checkpoint" and step.requires_human_approval),
        "covered_binding_count": covered_binding_count,
        "rollback_ready_count": sum(1 for step in steps if bool(step.rollback_anchor)),
        "execution_blocked_count": sum(1 for step in steps if step.execution_enabled is False),
    }
    if covered_binding_count != len(bindings):
        issues.append("binding_coverage_incomplete")

    return MigrationPlan(
        stage="137",
        baseline_stage="136",
        status="pass" if not issues else "blocked",
        steps=tuple(steps),
        issues=tuple(issues),
        counters=counters,
    )
