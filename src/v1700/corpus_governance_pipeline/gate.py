from __future__ import annotations

from typing import Any

from .contracts import CorpusCasePacket, CorpusGovernancePipeline, NamespaceGovernanceProfile, ReviewQueuePacket

CORPUS_GOVERNANCE_MODE = "CORPUS_GOVERNANCE_PIPELINE_DRY_RUN"


def build_corpus_governance_pipeline(stage138_report: dict[str, Any]) -> CorpusGovernancePipeline:
    catalog = stage138_report.get("parts", {}).get("storage_contract_catalog", {})
    contracts = catalog.get("contracts", [])
    routes = catalog.get("routes", [])
    approval_lanes = catalog.get("approval_lanes", [])

    governance_profiles: list[NamespaceGovernanceProfile] = []
    case_packets: list[CorpusCasePacket] = []
    review_queue_packets: list[ReviewQueuePacket] = []
    issues: list[str] = []

    if not contracts:
        issues.append("missing_stage138_contracts")
    if not routes:
        issues.append("missing_stage138_routes")
    if not approval_lanes:
        issues.append("missing_stage138_approval_lanes")

    profile_by_contract_id: dict[str, str] = {}
    retention_by_contract_id: dict[str, str] = {}

    for contract in contracts:
        contract_id = str(contract.get("contract_id", ""))
        governance_channel = str(contract.get("governance_channel", "automatic_registry"))
        review_required = bool(contract.get("requires_human_approval"))
        record_kind = str(contract.get("record_kind", "unknown"))
        profile_id = contract_id.replace("CONTRACT", "PROFILE", 1)
        retention_class = "writer_review_hold" if review_required else f"{record_kind}_registry_hold"
        governance_profiles.append(
            NamespaceGovernanceProfile(
                profile_id=profile_id,
                contract_id=contract_id,
                target_namespace=str(contract.get("target_namespace", "")),
                governance_channel=governance_channel,  # type: ignore[arg-type]
                retention_class=retention_class,
                evidence_scope="candidate_registry_governance",
                requires_human_approval=review_required,
                stage140_release_ready=True,
                rollback_anchor=str(contract.get("rollback_anchor", "")),
            )
        )
        profile_by_contract_id[contract_id] = profile_id
        retention_by_contract_id[contract_id] = retention_class

    route_ids: set[str] = set()
    reviewed_case_ids: set[str] = set()
    reviewed_profile_ids: set[str] = set()

    for route in routes:
        route_id = str(route.get("route_id", ""))
        route_ids.add(route_id)
        contract_id = str(route.get("contract_id", ""))
        profile_id = profile_by_contract_id.get(contract_id, "")
        if not profile_id:
            issues.append(f"missing_governance_profile:{contract_id}")
            continue
        approval_lane = str(route.get("approval_lane", "automatic_registry"))
        requires_human_approval = approval_lane == "writer_review_queue"
        target_namespace = str(route.get("target_namespace", ""))
        if "review_only_candidate" in target_namespace:
            corpus_status = "review_only"
        elif "accepted_candidate" in target_namespace:
            corpus_status = "accepted_candidate"
        else:
            corpus_status = "rejected_candidate"
        case_id = str(route.get("case_id", ""))
        case_packets.append(
            CorpusCasePacket(
                packet_id=route_id.replace("ROUTE", "CASE", 1),
                case_id=case_id,
                contract_id=contract_id,
                governance_profile_id=profile_id,
                target_namespace=target_namespace,
                storage_key=str(route.get("storage_key", "")),
                approval_lane=approval_lane,  # type: ignore[arg-type]
                corpus_status=corpus_status,
                retention_class=retention_by_contract_id.get(contract_id, ""),
                audit_event_key=f"audit:stage139:{case_id}:governance",
                depends_on_route=route_id,
                requires_human_approval=requires_human_approval,
                stage140_release_ready=bool(route.get("stage139_governance_ready")),
                rollback_anchor=str(route.get("rollback_anchor", "")),
            )
        )
        if requires_human_approval:
            reviewed_case_ids.add(case_id)
            reviewed_profile_ids.add(profile_id)

    for lane in approval_lanes:
        lane_name = str(lane.get("lane_name", "automatic_registry"))
        packet_id = str(lane.get("lane_id", "")).replace("LANE", "QUEUE", 1)
        lane_reviewed_case_ids = tuple(str(case_id) for case_id in lane.get("reviewed_case_ids", []))
        for case_id in lane_reviewed_case_ids:
            if case_id not in reviewed_case_ids:
                issues.append(f"missing_review_case_packet:{case_id}")
        review_queue_packets.append(
            ReviewQueuePacket(
                packet_id=packet_id,
                lane_name=lane_name,  # type: ignore[arg-type]
                queue_namespace=str(lane.get("queue_namespace", "")),
                reviewed_case_ids=lane_reviewed_case_ids,
                governance_profile_ids=tuple(sorted(reviewed_profile_ids)),
                depends_on_steps=tuple(str(step) for step in lane.get("depends_on_steps", [])),
                audit_event_key=f"audit:stage139:{lane_name}:queue",
                stage140_release_ready=True,
                rollback_anchor=str(lane.get("rollback_anchor", "")),
            )
        )

    total_items = len(governance_profiles) + len(case_packets) + len(review_queue_packets)
    rollback_ready_count = sum(1 for profile in governance_profiles if profile.rollback_anchor) + sum(
        1 for packet in case_packets if packet.rollback_anchor
    ) + sum(1 for packet in review_queue_packets if packet.rollback_anchor)
    execution_blocked_count = sum(1 for profile in governance_profiles if profile.write_enabled is False) + sum(
        1 for packet in case_packets if packet.write_enabled is False
    ) + sum(1 for packet in review_queue_packets if packet.write_enabled is False)
    audit_trail_ready_count = sum(1 for packet in case_packets if packet.audit_event_key) + sum(
        1 for packet in review_queue_packets if packet.audit_event_key
    ) + sum(1 for profile in governance_profiles if profile.evidence_scope)
    retention_ready_count = sum(1 for packet in case_packets if packet.retention_class)
    stage140_release_ready_count = sum(1 for profile in governance_profiles if profile.stage140_release_ready) + sum(
        1 for packet in case_packets if packet.stage140_release_ready
    ) + sum(1 for packet in review_queue_packets if packet.stage140_release_ready)
    policy_binding_count = sum(1 for packet in case_packets if packet.governance_profile_id)
    unique_profile_count = len({profile.profile_id for profile in governance_profiles})

    if len(case_packets) != len(routes):
        issues.append("governed_case_coverage_incomplete")
    if reviewed_case_ids and not review_queue_packets:
        issues.append("review_queue_packet_missing")
    if unique_profile_count != len(governance_profiles):
        issues.append("duplicate_governance_profile")
    if rollback_ready_count != total_items:
        issues.append("rollback_anchor_missing")
    if execution_blocked_count != total_items:
        issues.append("governance_write_enabled")
    if audit_trail_ready_count != total_items:
        issues.append("audit_trail_metadata_missing")
    if stage140_release_ready_count != total_items:
        issues.append("stage140_release_readiness_incomplete")
    if policy_binding_count != len(case_packets):
        issues.append("policy_binding_incomplete")
    if retention_ready_count != len(case_packets):
        issues.append("retention_metadata_incomplete")
    if any(profile.provider_call_required for profile in governance_profiles) or any(
        packet.provider_call_required for packet in case_packets
    ) or any(packet.provider_call_required for packet in review_queue_packets):
        issues.append("provider_call_required")
    if any(packet.depends_on_route not in route_ids for packet in case_packets):
        issues.append("route_dependency_missing")

    counters = {
        "governance_profile_count": len(governance_profiles),
        "case_packet_count": len(case_packets),
        "review_queue_packet_count": len(review_queue_packets),
        "governed_case_count": len(case_packets),
        "review_required_case_count": sum(1 for packet in case_packets if packet.requires_human_approval),
        "retention_ready_count": retention_ready_count,
        "audit_trail_ready_count": audit_trail_ready_count,
        "stage140_release_ready_count": stage140_release_ready_count,
        "execution_blocked_count": execution_blocked_count,
        "rollback_ready_count": rollback_ready_count,
        "policy_binding_count": policy_binding_count,
        "unique_profile_count": unique_profile_count,
    }

    return CorpusGovernancePipeline(
        stage="139",
        baseline_stage="138",
        status="pass" if not issues else "blocked",
        governance_profiles=tuple(governance_profiles),
        case_packets=tuple(case_packets),
        review_queue_packets=tuple(review_queue_packets),
        issues=tuple(issues),
        counters=counters,
    )
