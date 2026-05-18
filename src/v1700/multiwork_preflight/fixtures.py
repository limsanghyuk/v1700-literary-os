from __future__ import annotations

from .contracts import CrossWorkAccessEdge, ProjectIdentity


def sample_projects() -> list[ProjectIdentity]:
    return [
        ProjectIdentity(
            project_id="project_alpha",
            title="Alpha Sovereign Series",
            owner_id="author_a",
            genre="mystery-drama",
            canon_root_id="canon_alpha",
            license_policy_id="license_alpha_private",
        ),
        ProjectIdentity(
            project_id="project_beta",
            title="Beta Shared-World Candidate",
            owner_id="author_a",
            genre="thriller-drama",
            canon_root_id="canon_beta",
            license_policy_id="license_beta_private",
        ),
    ]


def safe_cross_work_edges() -> list[CrossWorkAccessEdge]:
    return [
        CrossWorkAccessEdge(
            source_project_id="project_beta",
            target_project_id="project_alpha",
            access_type="read",
            license_edge_exists=True,
            approved_by_author=True,
            resource_scope_permits=True,
            isolation_policy_allows=True,
        ),
        CrossWorkAccessEdge(
            source_project_id="project_beta",
            target_project_id="project_alpha",
            access_type="reference",
            license_edge_exists=True,
            approved_by_author=True,
            resource_scope_permits=True,
            isolation_policy_allows=True,
        ),
    ]


def blocked_probe_edges() -> list[CrossWorkAccessEdge]:
    return [
        CrossWorkAccessEdge(
            source_project_id="project_alpha",
            target_project_id="project_beta",
            access_type="write",
            license_edge_exists=True,
            approved_by_author=True,
            resource_scope_permits=True,
            isolation_policy_allows=True,
        ),
        CrossWorkAccessEdge(
            source_project_id="project_beta",
            target_project_id="project_alpha",
            access_type="read",
            license_edge_exists=False,
            approved_by_author=False,
            resource_scope_permits=True,
            isolation_policy_allows=True,
        ),
    ]
