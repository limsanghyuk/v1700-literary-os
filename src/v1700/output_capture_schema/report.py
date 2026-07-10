from __future__ import annotations

from typing import Any


def build_output_capture_schema(work_id: str) -> dict[str, Any]:
    """Build a disabled-by-default output capture schema for Page18 preflight."""

    return {
        "schema_id": f"page18-output-capture-schema:{work_id}:preflight",
        "work_id": work_id,
        "output_capture_started": False,
        "capture_allowed": False,
        "capture_path_policy": "disabled_until_schema_freeze",
        "generated_output_hash_required": True,
        "canonical_mutation_allowed": False,
        "provider_generation_allowed": False,
    }


def build_canonical_mutation_blocker(work_id: str) -> dict[str, Any]:
    """Build the default canonical mutation blocker for Page18 preflight."""

    return {
        "blocker_id": f"page18-canonical-mutation-blocker:{work_id}:preflight",
        "work_id": work_id,
        "canonical_mutation_allowed": False,
        "requires_approval_decision_record": True,
        "requires_rollback_record": True,
        "blocked_mutation_targets": [
            "canonical_manuscript",
            "canonical_memory",
            "writer_approved_output",
        ],
    }
