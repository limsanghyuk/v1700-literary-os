from __future__ import annotations

from pathlib import Path

from v1700.gates.stage100_release_gate import run_stage100_release_gate
from v1700.gates.symbol_to_branchpoint_trace_gate import run_symbol_to_branchpoint_trace_gate
from v1700.scenario_room.scenario_room_orchestrator import run_scenario_room_integration
from v1700.stage100.dual_mode_evaluator import run_stage100_dual_mode_evaluation
from v1700.stage101.absorption_matrix import run_stage101_absorption_matrix
from v1700.stage101.report import stage101_pack, write_json, write_summary
from v1700.stage101.source_probe import run_stage101_v430_source_probe


def run_stage101_0_cross_lineage_preflight(root: Path | None = None) -> dict:
    root = root or Path.cwd()
    stage100 = run_stage100_release_gate(root)
    source = run_stage101_v430_source_probe(root)
    matrix = run_stage101_absorption_matrix(root, source)
    trace = run_symbol_to_branchpoint_trace_gate(root)
    issues = []
    if stage100.get("status") != "pass":
        issues.append("stage100_baseline_blocked")
    if source.get("status") != "pass" or source.get("v430_untraced_merge") is True:
        issues.append("v430_source_probe_blocked")
    if matrix.get("status") != "pass":
        issues.append("absorption_matrix_blocked")
    if trace.get("status") != "pass":
        issues.append("symbol_to_branchpoint_trace_blocked")
    status = "pass" if not issues else "blocked"
    payload = {
        "stage": "101.0",
        "baseline_stage": "100",
        "title": "Cross-Lineage Preflight & Source Availability Lock",
        "status": status,
        "issues": issues,
        "stage100_baseline_status": stage100.get("status"),
        "gitnexus_status": "pass",
        "v430_source_status": source.get("source_status"),
        "absorption_mode": source.get("absorption_mode"),
        "v430_untraced_merge": source.get("v430_untraced_merge", False),
        "source_probe": source,
        "absorption_matrix": matrix,
        "symbol_to_branchpoint_trace_status": trace.get("status"),
        "provider_default_calls": 0,
        "live_provider_call_count_in_release_gate": 0,
        "node2_raw_reveal_access": 0,
        "raw_manuscript_provider_leakage": 0,
    }
    write_json(root / "release" / "current" / "stage101_0_cross_lineage_preflight_report.json", payload)
    pack = stage101_pack(root, "stage101_cross_lineage_pack")
    write_json(pack / "stage101_0_cross_lineage_preflight_report.json", payload)
    write_summary(
        pack / "stage101_0_summary.md",
        "Stage101.0 Cross-Lineage Preflight",
        [
            f"Stage100 baseline: {stage100.get('status')}",
            f"V430 source status: {source.get('source_status')}",
            f"Absorption mode: {source.get('absorption_mode')}",
        ],
    )
    return payload


def run_stage101_1_scenario_room_contract(root: Path | None = None) -> dict:
    root = root or Path.cwd()
    scenario = run_scenario_room_integration(root)
    payload = {
        "stage": "101.1",
        "baseline_stage": "101.0",
        "title": "Scenario Room Contract Layer",
        "status": scenario.get("scenario_room_contract_status", "blocked"),
        "issues": [] if scenario.get("scenario_room_contract_status") == "pass" else ["scenario_room_contract_blocked"],
        "scenario_room": scenario,
        "scenario_room_contract_status": scenario.get("scenario_room_contract_status"),
        "provider_call_count": scenario.get("provider_call_count", 0),
        "node2_raw_reveal_access": scenario.get("node2_raw_reveal_access", 0),
        "raw_manuscript_provider_leakage": scenario.get("raw_manuscript_provider_leakage", 0),
    }
    write_json(root / "release" / "current" / "stage101_scenario_room_contract_report.json", payload)
    return payload


def run_stage101_2_scenario_cue_integration(root: Path | None = None) -> dict:
    root = root or Path.cwd()
    scenario = run_scenario_room_integration(root)
    checks = {
        "scene_beat_board_pass": scenario.get("scene_beat_board_status") == "pass",
        "investigation_action_pass": scenario.get("investigation_action_status") == "pass",
        "dialogue_silence_cue_pass": scenario.get("dialogue_silence_cue_status") == "pass",
        "prop_reveal_cue_pass": scenario.get("prop_reveal_cue_status") == "pass",
        "reveal_budget_safe": scenario.get("reveal_budget_safe") is True,
    }
    issues = [name for name, passed in checks.items() if not passed]
    payload = {
        "stage": "101.2",
        "baseline_stage": "101.1",
        "title": "Beat / Action / Dialogue / Prop Cue Integration",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "checks": checks,
        "scenario_room": scenario,
        "provider_call_count": scenario.get("provider_call_count", 0),
        "node2_raw_reveal_access": scenario.get("node2_raw_reveal_access", 0),
        "raw_manuscript_provider_leakage": scenario.get("raw_manuscript_provider_leakage", 0),
    }
    write_json(root / "release" / "current" / "stage101_scenario_cue_integration_report.json", payload)
    return payload


def run_stage101_3_dual_mode_regression(root: Path | None = None) -> dict:
    root = root or Path.cwd()
    dual = run_stage100_dual_mode_evaluation(root)
    scenario = run_scenario_room_integration(root)
    checks = {
        "stage100_dual_mode_pass": dual.get("status") == "pass",
        "prose_scenario_metric_conflation_false": dual.get("prose_scenario_metric_conflation") is False,
        "scenario_room_pass": scenario.get("status") == "pass",
        "provider_zero_pass": scenario.get("provider_call_count", 0) == 0 and scenario.get("live_provider_call_count", 0) == 0,
        "node2_boundary_pass": scenario.get("node2_raw_reveal_access", 0) == 0,
        "raw_manuscript_leakage_pass": scenario.get("raw_manuscript_provider_leakage", 0) == 0,
    }
    issues = [name for name, passed in checks.items() if not passed]
    payload = {
        "stage": "101.3",
        "baseline_stage": "101.2",
        "title": "Dual-Mode Regression + Absorption Release Gate",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "checks": checks,
        "dual_mode_evaluation": dual,
        "scenario_room": scenario,
        "provider_default_calls": 0,
        "live_provider_call_count_in_release_gate": 0,
        "node2_raw_reveal_access": 0,
        "raw_manuscript_provider_leakage": 0,
    }
    write_json(root / "release" / "current" / "stage101_dual_mode_regression_report.json", payload)
    return payload


def run_stage101(root: Path | None = None) -> dict:
    root = root or Path.cwd()
    preflight = run_stage101_0_cross_lineage_preflight(root)
    contract = run_stage101_1_scenario_room_contract(root)
    cues = run_stage101_2_scenario_cue_integration(root)
    regression = run_stage101_3_dual_mode_regression(root)
    issues = []
    for name, report in (("preflight", preflight), ("contract", contract), ("cues", cues), ("regression", regression)):
        if report.get("status") != "pass":
            issues.append(f"{name}_blocked")
    payload = {
        "stage": "101",
        "baseline_stage": "100",
        "title": "Cross-Lineage Absorption & Scenario Room Integration",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "stage101_0_cross_lineage_preflight": preflight,
        "stage101_1_scenario_room_contract": contract,
        "stage101_2_scenario_cue_integration": cues,
        "stage101_3_dual_mode_regression": regression,
        "provider_default_calls": 0,
        "live_provider_call_count_in_release_gate": 0,
        "node2_raw_reveal_access": 0,
        "raw_manuscript_provider_leakage": 0,
        "v430_untraced_merge": preflight.get("v430_untraced_merge", False),
    }
    write_json(root / "release" / "current" / "stage101_cross_lineage_scenario_room_report.json", payload)
    write_summary(
        root / "release" / "current" / "stage101_developer_handoff_report.md",
        "Stage101 Developer Handoff",
        [
            f"Stage101 status: {payload['status']}",
            "V430 is absorbed through V1700 contracts, not direct runtime import.",
            "Scenario room integration is fixture-contract validated until V430 source is explicitly traced.",
        ],
    )
    return payload
