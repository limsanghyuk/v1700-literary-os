from __future__ import annotations

from pathlib import Path

from v1700.gates.stage97_release_gate import run_stage97_release_gate
from v1700.longform_adversarial.attention_fatigue_cases import build_attention_fatigue_cases
from v1700.longform_adversarial.broken_load_cases import build_broken_load_cases
from v1700.longform_adversarial.broken_payoff_cases import build_broken_payoff_cases
from v1700.longform_adversarial.broken_topology_cases import build_broken_topology_cases
from v1700.longform_adversarial.contracts import AdversarialCase
from v1700.longform_adversarial.passive_agency_cases import build_passive_agency_cases
from v1700.longform_adversarial.speech_level_violation_cases import build_speech_level_violation_cases
from v1700.longform_adversarial.style_drift_violation_cases import build_style_drift_violation_cases
from v1700.longform_adversarial.weak_scene_cases import build_weak_scene_cases


def build_normal_stage97_case(root: Path | None = None) -> AdversarialCase:
    root = root or Path.cwd()
    gate = run_stage97_release_gate(root)
    return AdversarialCase(
        case_id="ADV-NOR-001",
        case_type="normal_stage97_proof",
        source_stage="97",
        mutation_type="none",
        expected_status="PASS",
        expected_block_reason=None,
        episode_count=int(gate.get("episode_count_verified", 16)),
        payload_path="release/current/stage97_release_gate_report.json",
        invariants={
            "provider_default_calls": 0,
            "node2_raw_reveal_access": 0,
            "critical_debt_default_count": 0,
        },
        payload={
            "stage97_gate_status": gate.get("status"),
            "critical_debt_default_count": gate.get("critical_debt_default_count", 0),
            "provider_call_count": gate.get("provider_call_count", 0),
            "node2_raw_reveal_access": gate.get("node2_raw_reveal_access", 0),
        },
    )


def build_security_and_manifest_cases() -> tuple[AdversarialCase, ...]:
    return (
        AdversarialCase(
            case_id="ADV-SEC-001",
            case_type="security_boundary",
            source_stage="97",
            mutation_type="provider_live_call",
            expected_status="BLOCK",
            expected_block_reason="provider_live_call_detected",
            episode_count=16,
            payload_path="generated/adversarial/security/provider_live_call.json",
            invariants={"release_provider_calls": 0},
            payload={"provider_call_count": 1, "node2_raw_reveal_access": 0},
        ),
        AdversarialCase(
            case_id="ADV-SEC-002",
            case_type="security_boundary",
            source_stage="97",
            mutation_type="node2_raw_reveal_access",
            expected_status="BLOCK",
            expected_block_reason="node2_raw_reveal_access_detected",
            episode_count=16,
            payload_path="generated/adversarial/security/node2_raw_reveal_access.json",
            invariants={"node2_raw_reveal_access": 0},
            payload={"provider_call_count": 0, "node2_raw_reveal_access": 1},
        ),
        AdversarialCase(
            case_id="ADV-MAN-001",
            case_type="manifest_evidence",
            source_stage="97",
            mutation_type="stale_manifest",
            expected_status="BLOCK",
            expected_block_reason="stale_manifest_detected",
            episode_count=16,
            payload_path="generated/adversarial/manifest/stale_manifest.json",
            invariants={"active_version": "stage97.1"},
            payload={"stale_manifest": True, "missing_release_evidence": False},
        ),
        AdversarialCase(
            case_id="ADV-MAN-002",
            case_type="manifest_evidence",
            source_stage="97",
            mutation_type="missing_release_evidence",
            expected_status="BLOCK",
            expected_block_reason="missing_release_evidence_detected",
            episode_count=16,
            payload_path="generated/adversarial/manifest/missing_release_evidence.json",
            invariants={"release_evidence_required": True},
            payload={"stale_manifest": False, "missing_release_evidence": True},
        ),
    )


def build_stage97_1_adversarial_cases(root: Path | None = None) -> tuple[AdversarialCase, ...]:
    return (
        (build_normal_stage97_case(root),)
        + build_broken_topology_cases()
        + build_broken_load_cases()
        + build_broken_payoff_cases()
        + build_passive_agency_cases()
        + build_weak_scene_cases()
        + build_speech_level_violation_cases()
        + build_style_drift_violation_cases()
        + build_attention_fatigue_cases()
        + build_security_and_manifest_cases()
    )
