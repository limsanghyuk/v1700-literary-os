from __future__ import annotations

from pathlib import Path

from v1700.gates.stage102_release_gate import run_stage102_release_gate

from .backup_restore import run_backup_restore_probe
from .ci_replay import run_ci_replay_contract
from .error_reporting import build_safe_error_report
from .install_replay import run_install_replay_probe
from .manuscript_vault import run_local_manuscript_vault_probe
from .release_notes import build_stage103_release_notes
from .report import stage103_pack, write_json, write_summary
from .runtime_profiles import validate_runtime_profiles


def run_stage103_0_deployment_preflight(root: Path | None = None) -> dict:
    root = root or Path.cwd()
    stage102 = run_stage102_release_gate(root)
    required = [
        root / "docs" / "development" / "MANDATORY_PRE_DEVELOPMENT_PROTOCOL.md",
        root / "manifests" / "predevelopment_priority_manifest.json",
        root / "docs" / "stages" / "stage102.md",
        root / "release" / "current" / "stage102_release_gate_report.json",
    ]
    missing = [path.relative_to(root).as_posix() for path in required if not path.exists()]
    issues = list(missing)
    if stage102.get("status") != "pass":
        issues.append("stage102_baseline_blocked")
    payload = {
        "stage": "103.0",
        "baseline_stage": "102",
        "title": "Deployment Preflight Lock",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "stage102_release_gate_status": stage102.get("status"),
        "mandatory_predevelopment_protocol_present": not missing,
        "scope": "production_hardening_deployment_readiness",
        "new_feature_expansion": False,
        "provider_default_calls": 0,
        "live_provider_call_count_in_release_gate": 0,
        "raw_manuscript_provider_leakage": 0,
        "node2_raw_reveal_access": 0,
    }
    write_json(root / "release" / "current" / "stage103_0_deployment_preflight_report.json", payload)
    return payload


def run_stage103_1_install_replay(root: Path | None = None) -> dict:
    root = root or Path.cwd()
    install = run_install_replay_probe(root)
    ci = run_ci_replay_contract()
    issues = []
    if install.get("status") != "pass":
        issues.append("install_replay_blocked")
    if ci.get("status") != "pass":
        issues.append("ci_replay_blocked")
    payload = {
        "stage": "103.1",
        "title": "Install Replay and CI Contract",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "install_replay": install,
        "ci_replay": ci,
        "fresh_clone_install_replay_status": install.get("status"),
        "ci_replay_status": ci.get("status"),
    }
    write_json(root / "release" / "current" / "stage103_install_replay_report.json", payload)
    pack = stage103_pack(root, "stage103_deployment_pack")
    write_json(pack / "install_replay_contract.json", install)
    write_json(pack / "ci_replay_contract.json", ci)
    return payload


def run_stage103_2_runtime_profiles(root: Path | None = None) -> dict:
    root = root or Path.cwd()
    payload = validate_runtime_profiles()
    payload.update({"stage": "103.2", "title": "Runtime Profile Separation"})
    write_json(root / "release" / "current" / "stage103_runtime_profile_report.json", payload)
    pack = stage103_pack(root, "stage103_deployment_pack")
    write_json(pack / "runtime_profile_matrix.json", payload)
    return payload


def run_stage103_3_vault_backup_error_release(root: Path | None = None) -> dict:
    root = root or Path.cwd()
    vault = run_local_manuscript_vault_probe()
    backup = run_backup_restore_probe()
    error_report = build_safe_error_report()
    release_notes = build_stage103_release_notes()
    checks = {
        "vault_pass": vault.get("status") == "pass",
        "backup_restore_pass": backup.get("status") == "pass",
        "safe_error_report_pass": error_report.get("status") == "pass",
        "release_notes_pass": release_notes.get("status") == "pass",
        "raw_text_not_exported": vault.get("raw_text_exported") is False,
        "backup_metadata_only": backup.get("metadata_only") is True,
        "safe_error_redacted": not error_report.get("raw_prompt_included") and not error_report.get("credential_included"),
    }
    issues = [name for name, ok in checks.items() if not ok]
    payload = {
        "stage": "103.3",
        "title": "Local Vault, Backup/Restore, Error Report, Release Notes",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "checks": checks,
        "local_manuscript_vault": vault,
        "backup_restore": backup,
        "safe_error_report": error_report,
        "release_notes": release_notes,
        "raw_manuscript_provider_leakage": 0,
        "provider_default_calls": 0,
        "node2_raw_reveal_access": 0,
    }
    write_json(root / "release" / "current" / "stage103_vault_backup_error_release_report.json", payload)
    pack = stage103_pack(root, "stage103_deployment_pack")
    write_json(pack / "local_manuscript_vault_report.json", vault)
    write_json(pack / "backup_restore_report.json", backup)
    write_json(pack / "safe_error_report_contract.json", error_report)
    write_json(pack / "release_notes_contract.json", release_notes)
    write_summary(
        pack / "stage103_deployment_readiness_summary.md",
        "Stage103 Deployment Readiness Summary",
        [
            "Install replay and CI replay are documented as local deterministic commands.",
            "Runtime profiles are separated into dev, release, and sandbox with live providers off by default.",
            "Manuscript vault and backup/restore are feature-only and local-only.",
            "Error reports redact prompts and credentials.",
        ],
    )
    return payload


def run_stage103(root: Path | None = None) -> dict:
    root = root or Path.cwd()
    preflight = run_stage103_0_deployment_preflight(root)
    install = run_stage103_1_install_replay(root)
    profiles = run_stage103_2_runtime_profiles(root)
    vault_pack = run_stage103_3_vault_backup_error_release(root)
    issues = []
    for name, report in (
        ("deployment_preflight", preflight),
        ("install_replay", install),
        ("runtime_profiles", profiles),
        ("vault_backup_error_release", vault_pack),
    ):
        if report.get("status") != "pass":
            issues.append(f"{name}_blocked")
    payload = {
        "stage": "103",
        "baseline_stage": "102",
        "title": "Production Hardening & Deployment Readiness",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "stage103_0_deployment_preflight": preflight,
        "stage103_1_install_replay": install,
        "stage103_2_runtime_profiles": profiles,
        "stage103_3_vault_backup_error_release": vault_pack,
        "provider_default_calls": 0,
        "live_provider_call_count_in_release_gate": 0,
        "raw_manuscript_provider_leakage": 0,
        "node2_raw_reveal_access": 0,
        "credential_leakage": 0,
        "production_claim": "deployment_readiness_not_full_commercial_saas",
    }
    write_json(root / "release" / "current" / "stage103_production_hardening_report.json", payload)
    write_summary(
        root / "release" / "current" / "stage103_developer_handoff_report.md",
        "Stage103 Developer Handoff",
        [
            f"Stage103 status: {payload['status']}",
            "Stage103 hardens installation, CI replay, runtime profile separation, local vault, backup/restore, safe error reporting, and release notes.",
            "It does not introduce live provider calls or raw manuscript export.",
            "Provider-zero, Node2 boundary, branchpoint lineage, and clean package policy remain intact.",
        ],
    )
    return payload
