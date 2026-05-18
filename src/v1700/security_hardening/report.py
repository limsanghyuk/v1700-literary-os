from __future__ import annotations

from pathlib import Path

from v1700.security_hardening.credential_audit import audit_credentials
from v1700.security_hardening.internal_marker_leakage_scan import scan_internal_marker_leakage
from v1700.security_hardening.node2_boundary_replay import replay_node2_boundary
from v1700.security_hardening.package_secret_scan import scan_package_cleanliness
from v1700.security_hardening.provider_live_call_replay import replay_provider_live_call_boundary
from v1700.security_hardening.raw_manuscript_leakage_simulator import simulate_raw_manuscript_leakage
from v1700.studio_workflow.report import write_json, write_summary


def run_stage99_1_security_privacy_hardening(root: Path | None = None) -> dict:
    root = root or Path.cwd()
    pack = root / "release" / "current" / "stage99_security_pack"
    pack.mkdir(parents=True, exist_ok=True)

    credential = audit_credentials(root)
    raw_manuscript = simulate_raw_manuscript_leakage(root)
    provider = replay_provider_live_call_boundary(root)
    node2 = replay_node2_boundary(root)
    markers = scan_internal_marker_leakage(root)
    package = scan_package_cleanliness(root)
    reports = {
        "credential_audit_report.json": credential,
        "raw_manuscript_leakage_simulation_report.json": raw_manuscript,
        "provider_live_call_replay_report.json": provider,
        "node2_boundary_replay_report.json": node2,
        "internal_marker_leakage_scan_report.json": markers,
        "package_secret_scan_report.json": package,
    }
    for name, payload in reports.items():
        write_json(pack / name, payload)

    issues = [name.removesuffix("_report.json") for name, payload in reports.items() if payload.get("status") != "pass"]
    write_summary(
        pack / "stage99_1_summary.md",
        "Stage99.1 Security / Privacy Boundary Hardening",
        [
            f"credential leakage: {credential['credential_leakage']}",
            f"raw manuscript provider leakage: {raw_manuscript['raw_manuscript_provider_leakage']}",
            f"provider live calls in release: {provider['provider_live_call_count_in_release']}",
            f"Node2 raw reveal access: {node2['node2_raw_reveal_access']}",
            f"internal marker leakage: {markers['internal_marker_leakage']}",
        ],
    )
    payload = {
        "stage": "99.1",
        "baseline_stage": "99.0",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "credential_audit_status": credential["status"],
        "raw_manuscript_leakage_simulation_status": raw_manuscript["status"],
        "provider_live_call_replay_status": provider["status"],
        "node2_boundary_replay_status": node2["status"],
        "internal_marker_leakage_scan_status": markers["status"],
        "package_secret_scan_status": package["status"],
        "credential_leakage": credential["credential_leakage"],
        "raw_manuscript_provider_leakage": raw_manuscript["raw_manuscript_provider_leakage"],
        "provider_live_call_count_in_release": provider["provider_live_call_count_in_release"],
        "provider_default_calls": provider["provider_default_calls"],
        "node2_raw_reveal_access": node2["node2_raw_reveal_access"],
        "internal_marker_leakage": markers["internal_marker_leakage"],
        "reader_only_leakage": markers["reader_only_leakage"],
        "full_text_exported_by_default": raw_manuscript["full_text_exported_by_default"],
        "security_pack": "release/current/stage99_security_pack",
    }
    write_json(root / "release" / "current" / "stage99_1_security_privacy_hardening_report.json", payload)
    return payload
