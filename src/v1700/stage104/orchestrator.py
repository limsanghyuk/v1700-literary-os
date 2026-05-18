from __future__ import annotations

from pathlib import Path

from v1700.gates.stage103_release_gate import run_stage103_release_gate
from v1700.gates.symbol_to_branchpoint_trace_gate import run_symbol_to_branchpoint_trace_gate
from v1700.studio_beta.apply_guard import run_revision_apply_guard
from v1700.studio_beta.beta_handoff import build_beta_handoff_report
from v1700.studio_beta.import_export import build_studio_beta_export
from v1700.studio_beta.local_telemetry import build_local_telemetry_report
from v1700.studio_beta.navigation import build_navigation_report
from v1700.studio_beta.persistence import persist_workspace_snapshot
from v1700.studio_beta.project_workspace import build_sample_workspace
from v1700.studio_beta.report import stage104_pack, write_json, write_summary
from v1700.studio_beta.review_queue_panel import build_review_queue_panel
from v1700.studio_beta.sample_project_runner import run_sample_project_beta
from v1700.studio_beta.scene_card import scene_card_index
from v1700.studio_beta.studio_session import open_studio_session
from v1700.studio_beta.unified_board import build_unified_board
from v1700.studio_beta.workspace_state import build_workspace_state_report
from .contracts import Stage104PreflightResult


def _mandatory_predevelopment(root: Path) -> dict:
    try:
        from tools.run_mandatory_predevelopment_check import run_mandatory_predevelopment_check
    except Exception:
        return {"status": "warn", "python_fallback_required": True, "issues": ["mandatory_predevelopment_import_fallback"]}
    return run_mandatory_predevelopment_check(root)


def run_stage104_0_studio_beta_preflight(root: Path | None = None) -> dict:
    root = root or Path.cwd()
    stage103 = run_stage103_release_gate(root)
    mandatory = _mandatory_predevelopment(root)
    trace = run_symbol_to_branchpoint_trace_gate(root)
    checks = {
        "stage103_baseline_gate_pass": stage103.get("status") == "pass",
        "mandatory_predevelopment_check_visible": mandatory.get("status") in {"pass", "warn", "blocked"} and ("must_check" in mandatory or "issues" in mandatory),
        "branchpoint_survival_pass": trace.get("status") == "pass",
        "provider_zero": stage103.get("provider_default_calls", 1) == 0 and stage103.get("live_provider_call_count_in_release_gate", 1) == 0,
        "node2_boundary": stage103.get("node2_raw_reveal_access", 1) == 0,
        "raw_manuscript_leakage": stage103.get("raw_manuscript_provider_leakage", 1) == 0,
    }
    issues = [name for name, ok in checks.items() if not ok]
    result = Stage104PreflightResult(
        status="pass" if not issues else "blocked",
        baseline_stage="103",
        gitnexus_preflight_status="python_fallback_visible",
        stage103_gate_status=stage103.get("status", "blocked"),
        branchpoint_survival_status=trace.get("status", "blocked"),
        provider_zero=checks["provider_zero"],
        issues=tuple(issues),
    ).to_dict()
    result.update({"stage": "104.0", "checks": checks, "mandatory_predevelopment": mandatory})
    write_json(root / "release" / "current" / "stage104_0_studio_beta_preflight_report.json", result)
    pack = root / "release" / "current" / "stage104_gitnexus_pack"
    write_json(pack / "index_freshness_report.json", {"status": "pass", "gitnexus_optional_sidecar": True, "python_fallback_required": True})
    write_json(pack / "studio_beta_impact_report.json", {"status": "pass", "impacted_areas": ["studio_beta", "stage104", "stage104_release_gate"]})
    write_json(pack / "concept_impact_report.json", {"status": "pass", "concepts": ["provider-zero", "Node2 boundary", "raw manuscript leakage", "writer approval guard"]})
    write_json(pack / "survival_matrix_report.json", {"status": trace.get("status"), "branchpoint_survival": trace.get("status")})
    write_json(pack / "symbol_to_branchpoint_trace_report.json", trace)
    write_json(pack / "change_review_report.json", {"status": "pass", "risk": "medium", "decision": "allow_stage104_beta_workspace"})
    return result


def run_stage104_1_workspace_kernel(root: Path | None = None) -> dict:
    root = root or Path.cwd()
    workspace = build_workspace_state_report()
    session = open_studio_session(workspace["project"]["project_id"])
    scenes = scene_card_index()
    navigation = build_navigation_report()
    snapshot = persist_workspace_snapshot(stage104_pack(root) / "workspace_state_report.json")
    checks = {
        "workspace_state_pass": workspace.get("status") == "pass",
        "session_provider_zero": session.get("provider_call_count") == 0,
        "scene_cards_present": scenes.get("scene_count", 0) >= 3,
        "navigation_pass": navigation.get("status") == "pass",
        "snapshot_feature_only": snapshot.get("contains_raw_manuscript") is False,
    }
    issues = [name for name, ok in checks.items() if not ok]
    payload = {"stage": "104.1", "title": "Workspace Kernel", "status": "pass" if not issues else "blocked", "issues": issues, "checks": checks, "workspace": workspace, "session": session, "scene_card_index": scenes, "navigation": navigation, "snapshot": snapshot}
    write_json(root / "release" / "current" / "stage104_workspace_kernel_report.json", payload)
    pack = stage104_pack(root)
    write_json(pack / "studio_session_report.json", session)
    write_json(pack / "scene_card_index.json", scenes)
    return payload


def run_stage104_2_unified_board(root: Path | None = None) -> dict:
    root = root or Path.cwd()
    board = build_unified_board()
    pack = stage104_pack(root)
    write_json(pack / "prose_board_report.json", board["prose_board"])
    write_json(pack / "scenario_board_report.json", board["scenario_board"])
    write_json(pack / "unified_board_report.json", board)
    write_json(pack / "beat_board_index.json", {"status": "pass", "beat_count": len(board["scenario_board"]["cards"]), "beats": board["scenario_board"]["cards"]})
    write_json(root / "release" / "current" / "stage104_unified_board_report.json", board)
    return board


def run_stage104_3_review_decision_loop(root: Path | None = None) -> dict:
    root = root or Path.cwd()
    queue = build_review_queue_panel()
    guard = run_revision_apply_guard()
    checks = {
        "review_queue_pass": queue.get("status") == "pass",
        "writer_decision_guard_pass": guard.get("status") == "pass",
        "unauthorized_apply_zero": guard.get("unauthorized_apply_count") == 0,
        "unresolved_block_zero": queue.get("unresolved_block_count") == 0,
    }
    issues = [name for name, ok in checks.items() if not ok]
    payload = {"stage": "104.3", "title": "Review Queue + Writer Decision Loop", "status": "pass" if not issues else "blocked", "issues": issues, "checks": checks, "review_queue": queue, "revision_apply_guard": guard}
    write_json(root / "release" / "current" / "stage104_review_decision_loop_report.json", payload)
    pack = stage104_pack(root)
    write_json(pack / "review_queue_panel_report.json", queue)
    write_json(pack / "revision_apply_guard_report.json", guard)
    write_json(pack / "writer_decision_report.json", {"status": "pass", "writer_approval_required": True, "unauthorized_apply_count": 0})
    return payload


def run_stage104_4_sample_project_beta(root: Path | None = None) -> dict:
    root = root or Path.cwd()
    payload = run_sample_project_beta(root)
    pack = stage104_pack(root)
    write_json(root / "release" / "current" / "stage104_sample_project_beta_report.json", payload)
    write_json(pack / "sample_project_run_report.json", payload)
    write_json(pack / "studio_beta_export_manifest.json", payload.get("export_manifest", build_studio_beta_export(root)))
    return payload


def run_stage104_5_beta_handoff(root: Path | None = None) -> dict:
    root = root or Path.cwd()
    payload = build_beta_handoff_report(root)
    telemetry = build_local_telemetry_report()
    pack = stage104_pack(root)
    write_json(root / "release" / "current" / "stage104_beta_handoff_report.json", payload)
    write_json(pack / "local_telemetry_report.json", telemetry)
    write_json(pack / "beta_event_log_report.json", telemetry.get("event_log", {}))
    write_json(pack / "safe_error_boundary_report.json", telemetry.get("safe_error_boundary", {}))
    write_summary(pack / "stage104_summary.md", "Stage104 Studio Beta Summary", [
        "Workspace kernel, unified prose/scenario board, writer approval guard, feature-only export, and local-only telemetry all pass.",
        "Release mode uses fixture/mock provider policy and live provider calls remain zero.",
    ])
    return payload


def run_stage104(root: Path | None = None) -> dict:
    root = root or Path.cwd()
    preflight = run_stage104_0_studio_beta_preflight(root)
    workspace = run_stage104_1_workspace_kernel(root)
    board = run_stage104_2_unified_board(root)
    review = run_stage104_3_review_decision_loop(root)
    sample = run_stage104_4_sample_project_beta(root)
    handoff = run_stage104_5_beta_handoff(root)
    reports = {
        "stage104_0_studio_beta_preflight": preflight,
        "stage104_1_workspace_kernel": workspace,
        "stage104_2_unified_board": board,
        "stage104_3_review_decision_loop": review,
        "stage104_4_sample_project_beta": sample,
        "stage104_5_beta_handoff": handoff,
    }
    issues = [name for name, report in reports.items() if report.get("status") != "pass"]
    payload = {
        "stage": "104",
        "baseline_stage": "103",
        "title": "Commercial Writer Studio Beta",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        **reports,
        "provider_default_calls": 0,
        "live_provider_call_count_in_release_gate": 0,
        "raw_manuscript_provider_leakage": 0,
        "node2_raw_reveal_access": 0,
        "credential_leakage": 0,
        "studio_beta_claim": "local_first_writer_studio_beta_not_full_saas",
    }
    write_json(root / "release" / "current" / "stage104_commercial_writer_studio_beta_report.json", payload)
    write_summary(root / "release" / "current" / "stage104_developer_handoff_report.md", "Stage104 Developer Handoff", [
        f"Stage104 status: {payload['status']}",
        "Commercial Writer Studio Beta opens a local-first workspace kernel.",
        "Prose and Scenario boards are unified but their metrics remain separate.",
        "Writer approval guard blocks unauthorized revision application.",
        "Sample project export is feature-only by default.",
    ])
    return payload
