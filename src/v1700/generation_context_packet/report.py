from __future__ import annotations

from typing import Any


def build_generation_context_packet(work_id: str) -> dict[str, Any]:
    """Build reference-only context for the Page18 boundary preflight."""

    return {
        "context_packet_id": f"page18-generation-context:{work_id}:preflight",
        "work_id": work_id,
        "metadata_refs": [],
        "proof_packet_refs": [],
        "source_text_allowed": False,
        "provider_generation_allowed": False,
        "canonical_mutation_allowed": False,
    }
