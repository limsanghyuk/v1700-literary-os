from __future__ import annotations

from .contracts import ReadOnlyAccessRequest, SharedCharacterRecord, SharedWorldRecord


def shared_character_records() -> list[SharedCharacterRecord]:
    return [
        SharedCharacterRecord(
            character_id="char_alpha_mentor",
            owner_project_id="project_alpha",
            owner_id="author_a",
            display_name="Alpha Mentor",
            license_policy_id="author_a_private",
            raw_manuscript_excerpt="redacted private character backstory",
            surface_traits=("mentor", "strategic", "recurring"),
        ),
        SharedCharacterRecord(
            character_id="char_beta_guest",
            owner_project_id="project_beta",
            owner_id="author_a",
            display_name="Beta Guest",
            license_policy_id="shared_with_author_a_projects",
            surface_traits=("guest", "cross-reference-safe"),
        ),
        SharedCharacterRecord(
            character_id="char_public_legend",
            owner_project_id="public_domain",
            owner_id="public",
            display_name="Public Legend",
            public_domain_flag=True,
            license_policy_id="public_domain",
            surface_traits=("legend", "public-domain"),
        ),
    ]


def shared_world_records() -> list[SharedWorldRecord]:
    return [
        SharedWorldRecord(
            world_id="world_alpha_city",
            owner_project_id="project_alpha",
            owner_id="author_a",
            display_name="Alpha City",
            world_rule_summary=("late-night judiciary", "cold-case archive"),
            raw_world_bible_excerpt="redacted world bible text",
        ),
        SharedWorldRecord(
            world_id="world_beta_port",
            owner_project_id="project_beta",
            owner_id="author_a",
            display_name="Beta Port",
            world_rule_summary=("port syndicate", "fog-bound logistics"),
        ),
    ]


def safe_read_requests() -> list[ReadOnlyAccessRequest]:
    return [
        ReadOnlyAccessRequest(
            source_project_id="project_beta",
            target_project_id="project_alpha",
            resource_id="char_alpha_mentor",
            resource_type="shared_character",
            access_type="read",
            same_owner=True,
            license_edge_exists=False,
            author_approval_valid=True,
        ),
        ReadOnlyAccessRequest(
            source_project_id="project_beta",
            target_project_id="project_alpha",
            resource_id="world_alpha_city",
            resource_type="shared_world",
            access_type="reference",
            same_owner=True,
            license_edge_exists=True,
            author_approval_valid=True,
        ),
        ReadOnlyAccessRequest(
            source_project_id="project_gamma",
            target_project_id="public_domain",
            resource_id="char_public_legend",
            resource_type="shared_character",
            access_type="read",
            same_owner=False,
            license_edge_exists=False,
            author_approval_valid=True,
            public_domain_flag=True,
        ),
    ]


def blocked_probe_requests() -> list[ReadOnlyAccessRequest]:
    return [
        ReadOnlyAccessRequest(
            source_project_id="project_alpha",
            target_project_id="project_beta",
            resource_id="char_beta_guest",
            resource_type="shared_character",
            access_type="write",
            same_owner=True,
            license_edge_exists=True,
            author_approval_valid=True,
        ),
        ReadOnlyAccessRequest(
            source_project_id="project_delta",
            target_project_id="project_alpha",
            resource_id="char_alpha_mentor",
            resource_type="shared_character",
            access_type="read",
            same_owner=False,
            license_edge_exists=False,
            author_approval_valid=False,
        ),
        ReadOnlyAccessRequest(
            source_project_id="project_delta",
            target_project_id="project_alpha",
            resource_id="world_alpha_city",
            resource_type="shared_world",
            access_type="adapt",
            same_owner=False,
            license_edge_exists=False,
            author_approval_valid=False,
        ),
    ]
