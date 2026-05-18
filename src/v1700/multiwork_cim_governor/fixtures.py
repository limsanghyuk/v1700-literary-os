from __future__ import annotations

from .contracts import CanonConflict, CrossProjectInfluenceEdge, ProjectCIMSnapshot


def project_cim_fixtures() -> list[ProjectCIMSnapshot]:
    return [
        ProjectCIMSnapshot("proj_alpha", "canon_alpha", 12, 8, 21),
        ProjectCIMSnapshot("proj_beta", "canon_beta", 9, 11, 18),
        ProjectCIMSnapshot("proj_shared_reference", "canon_shared_reference", 4, 5, 7),
    ]


def cross_project_influence_fixtures() -> list[CrossProjectInfluenceEdge]:
    return [
        CrossProjectInfluenceEdge(
            edge_id="cpi-read-001",
            source_project_id="proj_alpha",
            target_project_id="proj_shared_reference",
            entity_id="shared_city_rule",
            access_type="read",
            license_edge_exists=True,
            approved_by_author=True,
            resource_scope_permits=True,
        ),
        CrossProjectInfluenceEdge(
            edge_id="cpi-reference-001",
            source_project_id="proj_beta",
            target_project_id="proj_shared_reference",
            entity_id="shared_calendar_rule",
            access_type="reference",
            license_edge_exists=True,
            approved_by_author=True,
            resource_scope_permits=True,
        ),
        CrossProjectInfluenceEdge(
            edge_id="cpi-block-write-001",
            source_project_id="proj_alpha",
            target_project_id="proj_beta",
            entity_id="private_character_arc",
            access_type="write",
            license_edge_exists=True,
            approved_by_author=True,
            resource_scope_permits=True,
            read_only=False,
        ),
        CrossProjectInfluenceEdge(
            edge_id="cpi-block-license-001",
            source_project_id="proj_beta",
            target_project_id="proj_alpha",
            entity_id="unlicensed_character",
            access_type="reference",
            license_edge_exists=False,
            approved_by_author=False,
            resource_scope_permits=False,
        ),
    ]


def canon_conflict_fixtures() -> list[CanonConflict]:
    return [
        CanonConflict(
            conflict_id="canon-pass-001",
            source_project_id="proj_alpha",
            target_project_id="proj_shared_reference",
            entity_id="shared_city_rule",
            timeline_conflict=0.0,
            world_rule_conflict=0.2,
            character_identity_conflict=0.0,
            relationship_conflict=0.0,
            evidence=("shared rule has compatible local override",),
            recommended_action="allow_read_only_reference",
        ),
        CanonConflict(
            conflict_id="canon-warn-001",
            source_project_id="proj_beta",
            target_project_id="proj_shared_reference",
            entity_id="shared_calendar_rule",
            timeline_conflict=0.5,
            world_rule_conflict=0.2,
            character_identity_conflict=0.0,
            relationship_conflict=0.1,
            evidence=("calendar drift requires author-facing note",),
            recommended_action="warn_and_preserve_project_local_canon",
        ),
        CanonConflict(
            conflict_id="canon-block-001",
            source_project_id="proj_alpha",
            target_project_id="proj_beta",
            entity_id="private_character_arc",
            timeline_conflict=1.0,
            world_rule_conflict=0.7,
            character_identity_conflict=1.0,
            relationship_conflict=0.8,
            evidence=("private character arc cannot merge into another project",),
            recommended_action="block_cross_work_canon_merge",
        ),
    ]
