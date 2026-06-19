from __future__ import annotations

from typing import Any


def build_generation_context_packet(
    work_id: str,
    *,
    metadata_refs: list[dict[str, Any]] | None = None,
    proof_packet_refs: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Build reference-only context for the Page18 boundary preflight."""

    return {
        "context_packet_id": f"page18-generation-context:{work_id}:preflight",
        "work_id": work_id,
        "metadata_refs": metadata_refs or [],
        "proof_packet_refs": proof_packet_refs or [],
        "source_text_allowed": False,
        "provider_generation_allowed": False,
        "canonical_mutation_allowed": False,
    }
