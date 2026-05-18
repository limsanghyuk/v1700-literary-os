from __future__ import annotations

from typing import Any

from v1700.lineage_absorption.contracts import LineageRelationship
from v1700.stage121.fixtures import CANDIDATE_ARCHIVES, TRUNK_STAGE


def build_lineage_relationship_map() -> dict[str, Any]:
    relationships: list[LineageRelationship] = []
    for audit in CANDIDATE_ARCHIVES:
        relationships.append(
            LineageRelationship(
                trunk_stage=TRUNK_STAGE,
                candidate_version=audit.source_version,
                relationship_type="successor_candidate",
                clean_packaging_pass=audit.clean_packaging_pass,
                has_internal_filelist=audit.has_internal_filelist,
                has_internal_sha256sums=audit.has_internal_sha256sums,
                cache_file_count=audit.cache_file_count,
                direct_merge_allowed=audit.direct_merge_allowed,
                rationale="Candidate contains post-Stage120 concepts but is blocked from direct merge until formulas, gates, and packaging are reconciled.",
            )
        )
    return {
        "status": "pass",
        "trunk_stage": TRUNK_STAGE,
        "candidate_count": len(CANDIDATE_ARCHIVES),
        "candidates": [a.to_dict() for a in CANDIDATE_ARCHIVES],
        "relationships": [r.to_dict() for r in relationships],
        "direct_merge_allowed_count": sum(1 for a in CANDIDATE_ARCHIVES if a.direct_merge_allowed),
        "all_direct_merges_blocked": all(not a.direct_merge_allowed for a in CANDIDATE_ARCHIVES),
    }
